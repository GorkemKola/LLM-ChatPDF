from chatpdf.config import ConfigurationManager
from chatpdf.components import EmbeddingComponent

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
    embedding_pipeline = EmbeddingPipeline()

    text_embedding = embedding_pipeline.main('Hello How are you?')
    
    print(text_embedding)