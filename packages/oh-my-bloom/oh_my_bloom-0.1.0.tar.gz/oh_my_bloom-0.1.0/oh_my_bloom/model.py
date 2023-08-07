import lightning as L
from transformers import BloomTokenizerFast, BloomForCausalLM, BloomConfig, GenerationConfig, get_linear_schedule_with_warmup
from lightning_utilities.core.overrides import is_overridden
from torchmetrics import MeanMetric
from typing import List
import torch
from deepspeed.ops.adam import FusedAdam, DeepSpeedCPUAdam


class ChatBloom(L.LightningModule):
    def __init__(self, 
                 plm_path: str, 
                 chat_tokenizer: BloomTokenizerFast,
                 lr: float = 2e-5,
                 weight_decay: float = 0.01,
                 num_warmup_steps: int = 100,
                 **kwargs) -> None:
        super().__init__()
        
        self.save_hyperparameters()
        
        self.tokenizer = self.hparams.chat_tokenizer
        
        #判断configure_shared_model方法是否被重写
        if not is_overridden('configure_sharded_model', self, L.LightningModule):
            self.net = self.get_net()
        
        self.train_loss = MeanMetric()
        self.val_loss = MeanMetric()

        
    def get_net(self) -> BloomForCausalLM:
        if 'bloom_config' in self.hparams.keys():
            bloom_config = BloomConfig.from_dict(config_dict=self.hparams['bloom_config'])
            net = BloomForCausalLM(bloom_config)
        else:
            bloom_config = BloomConfig.from_pretrained(self.hparams.plm_path)
            self.hparams['bloom_config'] = bloom_config.to_dict()
            net = BloomForCausalLM.from_pretrained(self.hparams.plm_path)
        if bloom_config.vocab_size != len(self.tokenizer):
            bloom_config.vocab_size = len(self.tokenizer)
            net.resize_token_embeddings(len(self.tokenizer))
        return net
        
    def forward(self, input_ids, attention_mask = None, **kwargs):
        return self.net(input_ids=input_ids, attention_mask=attention_mask, **kwargs)
        
    def on_train_start(self) -> None:
        self.train_loss.reset()
        self.val_loss.reset()

    def training_step(self, batch, batch_idx):
        outputs = self.net(**batch)
        loss = outputs.loss
        self.train_loss(loss)
        self.log('train/loss', self.train_loss, on_epoch=True, on_step=True, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        outputs = self.net(**batch)
        loss = outputs.loss
        self.val_loss(loss)
        self.log('val/loss', self.val_loss, on_epoch=True, on_step=False, prog_bar=True)    
        
    
    @torch.no_grad()
    def generate(self, 
                 prompt: str,
                 temperature: float = 0.8, 
                 top_p: float = 0.5, 
                 top_k: int = 40, 
                 num_beams: int = 4, 
                 max_new_tokens: int = 256, 
                 min_new_tokens: int = 1, 
                 repetition_penalty: float = 1.5,
                 skip_special_tokens: bool = False,
                 **kwargs):
        generation_config = GenerationConfig(temperature=temperature,
                                             top_p=top_p,
                                             top_k=top_k,
                                             num_beams=num_beams,
                                             bos_token_id=1,
                                             eos_token_id=2,
                                             pad_token_id=3,
                                             max_new_tokens=max_new_tokens, # max_length=max_new_tokens+input_sequence
                                             min_new_tokens=min_new_tokens, # min_length=min_new_tokens+input_sequence
                                             **kwargs)
        
        prompt = self.tokenizer.bou_token + prompt + self.tokenizer.eou_token + '\n'

        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.net.device)

        ids = self.net.generate(inputs['input_ids'], 
                                generation_config=generation_config, 
                                repetition_penalty=repetition_penalty)
        return self.tokenizer.decode(ids[0], skip_special_tokens=skip_special_tokens)

    
    
class DeepSpeedChatBloom(ChatBloom):
    
    def __init__(self, 
                 plm_path: str, 
                 chat_tokenizer: BloomTokenizerFast,
                 lr: float = 2e-5, 
                 weight_decay: float = 0, 
                 num_warmup_steps: int = 100,
                 offload: bool = False) -> None:
        super().__init__(plm_path=plm_path, 
                         chat_tokenizer=chat_tokenizer, 
                         lr=lr, 
                         weight_decay=weight_decay, 
                         num_warmup_steps=num_warmup_steps)

        self.save_hyperparameters()
        
    def configure_optimizers(self):
        # create the optimizer
        no_decay = ["bias", "LayerNorm.weight"]
        params_decay = [p for n, p in self.named_parameters() if not any(nd in n for nd in no_decay)]
        params_nodecay = [p for n, p in self.named_parameters() if any(nd in n for nd in no_decay)]
        optim_groups = [
            {"params": params_decay, "weight_decay": self.hparams.weight_decay},
            {"params": params_nodecay, "weight_decay": 0.0},
        ]
        if self.hparams.offload:
            optimizer = DeepSpeedCPUAdam(optim_groups, lr=self.hparams.lr)
        else:
            optimizer = FusedAdam(params=optim_groups, lr=self.hparams.lr)
        num_train_steps = self.trainer.estimated_stepping_batches
        scheduler = get_linear_schedule_with_warmup(optimizer=optimizer, 
                                                    num_training_steps=num_train_steps, 
                                                    num_warmup_steps=self.hparams.num_warmup_steps)
        scheduler_config = {'scheduler': scheduler, 'interval':'step', "frequency": 1}
        
        return [optimizer], [scheduler_config]