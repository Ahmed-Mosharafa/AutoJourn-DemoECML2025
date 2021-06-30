from summarization.bartcnn import BartSummarizationModel
from twitter_api.twitter_api import TweetAPI
from topic_modeling.Bertopic import Bertopic
from flask import Flask, request, jsonify
import config
import json
import logging


# Initialize the application's components
app = Flask('NLPLAB')
config.init()
api = TweetAPI()
bertopic = Bertopic()
summarizer = BartSummarizationModel()


@app.route('/search', methods=["GET"])
def fetch_tweets():
    query = request.args["query"]
    response = api.get_conversations(search_keyword=query,
                                     max_num_conv=config.Config.API_MAX_NUM_CONVERSATIONS,
                                     max_num_pages=config.Config.API_MAX_NUM_PAGES,
                                     max_page_res=config.Config.API_MAX_PAGE_NUM_RESULTS,
                                     parse_func=api.parse_as_samsum_dataset)
    return jsonify({"conversations": response})


@app.route('/topics', methods=["GET"])
def fetch_topics():
    conversations = request.args["conversations"]
    num_topics = request.args["num_topics"]

    if config.Config.TOPIC_PER_TWEET:
        conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(conversations, num_topics=num_topics)
    else:
        conv_topic_probs, topics = bertopic.run_con_topic_modeling(conversations, num_topics=num_topics)

    return jsonify({"topics": conv_topic_probs, "index_to_topic": topics})


@app.route('/summarize', methods=["GET"])
def fetch_summaries():
    conversations = request.args["conversations"]
    conv_summary_dict = summarizer.run(conversations)
    return jsonify({"summaries": conv_summary_dict})


@app.route('/health', methods=["GET"])
def get_health_status():
    """
    API endpoint to check if the app has started running
    :return: The health status of the app.
    """
    return jsonify({"status": "healthy"})


# Error handlers
@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"message": error.description}), 404


@app.errorhandler(Exception)
def handle_server_error(error):
    return jsonify({"message": "Internal server error: {}".format(error)}), 500


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     logging.error("Run as python app.py <search_keyword>")
    # else:

    #

    with open('data.json', 'r') as f:
        data = json.load(f)

    # with open('data.json', 'w') as outfile:
    #     json.dump(data, outfile)
    #
    # if config.Config.TOPIC_PER_TWEET:
    #     conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(data, num_topics=10)
    # else:
    #     conv_topic_probs, topics = bertopic.run_con_topic_modeling(data, num_topics=10)
    #
    # with open('conv_topics.json', 'w') as outfile:
    #     json.dump(conv_topic_probs, outfile)
    #
    # with open('topics.json', 'w') as outfile:
    #     json.dump(topics, outfile)

    with open('summary.json', 'w') as summary_file:
        conv_summary_dict = summarizer.run(data[1:3])
        json.dump(conv_summary_dict, summary_file)
