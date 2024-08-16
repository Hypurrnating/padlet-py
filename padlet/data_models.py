"""
This file just contains skeleton classes that can be used to populate data about objects 
"""
import typing
from typing import Union, Literal
import datetime
from datetime import datetime, timezone, timedelta

class board_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'board'
        self.attributes: self._board_attributes_object = self._board_attributes_object
        self.posts: dict = None
        self.sections: dict = None

    class _board_attributes_object:
        def __init__(self) -> None:
            self.title: str = None
            self.description: str = None
            self.builder: str = None
            self.icon_url: str = None
            self.domain_name: str = None
            self.settings: dict = None
            self.created_at: datetime = None
            self.updated_at: datetime = None

class section_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'section'
        self.board: board_object = None
    
    class _section_attributes_object:
        def __init__(self) -> None:
            self.title: str = None
            self.index: int = None
            self.created_at: str = None
            self.updated_at: str = None


class post_object():
    def __init__(self) -> None:
        self.id: str = None
        self.type: str = 'post'
        self.board: board_object = None
        self.section: section_object = None
        self.attachment: dict = None # More info about this can be given in docs ig
        
    class _post_attributes_object:
        def __init__(self) -> None:
            self.author: object #TODO 
            self.index: int = None
            self.content: object #TODO
            self.color: str = None
            self.status: Literal['approved', 'pending_moderation', 'scheduled']
            self.map_properties: object #TODO
            self.canvas_properties: object #TODO
            self.created_at: datetime = None
            self.updated_at: datetime = None
            