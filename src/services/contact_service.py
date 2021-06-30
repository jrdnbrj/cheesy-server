from ..db.documents import Contact


def create_contact(**kwargs):
    return Contact(**kwargs).save()

def get_contacts():
    return Contact.objects()