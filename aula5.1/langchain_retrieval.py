from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.globals import set_debug
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationSummaryMemory
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
import os
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA

from dotenv import load_dotenv

load_dotenv()
set_debug(True)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=os.getenv("OPENAI_API_KEY"))

carregador = TextLoader("GTB_gold_Nov23.txt", encoding="utf-8")
documentos = carregador.load()


quebrador = CharacterTextSplitter(chunk_size=1000)
textos = quebrador.split_documents(documentos)
# print(textos)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(textos, embeddings)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

pergunta = "Como devo proceder caso tenha um item comprado roubado"
resultado = qa_chain.invoke({ "query" : pergunta})
print(resultado)
