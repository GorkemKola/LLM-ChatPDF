from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PDFProcessingConfig:
    doc_dir: str


@dataclass(frozen=True)
class TextSplittingConfig:
    chunk_size: int
    chunk_overlap: int

@dataclass(frozen=True)
class EmbeddingConfig:
    model_name: str


@dataclass(frozen=True)
class VectorStoreConfig:
    cloud:str
    region: str
    n_dim: int
    metric: str
    index_name: str
    model_name: str
    
@dataclass(frozen=True)
class QAChainConfig:
    model_name: str
    chain_type: str
    top_k: int
    include_metadata: bool

