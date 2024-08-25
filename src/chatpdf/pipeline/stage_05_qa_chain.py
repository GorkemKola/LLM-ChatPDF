from chatpdf.config import ConfigurationManager
from chatpdf.components import QAChainComponent

class QAChainPipeline():
    def __init__(self) -> None:
        pass
    
    def main(
            self,
            index,
            query
    ):
        config = ConfigurationManager()
        qa_chain_config = config.get_qa_chain_config()
        qa_chain = QAChainComponent(config=qa_chain_config)

        llm = qa_chain.get_llm()
        prompt_template = qa_chain.get_prompt_template()
        chain = qa_chain.get_chain(llm, prompt_template)

        answer = qa_chain.get_answer(
            index=index,
            chain=chain,
            query=query
        )
        
        return answer

if __name__ == '__main__':
    from chatpdf.pipeline import PDFProcessingPipeline, TextSplittingPipeline, VectorStorePipeline
    from dotenv import load_dotenv

    load_dotenv()

    import os

    config = ConfigurationManager()
    qa_chain_config = config.get_qa_chain_config()

    pdf_processing_pipeline = PDFProcessingPipeline()
    text_splitting_pipeline = TextSplittingPipeline()
    
    docs = pdf_processing_pipeline.main()

    chunked_docs = text_splitting_pipeline.main(docs)

    vector_store_pipeline = VectorStorePipeline()
    index = vector_store_pipeline.main(chunked_docs, api_key=os.getenv('PINECONE_API_KEY'))

    qa_chain_pipeline = QAChainPipeline()

    answer = qa_chain_pipeline.main(
        index=index,
        query='How does attention mechanism work, can you explain step by step?'
    )
    
    print(answer)