import torch


def encode_passages(batch_text_passages, tokenizer, max_length):
    passage_ids, passage_masks = [], []
    max_len = max([len(text) for text in batch_text_passages])
    for text in batch_text_passages:
        text.extend([""]*(max_len-len(text)))

    for k, text_passages in enumerate(batch_text_passages):
        p = tokenizer.batch_encode_plus(
            text_passages,
            max_length=max_length,
            pad_to_max_length=True,
            return_tensors='pt',
            truncation=True
        )
        passage_ids.append(p['input_ids'][None])
        passage_masks.append(p['attention_mask'][None])

    passage_ids = torch.cat(passage_ids, dim=0)
    passage_masks = torch.cat(passage_masks, dim=0)
    return passage_ids, passage_masks.bool()


class DataCollatorForFid(object):
    def __init__(self, text_maxlength, tokenizer, max_target_length=128):
        self.tokenizer = tokenizer
        self.text_maxlength = text_maxlength
        self.max_target_length = max_target_length

    def __call__(self, batch):
        # assert (batch[0]['target'] != None)
        # print(batch)
        if "labels" in batch[0].keys():
            target = [ex['labels'] for ex in batch]
            target = self.tokenizer.batch_encode_plus(
                target,
                max_length=self.max_target_length if self.max_target_length > 0 else None,
                pad_to_max_length=True,
                return_tensors='pt',
                truncation=True if self.max_target_length > 0 else False,
            )
            target_ids = target["input_ids"]
            target_mask = target["attention_mask"].bool()
            target_ids = target_ids.masked_fill(~target_mask, -100)
        else:
            target_ids = None
            target_mask = None
        def append_question(example):
            return ["summarize: " + t for t in example['paragraphs']]

        text_passages = [append_question(example) for example in batch]
        passage_ids, passage_masks = encode_passages(text_passages,
                                                     self.tokenizer,
                                                     self.text_maxlength)

        return (target_ids, target_mask, passage_ids, passage_masks)
