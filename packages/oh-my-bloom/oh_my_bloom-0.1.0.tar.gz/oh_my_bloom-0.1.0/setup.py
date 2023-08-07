# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oh_my_bloom']

package_data = \
{'': ['*']}

install_requires = \
['deepspeed>=0.9.0',
 'lightning>=2.0.1',
 'transformers>=4.27.1',
 'wandb>=0.14.2']

setup_kwargs = {
    'name': 'oh-my-bloom',
    'version': '0.1.0',
    'description': '中文BLOOM语言模型',
    'long_description': '<!-- PROJECT: AUTO-GENERATED DOCS START (do not remove) -->\n\n# 🪐 Project: Oh-My-Bloom\n\n中文版本bloom\n\n## 📋 project.yml\n\nThe [`project.yml`](project.yml) defines the data assets required by the\nproject, as well as the available commands and workflows. \n\n### ⏯ Commands\n\nThe following commands are defined by the project. They\ncan be executed using `project run [name]`.Commands are only re-run if their inputs have changed.\n\n| Command | Description |\n| --- | --- |\n| `train` | 训练模型 |\n| `dev` | 调试模型训练整个流程，用于debug |\n| `fast-run` | 快速跑通训练流程，用于debug |\n\n<!-- PROJECT: AUTO-GENERATED DOCS END (do not remove) -->',
    'author': '善若水',
    'author_email': '790990241@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
