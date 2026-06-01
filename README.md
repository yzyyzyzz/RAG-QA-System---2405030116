# RAG智能问答系统

基于Ollama本地大模型、LangChain框架和Streamlit构建的智能问答系统，能够"学习"指定本地文档并回答相关问题。

## 功能特点

- 📚 支持PDF、DOCX、TXT多种文档格式
- 🔍 基于Chroma向量数据库的高效检索
- 🤖 集成Ollama本地大模型
- 💬 支持多轮对话记忆
- 📊 可视化Web界面

## 环境要求

- Python 3.8+
- Ollama
- 至少8GB内存（推荐16GB+）

## 安装步骤

### 1. 安装Ollama

访问 [Ollama官方网站](https://ollama.com/) 下载并安装Ollama。

### 2. 下载模型

```bash
ollama pull qwen2:7b
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

### 使用步骤

1. 在左侧侧边栏上传文档（支持PDF、DOCX、TXT格式）
2. 点击"构建知识库"按钮，系统会自动解析文档并构建向量库
3. 在问答交互区输入问题并提问
4. 系统会基于知识库内容回答问题

### 命令行版本

```bash
python cli_qa.py
```

## 项目结构

```
.
├── app.py              # Streamlit Web应用
├── knowledge_base.py   # 知识库模块
├── rag_chain.py        # RAG问答链模块
├── cli_qa.py           # 命令行版本
├── test_ollama.py      # Ollama测试脚本
├── requirements.txt    # 依赖清单
├── .gitignore          # Git忽略配置
├── documents/          # 示例文档目录
│   ├── nlp_introduction.txt
│   ├── transformer_architecture.txt
│   ├── bert_model.txt
│   └── gpt_model.txt
└── chroma_db/          # 向量数据库（运行后自动生成）
```

## 关键技术点

### RAG流程

1. **文档加载**：支持PDF、DOCX、TXT等多种格式文档的读取
2. **文本分块**：使用RecursiveCharacterTextSplitter进行分块（chunk_size=1000, chunk_overlap=200）
3. **向量化**：使用HuggingFace的all-MiniLM-L6-v2模型进行文本嵌入
4. **向量存储**：使用Chroma向量数据库存储向量
5. **相似性检索**：根据用户问题检索最相关的3个文本块
6. **答案生成**：结合检索结果和大模型生成答案

### 模型配置

- **嵌入模型**：all-MiniLM-L6-v2
- **大模型**：qwen2:7b（可通过修改代码切换为其他Ollama模型）
- **向量数据库**：Chroma

## 已知问题与改进方向

- [ ] 支持更多文档格式（如PPT、Excel）
- [ ] 添加文档内容预览功能
- [ ] 支持批量删除文档
- [ ] 添加夜间模式
- [ ] 支持导出问答记录

## 许可证

MIT License