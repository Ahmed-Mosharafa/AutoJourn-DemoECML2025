import re
from nltk.tokenize import RegexpTokenizer
import spacy

def remove_patterns(text):
    """
        Remove punctions, emails, hashtags in given text
    """

    if isinstance(text, spacy.tokens.span.Span):
        text = text.text
    # Remove return char
    text = re.sub(r'\n', ' ', text)
    # Remove emails
    text = re.sub(r'\S*@\S*\s?', '', text)
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    return text

def extract_patterns(text):
    """
        Extract punctions, emails, hashtags in given text
    """
    # extract emails
    emails = re.findall(r'\S+@\S+', text)
    # extract hashtags
    hashtags = re.findall(r'#\w+', text)
    # extract punctuation
    punctuation = re.findall(r'[^\w\s]', text)
    
    return punctuation, emails, hashtags

def remove_punct_nltk(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokenizer.tokenize(text)
    return text