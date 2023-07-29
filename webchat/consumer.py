from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class WebChatConsumer(JsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None
    
    def connect(self):
        self.accept()
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]
        
        async_to_sync(self.channel_layer.group_add)(
            self.channel_id,
            self.channel_name,
        )

    def receive_json(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.channel_id,
            {
                "type": "chat.message",
                "new_message": content["message"],
            }
        )

    def chat_message(self, event):
        self.send_json(event)

    def disconnect(self, close_code):
        pass
