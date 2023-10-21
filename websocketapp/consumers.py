import json
from channels.generic.websocket import AsyncWebsocketConsumer

import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


from evolutionlab.settings import BASE_DIR







from datetime import datetime
from channels.generic.http import AsyncHttpConsumer

class ServerSentEventsConsumer1(AsyncHttpConsumer):
    async def handle(self, body):
        await self.send_headers(headers=[
           (b"Cache-Control", b"no-cache"),
            (b"Content-Type", b"text/event-stream"),
            (b"Transfer-Encoding", b"chunked"),
            (b'Access-Control-Allow-Origin', b'*'),
        ])
        while True:
            payload = "data: %s\n\n" % datetime.now().isoformat()
            await self.send_body(payload.encode("utf-8"), more_body=True)
            await asyncio.sleep(1)


class ServerSentEventsConsumer(AsyncHttpConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keepalive = False

    async def handle(self, body):
        print('start handle')
        await self.send_headers(headers=[
            (b'Cache-Control', b'no-cache'),
            (b'Content-Type', b'text/event-stream'),
            (b"Transfer-Encoding", b"chunked"),
            (b'Access-Control-Allow-Origin', b'*'),
        ])

        await self.send_body(b'', more_body=True)
        await self.channel_layer.group_add('test123', self.channel_name)

    async def send_body(self, body, *, more_body=False):
        if more_body:
            self.keepalive = True
        assert isinstance(body, bytes), "Body is not bytes"
        await self.send(
            {"type": "http.response.body", "body": body, "more_body": more_body}
        )

    async def http_request(self, message):
        if "body" in message:
            self.body.append(message["body"])
        if not message.get("more_body"):
            try:
                await self.handle(b"".join(self.body))
            finally:
                if not self.keepalive:
                    await self.disconnect()
                    # raise StopConsumer()

    async def chat_message(self, event):
        payload = 'event: test\ndata: 2\n\n'
        await self.send_body(payload.encode('utf-8'), more_body=True)




class LogStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def start_log_stream(self, log_file_path):
        try:
            while True:
                with open(log_file_path) as log_file:
                    for line in log_file:
                        await self.send(line)
                        await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass

    async def stop_log_stream(self):
        # Stop the log stream
        pass



# consumers.py

class CeleryLogConsumer(LogStreamConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def start_celery_log_stream(self, log_file_path):
        await self.start_log_stream(log_file_path)

    async def stop_celery_log_stream(self):
        await self.stop_log_stream()


class NginxLogConsumer(LogStreamConsumer):
    async def connect(self):
        print("call accept")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def start_nginx_log_stream(self, log_file_path):
        print("call nginx log")
        log_file_path = f'{BASE_DIR}/nginx.log'
        await self.start_log_stream(log_file_path)

    async def stop_nginx_log_stream(self):
        print("call end")
        await self.stop_log_stream()



import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print("call 3")
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        self.chat_message({'message' : 'test'})

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("message: ", text_data)
        print("call 2")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = 'ssss'
        print("call 1")
        # Send message to WebSocket
        log_file = f'{BASE_DIR}/access.log'  # Update with your Nginx log file path
        current_position = 0
        print("log file: ",log_file)
        while True:
            try:
                with open(log_file, 'r') as file:
                    file.seek(current_position)
                    new_lines = file.readlines()
                    if new_lines:
                        print("call new lines")
                        current_position = file.tell()  # Update the current position
                        print("Sending!")
                        print("length: ", len(new_lines))
                        print("data : ", new_lines[:2])
                        await self.send(text_data=json.dumps({'message': '\n'.join(new_lines)}))
                        print("Sent!")
                    else:
                        time.sleep(0.1)  # Sleep briefly if no new data
            except FileNotFoundError:
                # Handle the case where the log file doesn't exist yet
                print("error")
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # await self.send(text_data=json.dumps({"message": message}))

    async def send_logs():
        # Send message to WebSocket
        log_file = f'{BASE_DIR}/access.log'  # Update with your Nginx log file path
        current_position = 0
        print("log file: ",log_file)
        while True:
            try:
                with open(log_file, 'r') as file:
                    file.seek(current_position)
                    new_lines = file.readlines()
                    if new_lines:
                        print("call new lines")
                        current_position = file.tell()  # Update the current position
                        print("Sending!")
                        print("length: ", len(new_lines))
                        print("data : ", new_lines[:2])
                        await self.send(text_data=json.dumps({'message': '\n'.join(new_lines)}))
                        print("Sent!")
                    else:
                        time.sleep(0.1)  # Sleep briefly if no new data
            except FileNotFoundError:
                # Handle the case where the log file doesn't exist yet
                print("error")
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

