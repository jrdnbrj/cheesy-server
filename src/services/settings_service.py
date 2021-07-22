from ..db.documents import Settings


def get_settings():
    return Settings.objects().first()

def update_discounts(month, two_months):
    settings = Settings.objects().first()
    settings.discount_month = month
    settings.discount_2months = two_months
    settings.save()

    response = {
        'month': month,
        'two_months': two_months
    }
    return response

def update_password(password, new_password):
    settings = Settings.objects().first()
    settings.password = new_password
    settings.save()
    return settings
