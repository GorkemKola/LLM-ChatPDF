from chatpdf.config import ConfigurationManager
from chatpdf.components import VectorStoreComponent

class VectorStorePipeline():
    def __init__(self) -> None:
        pass
    
    def main(
            self,
            docs,
            api_key
    ):
        config = ConfigurationManager()
        vector_store_config = config.get_vector_store_config()
        vector_store = VectorStoreComponent(config=vector_store_config)

        pc = vector_store.get_client(api_key)
        spec = vector_store.get_spec()
        index = vector_store.create_and_get_index(pc, spec)
        vector_store.upsert_documents(docs, index)

        return index

if __name__ == '__main__':
    from chatpdf.pipeline import PDFProcessingPipeline, TextSplittingPipeline
    from dotenv import load_dotenv

    load_dotenv()

    import os

    pdf_processing_pipeline = PDFProcessingPipeline()
    text_splitting_pipeline = TextSplittingPipeline()
    
    docs = pdf_processing_pipeline.main()

    chunked_docs = text_splitting_pipeline.main(docs)

    vector_store_pipeline = VectorStorePipeline()
    index = vector_store_pipeline.main(chunked_docs, api_key=os.getenv('PINECONE_API_KEY'))

    print(index.describe_index_stats())