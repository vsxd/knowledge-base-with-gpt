"""
命令行方式的用户提问搜索
"""
import openai
import os
from embedding import create_embedding
from vector_db import Storage

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
             'content': '''你是一个非常有帮助的AI助手，能准确地使用现有文档回答用户的问题。
             使用所提供的文本来形成你的答案，在可能的情况下，尽量使用自己的话而不是逐字逐句地抄袭原文。
             要准确、有帮助、简明、清晰。'''},
            {'role': 'user', 'content': f'我的问题是：{query}，请使用以下段落来提供问题的答案：\n{text}'},
        ],
    )
    print(f"使用的tokens: {response.usage.total_tokens}")
    return response.choices[0].message.content


def user_query_loop() -> None:
    """
    Loop for user queries.
    """
    storage = Storage()
    limit = 10
    while True:
        query = input("请输入问题: \n> ")
        if query == "quit":
            break
        _, embedding = create_embedding(query)
        texts = storage.get_texts(embedding, limit)
        print(f"已找到相关片段: {len(texts)}")

        answer = completion(query, texts)
        print(">> Answer:")
        print(answer.strip())
        print("=====================================")


if __name__ == '__main__':
    user_query_loop()
