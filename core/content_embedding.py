"""
遍历Markdown文件，将文件内容分割为合适的大小，并通过embedding将数据存入向量数据库
"""

import os
import re
from typing import Generator
from core.embedding_old import create_embedding
from core.vector_db import Storage


def walk_mds(top: str) -> Generator[str, None, None]:
    """
    该函数用于递归遍历以'top'为根目录的文件夹树，并生成发现的.md文件的文件路径。
    参数:
        top: 开始递归搜索的根目录。
    生成:
        每个发现的.md文件的文件路径。
    """
    for root, dirs, files in os.walk(top, topdown=True):
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith('.md'):
                yield file_path


def split_string(input_string: str) -> Generator[str, None, None]:
    """
    将一个较长的字符串分成最大长度为600的块。
    参数：
        input_string: 要分割的字符串。
    生成：
        输入字符串的每个块, 最大长度为600。
    """
    max_length = 600
    while len(input_string) > max_length:
        yield input_string[:max_length]
        input_string = input_string[max_length:]
    yield input_string


def md_files_to_string(dir_path: str) -> Generator[Generator[str, None, None], None, None]:
    """
    此函数用于读取给定目录下所有的 .md 文件，并将其内容分成最大长度为 600 的字符串，逐一生成这些字符串。
    参数：
        dir_path: 包含 .md 文件的目录路径。
    生成器输出：
        每个 .md 文件的内容被拆分为长度最大为 600 的多个字符串，逐一生成这些字符串。
    """
    for file_path in walk_mds(dir_path):
        with open(file_path, encoding="utf-8") as f:
            read_data = f.read()
            yield split_string(read_data)

TAGS_REGEX = r"- (.+)"
def excel_to_db(docs_dir: str) -> None:
    """
    将指定目录中的md文件内容添加到数据库中。
    :param docs_dir: md文件所在目录
    """
    storage = Storage()
    for str_list in md_files_to_string(docs_dir):
        str_list = list(str_list)
        tags = []
        tags_match = re.findall(TAGS_REGEX, str_list[0])
        if tags_match:
            for tag_str in tags_match:
                tags.append(tag_str)
        tag = ",".join(tags[:3])
        for text in str_list:
            try:
                content_str = tag+"\n"+str(text)
                _, vector = create_embedding(content_str)
            except Exception as exce:
                print(str(exce))
                input("wait for command to retry")
                _, vector = create_embedding(str(text))
            storage.add(text, vector)
            print(f"> 完成插入text: [{text[0:10]}], embedding: {vector[0:3]}")


if __name__ == '__main__':
    excel_to_db("/Users/abcd/Desktop/md-docs")
