# RAG-QA-System (检索增强生成问答系统)

## 项目简介

RAG-QA-System 是一个基于检索增强生成（RAG）技术的智能问答系统，支持上传文档、提取关键信息、通过本地语言模型进行智能问答。系统采用Streamlit构建Web界面，使用Ollama集成本地LLM，实现离线、隐私保护的智能文档问答能力。

## 环境要求与安装步骤

### Python版本要求
- Python 3.9+

### 1. 克隆仓库
```bash
git clone https://github.com/yzyyzyzz/RAG-QA-System---2405030116.git
cd RAG-QA-System---2405030116
```

### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖库
```bash
pip install -r requirements.txt
```

### 4. 安装Ollama
- **Windows/macOS**: 访问 [Ollama官网](https://ollama.ai) 下载安装程序
- **Linux**: 
```bash
curl https://ollama.ai/install.sh | sh
```

### 5. 下载模型
```bash
# 下载Mistral模型（推荐，7B，速度快）
ollama pull mistral

# 或下载其他模型
ollama pull llama2
ollama pull neural-chat
```

### 6. 启动Ollama服务
```bash
ollama serve
```
Ollama默认运行在 `http://localhost:11434`

## 使用说明

### 启动Web应用
```bash
# 确保Ollama服务已运行
streamlit run app.py
```
应用将在 `http://localhost:8501` 打开

### 如何上传文档
1. 在左侧边栏"文档管理"部分点击"上传PDF文件"
2. 选择本地PDF文件（支持单个或批量上传）
3. 系统自动提取文本和进行向量嵌入
4. 成功提示后即可开始提问

### 如何提问
1. 在主界面"输入您的问题"文本框输入问题
2. 点击"提交问题"按钮
3. 系统检索相关文档片段并生成答案
4. 查看答案和引用源的文档片段

### 高级功能
- **参数调整**：左侧边栏可调整检索相关性阈值、答案生成参数
- **文档管理**：查看已上传文档、删除文档、管理向量数据库
- **历史记录**：查看问答历史记录、导出对话

## 关键技术点说明

### RAG流程
```
文档输入 → 文本分割 → 向量嵌入 → 向量数据库存储
                              ↓
用户问题 → 向量嵌入 → 向量检索 → 相关段落 → 提示词构造 → LLM生成答案
```

### 所用模型
- **LLM模型**: Mistral 7B（默认）或 Llama2 等本地模型，通过Ollama调用
- **嵌入模型**: sentence-transformers 的 all-MiniLM-L6-v2（轻量级、速度快）
- **向量数据库**: Chroma（轻量级向量数据库，便于本地部署）

### 嵌入方式
- 文档分割：使用RecursiveCharacterTextSplitter，chunk_size=1000，overlap=200
- 向量化：使用HuggingFace sentence-transformers模型
- 相似度匹配：使用余弦相似度检索Top-K相关文档

### 系统架构
```
┌─────────────────────────────────────┐
│      Streamlit Web Interface        │
├─────────────────────────────────────┤
│  Document Manager | Chat Interface  │
├─────────────────────────────────────┤
│         RAG Pipeline                │
├─────────────────────────────────────┤
│  Embedding │ Vector DB │ LLM API    │
└─────────────────────────────────────┘
     ↓             ↓           ↓
  sentence-      Chroma    Ollama
  transformers             Service
```

## 项目结构
```
RAG-QA-System-2405030116/
├── app.py                    # Streamlit主应用
├── requirements.txt          # 依赖库列表
├── .gitignore               # Git忽略文件配置
├── README.md                # 项目说明文档
├── config.py                # 配置文件
├── core/
│   ├── __init__.py
│   ├── rag_pipeline.py      # RAG核心逻辑
│   ├── document_processor.py # 文档处理模块
│   ├── embedding.py         # 向量嵌入模块
│   └── llm_handler.py       # LLM调用处理
├── utils/
│   ├── __init__.py
│   ├── file_handler.py      # 文件处理工具
│   ├── logging_config.py    # 日志配置
│   └── constants.py         # 常量定义
├── data/
│   └── uploads/             # 上传文档存储目录
├── docs/
│   ├── architecture.md      # 架构设计文档
│   ├── api_reference.md     # API参考
│   └── examples/            # 使用示例
└── tests/
    ├── test_rag_pipeline.py
    └── test_document_processor.py
```

## 项目效果截图

### 1. 首页 - 问答界面
![Home Page](docs/screenshots/01_home_page.png)
- 左侧边栏：文档管理和参数设置
- 中央区域：问题输入框和答案显示
- 实时显示检索的相关文档片段

### 2. 文档上传 - 处理进度
![Document Upload](docs/screenshots/02_document_upload.png)
- 支持拖拽上传PDF文件
- 实时显示文件处理进度
- 成功/失败提示

### 3. 检索结果 - 带源文档
![Retrieval Results](docs/screenshots/03_retrieval_results.png)
- 展示LLM生成的答案
- 显示检索到的相关文档片段
- 标注来源和相关性评分

### 4. 问答示例
```
Q: 如何安装Ollama？
A: 根据您上传的文档，安装Ollama的步骤如下：
   1. 访问Ollama官网下载安装程序
   2. Windows/macOS用户可直接下载安装包
   3. Linux用户可运行安装脚本
   
   [来源文档] 第2页，第15-20行
```

## 性能指标
- **文档处理速度**: ~50KB/s（取决于文档复杂度）
- **向量检索速度**: <100ms（Chroma向量数据库）
- **LLM响应时间**: 2-5秒（Mistral 7B，取决于硬件）
- **支持文档大小**: 单个文件 < 100MB

## 已知问题与改进方向

### 已知问题
1. **大文件处理**: 超大PDF文件（>100MB）可能导致内存溢出
2. **模型切换**: 当前仅支持单个Ollama模型，需重启服务切换
3. **中文支持**: 部分embedding模型对中文支持有限

### 改进方向
- [ ] 支持多种文档格式（Word、Excel、网页等）
- [ ] 实现流式答案生成，提升用户体验
- [ ] 添加答案评分和反馈机制
- [ ] 支持多模型并行调用
- [ ] 实现对话上下文记忆和多轮问答
- [ ] 添加向量数据库持久化和备份功能
- [ ] 优化文档分块策略，提升检索精度

## 故障排除

### Ollama连接失败
```bash
# 检查Ollama服务是否运行
curl http://localhost:11434/api/tags

# 如果无响应，重启Ollama服务
ollama serve
```

### 内存不足
- 减少chunk_size（在config.py中修改）
- 使用更小的embedding模型
- 限制单次检索的文档数量

### 文档解析失败
- 确保PDF文件不损坏
- 尝试重新导出PDF（某些加密PDF可能无法解析）

## 许可证
MIT License

## 贡献指南
欢迎提交Issue和Pull Request！

## 联系方式
如有问题或建议，请联系项目维护者。

---
**最后更新**: 2026年5月25日
