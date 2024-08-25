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

# PDF Processing Stage
run_stage('PDF Processing Stage', PDFProcessingPipeline())

# Text Splitting Stage
run_stage('Text Splitting Stage', TextSplittingPipeline())

# Embedding Stage
query = "what is the prompt?"
query_embedding = run_stage('Embedding Stage', EmbeddingPipeline(), query)

if isinstance(query_embedding, list):
    logger.info(f'>>>>> Embedding works fine <<<<<')

api_key = os.getenv('PINECONE_API_KEY')

# Vector Store Stage
run_stage('Vector Store Stage', VectorStorePipeline(), api_key)

# QA Chain Stage
answer = run_stage('QA Chain Stage', QAChainPipeline(), api_key, query)

print(f"Answer: {answer}")