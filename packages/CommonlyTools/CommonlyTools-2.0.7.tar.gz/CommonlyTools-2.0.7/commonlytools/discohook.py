from .error import *
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
        if name == None and url == None and icon_url == None:
            return self._author
        self._author={"name": name, "url": url, "icon_url": icon_url}


    def footer(self, text:str=None, icon_url:str=None):
        if text == None and icon_url == None:
            return self._footer
        self._footer={"text": text, "icon_url": icon_url}


    def image(self, image_url:str=None):
        if image_url == None:
            return self._image
        self._image={"url": image_url}


    def thumbnail(self, thumbnail_url:str=None):
        if thumbnail_url == None:
            return self._thumbnail
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


    def fields(self):
        return self._field


def send(webhook_url:str, username:str=None, avatar_url:str=None, content:str=None, embeds:list=[]):
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        raise UrlError("This is not Discord webhook URL!\n")
    if username == None and avatar_url == None and content == None and embeds == []:
        raise MessageError("You have not set up anything to send!\n")
    embeds_dict=[]
    for embed in embeds:
        result={}
        if embed.title != None:
            result["title"]=embed.title
        if embed.description != None:
            result["description"]=embed.description
        result["color"]=embed.colour
        if embed.fields != []:
            result["fields"]=embed.fields
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