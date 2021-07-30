from ..db.documents import Settings

from decouple import config

from datetime import datetime
import jwt


def login(password):
    success, _, message = verify_password(password)
    if success:
        return generate_token(), True

    return message, False

def verify_password(password):
    settings = Settings.objects().first()
    response = decrypt_password(settings.password)

    if response['password'] == password:
        return True, settings, 'OK'
    else:
        return False, '', 'Your current password is incorrect.'

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
    success, settings, message = verify_password(password)

    if success:
        if len(new_password) < 8:
            return 'New password must be at least 8 characters long.'

        if len(new_password) > 20:
            return 'New password must be less than 20 characters long.'

        settings.password = encrypt_password(new_password)
        settings.save()
        return 'OK'
    else:
        return message

def encrypt_password(password):
    return jwt.encode({ 'password': password }, config('JWT_SECRET'), algorithm="HS256")

def decrypt_password(password):
    return jwt.decode(password, config('JWT_SECRET'), algorithms="HS256")

def generate_token():
    payload = { 
        "generated_at": str(datetime.utcnow()),
        "cheesy": "bittes"
    }
    return jwt.encode(payload, config('JWT_SECRET'), algorithm="HS256")
