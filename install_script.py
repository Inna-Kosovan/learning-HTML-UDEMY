import subprocess

def install_libraries():
    subprocess.run(["pip", "install", "tensorflow-gpu", "pandas", "scikit-learn"])

if __name__ == "__main__":
    install_libraries()
    