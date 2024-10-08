from chatpdf.config import ConfigurationManager
from chatpdf.components import PDFProcessingComponent
from chatpdf.utils import save_variable, run_stage

class PDFProcessingPipeline():
    def __init__(self) -> None:
        pass
    
    def main(self):
        config = ConfigurationManager()
        pdf_processing_config = config.get_pdf_processing_config()
        pdf_processing = PDFProcessingComponent(config=pdf_processing_config)
        docs = pdf_processing.read_docs()
        save_variable(docs, 'vars/docs.pkl')
        return docs

if __name__ == '__main__':
    # PDF Processing Stage
    run_stage('PDF Processing Stage', PDFProcessingPipeline())