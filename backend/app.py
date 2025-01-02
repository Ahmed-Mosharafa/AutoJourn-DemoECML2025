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
from language_detection.lang_detection import LangDetect
from summarization.delta_summarization.delta_summarization import DeltaSummarization
from summarization.models.bart import Bart
from summarization.agents.agent_factory import AgentsFactory
from summarization.topic_aware_summarization.topic_aware_summarization import TopicAwareSummarization
# from api_connection.twitter_api.twitter_api import TweetAPI
from api_connection.telegram_api.telegram_api import TelegramAPI
from api_connection.reddit_api.reddit_api import RedditAPI
from topic_modeling.Bertopic import Bertopic
#from topic_modeling.mistral import MistralTopicModeling
from topic_modeling.mistral_summary import MistralTopicModeling
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request, jsonify, send_file, redirect, url_for
from flask_restx import Api, Resource, fields
import config
import logging
import asyncio
from redis.asyncio import Redis

# Initialize the application's components
app = Flask('NLPLAB')

# Initialize Redis client globally
redis_client = Redis.from_url("redis://localhost:6379", decode_responses=True)

api = Api(app, version='1.0',
          title='Automated Journalist App',
          description='API for Automated Journalist App - NLP Summarization & Topic Modeling')

asgi_app = WsgiToAsgi(app)
config.init()

# twitter_api = TweetAPI()
tele_api = TelegramAPI()
reddit_api = RedditAPI()

bertopic = Bertopic(num_topics=10)  # Default number of topics is 10.
mistral_modeling= MistralTopicModeling()
summarizer_model = Bart(config.Config.SUMMARIZATION_MODEL)
summarizer_agent = AgentsFactory.get_agent(summarizer_model)
topic_aware_summarizer = TopicAwareSummarization()
delta_summarizer = DeltaSummarization()
lang_detect = LangDetect()

samsum = api.model('Samsum', {
    'id': fields.String(description='id of the conversation'),
    'summary': fields.String(description='summary of the conversation'),
    'dialogue': fields.String(description='dialogue to summarize'),
})

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
    final_response = []
    for conv in response:
        try:
            if lang_detect.is_english(conv['dialogue']):
                final_response.append(conv)
        except:
            continue

    return jsonify({"conversations": final_response})


@api.route('/search-reddit')
class SearchReddit(Resource):
    @api.doc(params={'query': 'a string'})
    def get(self):
        query = request.args["query"]
        response = reddit_api.get_conversations(query, limit=5)
        return jsonify({"conversations": response})


# @app.route('/search-twitter', methods=["GET"])
# def fetch_tweets():
#     query = request.args["query"]
#     response = twitter_api.get_conversations(search_keyword=query,
#                                      max_num_conv=config.Config.API_MAX_NUM_CONVERSATIONS,
#                                      max_num_pages=config.Config.API_MAX_NUM_PAGES,
#                                      max_page_res=config.Config.API_MAX_PAGE_NUM_RESULTS,
#                                      parse_func=twitter_api.parse_as_conv_hierarchy)
#     return jsonify({"conversations": response})


# @api.route('/topics')
# class Topics(Resource):
#     @api.doc(body=api.model(
#         'Topics',
#         {
#             'conversations': fields.List(fields.String, description='list of conversations'),
#             'num_topics': fields.Integer(description='number of topics to extract')
#         })
#     )
#     def post(self):
#         conversation_list = request.json["conversations"]
#         num_topics = int(request.json["num_topics"])
#         # Update topic count if necessary.
#         bertopic.check_topic_count(num_topics)
#         if config.Config.TOPIC_PER_TWEET:
#             conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(
#                 conversation_list)
#         else:
#             conv_topic_probs, topics = bertopic.run_con_topic_modeling(
#                 conversation_list)

