# !/bin/sh
source .venv/Scripts/activate
pip install -r requirements.txt
# streamlit run your_script.py [-- script args]

# cp data/go/* data/saved/.
streamlit run server.py