from abc import ABC, abstractmethod
from typing import List, Dict


class Agent(ABC):

    @abstractmethod
    def run_conv(self, conv_root: Dict) -> str:
        pass

    def run_all(self, conv_list: List[Dict[str, List[str]]]) -> Dict[str, str]:
        summaries = {}  # conversation summaries
        for conv_dict in conv_list:
            conv_id, conv_root = next(iter(conv_dict.items()))
            conv_summary = self.run_conv(conv_root)
            summaries[conv_id] = conv_summary

        return summaries
