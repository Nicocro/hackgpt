install:
	python3.9 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	streamlit run app.py
