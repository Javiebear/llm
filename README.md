# Libraries and System Dependencies

- Uses Mistral 7B LLM Model

## Setup 

### Mac OS Silicon Chip

The ```llama.ccp``` is used to supercharge the silicon chip

```bash
brew install cmake
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make clean && make LLAMA_METAL=1
```
