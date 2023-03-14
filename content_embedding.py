import os

from embedding import create_embedding
from vector_db import Storage


def walk_mds(top: str):
    for root, dirs, files in os.walk(top, topdown=True):
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith('.md'):
                yield file_path


def split_string(input_string: str):
    max_length = 600
    while len(input_string) > max_length:
        yield input_string[:max_length]
        input_string = input_string[max_length:]
    yield input_string


def md_files_to_string(dir_path: str):
    for file_path in walk_mds(dir_path):
        with open(file_path, encoding="utf-8") as f:
            read_data = f.read()
            yield split_string(read_data)


def content_to_db(docs_dir: str):
    storage = Storage()
    for str_list in md_files_to_string(docs_dir):
        for text in str_list:
            try:
                _, vector = create_embedding(str(text))
            except Exception as exce:
                print(str(exce))
                input("wait for command to retry")
                _, vector = create_embedding(str(text))
            storage.add(text, vector)
            print(f"> 完成插入text: [{text[0:10]}], embedding: {vector[0:3]}")


if __name__ == '__main__':
    content_to_db("/Users/abcd/Desktop/md-docs")
