# Libraries and System Dependencies

- Tested on MacOS Silicon chip environment
- Python Ver: ```python3.12```
- Uses Mistral 7B LLM Model
- huggingface_hub
- pip install llama-cpp-python

## requirements

```bash
pip install huggingface_hub
pip install llama-cpp-python
```

## Setup 



**The ```llama.ccp``` is used to supercharge the silicon chip**

```bash
brew install cmake
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

mkdir build
cd build
cmake .. -DLLAMA_METAL=ON
cmake --build . --parallel

cd ..
```

**Dowloading the model in the llama directory**

This model is selected for a system with 8gb of ram
```bash
wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_0.gguf -P ./models

```

**Running the model**
```bash
cd build/bin
./llama-server -m ../../models/mistral-7b-v0.1.Q4_0.gguf -c 2048 -n 256 --threads 8 --n-gpu-layers 50
```
