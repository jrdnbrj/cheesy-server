from ..db.documents import Home, OurFamily


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
