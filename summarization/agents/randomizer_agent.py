from typing import Dict, List

from summarization.agents.base_agent import BaseAgent
from summarization.models.summarizer import SummarizationModel
import random


class RandomizerAgent(BaseAgent):
    def __init__(self, summarizer_model: SummarizationModel, sample_size: int):
        super(BaseAgent).__init__(summarizer_model)
        self.sample_size = sample_size

    def __sample(self, tweets: List[str]) -> List[str]:
        idx_set = set([])
        while len(idx_set) < self.sample_size:
            rand_idx = random.randrange(len(tweets))
            if rand_idx not in idx_set:
                idx_set.add(rand_idx)

        idx_set = sorted(idx_set)
        reservoir = [tweets[k] for k in idx_set]
        return reservoir

    def run_conv(self, conv_root: Dict) -> str:
        tweets_list = []
        self.__flatten_tree(conv_root, tweets_list)
        tweets_list = self.__sample(tweets_list)
        summary = self.summarizer_model.summarize(tweets_list)
        return summary
