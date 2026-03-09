1. Clone PageIndex repository:
```bash
git clone https://github.com/VectifyAI/PageIndex.git
```

2. Run the following to generate the JSON index tree:
```bash
uv run python PageIndex/run_pageindex.py --pdf_path data/The-AI-Act.pdf --if-add-node-text yes 
```