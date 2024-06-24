from telethon import TelegramClient
from telethon import functions, types
import asyncio
from summarization.models.samsum import Samsum, MessageThread
import json
import config as config


class TelegramAPI:
    def __init__(self):
        self.client = TelegramClient(
            'nlp_user', config.Config.TELEGRAM_API_ID, config.Config.TELEGRAM_API_HASH)

    def get_conversations(self, query: str, channel_limit=5, message_limit=10, parse_func=None):
        result = self.query(query, channel_limit, message_limit)
        return parse_func(result) if parse_func else self.parse_all_messages_json(result)

    def query(self, query: str, channel_limit=5, message_limit=10) -> list[MessageThread]:
        print("before loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(self.query_async(query, channel_limit, message_limit))
        result = loop.run_until_complete(task)
        loop.close()
        print("closing loop")
        # result = asyncio.run(self.query_async(
        #     query, channel_limit, message_limit))
        return result

    async def query_async(self, query: str, channel_limit=5, message_limit=10) -> list[MessageThread]:
        async with self.client:
            await self.start_app()
            channels = await self.search_channels(query, channel_limit)
            query_result = []

            for channel in channels:
                try:
                    messages = await self.get_messages_from_channel(channel.title, message_limit)
                    message_thread = MessageThread(channel.id, messages)
                    query_result.append(message_thread)
                except Exception as e:
                    print(e)
                    continue

            return query_result

    async def start_app(self) -> None:
        await self.client.start()

        passkey = config.Config.TELEGRAM_PASSWORD
        phone = config.Config.TELEGRAM_PHONE_NUMBER

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(phone)
        try:
            await self.client.sign_in(phone, passkey)
        except Exception:
            await self.client.sign_in(password=input('Password: '))

    async def get_messages_from_channel(self, channel_name: str, limit=10) -> list[types.Message]:
        messages = []
        async for message in self.client.iter_messages(channel_name, limit=limit):
            messages.append(message)

        return messages

    async def search_channels(self, search_word: str, limit=5) -> list[types.Channel]:
        channels = []

        result = await self.client(functions.contacts.SearchRequest(
            q=search_word,
            limit=limit
        ))

        for chat in result.chats:
            if isinstance(chat, types.Channel):
                channels.append(chat)

        return channels

    def parse_all_messages(self, message_threads: list[MessageThread]) -> list[Samsum]:
        samsums = []
        for message_thread in message_threads:
            samsums.append(self.parse_message(
                message_thread.messages, message_thread.id))
        return samsums

    def parse_message(self, messages: list[types.Message], id) -> Samsum:
        samsum = Samsum(id, "", "")
        for message in messages:
            try:
                samsum.add_dialogue(message.sender_id, message.text)
            except Exception as e:
                print(e)

        return samsum

    def parse_message_json(self, messages: list[types.Message], id) -> dict:
        return self.parse_message(messages, id).to_json()

    def parse_all_messages_json(self, message_threads: list[MessageThread]) -> list[dict]:
        return [self.parse_message_json(messages=message_thread.messages, id=message_thread.id) for message_thread in message_threads]

    # for testing purposes
    def export_query_as_json(self, query: str, channel_limit=5, message_limit=10, filename="results.json") -> None:
        result = self.query(query, channel_limit, message_limit)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.parse_all_messages_json(
                result), file, ensure_ascii=False)


# def main():
#     tapi = TelegramAPI("20866665", "9efc05b1e5d0aa89fa195326deff987b")
#     result = tapi.query("football")
#     sumsum = tapi.parse_all_messages_json(result)

#     def export_to_json(data, filename):
#         with open(filename, 'w', encoding='utf-8') as file:
#             json.dump(data, file, ensure_ascii=False)

#     export_to_json(sumsum, 'first_results_telegram_api.json')


# if __name__ == "__main__":
#     main()
