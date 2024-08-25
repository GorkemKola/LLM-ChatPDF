from pinecone import Pinecone
from pinecone import ServerlessSpec
import time
from .embedding import EmbeddingComponent
from chatpdf.utils import logger
from chatpdf.entity import VectorStoreConfig

class VectorStoreComponent:
    def __init__(
            self,
            config: VectorStoreConfig,
    ) -> None:
        self.config = config

    def get_client(self, api_key):
        pc = Pinecone(api_key=api_key)

        logger.info("Pinecone client initialized.")

        return pc


    def get_spec(self):
        cloud = self.config.cloud
        region = self.config.region

        spec = ServerlessSpec(cloud=cloud, region=region)

        logger.info("Serverless spec created for cloud: %s, region: %s", cloud, region)

        return spec


    def create_and_get_index(
            self,
            pc, 
            spec, 
        ):

        index_name = self.config.index_name
        dimension = self.config.n_dim
        metric = self.config.metric

        if index_name in pc.list_indexes().names():
            logger.info("Deleting existing index: %s", index_name)
            pc.delete_index(index_name)

        logger.info("Creating index: %s", index_name)

        pc.create_index(
            index_name,
            dimension=dimension,
            metric=metric,
            spec=spec
        )

        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)

        index = pc.Index(index_name)
        # wait a moment for connection
        time.sleep(1)

        logger.info("Index created and ready.")

        return index


    def upsert_documents(self, documents, index):
        embedding_component = EmbeddingComponent(config=self.config)
        logger.info("Upserting %d documents.", len(documents))
        
        upserts = []
        for i, doc in enumerate(documents):
            metadata = doc.metadata
            metadata['text'] = doc.page_content

            upserts.append(
                {
                    'id': str(i),
                    'values': embedding_component.get_embedding(doc.page_content),
                    'metadata': metadata
                }
            )

        index.upsert(upserts)





