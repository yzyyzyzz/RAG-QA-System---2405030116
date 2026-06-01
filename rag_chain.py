from langchain.chains import ConversationalRetrievalChain
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class RAGChain:
    def __init__(self, retriever, model_name="qwen2:7b"):
        self.llm = Ollama(model=model_name)
        self.retriever = retriever
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""基于以下参考文档回答问题：

{context}

问题：{question}

请严格基于提供的参考文档回答问题。如果文档中没有相关信息，请明确说"文档中未找到相关答案"。不要编造答案。"""
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )

    def ask(self, question):
        try:
            result = self.chain({"question": question})
            answer = result["answer"]
            source_docs = result.get("source_documents", [])
            
            if "文档中未找到相关答案" in answer:
                return answer, []
            
            sources = []
            for doc in source_docs:
                source_info = doc.metadata.get("source", "未知来源")
                if source_info not in sources:
                    sources.append(source_info)
            
            return answer, sources
        except Exception as e:
            return f"回答过程中发生错误: {str(e)}", []

    def clear_memory(self):
        self.memory.clear()