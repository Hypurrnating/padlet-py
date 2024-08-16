"""
This file just contains skeleton classes that can be used to populate data about objects 
"""
import typing
from typing import Union, Literal
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp


class user_object():
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
    def __init__(self, padlet, post) -> None:
        self.subject: str = None
        self.body_html: str = None
        self.attachment: attachment_object = attachment_object(padlet, post)
        self.updated_at: datetime = None

class attachment_object():
    def __init__(self, padlet, post) -> None:
        self.url: str = None
        self.caption: str = None
        self.post: post_object = post
        self.padlet = padlet
        # These need to be fetched
        self.preview_image_url: str = None
        self.embed_code: str = None

    async def fetch(self):
        if not self.url:
            return
        async with aiohttp.ClientSession(headers={'X-Api-Key': self.padlet.api_key}) as connection:
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

class canvas_object():
    def __init__(self) -> None:
        self.left: int = None
        self.top: int = None
        self.width: int = None


" The BIG objects start here "

class board_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'board'
        self.title: str = None
        self.description: str = None
        self.builder: user_object = user_object()
        self.icon_url: str = None
        self.domain_name: str = None
        self.settings: settings_object = settings_object()
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.web_url: web_url_object = web_url_object()
        self.posts: dict = dict()
        self.sections: dict = dict()


class section_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'section'
        self.board: board_object = None
        self.title: str = None
        self.index: int = None
        self.created_at: str = None
        self.updated_at: str = None


class post_object():
    def __init__(self, padlet) -> None:
        self.id: str = None
        self.type: str = 'post'
        self.board: board_object = None
        self.section: section_object = None
        self.author: user_object = user_object()
        self.index: int = None
        self.content: post_content_object = post_content_object(padlet, self)
        self.color: str = None
        self.status: Literal['approved', 'pending_moderation', 'scheduled']
        self.map_properties: map_object = map_object()
        self.canvas_properties: canvas_object = canvas_object()
        self.web_url: web_url_object = web_url_object()
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.custom_fields: dict = dict()
            