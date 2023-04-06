"""
命令行方式的用户提问搜索
"""
import openai
import os
from core.embedding import create_embedding
from core.vector_db import Storage

def limit_context_length(context, max_length=3000):
    """
    限制文本列表的总长度不超过指定的最大值。
    :param context: 文本列表。
    :param max_length: 最大长度限制，默认为3000。
    :return: 截取到的前n个文本段落。
    """
    # 获取每个文本段落的长度。
    paragraph_lengths = [len(paragraph) for paragraph in context]

    total_length = sum(paragraph_lengths)
    if total_length <= max_length:
        # 如果总长度小于等于最大长度限制，则不需要截断文本。
        return context

    # 如果总长度超过最大长度限制，则截取到前n个文本段落。
    current_length = 0
    for index, length in enumerate(paragraph_lengths):
        current_length += length
        if current_length > max_length:
            # 切片复制新的列表，并返回截取到的前n个文本段落。
            return context[:index]

    # 如果所有的文本段落都被包含，则返回整个文本列表。
    return context


def completion(query: str, context: list[str]) -> str:
    """
    根据query和context调用openai ChatCompletion
    """
    context = limit_context_length(context, 3000)

    text = "\n".join(f"{index}. {text.strip()}" for index,
                     text in enumerate(context))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'system',
             'content': '''我是一个非常有帮助的QA机器人，能准确地使用现有文档回答用户的问题。
             我可以使用所提供的文本来形成我的答案，在可能的情况下，尽量使用自己的话而不是逐字逐句地抄袭原文。
             我的回答是准确、有帮助、简明、清晰的。'''},
            {'role': 'user', 'content': f'我的问题是：{query}\n请使用以下的知识库内容来提供问题的答案：\n{text}'},
        ],
    )
    print(f"使用的tokens: {response.usage.total_tokens}")
    return response.choices[0].message.content


def user_query_loop() -> None:
    """
    Loop for user queries.
    """
    storage = Storage()

    while True:
        query = input("请输入问题: \n> ")
        if query == "quit":
            break
        answer = get_answer(storage, query)
        print(">> Answer:")
        print(answer.strip())
        print("=====================================")


def get_answer(storage: Storage, query: str) -> str:
    """
    Embedding user question and get query answer
    """
    limit = 8
    _, embedding = create_embedding(query)
    texts = storage.get_texts(embedding, limit)
    texts = list(set(texts)) # drop duplicated texts
    print(f"已找到相关片段: {len(texts)}")

    answer = completion(query, texts)
    return answer


if __name__ == '__main__':
    user_query_loop()