#         return jsonify({"topics": conv_topic_probs, "index_to_topic": topics})

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)
@api.route('/topics/Mistral', methods=['POST'])
class Topics(Resource):
    # @api.doc(body=api.model(
    #     'Topics',
    #     {
    #         'conversations': fields.List(fields.String, description='list of conversations')
    #     })
    # )
    # def post(self):
    #     try:
    #         # Parse input
    #         conversation_list = request.json["conversations"]

    #         # # Preprocess conversations and concatenate them into one string
    #         # preprocessed_conversations = [
    #         #     phi_modeling.preprocess(conversation) for conversation in conversation_list
    #         # ]
    #         combined_conversations = " ".join(conversation_list)

    #         # Dynamically extract topics
    #         #probs, keywords, topics = phi_modeling.get_topics(combined_conversations)

    #         probs, keywords, topics = mistral_modeling.get_topics(combined_conversations)

    #         # Create a response
    #         response = {
    #             "topics": probs,  # Probabilities for each topic
    #             "index_to_topic": topics,  # List of topic names
    #             "keywords": keywords  # Keywords associated with each topic
    #         }
    #         return jsonify(response)

    #     except Exception as e:
    #         return {"error": str(e)}, 400

    def post(self):
        selectedOption= "mistral"

        try:
            # Parse input
            conversation_list = request.json["conversations"]
            #selectedOption = request.json["selectedModel"]
            combined_conversations = " ".join(conversation_list)

            # Dynamically choose the topic modeling method
            if selectedOption.lower() == "mistral":
                probs, keywords, topics, topics_and_keywords = mistral_modeling.get_topics_test(combined_conversations)
            #elif selectedOption.lower() == "phi":
                # Assuming a PhiModeling class exists
                #probs, keywords, topics = phi_modeling.get_topics(combined_conversations)
            else:
                return {"error": f"Invalid option: {selectedOption}"}, 400

            
            # Offload summary inference to a background thread
            def infer_and_cache_summaries():
                try:
                    # Generate summaries
                    summaries = mistral_modeling.summarize_with_hint_test(combined_conversations, topics_and_keywords)
                    print("Generated summaries:", summaries)  # Debug log to confirm summaries are generated

                    # Cache summaries asynchronously
                    async def cache_summaries():
                        await redis_client.set("mistral_summaries", json.dumps(summaries))
                        print("Summaries cached successfully.")  # Debug log to confirm caching

                    asyncio.run(cache_summaries())
                except Exception as e:
                    print(f"Error in summary generation or caching: {e}")
            print("Submitting background task for summary inference.")
            executor.submit(infer_and_cache_summaries)
            print("Background task submitted.")

            # Create a response
            response = {
                "topics": probs,  # Probabilities for each topic
                "index_to_topic": topics,  # List of topic names
                "keywords": keywords  # Keywords associated with each topic
            }
            return jsonify(response)
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/topics/Mistral/summaries', methods=['GET'])
class Summaries(Resource):
    def get(self):
        try:
            # Fetch summaries asynchronously
            async def fetch_cached_summaries():
                summaries = await redis_client.get("mistral_summaries")
                if summaries:
                    await redis_client.delete("mistral_summaries")  # Delete the key after retrieval
                return json.loads(summaries) if summaries else None

            cached_summaries = asyncio.run(fetch_cached_summaries())

            if not cached_summaries:
                print("Summaries not found in Redis.")
                return {"status": "Summaries are still being processed. Please try again later."}, 202

            print("Retrieved summaries from Redis:", cached_summaries)  # Debug log
            return jsonify({"summaries": cached_summaries})
        except Exception as e:
            print(f"Error retrieving summaries: {e}")
            return {"error": f"Failed to retrieve summaries: {e}"}, 400




@api.route('/summarize')
class Summarize(Resource):
    @api.doc(body=api.model(
        'Summarize', {
            'conversations': fields.List(fields.String, description='list of conversations')
        }
    ))
    def post(self):
        conversation_list = request.json["conversations"]
        conv_summaries = summarizer_agent.run_all(conversation_list)
        return jsonify({"summaries": conv_summaries})


""" @api.route('/topic-aware-summarize')
class TopicAwareSummarize(Resource):
    @api.doc(body=api.model(
        'TopicAwareModel', {
            'conversations': fields.List(fields.String, description='list of conversations'),
            'dialogue': fields.ClassName('Samsum', description='dialogue to summarize'),
            'num_topics': fields.Integer(description='number of topics to extract')
        }
    ))
    def post(self):
        conversation_list = request.json["conversations"]
        dialogue_to_summarize = request.json["dialogue"]
        num_topics = int(request.json["num_topics"])
        user_topics = request.json.get("user_topics", [])
        # Update topic count if necessary.
        bertopic.check_topic_count(num_topics)
        
        try:
            if len(user_topics) > 0:
                topics_df, topic_embeddings = bertopic.get_input_topic_embeddings(
                    user_topics)
            else:
                topics_df, topic_embeddings = bertopic.get_topic_embeddings(
                    conversation_list)
                if len(topic_embeddings < 3):
                    topics_df, topic_embeddings = bertopic.get_static_topics()
        except:
            topics_df, topic_embeddings = bertopic.get_static_topics()
        dict_topic_sentences = topic_aware_summarizer.extract_topic_sentences(dialogue_to_summarize, topics_df,
                                                                              topic_embeddings)
        conv_summaries = summarizer_agent.run_all_topic_aware(
            dict_topic_sentences)
        return jsonify({"conv_summaries": conv_summaries}) """

@api.route('/topic-aware-summarize')
class TopicAwareSummarize(Resource):
    @api.doc(body=api.model(
        'TopicAwareModel', {
            'conversations': fields.List(fields.String, description='list of conversations')
        }
    ))
    def post(self):
        try:
            conversation_list = request.json["conversations"]
            combined_conversations = " ".join(conversation_list)

            # Retrieve cached topics and keywords
            async def fetch_cached_topics():
                cached_data = await redis_client.get("mistral_topics")
                return json.loads(cached_data) if cached_data else None

            cached_topics = asyncio.run(fetch_cached_topics())
            if not cached_topics:
                return {"error": "No cached topics found. Please perform topic modeling first."}, 400

            # Perform summarization
            topics_and_keywords = cached_topics["topics_and_keywords"]
            summaries = mistral_modeling.summarize_with_hint_test(combined_conversations, topics_and_keywords)

            return jsonify({"summaries": summaries})
        except Exception as e:
            return {"error": str(e)}, 400



@api.route('/delta-summarize')
class DeltaSummarize(Resource):
    @api.doc(body=api.model(
        'DeltaSummarize', {
            'summaries': fields.List(fields.String, description='list of summaries'),
            'plot_type': fields.String(description='type of plot'),
            'dialogue': fields.ClassName('Samsum', description='dialogue to summarize'),
            'default_summary': fields.String(description='default summary')
        }
    ))
    def post(self):
        summaries = request.json["summaries"]
        plot_type = request.json["plot_type"]
        dialogue = request.json["dialogue"]
        default_summary = request.json["default_summary"]
        plot_img = delta_summarizer.send_plot(
            plot_type, summaries, dialogue, default_summary)
        return send_file(plot_img, mimetype='image/png')


@app.route('/health')
class Health(Resource):
    @api.doc(description='Check if the app is running.')
    def get(self):
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
