# Research Paper Recommender System

This project is a **content-based research paper recommender system** that helps users discover relevant research papers based on the content of abstracts. The system is built using **web-scraped data** from research papers and applies **NLP techniques** for text preprocessing, vectorization, and similarity ranking. The project includes three components: `vectorize.py` (for NLP and content similarity), `webscrape.py` (for scraping research paper data), and `website.py` (a front-end interface built with Streamlit).

## Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Web Scraping](#web-scraping)
7. [Content-based Recommender](#content-based-recommender)
8. [Streamlit Application](#streamlit-application)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview

The **Research Paper Recommender System** scrapes research paper metadata (title, authors, abstract, year, etc.) from IEEE Xplore and creates a content-based recommendation engine using **Natural Language Processing (NLP)**. The goal is to provide users with research papers that are most similar to a given input query abstract.

The recommendation engine ranks papers based on **cosine similarity** of their vectorized abstract content, and the front-end is powered by a **Streamlit web app** for an intuitive user experience.

## Tech Stack

- **Python**
- **Streamlit**: For building the web application.
- **BeautifulSoup & Selenium**: For web scraping research papers.
- **NLTK**: For natural language preprocessing.
- **Sentence Transformers**: For embedding abstract texts.
- **sklearn**: For cosine similarity calculations and vectorization.
- **Pandas**: For handling scraped data and CSV files.

## Project Structure
│ ├── vectorize.py # Contains NLP and content similarity logic ├── webscrape.py # Web scraping functionality to extract research papers from IEEE Xplore ├── website.py # Streamlit app for user interaction ├── requirements.txt # Dependencies for the project └── README.md # Project documentation


### Files Explained

1. **vectorize.py**:
   - Preprocesses text using tokenization, lemmatization, and removing stop words.
   - Vectorizes text using pre-trained `SentenceTransformer` embeddings.
   - Ranks abstracts based on cosine similarity.

2. **webscrape.py**:
   - Uses Selenium and BeautifulSoup to scrape research paper metadata from IEEE Xplore.
   - Extracts titles, authors, year, conference/journal names, and abstracts.
   - Saves the scraped data in a CSV file.

3. **website.py**:
   - Streamlit web interface where users can input a query and receive paper recommendations.
   - Allows filtering by author, year, and publisher.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/research-paper-recommender.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app
   ```bash
   streamlit run website.py
   ```

## Usage

### 1. Web Scraping
To scrape research papers from IEEE Xplore, run the webscrape.py file:
```bash
python webscrape.py
```
This script will scrape metadata (titles, authors, abstracts, etc.) from IEEE Xplore for a specified number of pages. The data will be saved in a CSV file called publications.csv.

### 2. Content-based Recommender
To generate recommendations based on the content of research paper abstracts, use the vectorize.py file:
```bash
python vectorize.py
```
You can modify the abstracts list in the script to include the papers you want to compare.

### 3. Streamlit Application
Run the Streamlit app using the following command:
```bash
streamlit run website.py
```
This will launch a local web app where you can search for a paper, view the abstract, and get recommendations based on content similarity.

## Web Scraping
The webscrape.py file uses Selenium to automate the retrieval of research papers from IEEE Xplore. It scrapes the following data for each paper:
- Title
- Authors
- Year
- Conference/Journal name
- Paper type (Conference Paper, Journal Article, etc.)
- Publisher
- Abstract
All scraped data is saved in a publications.csv file for later use in the recommendation engine.

## Content-based Recommender
The recommender system uses a content-based filtering approach by analyzing the text of research paper abstracts. The workflow includes:
1. Preprocessing: Abstracts are tokenized, stop words are removed, and text is lemmatized.
2. Vectorization: Abstracts are converted into dense vectors using pre-trained SentenceTransformer models.
3. Similarity Calculation: Cosine similarity is used to find papers most similar to the query abstract.
4. Ranking: Research papers are ranked based on their similarity scores.
```python
# Define a list of paper abstracts
abstracts = [
    "Deep learning for image detection...",
    "Mathematical theory of communication...",
    "Automatic license plate recognition...",
    "Statistics of random signals...",
]

# Query abstract
query_abstract = "Deep learning for image detection..."

# Get ranked abstracts based on content similarity
ranked_abstracts = rank_abstracts(query_abstract, abstracts)
```
## Streamlit Application
The website.py file creates a Streamlit app where users can:
- Search for research papers by title.
- Filter results based on author, year, or publisher.
- View research paper metadata (title, authors, abstract, etc.).
### Interface
- Search Query: Select a research paper from the drop-down menu.
- Filters: Filter by content, author, year, or publisher.
- Pagination: Navigate through search results with pagination.

## Contributing
If you'd like to contribute, feel free to fork the repository and submit a pull request. All contributions are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.
