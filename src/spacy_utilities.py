### Imports
import spacy
from spacy.lang.en import English
from spacy import displacy

import pandas as pd

import traceback

class SpacySegmentizer:
    ##==========================================================================================================
    """
    Definition of attributes
    """
    __nlp_SpaCy = None
    ##==========================================================================================================
    """
    Function: __init__
    """
    def __init__(self):
        if self.__nlp_SpaCy == None:
            print("Initializing spacy")
            self.initialize_spacy()
    ##==========================================================================================================
    """
    Function: initialize_spacy
    """
    def initialize_spacy(self):
        try:
            self.__nlp_SpaCy = English()
            #self.__nlp_spacy = spacy.load("en_core_web_sm")
            self.__nlp_SpaCy.add_pipe("sentencizer")
            #nlp.add_pipe("sentencizer", config={"punct_chars":[".", ";"]})
        except Exception as excmsg:
            print(f"An error happens in initialize_spacy(...) {traceback.format_exc()}.")
            self.__nlp_SpaCy = None
        return self.__nlp_SpaCy
    ##==========================================================================================================
    """
    Function: segment_into_sentences
    """
    def segment_into_sentences(self, src_text="", _format=""):
        intermediate_result = None

        if isinstance(src_text, str):
            intermediate_result = [s for s in (self.__nlp_SpaCy(src_text)).sents]
        elif isinstance(src_text, list):
            intermediate_result = list()

            for sent in src_text:
                intermediate_result.extend([s for s in (self.__nlp_SpaCy(sent)).sents])

        if _format == "str":
            sentences_new_doc = list()
    
            for intsent in intermediate_result:
                sentences_new_doc.append(" ".join([str(s) for s in intsent]))
            
            return sentences_new_doc
        else:
            return intermediate_result
    ##==========================================================================================================

##==========================================================================================================