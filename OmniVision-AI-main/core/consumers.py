import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Camera


class CameraStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.camera_id = self.scope['url_route']['kwargs'].get('camera_id')
        self.group_name = f"camera_{self.camera_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Echo/ping for now; actual streaming will send binary frames
        if text_data:
            await self.send(text_data=json.dumps({"status": "ok"}))

    async def frame(self, event):
        # Expect event with 'bytes' key for frame data (e.g., JPEG bytes)
        data = event.get('bytes')
        if data:
            await self.send(bytes_data=data)

    async def camera_frame(self, event):
        frame_data = event.get('frame')
        if frame_data:
            await self.send(bytes_data=frame_data)

    @database_sync_to_async
    def get_camera(self, camera_id):
        try:
            return Camera.objects.get(id=camera_id)
        except Camera.DoesNotExist:
            return None


