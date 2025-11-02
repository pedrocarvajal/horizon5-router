import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        pass

    async def receive(self, text_data: str) -> None:
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"message": "Data received", "data": data}))

