from dotenv import load_dotenv
import os
from chatpdf.utils import logger, run_stage
from chatpdf.pipeline import (
    PDFProcessingPipeline,
    TextSplittingPipeline,
    EmbeddingPipeline,
    VectorStorePipeline,
    QAChainPipeline
)

load_dotenv()

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