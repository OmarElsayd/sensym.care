import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
import webbrowser
import joblib
import matplotlib.pyplot as plt
from collections import Counter
from summa import keywords
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from networkx import Graph
from networkx.algorithms.link_analysis.pagerank_alg import pagerank



class SentimentAnalyzer:
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path)
        self.best_model = None

    @staticmethod
    def summarize(text, n):
        # Tokenize the text into sentences and words
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        # Remove stop words and stem the words
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()
        words = [ps.stem(word) for word in words if word not in stop_words]

        # Calculate the frequency distribution of the words
        freq_dist = FreqDist(words)

        # Create a graph of bigrams
        finder = BigramCollocationFinder.from_words(words)
        bigram_measures = BigramAssocMeasures()
        graph = Graph()
        for w1, w2 in finder.nbest(bigram_measures.pmi, 10):
            graph.add_edge(w1, w2)

        # Create a graph of sentences
        graph.add_nodes_from(sentences)
        for i, sentence1 in enumerate(sentences):
            for j, sentence2 in enumerate(sentences):
                if i != j:
                    words1 = word_tokenize(sentence1.lower())
                    words2 = word_tokenize(sentence2.lower())
                    words1 = [ps.stem(word) for word in words1 if word not in stop_words]
                    words2 = [ps.stem(word) for word in words2 if word not in stop_words]
                    common_words = set(words1) & set(words2)
                    if common_words:
                        weight = len(common_words) / (len(words1) + len(words2))
                        graph.add_edge(sentence1, sentence2, weight=weight)

        # Rank the sentences based on PageRank algorithm
        scores = pagerank(graph)

        # Sort the sentences by score in descending order
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top n sentences
        top_sentences = [sentence for sentence, score in sorted_scores[:n]]

        return ' '.join(top_sentences)

    @staticmethod
    def preprocess_text(text):
        return text.lower()

    def train(self):
        data = self.data_df["sentence"]
        target = self.data_df["label"]

        train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=0.2, random_state=42)

        pipeline = Pipeline([
            ("vectorizer", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=5000)),
            ("classifier", LogisticRegression(solver="liblinear", random_state=42)),
        ])

        param_grid = {
            "vectorizer__min_df": [2, 5],
            "classifier__C": [0.1, 1, 10],
        }

        grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
        grid_search.fit(train_data.apply(self.preprocess_text), train_target)

        self.best_model = grid_search.best_estimator_

    def test(self):
        data = self.data_df["sentence"]
        target = self.data_df["label"]

        train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=0.2, random_state=42)

        predictions = self.best_model.predict(test_data.apply(self.preprocess_text))

        accuracy = accuracy_score(test_target, predictions)
        "Model Accuracy: {accuracy}", accuracy
        return accuracy

    def predict(self, new_data):
        preprocessed_data = [self.preprocess_text(text) for text in new_data]
        predictions = self.best_model.predict(preprocessed_data)
        return predictions

    def save_model(self, file_path):
        joblib.dump(self.best_model, file_path)

    def load_model(self, file_path):
        self.best_model = joblib.load(file_path)

# read data from text file
def read_data(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return data

# convert text to list of sentences
def convert_to_list(data):
    sentences = data.split(".")
    return sentences




def sentiments_histogram(sentiments, path):
    # Plot a histogram of the sentiment frequencies
    # Count the occurrences of each unique element using Counter
    element_counts = Counter(sentiments)

    # Separate the labels (unique elements) and their counts
    labels = list(element_counts.keys())
    counts = list(element_counts.values())

    print("\n====== UNIQUE LABELS: =======\n\n")

    # Plot the histogram using the counts and labels

    plt.hist(list(element_counts.values()), bins=range(1, 10))


    # Plot a histogram of the keyword frequencies
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.title('Histogram of Sentiments in Paragraph')

    # save the histogram to a file
    plt.savefig(f'{path}/sentiment_histogram.png')

    # Add the histogram to the report
    plt.show()

def sentiments_piechart(sentiments, path):
    # Plot a pie chart of the sentiment frequencies

    # Count the occurrences of each unique element using Counter
    element_counts = Counter(sentiments)

    # Separate the labels (unique elements) and their counts
    labels = list(element_counts.keys())
    counts = list(element_counts.values())

    # Plot the pie chart using the counts and labels
    plt.pie(counts, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Unique Sentiment Counts')

    # save the pie chart to a file
    plt.savefig(f'{path}/sentiment_piechart.png')
    plt.show()
    
    
def train_model():
    # Train the model
    analyzer = SentimentAnalyzer("sensym_db_api/db_apis/voice/sentiment_dataset.csv")
    analyzer.train()

    # Save the model
    analyzer.save_model("sensym_db_api/db_apis/voice/sentiment_analysis.joblib")