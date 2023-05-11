from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType
)


class Storage:
    CollectionName = "xfyunqa"

    def __init__(self):
        connections.connect(
            alias="default",
            user='u_open_milvus',
            password='r19jIIQuDbUw',
            host='172.31.101.17',
            port='19530'
        )
        self._collection = Collection(Storage.CollectionName)
        self._collection.load()

    def __del__(self):
        self._collection.release()

    def add(self, pid: int, text: str,
            external_id: int, embedding: list[float]):
        data = [
            [pid],
            [text],
            [external_id],
            [embedding]
        ]
        return self._collection.insert(
            data, auto_id=True
        )

    def get_texts(self, embedding: list[float], top_k=5):
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}, "offset": 5
        }
        results = self._collection.search(
            data=[embedding],
            anns_field="embedding",
            param=search_params,
            limit=10,
            # expr=None,
            # set the names of the fields you want to retrieve from the search result.
            # output_fields=['text'],
            # consistency_level="Bounded"
        )
        print(results)
        print(results[0].ids)
        return None

    @classmethod
    def _create_collection(cls):
        connections.connect(
            alias="default",
            user='u_open_milvus',
            password='r19jIIQuDbUw',
            host='172.31.101.17',
            port='19530'
        )
        primary_id = FieldSchema(
            name="id",
            dtype=DataType.INT64,
            is_primary=True,
        )
        text = FieldSchema(
            name="text",
            dtype=DataType.VARCHAR,
            max_length=4096,
        )
        external_id = FieldSchema(
            name="external_id",
            dtype=DataType.INT64,
        )
        embedding = FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=768
        )
        schema = CollectionSchema(
            fields=[primary_id, text, external_id, embedding],
            description=Storage.CollectionName
        )
        collection = Collection(
            name=Storage.CollectionName,
            schema=schema,
            using='default',
            shards_num=2
        )
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index(
            field_name="embedding",
            index_params=index_params
        )


if __name__ == '__main__':
    # Storage._create_collection()
    storage = Storage()

    print('0')
    # storage.add(1132132131, 'text', 111, [0.5]*768)
    print('1')
    vec = [0.5]*768
    vec[0] = 0.4
    storage.get_texts(vec)
    print('2')
    del storage
