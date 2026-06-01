import subprocess
import sys
import os

def main():
    streamlit_script = os.path.join(os.path.dirname(__file__), "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_script, "--server.port", "8501"])

if __name__ == "__main__":
    main()