

class TrainingArguments():

    def __init__(self):
        original_work_dir: ${hydra: runtime.cwd}
        data_dir: ${original_work_dir} / data /
        print_config: true
        ignore_warnings: true
        train: true
        test: true
        seed: null
        name: default
        model_name: scibert - uncased.pt
        datamodule:
        _target_: SciAssist.datamodules.mup_datamodule.MupDataModule
        data_repo: allenai / mup
        train_batch_size: 4
        num_workers: 0
        pin_memory: false
        data_cache_dir: ${paths.data_dir} / mup /
        data_utils:
        _target_: SciAssist.utils.data_utils.DataUtilsForSeq2Seq


        model:
        _target_: SciAssist.models.cora_module.CoraLitModule
        lr: 2.0e-05
        data_utils:
        _target_: SciAssist.utils.data_utils.DataUtilsForTokenClassification
        model:
        _target_: SciAssist.models.components.bert_token_classifier.BertForTokenClassifier
        model_checkpoint: allenai / scibert_scivocab_uncased
        output_size: 13
        cache_dir: ${paths.root_dir} /.cache /
        save_name: ${model_name}
        model_dir: ${paths.model_dir}
        callbacks:
        model_checkpoint:
        _target_: pytorch_lightning.callbacks.ModelCheckpoint
        monitor: val / micro_f1
        mode: max
        save_top_k: ${trainer.max_epochs}
        save_last: true
        verbose: false
        dirpath: ${paths.ckpt_dir}
        filename: epoch_
        {epoch: 03d}
        auto_insert_metric_name: false
        early_stopping:
        _target_: pytorch_lightning.callbacks.EarlyStopping
        monitor: val / micro_f1
        mode: max
        patience: 100
        min_delta: 0
        model_summary:
        _target_: pytorch_lightning.callbacks.RichModelSummary
        max_depth: -1
        rich_progress_bar:
        _target_: pytorch_lightning.callbacks.RichProgressBar
        logger:
        wandb:
        _target_: pytorch_lightning.loggers.wandb.WandbLogger
        project: ce384ad053376bf4d5e6ab3ba097719c5a4ed579
        save_dir: ${paths.log_dir}
        offline: false
        id: null
        log_model: false
        prefix: ''
        job_type: train
        group: ''
        tags: []
        trainer:
        _target_: pytorch_lightning.Trainer
        accelerator: gpu
        devices: 1
        min_epochs: 1
        max_epochs: 5
        resume_from_checkpoint: null
        paths:
        root_dir: ${oc.env: PROJECT_ROOT}
        data_dir: ${paths.root_dir} / data /
        log_dir: ${paths.root_dir} / logs /
        output_dir: ${paths.root_dir} / output
        work_dir: ${hydra: runtime.cwd}
        model_dir: ${paths.root_dir} / pretrained /${name}
        ckpt_dir: ${paths.model_dir} / checkpoints
