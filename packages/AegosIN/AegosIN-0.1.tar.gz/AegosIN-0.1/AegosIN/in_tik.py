import requests
def InfoTik(user):
    resp4 = requests.get(f'https://api.dlyar-dev.tk/info-tiktok.json?user={user}').json()
    if resp4['status'] == True:
        i1 = resp4['id']
        i2 = resp4['name']
        i3 = resp4['country']
        i4 = resp4['code-country']
        i5 = resp4['flag']
        i6 = resp4['followers']
        i7 = resp4['following']
        i8 = resp4['likes']
        i9 = resp4['video']
        i10 = resp4['img']
        return {'result':'true','id':i1,'name':i2,'country':i3,'code-country':i4,'flag':i5,'followers':i6,'following':i7,'likes':i8,'video':i9,'img':i10,'By':'@G_4_2'}
    else:
        return {'result':'false','By':'@G_4_2'}