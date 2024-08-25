from langchain.text_splitter import RecursiveCharacterTextSplitter
from chatpdf.utils import logger
from chatpdf.entity import TextSplittingConfig

class TextSplittingComponent:
    def __init__(
        self,
        config: TextSplittingConfig
    ) -> None:
        self.config = config
    def chunk_data(self, docs):
        """Chunks a list of documents into smaller chunks.

        Args:
            docs (list): A list of documents to chunk.
            chunk_size (int, optional): The desired chunk size. Defaults to 800.
            chunk_overlap (int, optional): The amount of overlap between chunks. Defaults to 50.

        Returns:
            list: A list of chunked documents.
        """

        chunk_size = self.config.chunk_size
        chunk_overlap = self.config.chunk_overlap

        logger.info(f"Chunking {len(docs)} documents with chunk size {chunk_size} and overlap {chunk_overlap}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunked_docs = text_splitter.split_documents( 
            docs
        )

        logger.info(f"Chunked documents into {len(chunked_docs)} chunks")

        return chunked_docs