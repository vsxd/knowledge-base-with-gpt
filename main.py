from core.content_embedding import md_to_db
from core.excel_embedding import excel_to_db
from core.user_query import user_query_loop

def main() -> None:
    """
    main
    """
    # 将数据向量化后存入数据库
    # excel_to_db('/Users/xudongsun/Desktop/接口文档')
    # excel_to_db('/Users/xudongsun/Desktop/IM知识库.xlsx')
    
    # 用户提问查询
    # user_query_loop()

if __name__ == '__main__':
    main()
