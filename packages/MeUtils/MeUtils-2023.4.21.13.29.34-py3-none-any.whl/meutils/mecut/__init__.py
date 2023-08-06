#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/4/18 18:33
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from paddlenlp import Taskflow


class Cut(object):

    def __init__(self, mode='fast', user_dict=None, batch_size=32, device='cpu'):
        """https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D

        :param mode:
            base 实体粒度分词，在精度和速度上的权衡，基于百度LAC
            ner/lac 实体粒度分词，在精度和速度上的权衡，基于百度LAC
            fast 最快：实现文本快速切分，基于jieba中文分词工具
            accurate 精确模式————最准：实体粒度切分准确度最高，基于百度解语, 精确模式基于预训练模型，更适合实体粒度分词需求，适用于知识图谱构建、企业搜索Query分析等场景中

        :param user_dict:
            在快速模式下，词典文件每一行为一个自定义item+"\t"+词频（词频可省略，词频省略则自动计算能保证分出该词的词频），暂时不支持黑名单词典（即通过设置”年“、”末“，以达到切分”年末“的目的）。
                平原上的火焰  10

            在base模式和精确模式下，词典文件每一行由一个或多个自定义item组成。
                平原上的火焰
                上 映

            在lac词性标注下，你可以通过装载自定义词典来定制化分词和词性标注结果。词典文件每一行表示一个自定义item，可以由一个单词或者多个单词组成，单词后面可以添加自定义标签，格式为item/tag，如果不添加自定义标签，则使用模型默认标签n。
                赛里木湖/LAKE
                高/a 山/n
                海拔最高

        :param batch_size:
        """

        if mode in ('ner', 'lac', 'tag', 'flag', 'pos_tagging'):
            self.word_segmentation = Taskflow(
                "pos_tagging",
                batch_size=batch_size,
                user_dict=user_dict,
                device=device
            )
        else:
            self.word_segmentation = Taskflow(
                "word_segmentation",
                mode=mode,
                batch_size=batch_size,
                user_dict=user_dict,
                device=device
            )

    def __call__(self, *texts):
        return self.word_segmentation(*texts)


# 名词标注 https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E8%A7%A3%E8%AF%AD%E7%9F%A5%E8%AF%86%E6%A0%87%E6%B3%A8
# >>> from paddlenlp import Taskflow
# >>> nptag = Taskflow("knowledge_mining", model="nptag")
# >>> nptag("糖醋排骨")
# [{'text': '糖醋排骨', 'label': '菜品'}]

if __name__ == '__main__':
    print(Cut('lac')('我是中国人'))
    print(Cut('lac')('我是中国人') | xfilter_(lambda w2t: w2t[1] in {'LOC'}))
