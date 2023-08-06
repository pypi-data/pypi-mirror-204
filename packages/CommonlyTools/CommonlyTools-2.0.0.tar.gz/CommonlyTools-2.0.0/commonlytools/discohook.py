import requests
import datetime


def Colour(colour:int=0):
    colour=int(str(colour), 10)
    return colour


def Timestamp(timestamp:datetime.datetime):
    return f"{timestamp.year}-{timestamp.month}-{timestamp.day}T{timestamp.hour}:{timestamp.minute}:{timestamp.second}.{timestamp.microsecond}Z"


class Embed:
    def __init__(self, title:str=None, description:str=None, timestamp:Timestamp=None, color:Colour=None):
        self._title=title
        self._description=description
        self._colour=color
        self._timestamp=timestamp
        self._image={}
        self._author={}
        self._footer={}
        self._thumbnail={}
        self._field=[]
        

    def author(self, name:str=None, url:str=None, icon_url:str=None):
        self._author={"name": name, "url": url, "icon_url": icon_url}


    def footer(self, text:str=None, icon_url:str=None):
        self._footer={"text": text, "icon_url": icon_url}


    def image(self, image_url):
        self._image={"url": image_url}


    def thumbnail(self, thumbnail_url):
        self._thumbnail={"url": thumbnail_url}


    def add_field(self, name:str=None, value:str=None, inline:bool=False):
        self._field.append({"name": name, "value": value, "inline": inline})


    def to_dict(self):
        result={}
        if self._title != None:
            result["title"]=self._title
        if self._description != None:
            result["description"]=self._description
        result["color"]=self._colour
        if self._field != {}:
            result["fields"]=self._field
        if self._author != {}:
            result["author"]=self._author
        if self._footer != {}:
            result["footer"]=self._footer
        if self._timestamp:
            result["timestamp"]=self._timestamp
        if self._image != {}:
            result["image"]=self._image
        if self._thumbnail != {}:
            result["thumbnail"]=self._thumbnail
        return result


def send(webhook_url:str, username:str=None, avatar_url:str=None, content:str=None, embeds:list=[]):
    embeds_dict=[]
    for embed in embeds:
        embed_dict=embed.to_dict()
        embeds_dict.append(embed_dict)
    requests.post(url=webhook_url, json={"username": username, "avatar_url": avatar_url, "content": content, "embeds": embeds_dict})