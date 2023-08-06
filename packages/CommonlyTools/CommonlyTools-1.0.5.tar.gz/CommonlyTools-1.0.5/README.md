# CommonlyTools

----------

How to use CommonlyTools?
>```pip install CommonlyTools```
----------

>CommonlyTools/discohook.py
>>Discord Webhook Sender
>>>Step 1(If you do not need to use embed, you can skip this step.)
>>>```py
>>>from CommonlyTools import discohook
>>>
>>>embed=discohook.Embed(color=dc.Colour(...), title="...", description="...") #If you need, you can enter the colour, title or descriotion
>>>embed.author(name="...", url="...", icon_url="...") #author
>>>embed.footer(text="...", icon_url="...") #footer
>>>embed.image(image_url="...") #image
>>>embed.thumbnail(thumbnail_url="...") #thumbnail
>>>embed.add_field(name="...", value="...", inline=...) #add_field #This function can unlimited superposition.
>>>```
>>
>>Step 2
>>>```py
>>>discohook.send(webhook_url="...", username="...", avatar_url="...", content="...", embeds=[...])
>>>```
>>
>>Step 3
>>>```
>>>Message was sent!
>>>```