install:
	python3.9 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python3.9 streamlit run streamlit_app.py
