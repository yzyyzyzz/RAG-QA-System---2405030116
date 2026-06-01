import os
import PyPDF2
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader

class KnowledgeBase:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def load_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def load_docx(self, file_path):
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def load_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self.load_pdf(file_path)
        elif ext == ".docx":
            return self.load_docx(file_path)
        elif ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

    def load_directory(self, directory):
        documents = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                try:
                    text = self.load_file(file_path)
                    documents.append({"content": text, "source": filename})
                    print(f"已加载文件: {filename}")
                except Exception as e:
                    print(f"加载文件 {filename} 失败: {e}")
        return documents

    def split_text(self, documents, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        chunks = []
        for doc in documents:
            texts = text_splitter.split_text(doc["content"])
            for i, text in enumerate(texts):
                chunks.append({
                    "content": text,
                    "source": doc["source"],
                    "chunk_index": i
                })
        return chunks

    def build_vector_store(self, chunks):
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [{"source": chunk["source"], "chunk_index": chunk["chunk_index"]} for chunk in chunks]
        
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()
        print(f"向量库构建完成，共 {len(chunks)} 个文本块")

    def load_vector_store(self):
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("向量库加载成功")
            return True
        return False

    def search(self, query, k=3):
        if not self.vector_store:
            raise ValueError("向量库未初始化，请先构建或加载向量库")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def get_retriever(self):
        if not self.vector_store:
            raise ValueError("向量库未初始化")
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

    def get_documents_count(self):
        if not self.vector_store:
            return 0
        return len(self.vector_store.get()["documents"])