from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer


class PaintConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.paint_name = self.scope['url_route']['kwargs']['paint_name']
        self.paint_group_name = 'chat_%s' % self.paint_name

        # Join paint group
        async_to_sync(self.channel_layer.group_add)(
            self.paint_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.paint_group_name,
            self.channel_name
        )

    def receive_json(self, content):
        try:
            if content['type'] == 'draw_event':
                async_to_sync(self.channel_layer.group_send)(
                    self.paint_group_name,
                    {
                        'type': 'paint.draw',
                        'content': content
                    }
                )
            else:
                self.send_json({
                    'message': 'type doesn\'t exists'
                })
        except Exception as e:
            print('WS Error:', e)

    # paint message handlers

    def paint_draw(self, event):
        content = event['content']
        self.send_json(content)
