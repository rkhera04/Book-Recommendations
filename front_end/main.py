from website import run_streamlit
import pandas as pd

# CHANGE THIS 
csv = pd.read_csv("./Webscraping/publications.csv")

run_streamlit(csv)