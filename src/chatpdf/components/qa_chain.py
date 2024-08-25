from langchain.llms.base import LLM
from typing import Any, List, Optional
import ollama
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from chatpdf.utils import logger
from chatpdf.entity import QAChainConfig
from chatpdf.components import EmbeddingComponent

from langchain.llms.base import LLM
from typing import Any, List, Optional
import ollama
from pydantic import Field

class OllamaLLM(LLM):
    model_name: str = Field(..., description="Name of the Ollama model to use")

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        response = ollama.generate(model=self.model_name, prompt=prompt)
        return response['response']

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model_name}

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "ollama"
class QAChainComponent:
    def __init__(
            self,
            config: QAChainConfig
    ) -> None:
        self.config = config

    def get_llm(self):
        # Initialize the custom Ollama LLM
        llm = OllamaLLM(model_name=self.config.model_name)

        return llm


    def get_prompt_template(self, prompt_template=None):
        # Create a custom prompt template
        prompt_template = prompt_template or """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Answer:"""

        prompt_template = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        return prompt_template


    def get_chain(self, llm, prompt_template):
        # Create the QA chain
        chain = load_qa_chain(llm, chain_type=self.config.chain_type, prompt=prompt_template)

        return chain

    def retrieve_query(self, index, query):

        top_k = self.config.top_k
        include_metadata = self.config.include_metadata

        logger.info(f"Retrieving top {top_k} results for query: {query}")

        embedding_component = EmbeddingComponent(config=self.config)

        embedding = embedding_component.get_embedding(query)
        
        search_response = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=include_metadata
        )
        
        return search_response
    
    # Function to get answer
    def get_answer(self, index, chain, query):
        relevant_docs = self.retrieve_query(index, query)
        
        context = "\n\n".join([doc['metadata']['text'] for doc in relevant_docs['matches']])
        
        # Create a Document object
        doc = Document(page_content=context)
        
        return chain({"input_documents": [doc], "question": query}, return_only_outputs=True)['output_text']