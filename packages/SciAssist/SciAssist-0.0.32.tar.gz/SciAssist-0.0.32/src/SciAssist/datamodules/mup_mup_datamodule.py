# main developer: Yixi Ding <dingyixi@hotmail.com>
import csv
import math
import os
import random
from pathlib import Path
from typing import Optional

import datasets
from datasets import Dataset, DatasetDict
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, random_split

from SciAssist.utils.data_reader import csv_reader
from SciAssist.utils.data_utils import DataUtilsForSeq2Seq


class MupSciSummDataModule(LightningDataModule):
    def __init__(
        self,
        data_repo: str,
        train_batch_size: int = 8,
        num_workers: int = 0,
        pin_memory: bool = False,
        data_cache_dir: str = ".cache",
        seed: int = 777,
        data_utils = DataUtilsForSeq2Seq
    ):
        super().__init__()
        self.save_hyperparameters(logger=False)
        self.data_cache_dir = Path(self.hparams.data_cache_dir)
        self.data_utils = self.hparams.data_utils
        self.data_collator = self.data_utils.collator()

        self.data_train: Optional[Dataset] = None
        self.data_val: Optional[Dataset] = None
        self.data_test: Optional[Dataset] = None

    # def prepare_data(self) -> DatasetDict:
    #     mup_datasets  = datasets.load_dataset(
    #         self.hparams.data_repo,
    #         cache_dir=self.data_cache_dir
    #     )
    #     # Prepare keywords
    #     id2kw = {}
    #     with open("/home/dingyx/project/SciAssist/data/Task2/From-ScisummNet-2019/scisumm_flant5_target_Entities_sci2.csv", 'r', newline='', encoding='ISO-8859-1') as f:
    #         rows = csv.reader(f)
    #         # Get Column names
    #         keys = next(rows)
    #         # Add values by column
    #         for row in rows:
    #             id2kw[row[0]] = row[1]
    #
    #
    #     file_list = []
    #     root_dir = "/home/dingyx/project/SciAssist/data/Task2/From-ScisummNet-2019/"
    #     for dirpath, dirnames, files in os.walk(root_dir):
    #         file_list = dirnames
    #         break
    #
    #     texts = []
    #     summaries = []
    #     keywords = []
    #     for file in file_list:
    #         with open(os.path.join(root_dir, file, "summary", file + ".scisummnet_human.txt"), "r") as f:
    #             summary = f.readlines()
    #             summary = " ".join(summary[1:])
    #             summaries.append(summary)
    #         with open(os.path.join(root_dir, file, file + ".txt"), "r") as f:
    #             text = f.readlines()
    #             text = " ".join(text)
    #             texts.append(text)
    #         keywords.append(id2kw[file].split(","))
    #     scisumm_datasets = {
    #         "text": texts,
    #         "summary": summaries,
    #         "keywords": keywords,
    #         "length": [None for i in texts]
    #     }
    #
    #     lengths = [len(s.split(" ")) for s in mup_datasets["train"]["summary"]]
    #     lengths = [50*math.ceil(s/50) for s in lengths]
    #
    #     raw_datasets = DatasetDict()
    #     raw_datasets["train"] = {
    #         "text": scisumm_datasets["text"] + mup_datasets["train"]["text"],
    #         "summary": scisumm_datasets["summary"] + mup_datasets["train"]["summary"],
    #         "keywords": keywords + [None for i in mup_datasets["train"]["text"]],
    #         "length": scisumm_datasets["length"] + lengths
    #     }
    #
    #
    #
    #     raw_datasets["train"] = Dataset.from_dict(raw_datasets["train"])
    #     # raw_datasets["test"] = Dataset.from_dict(mup_datasets)
    #     # raw_datasets["validation"] = Dataset.from_dict(raw_datasets["validation"])
    #     # raw_datasets = Dataset.from_dict(raw_datasets)
    #     return raw_datasets


    def prepare_data(self) -> DatasetDict:

        # Prepare keywords
        summ = []
        kw = []
        text = []
        with open("/home/yixi/project/sciassist/data/train2.csv", 'r', newline='', encoding='ISO-8859-1') as f:
            rows = csv.reader(f)
            # Get Column names
            keys = next(rows)
            # Add values by column
            for row in rows:
                if row[0].isnumeric():
                    kws = row[4].split(",")
                    kws = list(set(kws))
                    summ.append(row[2])
                    kw.append(kws)
                    text.append(row[3])
                # lengths.append(100)

        lengths = [len(s.split(" ")) for s in summ]
        lengths = [50*math.ceil(s/50) for s in lengths]

        mask1=[]
        mask2=[]
        mask1 = random.sample(range(0, int(len(text))), int(len(text) / 3))
        mask2 = random.sample(range(0, int(len(text))), int(len(text) / 5))

        # for i in range(int(len(text)/3)):
        #     mask2.append(random.randint(0, len(text)-1))

        for i in mask1:
            if len(kw[i])<=1:
                kw[i] = None
        for i in mask2:
            if lengths[i] <= 100:
                lengths[i] = None

        raw_datasets = DatasetDict()
        raw_datasets["train"] = {
            "text": text,
            "summary": summ,
            "keywords": kw,
            "length": lengths
        }



        raw_datasets["train"] = Dataset.from_dict(raw_datasets["train"])
        # raw_datasets["test"] = Dataset.from_dict(mup_datasets)
        # raw_datasets["validation"] = Dataset.from_dict(raw_datasets["validation"])
        # raw_datasets = Dataset.from_dict(raw_datasets)
        return raw_datasets



    def setup(self, stage: Optional[str] = None):
        if not self.data_train and not self.data_val and not self.data_test:
            processed_datasets = self.prepare_data()
            tokenized_datasets = processed_datasets.map(
                lambda x: self.data_utils.tokenize_and_align_labels(x, inputs_column="text", labels_column="summary"),
                batched=True,
                remove_columns=processed_datasets["train"].column_names,
                load_from_cache_file=True
            )
            # self.data_train = tokenized_datasets["train"]
            # self.data_val = tokenized_datasets["validation"]
            length = len(tokenized_datasets["train"])
            train_size = int(0.9 * length)
            validate_size = length - train_size
            self.data_train, self.data_val = random_split(tokenized_datasets["train"], [train_size, validate_size])
            # self.data_test = tokenized_datasets["test"].select(range(100))
            # If labels are not provided, delete the column "labels"
            # self.data_test = tokenized_datasets["test"]

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
    #
