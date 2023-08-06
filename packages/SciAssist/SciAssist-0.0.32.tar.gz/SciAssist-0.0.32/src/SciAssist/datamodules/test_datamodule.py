# main developer: Yixi Ding <dingyixi@hotmail.com>
import csv
import math
import os
from pathlib import Path
from typing import Optional

import datasets
from datasets import Dataset, DatasetDict
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader, random_split

from SciAssist.utils.data_reader import csv_reader
from SciAssist.utils.data_utils import DataUtilsForSeq2Seq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



class TestDataModule(LightningDataModule):
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

        self.data_test: Optional[Dataset] = None

    def prepare_data(self) -> DatasetDict:

        stop_words = set(stopwords.words('english'))
        # Prepare keywords
        text = []
        summ = []
        kw = []
        id = []
        lengths = []
        with open("/home/dingyx/project/SciAssist/data/MUP/mup_flant5_target_Entities_sci2.csv", 'r', newline='', encoding='ISO-8859-1') as f:
            rows = csv.reader(f)
            # Get Column names
            keys = next(rows)
            # Add values by column
            for row in rows:
                # keywords = list(set(row[4].split(",")))
                # kws = []
                # for k in keywords:
                #     word_tokens = word_tokenize(k)
                #     for w in word_tokens:
                #         if w not in stop_words:
                #             kws.append(w)


                kws = row[4].split(",")

                kws = [kws[0]]
                # if int(row[0]) <= 300 and int(row[0]) % 10 == 0:
                #     with open("/home/dingyx/project/SciAssist/data/Flan-T5/" + row[0] +".txt","w") as f:
                #         f.write(row[3])
                #         f.write("\n\n")
                #         f.write(" ".join(kws))
                #         f.write(" => ")
                #     text.append(row[3])
                #     summ.append(row[2])
                #     kw.append(kws)
                #     id.append(int(row[0]))

                # with open("/home/dingyx/project/SciAssist/data/MUP_all2/" + row[0] + ".txt", "w") as f:
                #     f.write(" ".join(kws) + " => ")
                for i in range(5):
                    text.append(row[3])
                    summ.append(row[2])
                    kw.append(kws)
                    id.append(int(row[0]))
                    lengths.append((i+1)*50)


        # lengths = [len(s.split(" ")) for s in summ]
        # lengths = [50*math.ceil(s/50) for s in lengths]
        # lengths = [50 for s in lengths]
        mup_datasets = {
            "text": text,
            "summary": summ,
            # "keywords": kw,
            "length": lengths,
            "id": id,
            # "length": [None for i in text]
        }
        # raw_datasets["validation"] = {


        raw_datasets = DatasetDict()
        raw_datasets["test"] = Dataset.from_dict(mup_datasets)
        # raw_datasets["validation"] = Dataset.from_dict(raw_datasets["validation"])
        # raw_datasets = Dataset.from_dict(raw_datasets)
        return raw_datasets


    def setup(self, stage: Optional[str] = None):
        if not self.data_test:
            processed_datasets = self.prepare_data()
            tokenized_datasets = processed_datasets.map(
                lambda x: self.data_utils.tokenize_and_align_labels(x, inputs_column="text", labels_column="summary"),
                batched=True,
                remove_columns=processed_datasets["test"].column_names,
                load_from_cache_file=True
            )
            # self.data_train = tokenized_datasets["train"]
            # self.data_val = tokenized_datasets["validation"]
            self.data_test = tokenized_datasets["test"]
            # If labels are not provided, delete the column "labels"
            # self.data_test = tokenized_datasets["test"]



    def test_dataloader(self):
        return DataLoader(
            dataset=self.data_test,
            batch_size=self.hparams.train_batch_size,
            num_workers=self.hparams.num_workers,
            pin_memory=self.hparams.pin_memory,
            collate_fn=self.data_collator,
            shuffle=False,
        )

