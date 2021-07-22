from decouple import config

import jwt


def authentication_required():
    def decorator(resolver):
        def wrapper_func(source, info, **kwargs):
            request = info.context["request"]

            if("authorization" not in request.headers):
                raise Exception("Not Authorized!")

            try:
                token = request.headers["authorization"]
                decoded = jwt.decode(token, config('JWT_SECRET'), algorithms="HS256")

                if decoded.get('cheesy') != 'bittes':
                    raise Exception("Not Authorized!")
            except:
                raise Exception("Not Authorized!")

            result = resolver(source, info, **kwargs)

            return result
        return wrapper_func
    return decorator
