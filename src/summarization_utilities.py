### Imports
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import ProphetNetForConditionalGeneration, ProphetNetTokenizer
import torch

from config import config

### Classes and functions

##==========================================================================================================
class SummarizationUtilities:
    ##==========================================================================================================
    """
    Definition of attributes
    """
    model_name = None
    device = None
    tokenizer = None
    model = None
    ##==========================================================================================================
    """
    Function: __init__
    Arguments:
        - model_name
        - device
    """
    def __init__(self, model_name="google/pegasus-xsum", device=None, model_path=config.pegasus_model_path):
        self.model_name = model_name
        if device == None:
            self.device = self.detect_available_cuda_device()
        else:
            self.device = device

        self.tokenizer = PegasusTokenizer.from_pretrained(model_path)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_path).to(device)
    ##=========================================================================================================
    """
    Function: detect_available_cuda_device
    Arguments: NA
    """
    def detect_available_cuda_device(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    ##=========================================================================================================
    """
    Function: detect_available_cuda_device
    Arguments: NA
    """
    def tokenize(self, src_text, truncation = True, padding="longest", return_tensors="pt"):
        return self.tokenizer(src_text, truncation=truncation, padding=padding, return_tensors=return_tensors).to(self.device)
    ##=========================================================================================================
    """
    Function: generate
    Arguments: 
        - batch
    """
    def generate(self, batch):
        text_generated = self.model.generate(**batch)
        return text_generated
    ##=========================================================================================================
    """
    Function: decode_generated_text
    Arguments: 
        - batch
    """
    def decode_generated_text(self, generated_text, skip_special_tokens=True):
        return self.tokenizer.batch_decode(generated_text, skip_special_tokens=skip_special_tokens)
    ##=========================================================================================================
    """
    Function: get_summary
    Arguments: 
        - src_text
    """
    def get_summary(self, src_text):
        summary = None

        batch = self.tokenize(src_text)
        generated_text = self.generate(batch)
        target_text = self.decode_generated_text(generated_text)
        #print("target_text", target_text)
        summary = target_text

        return summary

    def summarize(self, src_text):
        summary = None

        batch = self.tokenize(src_text)
        generated_text = self.generate(batch)
        target_text = self.decode_generated_text(generated_text)
        #print("target_text", target_text)
        summary = target_text

        return summary
        
    ##=========================================================================================================
##==========================================================================================================



class BARTSummarizer:
    def __init__(self, device=None, model_path=config.bart_model_path):
        # https://stackoverflow.com/questions/66639722/why-does-huggingfaces-bart-summarizer-replicate-the-given-input-text
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-xsum-6-6") #facebook/bart-large-cnn
        # self.model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-xsum-6-6").to(self.device)
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model = BartForConditionalGeneration.from_pretrained(model_path)

    def summarize(self, text):
        inputs = self.tokenizer([text], truncation=True, padding="longest", return_tensors="pt").to(self.device)
        summary_ids = self.model.generate(inputs["input_ids"], num_beams=4, max_length=200, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
        return summary


class T5Summarizer:
    def __init__(self, device=None, model_path=config.t5_model_path):
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.tokenizer = T5Tokenizer.from_pretrained("t5-base")
        # self.model = T5ForConditionalGeneration.from_pretrained("t5-base").to(self.device)
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path).to(self.device)

    def summarize(self, text):
        inputs = self.tokenizer.encode_plus(text, return_tensors="pt", truncation=True, padding="longest").to(self.device)
        summary_ids = self.model.generate(inputs.input_ids)
        summary = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
        return summary


class ProphetNetSummarizer:
    def __init__(self, device=None, model_path=config.prophetnet_model_path):
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.tokenizer = ProphetNetTokenizer.from_pretrained("microsoft/prophetnet-large-uncased")
        # self.model = ProphetNetForConditionalGeneration.from_pretrained("microsoft/prophetnet-large-uncased").to(self.device)
        self.tokenizer = ProphetNetTokenizer.from_pretrained(model_path)
        self.model = ProphetNetForConditionalGeneration.from_pretrained(model_path).to(self.device)

    def summarize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding="longest").to(self.device)
        summary_ids = self.model.generate(inputs.input_ids)
        summary = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
        return summary