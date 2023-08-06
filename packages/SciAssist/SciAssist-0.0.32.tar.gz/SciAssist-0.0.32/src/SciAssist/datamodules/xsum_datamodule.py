# main developer: Yixi Ding <dingyixi@hotmail.com>
from pathlib import Path
from typing import Optional

import datasets
from datasets import Dataset, DatasetDict
from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader

from SciAssist.utils.data_reader import csv_reader
from SciAssist.utils.data_utils import DataUtilsForSeq2Seq


class XSumDataModule(LightningDataModule):
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

    def prepare_data(self) -> DatasetDict:
        raw_datasets = datasets.load_dataset(
            self.hparams.data_repo,
            cache_dir=self.data_cache_dir
        )
        # train_set =  raw_datasets["train"]
        # val_set = raw_datasets["validation"]
        # import xlwt
        # workbook = xlwt.Workbook(encoding='utf-8')  # 设置一个workbook，其编码是utf-8
        # worksheet = workbook.add_sheet("train_sheet")  # 新增一个sheet
        # worksheet2 = workbook.add_sheet("val_sheet")  # 新增一个sheet
        # worksheet.write(0, 0, label='列1')  # 将‘列1’作为标题
        # for k,i in enumerate(train_set):  # 循环将a和b列表的数据插入至excel
        #     l = i["summary"].split(" ")
        #     worksheet.write(k + 1, 0, label=len(l))
        # for k,i in enumerate(val_set):  # 循环将a和b列表的数据插入至excel
        #     l = i["summary"].split(" ")
        #     worksheet2.write(k + 1, 0, label=len(l))
        # workbook.save("mup.xls")  # 这里save需要特别注意，文件格式只能是xls，不能是xlsx，不然会报错

        # Get test from csv
        # raw_datasets["test"] = csv_reader("data/mup/test-release.csv")
        return raw_datasets

    def setup(self, stage: Optional[str] = None):
        if not self.data_train and not self.data_val and not self.data_test:
            processed_datasets = self.prepare_data()
            tokenized_datasets = processed_datasets.map(
                lambda x: self.data_utils.tokenize_and_align_labels(x, inputs_column="document", labels_column="summary"),
                batched=True,
                remove_columns=processed_datasets["train"].column_names,
                load_from_cache_file=True
            )
            self.data_train = tokenized_datasets["train"]
            self.data_val = tokenized_datasets["validation"]
            # If labels are not provided, delete the column "labels"
            self.data_test = tokenized_datasets["test"].remove_columns("labels")

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
