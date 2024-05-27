from telethon import TelegramClient
from telethon import functions, types
import asyncio
# from summarization.models.samsum import Samsum
from samsum import Samsum
import json


class TelegramAPI:
    def __init__(self, api_id: str, api_hash: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('nlp_user', self.api_id, self.api_hash)

    def query(self, query: str, channel_limit=5, message_limit=10) -> list[list[types.Message]]:
        result = asyncio.run(self.query_async(
            query, channel_limit, message_limit))
        return result

    async def query_async(self, query: str, channel_limit=5, message_limit=10) -> list[list[types.Message]]:
        async with self.client:
            await self.start_app()
            channels = await self.search_channels(query, channel_limit)
            query_result = []

            for channel in channels:
                messages = await self.get_messages_from_channel(channel.title, message_limit)
                query_result.extend(messages)

            return query_result

    async def start_app(self) -> None:
        await self.client.start()

        passkey = "51314"
        phone = "+491623761600"

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(phone)
        try:
            await self.client.sign_in(phone, passkey)
        except Exception as e:
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

    def parse_all_messages(self, messages: list[types.Message]) -> list[Samsum]:
        samsums = []
        for message in messages:
            samsums.append(self.parse_message(message))
        return samsums

    def parse_message(self, message: types.Message) -> Samsum:
        try:
            return Samsum(message.id, "", message.text)
        except Exception as e:
            print(e)
            return Samsum(message.id, "", "")

    def parse_message_json(self, message: types.Message) -> dict:
        return self.parse_message(message).to_json()

    def parse_all_messages_json(self, messages: list[types.Message]) -> list[dict]:
        return [self.parse_message_json(message) for message in messages]


def main():
    tapi = TelegramAPI("20866665", "9efc05b1e5d0aa89fa195326deff987b")
    result = tapi.query("türkiye")
    sumsum = tapi.parse_all_messages_json(result)

    def export_to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    export_to_json(sumsum, 'first_results_telegram_api.json')


if __name__ == "__main__":
    main()
