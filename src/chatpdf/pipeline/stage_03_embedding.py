from chatpdf.config import ConfigurationManager
from chatpdf.components import EmbeddingComponent
from chatpdf.utils import run_stage, logger

class EmbeddingPipeline():
    def __init__(self) -> None:
        pass
    
    def main(
            self,
            text
    ):
        config = ConfigurationManager()
        embedding_config = config.get_embedding_config()
        embedding = EmbeddingComponent(config=embedding_config)
        text_embedding = embedding.get_embedding(text=text)
        return text_embedding

if __name__ == '__main__':
    query = "what is the context?"
    query_embedding = run_stage('Embedding Stage', EmbeddingPipeline(), query)

    if isinstance(query_embedding, list):
        logger.info(f'>>>>> Embedding works fine <<<<<')
