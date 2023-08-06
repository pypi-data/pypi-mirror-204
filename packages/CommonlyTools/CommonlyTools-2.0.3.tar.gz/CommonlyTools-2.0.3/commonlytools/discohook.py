import requests
import datetime


class Embed:
    def __init__(self, title:str=None, description:str=None, timestamp:datetime.datetime=None, color:int=0xffffff, colour:int=0xffffff):
        self._title=title
        self._description=description
        self._colour=int(str(color), 10) or int(str(colour), 10)
        if timestamp != None:
            self._timestamp=f"{timestamp.year}-{timestamp.month}-{timestamp.day}T{timestamp.hour}:{timestamp.minute}:{timestamp.second}.{timestamp.microsecond}Z"
        else:
            self._timestamp=None
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


    def title(self):
        return self._title

    
    def description(self):
        return self._description

    def colour(self):
        return self._colour


    def timestamp(self):
        return self._timestamp


    def image(self):
        return self._image


    def author(self):
        return self._author
        

    def footer(self):
        return self._footer


    def thumbnail(self):
        return self._thumbnail


    def field(self):
        return self._field


def send(webhook_url:str, username:str=None, avatar_url:str=None, content:str=None, embeds:list=[]):
    embeds_dict=[]
    for embed in embeds:
        result={}
        if embed.title != None:
            result["title"]=embed.title
        if embed.description != None:
            result["description"]=embed.description
        result["color"]=embed.colour
        if embed.field != {}:
            result["fields"]=embed.field
        if embed.author != {}:
            result["author"]=embed.author
        if embed.footer != {}:
            result["footer"]=embed.footer
        if embed.timestamp:
            result["timestamp"]=embed.timestamp
        if embed.image != {}:
            result["image"]=embed.image
        if embed.thumbnail != {}:
            result["thumbnail"]=embed.thumbnail
        embeds_dict.append(result)
    requests.post(url=webhook_url, json={"username": username, "avatar_url": avatar_url, "content": content, "embeds": embeds_dict})