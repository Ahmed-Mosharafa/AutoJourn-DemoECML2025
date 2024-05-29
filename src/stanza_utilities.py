### Imports
import stanza
import pandas as pd
import traceback

class StanzaSegmentizer:
    ##==========================================================================================================
    """
    Definition of attributes
    """
    __nlp_stanza = None
    ##==========================================================================================================
    """
    Function: __init__
    """
    def __init__(self):
        try:
            if self.__nlp_stanza == None:
                print("Initializing stanza")
                self.initialize_stanza()
        except Exception as excMsg:
            print(excMsg)
    ##==========================================================================================================
    """
    Function: initialize_stanza
    """
    def initialize_stanza(self):
        try:            
            self.__nlp_stanza = stanza.Pipeline('en')
        except Exception as excmsg:
            print(f"An error happens in initialize_spacy(...) {traceback.format_exc()}.")
            self.__nlp_stanza = None
        return self.__nlp_stanza
    ##==========================================================================================================
    """
    Function: segment_into_sentences
    """
    def segment_into_sentences(self, src_text="", _format="str"):
        intermediate_result = None

        if isinstance(src_text, str):
            intermediate_result = [s for s in (self.__nlp_stanza(src_text)).sentences]
        elif isinstance(src_text, list):
            intermediate_result = list()

            for sent in src_text:
                intermediate_result.extend([s for s in (self.__nlp_stanza(sent)).sentences])

        if _format == "str":
            sentences_new_doc = list()
    
            for intsent in intermediate_result:
                sentences_new_doc.append(intsent.text)
            return sentences_new_doc
        else:
            return intermediate_result
    ##==========================================================================================================

##==========================================================================================================