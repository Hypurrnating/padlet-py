"""
This file just contains skeleton classes that can be used to populate data about objects 
"""
import typing
from typing import Union, Literal, Dict
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp


class _user_object():
    def __init__(self) -> None:
        self.username: str = None
        self.short_name: str = None
        self.full_name: str = None
        self.avatar_url: str = None

class web_url_object():
    """ In posts, this will only have live url """
    def __init__(self) -> None:
        self.live: str = None
        self.qr_code: str = None
        self.slideshow: str = None
        self.slideshow_qr_code: str = None

class settings_object():
    def __init__(self) -> None:
        self.font: int = None
        self.color_scheme: str = None

class post_content_object():
    def __init__(self, post) -> None:
        self.subject: str = None
        self.body_html: str = None
        self.attachment: attachment_object = attachment_object(post)
        self.updated_at: datetime = None

class attachment_object():
    def __init__(self, post) -> None:
        self.url: str = None
        self.caption: str = None
        self.post: post_object = post
        # These need to be fetched
        self.preview_image_url: str = None
        self.embed_code: str = None

    async def fetch(self):
        if not self.url:
            return
        async with aiohttp.ClientSession(headers={'X-Api-Key': self.post.board.user.api_key}) as connection:
            resp = await connection.get(f'https://api.padlet.dev/v1/posts/{self.post.id}/attachmentData')
        content = await resp.json()
        if not resp.status == 200:
            raise Exception(f'Non-200 status code: {content}')
        self.preview_image_url = content['data']['attributes']['previewImageUrl']
        self.embed_code = content['data']['attributes']['embedCode']
        print(self)
        return self

class map_object():
    def __init__(self) -> None:
        self.longitude: int = None
        self.latitude: int = None
        self.location_name: int = None
    
    @property
    def __dict__(self) -> dict:
        return {'longitude': self.longitude,
                'latitude': self.latitude,
                'location_name': self.location_name}

class canvas_object():
    def __init__(self) -> None:
        self.left: int = None
        self.top: int = None
        self.width: int = None
    
    @property
    def __dict__(self) -> dict:
        return {'left': self.left,
                'top': self.top,
                'width': self.width}


" The BIG objects start here "

class board_object():
    def __init__(self) -> None:
        self.user = None
        self.id: str = None
        self.type: str = 'board'
        self.title: str = None
        self.description: str = None
        self.builder: _user_object = _user_object()
        self.icon_url: str = None
        self.domain_name: str = None
        self.settings: settings_object = settings_object()
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.web_url: web_url_object = web_url_object()
        self.posts: Dict[str: post_object] = dict()
        self.sections: Dict[str: section_object] = dict()

class post_object():
    def __init__(self, user) -> None:
        self.id: str = None
        self.type: str = 'post'
        self.board: board_object = None
        self.section: section_object = None
        self.author: _user_object = _user_object()
        self.index: int = None
        self.content: post_content_object = post_content_object(self)
        self.color: str = None
        self.status: Literal['approved', 'pending_moderation', 'scheduled']
        self.map_properties: map_object = map_object()
        self.canvas_properties: canvas_object = canvas_object()
        self.web_url: web_url_object = web_url_object()
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.custom_fields: dict = dict()

class section_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'section'
        self.board: board_object = None
        self.title: str = None
        self.index: int = None
        self.created_at: str = None
        self.updated_at: str = None
        self.posts: Dict[str: post_object] = None    

    async def create(self,
                    subject: str,
                    body: str,
                    color: Literal['red', 'orange', 'green', 'blue', 'purple'] = None,
                    attachment_url: str = None,
                    attachment_caption: str = None,
                    status: Literal['approved', 'pending_moderation', 'scheduled'] = None,
                    map: map_object = map_object(),
                    canvas: canvas_object = map_object(),
                    previous_post: post_object = post_object()):
        payload = {'data':
                {'type': 'post',
                    'attributes': {
                        'content': {
                            'subject': subject,
                            'body': body,
                            'attachment': {
                                'attachment_url': attachment_url,
                                'attachment_caption': attachment_caption,
                            },
                        },
                    },
                    'color': color,
                    'manualSortPosition': {
                        'previousPostId': previous_post.id
                    },
                    'status': status,
                    'mapProps': map.__dict__,
                    'canvasProps': canvas.__dict__,
                    },
                'relationships': {
                    'section': {
                        'data': {
                            'id': self.id
                        }
                    }
                }
                }
        async with aiohttp.ClientSession(headers={'X-Api-Key': self.user.id,
                                                    "accept": "application/vnd.api+json",
                                                    "content-type": "application/vnd.api+json"}) as connection:
            resp = await connection.post(f'https://api.padlet.dev/v1/boards/{self.board.id}/posts',
                                            json=payload)
        content = await resp.json()
        if not resp.status == 200:
            raise Exception(f'Non-200 status code: {content}')
        # TODO: store new post to board object
