# main developer: Yixi Ding <dingyixi@hotmail.com>
import json
import math
import os
from pathlib import Path
from typing import Optional

import datasets
import torch
from datasets import Dataset, DatasetDict
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, random_split

from SciAssist.utils.data_utils import DataUtilsForSeq2Seq, DataUtilsForFlanT5


class LongSummDataModule(LightningDataModule):
    def __init__(
        self,
        train_batch_size: int = 8,
        num_workers: int = 0,
        pin_memory: bool = False,
        data_cache_dir: str = ".cache",
        seed: int = 777,
        data_utils = DataUtilsForFlanT5
    ):
        super().__init__()
        self.save_hyperparameters(logger=False)
        self.data_cache_dir = Path(self.hparams.data_cache_dir)
        self.data_utils = self.hparams.data_utils
        self.data_collator = self.data_utils.collator()

        self.data_train: Optional[Dataset] = None
        self.data_val: Optional[Dataset] = None
        self.data_test: Optional[Dataset] = None

    def prepare_data(self) -> DatasetDict:
        texts = []
        summaries = []
        lengths = []
        text_dir = "/home/dingyx/project/SciAssist/data/longsumm/"
        for (root,dirs,files) in os.walk("/home/dingyx/project/SciAssist/data/LongSumm-master/abstractive_summaries/by_clusters/", topdown=False):
            if len(files)<1:
                break
            for file in files:
                try:
                    json_file = os.path.join(root,file)
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                        id = str(data["id"]) + ".txt"
                        text_file = os.path.join(text_dir, id)
                        with open(text_file, 'r') as f:
                            text = f.readlines()
                            text = " ".join(text)
                            texts.append(text)
                        summary = " ".join(data["summary"])
                        summaries.append(summary)
                except:
                    print("File not exsists.")

        raw_datasets = {
            "text": texts,
            "summary": summaries,
        }
        raw_datasets = Dataset.from_dict(raw_datasets)

        return raw_datasets

    def setup(self, stage: Optional[str] = None):
        if not self.data_train and not self.data_val and not self.data_test:
            raw_datasets = self.prepare_data()
            processed_datasets = DatasetDict()
            processed_datasets["whole"] = raw_datasets
            tokenized_datasets = processed_datasets.map(
                lambda x: self.data_utils.tokenize_and_align_labels(x, inputs_column="text", labels_column="summary"),
                batched=True,
                remove_columns=processed_datasets["whole"].column_names,
                load_from_cache_file=True
            )

            length = len(tokenized_datasets["whole"])
            train_size = int(0.9 * length)
            validate_size = length - train_size
            self.data_train, self.data_val = random_split(tokenized_datasets["whole"], [train_size, validate_size])


    def train_dataloader(self):
        return DataLoader(
            dataset=self.data_train,
            batch_size=self.hparams.train_batch_size,
            num_workers=self.hparams.num_workers,
            pin_memory=self.hparams.pin_memory,
            collate_fn=self.data_collator,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            dataset=self.data_val,
            batch_size=self.hparams.train_batch_size,
            num_workers=self.hparams.num_workers,
            pin_memory=self.hparams.pin_memory,
            collate_fn=self.data_collator,
            shuffle=False,
        )
    #
    # def test_dataloader(self):
    #     return DataLoader(
    #         dataset=self.data_test,
    #         batch_size=self.hparams.train_batch_size,
    #         num_workers=self.hparams.num_workers,
    #         pin_memory=self.hparams.pin_memory,
    #         collate_fn=self.data_collator,
    #         shuffle=False,
    #     )

