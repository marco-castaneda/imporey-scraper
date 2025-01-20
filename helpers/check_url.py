
def check_url(url):
    if 'https' in url:
        return url
    else:
        if 'http' in url:
            return str(url.replace('http', 'https'))
        return str('https://' + url)
