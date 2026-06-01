import os
from knowledge_base import KnowledgeBase
from rag_chain import RAGChain

def main():
    kb = KnowledgeBase()
    
    if kb.load_vector_store():
        print("已加载现有向量库")
    else:
        docs_dir = "./documents"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            print(f"请将文档放入 {docs_dir} 目录后重新运行")
            return
        
        documents = kb.load_directory(docs_dir)
        if not documents:
            print("未找到任何文档")
            return
        
        chunks = kb.split_text(documents)
        kb.build_vector_store(chunks)
    
    retriever = kb.get_retriever()
    rag_chain = RAGChain(retriever)
    
    print("RAG问答系统已就绪！")
    print("输入 'exit' 或 'quit' 退出")
    
    while True:
        question = input("\n请输入问题: ")
        if question.lower() in ["exit", "quit"]:
            print("再见！")
            break
        
        answer, sources = rag_chain.ask(question)
        print(f"\n回答: {answer}")
        if sources:
            print(f"参考来源: {', '.join(sources)}")

if __name__ == "__main__":
    main()