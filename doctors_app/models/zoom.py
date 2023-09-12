from odoo import api, fields, models
import requests
import json


class ZoomSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    zoom_api_key = fields.Char(string='Zoom API Key', config_parameter='zoom.api_key')
    zoom_api_secret = fields.Char(string='Zoom API Secret',config_parameter='zoom.api_secret')
    unsplash_access_key=fields.Char(string='Access Key')
    unsplash_app_id=fields.Char(string='Access Key Id')
    @api.model
    def set_values(self):
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('zoom.api_key', self.zoom_api_key)
        config.set_param('zoom.api_secret', self.zoom_api_secret)


    @api.model
    def get_values(self):
        config = self.env['ir.config_parameter'].sudo()
        zoom_api_key = config.get_param('zoom.api_key', default='')
        zoom_api_secret = config.get_param('zoom.api_secret', default='')
        return {
            'zoom_api_key': zoom_api_key,
            'zoom_api_secret': zoom_api_secret,
        }

    def create_zoom_meeting(self):
        api_key = "EKgsBRIxS6nkvGfMnnH1w"
        api_secret = "N1CB2uRMKB9jyaO35kQ5lxt50M0MqtAH"
        # Construct the request to create a Zoom meeting
        # API endpoints
        base_url = "https://api.zoom.us/v2"
        meeting_create_url = f"{base_url}/users/me/meetings"

        # Create a meeting
        headers = {
            "Authorization": f"Bearer {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }

        payload = {
            "topic": "My Zoom Meeting",
            "type": 2,  # Scheduled meeting
            "start_time": "2023-06-20T09:00:00",
            "duration": 60,
            "timezone": "India"
        }

        response = requests.post(meeting_create_url, headers=headers, data=json.dumps(payload))
        data = response.json()

        # Handle the response
        if response.status_code == 201:
            meeting_id = data["id"]
            join_url = data["join_url"]
            meeting_link = f"https://zoom.us/j/{meeting_id}"  # Zoom meeting link
