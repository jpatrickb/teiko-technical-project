setup:
	pip install --quiet uv
	uv sync

pipeline:
	uv run python load_data.py
	uv run python analysis.py

dashboard:
	uv run streamlit run dashboard.py
