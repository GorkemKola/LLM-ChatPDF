from chatpdf.config import ConfigurationManager
from chatpdf.components import TextSplittingComponent
from chatpdf.utils import save_variable, load_variable
class TextSplittingPipeline():
    def __init__(self) -> None:
        pass
    
    def main(
            self,
    ):
        docs = load_variable('vars/docs.pkl')
        config = ConfigurationManager()
        text_splitting_config = config.get_text_splitting_config()
        text_splitting = TextSplittingComponent(config=text_splitting_config)
        chunked_docs = text_splitting.chunk_data(docs=docs)
        save_variable(chunked_docs, 'vars/chunked_docs.pkl')
        return chunked_docs

if __name__ == '__main__':
    from chatpdf.pipeline.stage_01_pdf_processing import PDFProcessingPipeline
    
    pdf_processing_pipeline = PDFProcessingPipeline()

    docs = pdf_processing_pipeline.main()

    text_splitting_pipeline = TextSplittingPipeline()

    chunked_docs = text_splitting_pipeline.main(docs)

    print(chunked_docs)