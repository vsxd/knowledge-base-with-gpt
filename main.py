from content_embedding import content_to_db
from user_query import user_query_loop

def main() -> None:
    """
    main
    """
    # 将数据向量化后存入数据库
    # content_to_db("<Markdown files dir>")
    
    # 用户提问查询
    user_query_loop()

if __name__ == '__main__':
    main()
