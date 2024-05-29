from abc import ABC, abstractmethod
from typing import List, Dict
from summarization.models.summarizer import SummarizationModel


class Agent(ABC):

    def __init__(self, summarizer_model: SummarizationModel):
        self.summarizer_model = summarizer_model

    @abstractmethod
    def run_conv(self, conv_root: Dict) -> str:
        pass

    def run_all(self, conv_list: List[Dict[str, List[str]]]) -> Dict[str, str]:
        print(4)
        summaries = {}  # conversation summaries
        print(5)
        for conv_dict in conv_list:
            conv_root = list(conv_dict.items())[0][1]
            conv_id = list(conv_dict.items())[1][1]

            #conv_root, conv_id = next(iter(conv_dict.items()))
            conv_summary = self.run_conv(conv_root)
            print(7)
            summaries[conv_id] = conv_summary
            print(8)

        return summaries
