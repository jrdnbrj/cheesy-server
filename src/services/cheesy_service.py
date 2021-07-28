from ..db.documents import Home, OurFamily

from instascrape import Profile

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
    cheesy = Profile('https://www.instagram.com/cheesybittes/')

    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": "sessionid=1583011116%3AvLJT5bpqQICKOE%3A5;"
    }

    cheesy.scrape(headers=headers)

    posts = cheesy.get_recent_posts(count)

    def to_instagram_type(url, image): 
        return { 'url': url, 'image': to_base64(image) }

    return [to_instagram_type(post.url, post.to_dict()['display_url']) for post in posts]


def to_base64(img):
    try:
        image = base64.b64encode(requests.get(img).content)
        return image.decode('utf-8')
    except:
        return ''
