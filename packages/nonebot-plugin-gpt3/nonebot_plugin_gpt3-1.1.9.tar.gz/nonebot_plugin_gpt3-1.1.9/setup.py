# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gpt3']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0',
 'nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot-plugin-htmlrender>=0.2.0.3,<0.3.0.0',
 'nonebot2>=2.0.0rc2,<3.0.0',
 'tiktoken==0.3.0']

setup_kwargs = {
    'name': 'nonebot-plugin-gpt3',
    'version': '1.1.9',
    'description': '',
    'long_description': '<div align="center">\n  <img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo">\n  <br>\n  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n\n<div align="center">\n\n# Nonebot-plugin-gpt3\n## 3.3日更新: 支持gpt-3.5-turbo模型\n_✨ 基于OpenAI 官方API的对话插件 ✨_\n\n<p align="center">\n  <img src="https://img.shields.io/github/license/EtherLeaF/nonebot-plugin-colab-novelai" alt="license">\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">\n  <img src="https://img.shields.io/badge/nonebot-2.0.0r4+-red.svg" alt="NoneBot">\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gpt3">\n      <img src="https://img.shields.io/pypi/dm/nonebot-plugin-gpt3" alt="pypi download">\n  </a>\n</p>\n</div>\n\n# 功能\n\n- [x] 上下文功能\n- [x] 连续会话\n- [x] 人格设置\n- [x] 切换群聊/会话导出\n- [x] 回答图片渲染\n\n# 如何使用\n\n私聊中是直接发送消息，**群聊中是以回复的方式发送。**\n\n以下是功能列表\n\n|        功能        |             指令             |\n| :----------------: | :--------------------------: |\n| **基本的聊天对话** | 基本会话（默认【gpt3】触发） |\n|    **连续对话**    |      chat/聊天/开始聊天      |\n|    **结束聊天**    |      stop/结束/结束聊天      |\n|    **切换会话**    |    切换群聊/切换会话/切换    |\n|    重置会话记录    |        刷新/重置对话         |\n|     重置AI人格     |           重置人格           |\n|     设置AI人格     |           设置人格           |\n|    导出历史会话    |      导出会话/导出对话       |\n|   回答渲染为图片   |     图片渲染（默认关闭）     |\n\n\n## 基本会话\n\n对话前，加上**默认前缀**即可与GPT3对话。\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20230118155505182.png" width="40%" />\n\n## 连续会话\n\n输入**chat/聊天/开始聊天**即可不加前缀，连续的对话，输入**结束/结束聊天**，即可结束聊天\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20221217230058979.png" width="40%" />\n\n## 人格设置\n\n预设了**AI助手/猫娘/nsfw猫娘**三种人格，可以通过人格设置切换。内置的设定可以从[这里看到](https://github.com/chrisyy2003/lingyin-bot/blob/main/plugins/gpt3/nonebot_plugin_gpt3/__init__.py#L16-L18)。\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20221217231703614.png" width="40%" />\n\n同样也可以手动指定人格\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/202303061532626.png" width="40%" />\n\n## 切换群聊\n\n命令切换+群号即可保留聊天信息并切换群聊。\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20230118161015957.png" width="40%"/>\n\n切换群聊到702280361\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20230118161509269.png" width="40%"/>\n\n\n\n\n## 图片渲染\n\n图片渲染可以在配置文件中选择配置是否需要渲染。\n\n<img src="https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20221217233729263.png" width="40%" />\n\n# 安装\n\n1.  使用 nb-cli\n\n```\nnb plugin install nonebot-plugin-gpt3\n```\n\n2.   通过包管理器安装，可以通过nb，pip，或者poetry等方式安装，以pip为例\n\n```\npip install nonebot-plugin-gpt3 -U\n```\n\n随后在`bot.py`中加上如下代码，加载插件\n\n```\nnonebot.load_plugin(\'nonebot_plugin_gpt3\')\n```\n\n# 配置\n\n对于官方OpenAI接口只需配置API Keys即可，所以请填写API在您的配置文件中配置API KEYS\n\n```\nopenai_api_key = "xxx"                             # API密钥\n```\n\n此外可以通过环境变量配置，例如在Linux命令行中输入如下命令之后，直接启动即可\n\n```\nexport openai_api_key="xxx"\n```\n\n之后是一些自定义配置，根据注释可以自行修改，如果需要请在对应的配置文件下进行配置。\n\n```\ngpt3_command_prefix = "."                          # 基本会话中的指令前缀\nopenai_api_key = "xxx"                             # API密钥\n\n# 默认人格\ngpt3_default_preset = "以下是与一个叫鸡哥的篮球高手的对话。你叫鸡哥，是一个唱跳rap篮球的高手，并且每句话后会带上厉不厉害你鸡哥!"\ngpt3_proxy = "http://127.0.0.1:7890"               # 代理地址\ngpt3_need_at = False                               # 是否需要@才触发命令\ngpt3_image_render = False                          # 是否渲染为图片\ngpt3_image_limit = 150                             # 长度超过多少才会渲染成图片\ngpt3_max_tokens = 1000                             # 回答内容最大长度\ngpt3_chat_count_per_day = 150                      # 普通用户每天聊天次数上限\ngpt3_model = \'gpt-3.5-turbo\'                       # 语言模型\n```\n\n## 图片渲染\n\n如果需要开启图片渲染，请在配置文件中，配置`gpt3_image_render = True  `\n\n并安装`playwright`，如果已经安装了`playwright`则请忽略\n\n```\npip3 install playwright && playwright install \n```\n\n>   启动后出现`PyTorch, TensorFlow`等提示问题，**忽略即可**\n>\n>   ![image-20230118105930615](https://chrisyy-images.oss-cn-chengdu.aliyuncs.com/img/image-20230118105930615.png)\n',
    'author': 'chrisyy',
    'author_email': '1017975501@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
