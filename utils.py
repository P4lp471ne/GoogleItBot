from urllib.parse import urlencode


def make_url(*args, params: dict = None):
    url = '/'.join(args)
    if params:
        qs = urlencode(params)
        url = f"{url}?{qs}"
    return url
