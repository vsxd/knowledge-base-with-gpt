"""
利用text2vec生成词向量
"""
import os
from typing import *

from text2vec import SentenceModel

m = SentenceModel()

def create_embedding(text: str):
    """Create an embedding for the provided text."""
    return text, m.encode(text)


if __name__ == '__main__':
    print(create_embedding('如何更换花呗绑定银行卡')[:5])
