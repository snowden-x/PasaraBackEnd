import json
from channels.generic.websocket import WebsocketConsumer

class chatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
           'type': 'connection-established',
            'message': 'Hurray',
        }))

    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data = json.dumps({
            'type':'background-color',
            'message':message
        }))
