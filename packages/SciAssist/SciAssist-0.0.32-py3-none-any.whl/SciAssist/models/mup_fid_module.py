# main developer: Yixi Ding <dingyixi@hotmail.com>

import os
from pathlib import Path
from typing import Any, List

import numpy as np
import torch
from pytorch_lightning import LightningModule
from torchmetrics import MaxMetric
from torchmetrics.text.rouge import ROUGEScore
from SciAssist.models.components.fid_summarization import FiDT5

from SciAssist.utils.data_utils import DataUtilsForFiD


class MupFiDLitModule(LightningModule):
    def __init__(
        self,
        model: FiDT5,
        data_utils = DataUtilsForFiD,
        lr: float = 2e-5,
    ):
        super().__init__()
        self.save_hyperparameters(logger=False)
        self.data_utils = data_utils
        self.model = model

        self.val_metric = ROUGEScore(use_stemmer=True)
        self.val_best_Rouge1 = MaxMetric()
        self.test_metric = ROUGEScore(use_stemmer=True)
        self.test_best_Rouge1 = MaxMetric()
        self.best_Rouge1 = 0

        self.val_gen_lens = []
        self.val_gen_len = 0
        self.test_gen_lens = []
        self.test_gen_len = 0

        self.save_path = Path(os.path.join(self.model.model_dir,self.model.save_name))

    def forward(self, inputs):
        inputs["return_dict"]=False
        return self.hparams.model(**inputs)


    def on_train_start(self):
        self.val_metric.reset()
        self.val_best_Rouge1.reset()
        self.test_metric.reset()
        self.test_best_Rouge1.reset()

    def step(self, batch: Any):
        (labels, _, context_ids, context_mask) = batch
        inputs = {
            "input_ids": context_ids,
            "attention_mask": context_mask,
            "labels": labels
        }
        # print(context_ids.shape)
        outputs = self.forward(inputs)
        loss = outputs[0]
        return loss, labels

    def training_step(self, batch: Any, batch_idx: int):
        outputs = self.step(batch)
        loss = outputs[0]
        self.log("train/loss", loss, on_step=True, on_epoch=True, prog_bar=False)
        return {"loss": loss}

    def training_epoch_end(self, outputs: List[Any]):
        pass

    def validation_step(self, batch: Any, batch_idx: int):
        (labels, _, input_ids, attention_mask) = batch
        outputs = self.step(batch)
        # print("batch",batch)
        # print("outputs",outputs)
        loss = outputs[0]
        self.log("val/loss", loss, on_step=False, on_epoch=True, prog_bar=False)

        # Get prediction ids sequence
        preds = self.model.generate(input_ids=input_ids,attention_mask=attention_mask)

        # Convert ids to strings
        decoded_preds, decoded_labels = self.data_utils.postprocess(preds, labels)

        # Compute Rouge Metrics
        rouge_metric = self.val_metric(preds=decoded_preds, target=decoded_labels)

        result = {key: value * 100 for key, value in rouge_metric.items()}

        # Compute average length of summaries
        self.val_gen_lens.extend([np.count_nonzero(pred != self.data_utils.tokenizer.pad_token_id) for pred in preds.to("cpu")])

        #  Log results
        self.log("val/Rouge-1", result["rouge1_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/PRouge-1", result["rouge1_precision"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/RRouge-1", result["rouge1_recall"], on_step=False, on_epoch=True, prog_bar=True)

        self.log("val/Rouge-2", result["rouge2_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/PRouge-2", result["rouge2_precision"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/RRouge-2", result["rouge2_recall"], on_step=False, on_epoch=True, prog_bar=True)

        self.log("val/Rouge-L", result["rougeL_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/PRouge-L", result["rougeL_precision"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/RRouge-L", result["rougeL_recall"], on_step=False, on_epoch=True, prog_bar=True)

        self.log("val/Rouge-Lsum", result["rougeLsum_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/PRouge-Lsum", result["rougeLsum_precision"], on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/RRouge-Lsum", result["rougeLsum_recall"], on_step=False, on_epoch=True, prog_bar=True)

        return result

    def validation_epoch_end(self, outputs: List[Any]):
        rouge = self.val_metric.compute()
        self.val_best_Rouge1.update(rouge["rouge1_fmeasure"])
        # Save the best model
        if rouge["rouge1_fmeasure"] > self.best_Rouge1:
            self.best_Rouge1 = rouge["rouge1_fmeasure"]
            print(f"Epoch: {self.current_epoch}: Save the current best model.")
            torch.save(self.model.state_dict(), self.save_path)

        # Compute the average length of summaries
        self.val_gen_len = np.mean(self.val_gen_lens)
        self.log("val/gen_len", self.val_gen_len, on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/best_rouge1", self.val_best_Rouge1.compute(), on_epoch=True, prog_bar=True)

    def test_step(self, batch: Any, batch_idx: int):
        (labels, _, input_ids, attention_mask) = batch
        result = {}

        if "labels" is not None:
            # Simply do prediction
            preds = self.model.generate(input_ids=input_ids, attention_mask=attention_mask)
            decoded_preds = self.data_utils.tokenizer.batch_decode(preds, skip_special_tokens=True)
            result["preds"] = decoded_preds

        else:
            # Do prediction and compute metrics
            # Get prediction ids sequence
            preds = self.model.generate(input_ids=input_ids, attention_mask=attention_mask)
            # Convert ids to strings
            decoded_preds, decoded_labels = self.data_utils.postprocess(preds, labels)

            # Compute Rouge Metrics
            rouge_metric = self.test_metric(preds=decoded_preds, target=decoded_labels)

            result = {key: value * 100 for key, value in rouge_metric.items()}
            result['preds'] = decoded_preds
            # Log results
            self.log("test/Rouge-1", result["rouge1_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
            self.log("test/Rouge-2", result["rouge2_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
            self.log("test/Rouge-L", result["rougeL_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)
            self.log("test/Rouge-Lsum", result["rougeLsum_fmeasure"], on_step=False, on_epoch=True, prog_bar=True)

        # Compute average length of summaries
        self.test_gen_lens.extend([np.count_nonzero(pred != self.data_utils.tokenizer.pad_token_id) for pred in preds.to("cpu")])
        return result


    def test_epoch_end(self, outputs: List[Any]):
        # Save prediction results
        with open(os.path.join(self.model.model_dir,"prediction.txt"),'w') as f:
            for batch in outputs:
                for res in batch["preds"]:
                    f.write(res)
                    f.write("\n")
        # Compute average length of summaries
        self.test_gen_len = np.mean(self.test_gen_lens)
        self.log("test/gen_len", self.test_gen_len, on_step=False, on_epoch=True, prog_bar=True)



    def on_validation_epoch_end(self):
        self.val_metric.reset()
        self.val_best_Rouge1.reset()
        self.val_gen_lens = []

    def on_test_epoch_end(self):
        self.test_metric.reset()
        self.test_best_Rouge1.reset()
        self.test_gen_lens = []

    def configure_optimizers(self):
        return torch.optim.AdamW(
            params=self.hparams.model.parameters(), lr=self.hparams.lr
        )
