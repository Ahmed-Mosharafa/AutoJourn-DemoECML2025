"""
    NLP Summarization & Topic Modeling.
    Current implemented endpoints:
    - "/search": fetch Twitter conversations related to passed query.
        - GET request
        - Query Parameters: query: <String>
        - Response is a JSON object of list of conversations.

    - "/topics": Perform topic modeling on passed twitter conversations.
        - GET request
        - Query Parameters: num_topics: <Int>
        - Body must be json of the format:
            {
                "conversation": <list of twitter conversation as returned from the /search endpoint>,
            }
        - Response is a JSON Object of conversations topics probabilities and topic names.

   - "/summarize": Perform summarization on passed twitter conversations.
        - GET request
        - Body must be json of the format:
            {
                "conversation": <list of twitter conversation as returned from the /search endpoint>,
            }
        - Response is a JSON Object of conversations summaries.

    - "/topic-aware-summarize": Perform topic aware summarization on passed twitter conversations.
        - POST request
        - Body must be json of the format:
            {
                "conversation": <list of twitter conversation as returned from the /search endpoint>,
            }
        - Response is a JSON Object of conversations summaries with respect to different topics.

    - "/delta-summarize": Perform delta summarization on passed topic aware summaries.
        - POST request
        - Body must be json of the format:
            {
                "summaries": <dict of topic aware summaries>,
            }
        - Response is a type of plot (image) showing how different are the summarizations.
"""

import json
from summarization.delta_summarization.delta_summarization import DeltaSummarization
from summarization.models.bart import Bart
from summarization.agents.agent_factory import AgentsFactory
from summarization.topic_aware_summarization.topic_aware_summarization import TopicAwareSummarization
# from api_connection.twitter_api.twitter_api import TweetAPI
from api_connection.telegram_api.telegram_api import TelegramAPI
from api_connection.reddit_api.reddit_api import RedditAPI
from topic_modeling.Bertopic import Bertopic
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request, jsonify, send_file
import config
import logging

# Initialize the application's components
app = Flask('NLPLAB')
asgi_app = WsgiToAsgi(app)
config.init()
# api = TweetAPI()
tele_api = TelegramAPI()
reddit_api = RedditAPI()
bertopic = Bertopic(num_topics=10)  # Default number of topics is 10.
summarizer_model = Bart(config.Config.SUMMARIZATION_MODEL)
summarizer_agent = AgentsFactory.get_agent(summarizer_model)
topic_aware_summarizer = TopicAwareSummarization()
delta_summarizer = DeltaSummarization()

if __name__ != '__main__':
    # App is being run externally (through gunicorn).
    gunicorn_logger_access = logging.getLogger("gunicorn.access")
    # Use the gunicorn logger as the app logger.
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    # Use the specified log level.
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/search-telegram', methods=["GET"])
async def fetch_telegram():
    query = request.args["query"]
    response = await tele_api.get_conversations(query, channel_limit=config.Config.MAX_NUM_OF_TELEGRAM_CHANNELS,
                                          message_limit=config.Config.MAX_NUM_OF_TELEGRAM_MESSAGES_PER_CHANNEL)
    return jsonify({"conversations": response})

@app.route('/search-reddit', method=["GET"])
def fetch_reddit():
    query = request.args["query"]
    response = reddit_api.search(query, limit=5)
    return jsonify({"conversations": response})

@app.route('/search', methods=["GET"])
def fetch_conversations():
    # Load conversations from a local JSON file
    with open('dataset/test.json', 'r') as infile:  # Replace with your dataset path
        conversations = json.load(infile)
    return jsonify({"conversations": conversations})


@app.route('/topics', methods=["POST"])
def fetch_topics():
    # return jsonify({"body": request.json, "num_topics": request.args["num_topics"]})
    conversation_list = request.json["conversations"]
    num_topics = int(request.json["num_topics"])
    # Update topic count if necessary.
    bertopic.check_topic_count(num_topics)
    if config.Config.TOPIC_PER_TWEET:
        conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(conversation_list)
    else:
        conv_topic_probs, topics = bertopic.run_con_topic_modeling(conversation_list)

    return jsonify({"topics": conv_topic_probs, "index_to_topic": topics})


@app.route('/summarize', methods=["POST"])
def fetch_summaries():
    conversation_list = request.json["conversations"]
    conv_summary_dict = summarizer_agent.run_all(conversation_list)
    return jsonify({"summaries": conv_summary_dict})


@app.route('/topic-aware-summarize', methods=["POST"])
def topic_aware_summarize():
    conversation_list = request.json["conversations"]
    num_topics = int(request.json["num_topics"])
    # Update topic count if necessary.
    bertopic.check_topic_count(num_topics)
    topics_df, topic_embeddings = bertopic.get_topic_embeddings(conversation_list)
    dict_topic_sentences = topic_aware_summarizer.extract_topic_sentences(conversation_list[:2], topics_df,
                                                                          topic_embeddings)
    conv_summaries = summarizer_agent.run_all_topic_aware(dict_topic_sentences)
    return jsonify({"conv_summaries": conv_summaries})


@app.route('/delta-summarize', methods=["POST"])
def delta_summarize():
    summaries = request.json["summaries"]
    plot_type = request.json["plot_type"]
    plot_img = delta_summarizer.send_plot(plot_type, summaries)
    return send_file(plot_img, mimetype='image/png')


@app.route('/health', methods=["GET"])
def get_health_status():
    """
    API endpoint to check if the app has started running
    :return: The health status of the app.
    """
    return jsonify({"status": "healthy"})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Error handlers
@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"message": error.description}), 404


@app.errorhandler(Exception)
def handle_server_error(error):
    return jsonify({"message": "Internal server error: {}".format(error)}), 500

# if __name__ == '__main__':
#     import json
#
#     data = api.get_conversations(search_keyword="Euro", max_num_conv=100, max_num_pages=50,
#                                  max_page_res=100,
#                                  parse_func=api.parse_as_conv_hierarchy)
#
#     with open('data.json', 'w') as outfile:
#         json.dump(data, outfile)
#
#     with open("/home/hatem/TUM/Semester 4/Practical Lab/Football_qeury/data.json", 'r') as infile:
#         data = json.load(infile)
#
#     if config.Config.TOPIC_PER_TWEET:
#         conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(data, num_topics=10)
#     else:
#         conv_topic_probs, topics = bertopic.run_con_topic_modeling(data, num_topics=10)
#
#     with open('conv_topics.json', 'w') as outfile:
#         json.dump(conv_topic_probs, outfile)
#
#     with open('topics_idx.json', 'w') as outfile:
#         json.dump(topics, outfile)
#
#     with open('summary.json', 'w') as summary_file:
#         conv_summary_dict = summarizer_agent.run_all(data[0:1])
#         json.dump(conv_summary_dict, summary_file)
