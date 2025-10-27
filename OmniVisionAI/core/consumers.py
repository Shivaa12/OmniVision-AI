import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Camera, Gate, UnrecognizedFace


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


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dashboard_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'lock_all_gates':
                await self.lock_all_gates()
            elif action == 'unlock_all_gates':
                await self.unlock_all_gates()
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Unknown action',
                    'action': action
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))

    async def lock_all_gates(self):
        gates = await self.get_all_gates()
        locked_count = 0
        
        for gate in gates:
            if gate.status != 'locked':
                await self.lock_gate(gate)
                locked_count += 1
        
        # Broadcast update to all dashboard clients
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'gate_status_update',
                'message': f'Locked {locked_count} gates',
                'action': 'lock_all'
            }
        )

    async def unlock_all_gates(self):
        gates = await self.get_all_gates()
        unlocked_count = 0
        
        for gate in gates:
            if gate.status != 'unlocked':
                await self.unlock_gate(gate)
                unlocked_count += 1
        
        # Broadcast update to all dashboard clients
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'gate_status_update',
                'message': f'Unlocked {unlocked_count} gates',
                'action': 'unlock_all'
            }
        )

    async def gate_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gate_update',
            'message': event['message'],
            'action': event['action']
        }))

    async def unrecognized_face_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'unrecognized_face_count_update',
            'count': event['count']
        }))

    @database_sync_to_async
    def get_all_gates(self):
        return list(Gate.objects.filter(is_active=True))

    @database_sync_to_async
    def lock_gate(self, gate):
        gate.lock()
        return gate

    @database_sync_to_async
    def unlock_gate(self, gate):
        gate.unlock()
        return gate


