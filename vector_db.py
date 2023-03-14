from pgvector.sqlalchemy import Vector
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
SQL_URL = "postgresql://localhost:5432/<YOUR_DB_NAME>"


class EmbeddingEntity(Base):
    __tablename__ = '<YOUR TABLE NAME>'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    embedding = Column(Vector(1536))


class Storage:
    """数据库存储类"""
    def __init__(self):
        """初始化存储"""
        self._postgresql = SQL_URL
        self._engine = create_engine(self._postgresql)
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def add(self, text: str, embedding: list[float]):
        """添加新的嵌入向量"""
        self._session.add(EmbeddingEntity(text=text, embedding=embedding))
        self._session.commit()

    def add_all(self, embeddings: list[tuple[str, list[float]]]):
        """添加多个嵌入向量"""
        data = [EmbeddingEntity(text=text, embedding=embedding)
                for text, embedding in embeddings]
        self._session.add_all(data)
        self._session.commit()

    def get_texts(self, embedding: list[float], limit=30) -> list[str]:
        """获取给定嵌入向量对应的文本"""
        result = self._session.query(EmbeddingEntity).order_by(
            EmbeddingEntity.embedding.cosine_distance(embedding)).limit(limit).all()
        return [s.text for s in result]

    def clear(self):
        """清空数据库"""
        self._session.query(EmbeddingEntity).delete()
        self._session.commit()

    def __del__(self):
        """关闭session"""
        self._session.close()


if __name__ == '__main__':
    storage = Storage()
    storage.add_all([('test', [0]*1536)])
