# PageIndex tutorial with local Ollama

## Preliminary steps:

1. Make a copy of `.env.template` and rename it `.env`. Replace `<CHATGPT_API_KEY>` and `<PAGEINDEX_API_KEY>` with your API keys.

2. Install [ollama](https://ollama.com/download) in your CLI then run the following commands to get the required model:
```bash
ollama pull qwen3:30b
```

3. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

4. Clone PageIndex repository:
```bash
git clone https://github.com/VectifyAI/PageIndex.git
```

## Steps to run tutorial:

1. Launch jupyter notebook in your browser by running the following command in your CLI
```bash
uv run jupyter notebook
```

2. Run the `remote_pageindex.py` script as a Jupyter notebook
> To run a `.py` script as Jupyter notebook right click on it and run it as a Jupytext notebook

3. Run the following to generate the JSON index tree:
```bash
uv run python PageIndex/run_pageindex.py --pdf_path data/The-AI-Act.pdf --if-add-node-text yes 
```
> If you skipped step 0 then you should dowload [The AI Act PDF](https://artificialintelligenceact.eu/wp-content/uploads/2021/08/The-AI-Act.pdf) and place inside `./data`.

4. Run the local PageIndex scripts, as Jupyter notebooks, in the following order:
- `local_pageindex.py`
- `local_pageindex_ollama.py`
- `local_pageindex_ollama_improved.py`
