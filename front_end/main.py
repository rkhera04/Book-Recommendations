from website import run_streamlit
import pandas as pd

# CHANGE THIS 
csv = pd.read_csv("/Users/rajkhera/Book-Recommendations-1/Webscraping/publications.csv")

run_streamlit(csv)