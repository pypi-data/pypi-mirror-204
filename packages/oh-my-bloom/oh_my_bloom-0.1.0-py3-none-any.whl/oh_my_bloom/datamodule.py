from lightning.pytorch import LightningDataModule
from datasets import load_dataset, DatasetDict
import torch
from typing import Optional, List, Dict
from torch.utils.data import DataLoader


class ChatDataModule(LightningDataModule):
    def __init__(self, 
                 tokenizer: str,
                 data_dir: str, 
                 batch_size: int= 8,
                 data_type: str = 'json',
                 val_size: Optional[float] = None,
                 cache_dir: Optional[str] = None,
                 seed: int= 42,
                 num_workers: int = 8) -> None:
        super().__init__()

        self.save_hyperparameters()

        self.tokenizer = tokenizer

        assert hasattr(self.tokenizer, 'bou_token'), "请确保tokenizer正确"


    def convert_to_features(self, examples):
        tokenizer = self.tokenizer
        max_length = self.tokenizer.model_max_length
        input_ids = torch.full((len(examples["prompt"]), max_length), tokenizer.pad_token_id, dtype=torch.long)

        # prompt 和 response之间添加一个换行符
        newline_tokens = tokenizer("\n", return_tensors="pt", add_special_tokens=False)["input_ids"][0, :]

        out = {"labels": [], "attention_mask": []}
        for i, (prompt, response) in enumerate(zip(examples["prompt"], examples["response"])):
            # 添加上input token作为一轮对话的开始标志
            prompt = tokenizer.bou_token + prompt + tokenizer.eou_token
            input_tokens = tokenizer(prompt, truncation=True, max_length=max_length // 2, return_tensors="pt")["input_ids"].squeeze()
            input_len = len(input_tokens)

            remaining_tokens = max_length - input_len - len(newline_tokens)
            
            # 添加上reply token作为对话助手回复的标志
            response = tokenizer.bos_token + response + tokenizer.eos_token
            target_tokens = tokenizer(response, truncation=True, max_length=remaining_tokens, return_tensors="pt")["input_ids"].squeeze()

            # 填充进去
            input_ids[i, :input_len] = input_tokens
            
            # 添加换行符token
            newline_plus_inputs = input_len + len(newline_tokens)
            input_ids[i, input_len: newline_plus_inputs] = newline_tokens

            # 将回复的token填充进去
            input_ids[i, newline_plus_inputs: newline_plus_inputs + len(target_tokens)] = target_tokens
            
            # 忽略掉用户的输入以及pad token
            labels = input_ids[i].clone()
            labels[: newline_plus_inputs] = -100
            labels[labels == tokenizer.pad_token_id] = -100

            attention_mask = input_ids[i].ne(tokenizer.pad_token_id).int()

            out["labels"].append(labels)
            out["attention_mask"].append(attention_mask)
            
        out["input_ids"] = input_ids

        out = {k: torch.stack(v) if isinstance(v, list) else v for k, v in out.items()}
        return out


    def collate_fn(self, instances: List[Dict[str, str]]):
        examples = {'prompt':[ins['prompt'] for ins in instances], 'response': [ins['response'] for ins in instances]}
        return self.convert_to_features(examples=examples)
    

    def setup(self, stage: str = 'fit') -> None:
        if stage == 'fit':
            self.dataset = load_dataset(self.hparams.data_type, 
                                        data_dir=self.hparams.data_dir, 
                                        cache_dir=self.hparams.cache_dir,
                                        split='train')
    

    def train_dataloader(self):
        if isinstance(self.dataset, DatasetDict):
            return DataLoader(dataset=self.dataset['train'], 
                              batch_size=self.hparams.batch_size,
                              num_workers=self.hparams.num_workers,
                              pin_memory=True,
                              collate_fn=self.collate_fn)
        else:
            return DataLoader(dataset=self.dataset, 
                              batch_size=self.hparams.batch_size,
                              num_workers=self.hparams.num_workers,
                              pin_memory=True,
                              collate_fn=self.collate_fn)