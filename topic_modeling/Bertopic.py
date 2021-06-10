from topic_modeling.topic_modeling import TopicModeling
import re
from bertopic import BERTopic
from umap import UMAP


class Bertopic(TopicModeling):

    def __init__(self):
        self.__int__(None)

    def __int__(self, num_topics=None):
        super(Bertopic, self).__init__()
        umap_model = UMAP(n_neighbors=15,
                          transform_seed=173,  # fix a seed to avoid randomization in UMAP (we use a prime number)
                          n_components=5,
                          min_dist=0.0,
                          metric='cosine')

        self.model = BERTopic(nr_topics=num_topics,
                              language="multilingual",  # Use multilingual sentence-tranformers embedding model
                              top_n_words=5,
                              calculate_probabilities=True,
                              verbose=True,
                              n_gram_range=(1, 1),
                              umap_model=umap_model)

    def get_topics(self, docs):
        _, probs = self.model.fit_transform(docs)
        topics_df = self.model.get_topic_info()
        return topics_df, probs

    def preprocess(self, tweet):
        t_tweet = re.sub(r"http\S+", "", tweet)  # remove links
        t_tweet = re.sub(r"@\S+", "", t_tweet)  # remove tags

        # remove author which is at the beginning of each tweet delimtted by ':'
        t_tweet = re.sub(r"\w+:\s?", "", t_tweet)
        t_tweet = self.__remove_emojis(t_tweet)
        return t_tweet

    def __remove_emojis(self, tweet):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', tweet)
