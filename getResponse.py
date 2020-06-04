from fake_useragent import UserAgent
import random
import requests

def createUserAgent():
    user_agent = UserAgent()
    return user_agent.random

def getResponseByGet(url):
    user_agent = createUserAgent()
    headers = {'cookie': 'SPC_EC=-; SPC_F=N8np8pS9AozFKJ0jLKKUEyHo3CKP5oaN; SPC_U=-; _fbp=fb.1.1568119117461.114405041; _ga=GA1.2.1607977111.1568119119; cto_lwid=a7f298c2-57a8-484d-926c-7ce70e5bbcdb; REC_T_ID=43ff2562-03a0-11ea-ba36-b49691277d16; __BWfp=c1573379766268x2fb410201; _gcl_au=1.1.1191230196.1589298111; _med=refer; csrftoken=AH3QGTNy4dXkn7JG0Jm0zkymd6nkGuHG; SPC_SI=josundjymgab0bah8z2m0hye54zg0bv9; welcomePkgShown=true; _gid=GA1.2.1732595968.1589298117; AMP_TOKEN=%24NOT_FOUND; G_ENABLED_IDPS=google; _dc_gtm_UA-61915057-6=1; SPC_CT_3321a1ce="1589346369.Y6GEe0CgJ6ByJFF1+X03oZR1WZuLQLZrj8wOjOwS2aM="; SPC_R_T_ID="2NC8PVg5heBFA7i1ysLHJt0tAfyQiB8uo1c25kn+1p/1zcFScXbRK7x4DF27y4STesLtwE3bHRnm9BzxMWRPCpDiW1/kzt1qwP78RxsoJyM="; SPC_T_IV="FNWHiAL7Jkk3NzSkgzYXfA=="; SPC_R_T_IV="FNWHiAL7Jkk3NzSkgzYXfA=="; SPC_T_ID="2NC8PVg5heBFA7i1ysLHJt0tAfyQiB8uo1c25kn+1p/1zcFScXbRK7x4DF27y4STesLtwE3bHRnm9BzxMWRPCpDiW1/kzt1qwP78RxsoJyM="',               
               'user-agent': user_agent}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        #raise SystemExit(err)
        return None
    except requests.exceptions.ConnectionError as err:
        #raise SystemExit(err)
        print('Connection is refused by the server..')
        print('Let me sleep for 5 seconds')
        print('ZZzzzz...')
        time.sleep(5)
        print('Reconnecting')
        response = getResponseByGet(url) #recursiving

    return response

def getResponseByPost(url, payload, payloadType):
    user_agent = createUserAgent()
    headers = {'cookie': 'SPC_EC=-; SPC_F=N8np8pS9AozFKJ0jLKKUEyHo3CKP5oaN; SPC_U=-; _fbp=fb.1.1568119117461.114405041; _ga=GA1.2.1607977111.1568119119; cto_lwid=a7f298c2-57a8-484d-926c-7ce70e5bbcdb; REC_T_ID=43ff2562-03a0-11ea-ba36-b49691277d16; __BWfp=c1573379766268x2fb410201; _gcl_au=1.1.1191230196.1589298111; _med=refer; csrftoken=AH3QGTNy4dXkn7JG0Jm0zkymd6nkGuHG; SPC_SI=josundjymgab0bah8z2m0hye54zg0bv9; welcomePkgShown=true; _gid=GA1.2.1732595968.1589298117; AMP_TOKEN=%24NOT_FOUND; G_ENABLED_IDPS=google; _dc_gtm_UA-61915057-6=1; SPC_CT_3321a1ce="1589346369.Y6GEe0CgJ6ByJFF1+X03oZR1WZuLQLZrj8wOjOwS2aM="; SPC_R_T_ID="2NC8PVg5heBFA7i1ysLHJt0tAfyQiB8uo1c25kn+1p/1zcFScXbRK7x4DF27y4STesLtwE3bHRnm9BzxMWRPCpDiW1/kzt1qwP78RxsoJyM="; SPC_T_IV="FNWHiAL7Jkk3NzSkgzYXfA=="; SPC_R_T_IV="FNWHiAL7Jkk3NzSkgzYXfA=="; SPC_T_ID="2NC8PVg5heBFA7i1ysLHJt0tAfyQiB8uo1c25kn+1p/1zcFScXbRK7x4DF27y4STesLtwE3bHRnm9BzxMWRPCpDiW1/kzt1qwP78RxsoJyM="',               
               'user-agent': user_agent}
    try:
        if payloadType == 'data':
            response = requests.post(url, headers=headers, data=payload)
        elif payloadType == 'json':
            response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        #raise SystemExit(err)
        return None
    except requests.exceptions.ConnectionError as err:
        #raise SystemExit(err)
        print('Connection is refused by the server..')
        print('Let me sleep for 5 seconds')
        print('ZZzzzz...')
        time.sleep(5)
        print('Reconnecting')
        response = getResponseByPost(url, payload) #recursiving

    return response
