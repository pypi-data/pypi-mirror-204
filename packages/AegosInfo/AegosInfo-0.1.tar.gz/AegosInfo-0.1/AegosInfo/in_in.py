import requests
from user_agent import generate_user_agent
gd = str(generate_user_agent())
from OneClick import Hunter
hd = str(Hunter.Services())
def InfoInsta(user):
    url= f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}"
    headers = {
                'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f'mid=Y3bGYwALAAHNwaKANMB8QCsRu7VA; ig_did=092BD3C7-0BB2-414B-9F43-3170EAED8778; ig_nrcb=1; shbid=1685054; shbts=1675191368.6684434090; rur=CLN; ig_direct_region_hint=ATN; csrftoken=Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7; ds_user_id=6684434090',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': gd,
        'x-asbd-id': '198387',
        'x-csrftoken': 'Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0g7ECdkTdrXy37TE9AoSnMndccWbB1cqrccYOZSLfcb0pE',
        'x-instagram-ajax': '1006383249',
    }
    r4 = requests.get(url,headers=headers).json()
    f1 = str(r4['data']['user']['full_name'])
    f2 = str(r4['data']['user']['id'])
    f3 = str(r4['data']['user']['edge_followed_by']['count'])
    f4 = str(r4['data']['user']['edge_follow']['count'])
    f5 = str(r4['data']['user']['edge_owner_to_timeline_media']['count'])
    r5 = requests.get(f"https://o7aa.pythonanywhere.com/?id={f2}").json()
    f6 = r5['date']
    try:
        hd5 = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            'Connection': 'Keep-Alive',
            'User-Agent': hd,
            'Accept-Language': 'en-US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': 'AQ==',
	    }
        d5 = {
            'ig_sig_key_version': '4',
            "user_id":f2
	    }
        u5 = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        r6 = requests.post(u5,headers=hd5,data=d5).json()
        f7 = r6['obfuscated_email']
        return {'status':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6,'reset':f7}
    except KeyError:
        return {'status':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6}