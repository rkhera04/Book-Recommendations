import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import BertTokenizer, BertModel
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize, MinMaxScaler

# download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    # convert to lowercase
    text = text.lower()
    
    # replace hyphens with space
    text = text.replace('-', ' ')

    # remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)

    # remove numbers
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\b\w*\d+\w*\b', '', text)
    
    # tokenize text
    tokens = word_tokenize(text)
    
    # remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    
    # lemmatize tokens
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # reassemble text
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def compute_embeddings(texts):
    preprocessed_texts = [preprocess_text(text) for text in texts]

    # initialize SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(preprocessed_texts, convert_to_tensor=True)
    
    return embeddings.cpu().numpy()

def get_similarities(embedding, embeddings):
    return cosine_similarity([embedding], embeddings)[0]

def rank_abstracts(query_abstract, abstracts):
    # preprocess texts
    preprocessed_abstracts = [preprocess_text(text) for text in abstracts]
    
    all_embeddings = compute_embeddings(abstracts)
    query_embedding = compute_embeddings([query_abstract])[0]
    
    # compute similarities
    similarities = get_similarities(query_embedding, all_embeddings)

    ranked_indices = np.argsort(similarities)[::-1]
    
    return [
        (abstracts[i], preprocessed_abstracts[i], similarities[i]) 
        for i in ranked_indices
    ]

# Example usage
if __name__ == "__main__":
    abstracts = [
        deep_learn_image_detect, math_theory_of_comm, auto_licenseplate_recog_img_process, 
        stats_rand_signals, matplotlib_2dgraphics, neural_networks_quantization_refine
    ]

    query_abstract = deep_learn_image_detect
    
    ranked_abstracts = rank_abstracts(query_abstract, abstracts)
    
    for original, preprocessed, score in ranked_abstracts:
        print(f"Similarity Score: {score:.4f}")
        print(f"Original Abstract: {original}")
        print(f"Preprocessed Abstract: {preprocessed}\n")
