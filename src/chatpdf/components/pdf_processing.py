from langchain.document_loaders import PyPDFDirectoryLoader
from chatpdf.utils import logger
from chatpdf.entity import PDFProcessingConfig

class PDFProcessingComponent:
    def __init__(
            self,
            config: PDFProcessingConfig 
    ) -> None:
        self.config = config

    def read_docs(self):
        """
        Loads documents from a directory of PDF files.

        Args:
            directory (str): The path to the directory containing PDF files.

        Returns:
            list: A list of Documents.
        """

        logger.info(f"Loading documents from directory: {self.config.doc_dir}")

        file_loader = PyPDFDirectoryLoader(self.config.doc_dir)

        docs = file_loader.load()

        logger.info(f"Loaded {len(docs)} documents")

        return docs