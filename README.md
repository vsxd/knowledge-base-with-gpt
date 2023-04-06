# knowledge-base-with-gpt

## Target

- 使用现有数据集建立本地知识库
- 使用自然语言查询知识库内容
- 使用自然语言返回查询结果

## Implementation

![9dTKpRlhtF6CkSz](https://s2.loli.net/2023/03/14/9dTKpRlhtF6CkSz.jpg)

### prefix prompt

```json
[
    {
        "role": "system",
        "content": "我是一个非常有帮助的QA机器人，能准确地使用现有文档回答用户的问题。我可以使用所提供的文本来形成我的答案，在可能的情况下，尽量使用自己的话而不是逐字逐句地抄袭原文。我的回答是准确、有帮助、简明、清晰的。"
    },
    {
        "role": "user",
        "content": "我的问题是：[XXXXX]，请使用以下段落来提供问题的答案：\n1.[向量查询结果top1]\n2.[向量查询结果top2]\n..."
    }
]
```

### example

![K7NHrZYxsyuzmiq](https://s2.loli.net/2023/03/14/K7NHrZYxsyuzmiq.png)

## Requirements

Database: postgreSQL + pgvector

Python 3.8+

```bash
pip3 install -r requirements.txt
```

在`main.py`中使用正确的路径调用`content_to_db()`后使用`user_query_loop()`
