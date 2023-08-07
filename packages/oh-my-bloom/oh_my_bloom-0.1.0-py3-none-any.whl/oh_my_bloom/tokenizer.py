from transformers import BloomTokenizerFast


def get_chatbloom_tokeizer(plm_path: str, 
                           model_max_length: int = 512,
                           bou_token: str = '<user>',
                           eou_token: str = '</user>'):
    """在`BlommTokenizerFast`的基础上面加了四个特殊token
    `bou`: begin of user
    `eou`: end of user
    """
    tokenizer: BloomTokenizerFast = BloomTokenizerFast.from_pretrained(plm_path)
    tokenizer.model_max_length = model_max_length
    tokenizer.bou_token = bou_token
    tokenizer.eou_token = eou_token
    chat_special_tokens = [bou_token, eou_token]
    tokenizer.add_tokens(chat_special_tokens)
    tokenizer.bou_token_id = tokenizer.encode(bou_token)[0]
    tokenizer.eou_token_id = tokenizer.encode(eou_token)[0]
    tokenizer.padding_side = 'right'
    return tokenizer
