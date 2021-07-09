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
"""

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

if __name__ != '__main__':
    # App is being run externally (through gunicorn).
    gunicorn_logger_access = logging.getLogger("gunicorn.access")
    # Use the gunicorn logger as the app logger.
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    # Use the specified log level.
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/search', methods=["GET"])
def fetch_tweets():
    query = request.args["query"]
    response = api.get_conversations(search_keyword=query,
                                     max_num_conv=config.Config.API_MAX_NUM_CONVERSATIONS,
                                     max_num_pages=config.Config.API_MAX_NUM_PAGES,
                                     max_page_res=config.Config.API_MAX_PAGE_NUM_RESULTS,
                                     parse_func=api.parse_as_samsum_dataset)
    return jsonify({"conversations": response})

@app.route('/topics', methods=["POST"])
def fetch_topics():
    # return jsonify({"body": request.json, "num_topics": request.args["num_topics"]})
    # print(request.form)
    conversation_list = request.json["conversations"]
    num_topics = int(request.args["num_topics"])
    if config.Config.TOPIC_PER_TWEET:
        conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(conversation_list, num_topics=num_topics)
    else:
        conv_topic_probs, topics = bertopic.run_con_topic_modeling(conversation_list, num_topics=num_topics)

    return jsonify({"topics": conv_topic_probs, "index_to_topic": topics})

@app.route('/summarize', methods=["GET"])
def fetch_summaries():
    conversation_list = request.json["conversations"]
    conv_summary_dict = summarizer.run(conversation_list)
    return jsonify({"summaries": conv_summary_dict})

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
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
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
#     data = api.get_conversations(search_keyword="Egypt", max_num_conv=100, max_num_pages=50,
#                                  max_page_res=100,
#                                  parse_func=api.parse_as_samsum_dataset)
#
#     with open('data.json', 'w') as outfile:
#         json.dump(data, outfile)
#
#     # with open('res.json', 'r') as infile:
#     #     data = json.load(infile)["conversations"]
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


#     with open('summary.json', 'w') as summary_file:
#         conv_summary_dict = summarizer.run(data[1:3])
#         json.dump(conv_summary_dict, summary_file)
