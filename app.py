import streamlit as st
import os
from knowledge_base import KnowledgeBase
from rag_chain import RAGChain

def init_session_state():
    if 'kb' not in st.session_state:
        st.session_state.kb = KnowledgeBase()
        st.session_state.kb.load_vector_store()
    
    if 'rag_chain' not in st.session_state:
        if st.session_state.kb.vector_store:
            st.session_state.rag_chain = RAGChain(st.session_state.kb.get_retriever())
        else:
            st.session_state.rag_chain = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

def save_uploaded_file(uploaded_file):
    save_dir = "./uploaded_docs"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def build_knowledge_base():
    if not st.session_state.uploaded_files:
        st.warning("请先上传文档")
        return
    
    documents = []
    for uploaded_file in st.session_state.uploaded_files:
        file_path = save_uploaded_file(uploaded_file)
        try:
            text = st.session_state.kb.load_file(file_path)
            documents.append({"content": text, "source": uploaded_file.name})
        except Exception as e:
            st.error(f"加载文件 {uploaded_file.name} 失败: {e}")
    
    if not documents:
        st.warning("没有成功加载任何文档")
        return
    
    chunks = st.session_state.kb.split_text(documents)
    st.session_state.kb.build_vector_store(chunks)
    st.session_state.rag_chain = RAGChain(st.session_state.kb.get_retriever())
    st.success(f"知识库构建完成！共处理 {len(documents)} 个文档，生成 {len(chunks)} 个文本块")

def main():
    st.set_page_config(page_title="RAG智能问答系统", page_icon="📚")
    init_session_state()
    
    st.title("📚 RAG智能问答系统")
    
    with st.sidebar:
        st.header("文档管理")
        
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.write(f"已选择 {len(uploaded_files)} 个文件")
            for file in uploaded_files:
                st.write(f"- {file.name}")
        
        if st.button("构建知识库"):
            with st.spinner("正在构建知识库..."):
                build_knowledge_base()
        
        if st.button("清空知识库"):
            import shutil
            if os.path.exists("./chroma_db"):
                shutil.rmtree("./chroma_db")
            if os.path.exists("./uploaded_docs"):
                shutil.rmtree("./uploaded_docs")
            st.session_state.kb = KnowledgeBase()
            st.session_state.rag_chain = None
            st.session_state.chat_history = []
            st.success("知识库已清空")
        
        st.header("知识库状态")
        doc_count = st.session_state.kb.get_documents_count()
        st.write(f"文本块数量: {doc_count}")
        if doc_count > 0:
            st.success("知识库已就绪")
        else:
            st.info("知识库为空，请上传文档")
    
    st.header("问答交互")
    
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])
            if "sources" in chat and chat["sources"]:
                st.caption(f"参考来源: {', '.join(chat['sources'])}")
    
    question = st.chat_input("请输入您的问题")
    
    if question:
        if not st.session_state.rag_chain:
            st.warning("请先构建知识库")
            return
        
        with st.chat_message("user"):
            st.write(question)
        
        with st.spinner("正在思考..."):
            answer, sources = st.session_state.rag_chain.ask(question)
        
        with st.chat_message("assistant"):
            st.write(answer)
            if sources:
                st.caption(f"参考来源: {', '.join(sources)}")
        
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "sources": sources})

if __name__ == "__main__":
    main()