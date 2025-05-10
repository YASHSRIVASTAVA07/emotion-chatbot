from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# Direct import for loading the data
from data_loader import load_data
from utils.preprocessor import clean_text

# Load and clean training data
train_texts, train_labels = load_data('data/train.txt')
train_texts = [clean_text(t) for t in train_texts]

# Load and clean validation data
val_texts, val_labels = load_data('data/val.txt')
val_texts = [clean_text(t) for t in val_texts]

# Create TF-IDF + Naive Bayes pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# Train the model
pipeline.fit(train_texts, train_labels)

# Validate the model
preds = pipeline.predict(val_texts)
print(classification_report(val_labels, preds))

# Save the trained model to a file
joblib.dump(pipeline, 'models/emotion_model.pkl')
print("Model saved to models/emotion_model.pkl")
