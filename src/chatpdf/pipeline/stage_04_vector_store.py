from chatpdf.config import ConfigurationManager
from chatpdf.components import VectorStoreComponent
from chatpdf.utils import save_variable, load_variable
from pinecone import ServerlessSpec
import json

class VectorStorePipeline:

    def main(self, api_key):
        chunked_docs = load_variable('vars/chunked_docs.pkl')
        config = ConfigurationManager()
        vector_store_config = config.get_vector_store_config()
        vector_store = VectorStoreComponent(config=vector_store_config)
        pc = vector_store.get_client(api_key)
        spec = vector_store.get_spec()
        index = vector_store.create_and_get_index(pc, spec)
        vector_store.upsert_documents(chunked_docs, index)
        
        # Instead of saving the entire index object, save the information needed to recreate it
        index_info = {
            'index_name': vector_store_config.index_name,  # Assuming this is defined in your config
            'dimension': vector_store_config.n_dim,
            'metric': vector_store_config.metric,
        }
        
        with open('vars/index_info.json', 'w') as f:
            json.dump(index_info, f)
        
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