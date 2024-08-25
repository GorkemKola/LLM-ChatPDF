from chatpdf.config import ConfigurationManager
from chatpdf.components import QAChainComponent
from chatpdf.utils import load_index

class QAChainPipeline():
    def __init__(self) -> None:
        pass
    
    def main(
            self,
            api_key,
            query
    ):
        index = load_index(api_key)
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
    from dotenv import load_dotenv
    import os
    from chatpdf.utils import logger
    from chatpdf.pipeline import (
        PDFProcessingPipeline,
        TextSplittingPipeline,
        EmbeddingPipeline,
        VectorStorePipeline,
        QAChainPipeline
    )

    load_dotenv()

    def run_stage(stage_name, pipeline_obj, *args):
        try:
            logger.info(f'>>>>> stage {stage_name} started <<<<<')
            result = pipeline_obj.main(*args)
            logger.info(f'>>>>> stage {stage_name} completed <<<<<\n\nx===========x')
            return result
        except Exception as e:
            logger.info(e)
            raise e
    
    query = 'according to context what is attention mechanism, can you explain detailed and step by step, do not use external knowledge to answer the question?'
    api_key = os.getenv('PINECONE_API_KEY')

    # QA Chain Stage
    answer = run_stage('QA Chain Stage', QAChainPipeline(), api_key, query)
    print(answer)