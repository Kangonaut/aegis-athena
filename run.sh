#!/bin/zsh
source ./venv/bin/activate
streamlit run streamlit_page.py > default.log 2> error.log &
