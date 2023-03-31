from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag


cl = None


def start():
    global cl
    cl = Client()
    cl.login("virtualhof", "Fame214228")
    print("Logined to instagram")


def publish_image(filepath):
    global cl
    cl.photo_upload(filepath, "New wall")