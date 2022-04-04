from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
import json
from items.models import Table

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.room_name = 'broadcast'
        self.send({
            "type": "websocket.accept",
        })
        print("Connect event is called")
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def websocket_receive(self, event):
        data = json.loads(event['text'])
        dataType = data['type']
        tableNumber = data['tableNumber']
        table = Table.objects.get(tableNumber = tableNumber)
        if dataType == 'Inactive':
            table.availaible = True
            table.unique_number = None
            table.save()
        print("New event is received")
        print(event)

    def websocket_message(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    def websocket_disconnect(self, event):
        print("connection is disconnected")
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
