import ollama

def test_ollama():
    try:
        response = ollama.chat(model='qwen2:7b', messages=[
            {
                'role': 'user',
                'content': 'Hello!',
            }
        ])
        print("Ollama API测试成功!")
        print("响应内容:", response['message']['content'])
        return True
    except Exception as e:
        print(f"Ollama API测试失败: {e}")
        print("请确保Ollama已安装并运行，且已下载qwen2:7b模型")
        return False

if __name__ == "__main__":
    test_ollama()