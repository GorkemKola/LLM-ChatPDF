from chatpdf.utils import read_yaml
from chatpdf.entity import *
from pathlib import Path
from chatpdf.constants import *

class ConfigurationManager:
    def __init__(
            self,
            config_filepath: Path = CONFIG_FILE_PATH,
            params_filepath: Path = PARAMS_FILE_PATH,
    ) -> None:
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)


    def get_pdf_processing_config(self):
        self._pdf_processing_config = PDFProcessingConfig(
            doc_dir = Path(self.config.DOC_DIR)
        )

        return self._pdf_processing_config
    
    def get_text_splitting_config(self):
        self._text_splitting_config = TextSplittingConfig(
            chunk_size = self.params.CHUNK_SIZE,
            chunk_overlap = self.params.CHUNK_OVERLAP
        )

        return self._text_splitting_config

    def get_embedding_config(self):
        self._embedding_config = EmbeddingConfig(
            model_name = self.params.MODEL_NAME
        )

        return self._embedding_config
    
    def get_vector_store_config(self):
        self._vector_store_config = VectorStoreConfig(
            cloud = self.params.CLOUD,
            region = self.params.REGION,
            n_dim = self.params.N_DIM,
            metric = self.params.METRIC,
            index_name = self.params.INDEX_NAME,
            model_name = self.params.MODEL_NAME
        )

        return self._vector_store_config

    def get_qa_chain_config(self):
        self._qa_chain_config = QAChainConfig(
            model_name = self.params.MODEL_NAME,
            chain_type = self.params.CHAIN_TYPE,
            top_k = self.params.TOP_K,
            include_metadata = self.params.INCLUDE_METADATA,

        )

        return self._qa_chain_config