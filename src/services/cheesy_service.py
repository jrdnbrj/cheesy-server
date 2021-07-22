from ..db.documents import Home, OurFamily

from igramscraper.instagram import Instagram

import base64
import requests


def get_home():
    return Home.objects().order_by('sequence')

def get_family():
    return OurFamily.objects().order_by('sequence')

def update_home(data):
    home = Home.objects().order_by('sequence')
    
    for i, item in enumerate(home):
        item.name = data[i].name
        item.description = data[i].description
        item.save()

    return get_home()


def update_family(data):
    family = OurFamily.objects().order_by('sequence')
    
    for i, item in enumerate(family):
        item.title = data[i].title
        item.description = data[i].description
        item.save()

    return get_family()


def get_instagram_media(count):
    instagram = Instagram()

    medias = instagram.get_medias('cheesybittes', count)

    def to_instagram_type(url, image): 
        return { 'url': url, 'image': to_base64(image) }

    return [to_instagram_type(media.link, media.image_high_resolution_url) for media in medias]


def to_base64(img):
    try:
        image = base64.b64encode(requests.get(img).content)
        return image.decode('utf-8')
    except:
        return ''