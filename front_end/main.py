from website import run_streamlit
import pandas as pd

csv = pd.read_csv("./webscraping/publications.csv")

run_streamlit(csv)