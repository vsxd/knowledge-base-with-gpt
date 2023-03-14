# knowledge-base-with-gpt

## Target

- 使用现有数据集建立本地知识库
- 使用自然语言查询知识库内容
- 使用自然语言返回查询结果

## Implementation

![9dTKpRlhtF6CkSz](https://s2.loli.net/2023/03/14/9dTKpRlhtF6CkSz.jpg)

## Requirements

Database: postgreSQL + pgvector
Python 3.8+

```bash
pip3 install -r requirements.txt
```

在`main.py`中使用正确的路径调用`content_to_db()`后使用`user_query_loop()`
