import ollama
from chatpdf.utils import logger
from chatpdf.entity import EmbeddingConfig

class EmbeddingComponent:
    def __init__(
            self,
            config: EmbeddingConfig
    ) -> None:
        self.config = config
        
    def get_embedding(self, text):
        """Generates an embedding for the given text using Ollama.

        Args:
            text (str): The text to generate an embedding for.

        Returns:
            list: A list of floats representing the embedding.
        """

        logger.info(f"Generating embedding for text: {text}")

        embeddings = ollama.embeddings(model=self.config.model_name, prompt=text)

        logger.info("Embedding generated successfully")

        return embeddings['embedding']