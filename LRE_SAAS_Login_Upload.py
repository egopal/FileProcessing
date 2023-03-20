import requests
import urllib3

urllib3.disable_warnings()

LRE_key = {}

def lreLogin():
    print("LRE_SAAS_Login ======================================================")

    url = 'https://lreorgprod4-pst.saas.microfocus.com/Loadtest/rest/authentication-point/authenticate'
    querystring = {"tenant": "88aa399d-b069-4115-8058-82621b2e1755"}

    lreUserName = "Jenkinsuser"
    lrePassword = 'Blue2023'

    payload = ""
    headers = {'Content-Type': "application/xml"}
    response = requests.request("GET", url, params=querystring, headers=headers, auth=(lreUserName, lrePassword), data=payload, verify=False)

    print("LRE_SAAS_Login_Response_Status_Code : " + str(response))
    #print("Login Headers")
    header = response.headers
    #print(header)
    #print("Login_Set-Cookie_KeyValues : ")
    setCookieKeyValues = header.get("Set-Cookie")
    #print(setCookieKeyValues)

    cookieTemp1 = setCookieKeyValues.split(",")

    count = 0
    for i in cookieTemp1:
        if "LWSSO_COOKIE_KEY" in i:
            key = count
            val = i
            if key in LRE_key:
                if val not in LRE_key[key]:
                    LRE_key[key].append(val)
            else:
                LRE_key[key] = [val]
            #print(LRE_key.get(count))
            count +=1

    cookieTemp2 = LRE_key.get(0)[0].split(";")[0]
    #print(type(LRE_Cookie))
    cookieTemp3 = cookieTemp2.lstrip()
    dynamicCookie = cookieTemp3 +";"
    print("LRE_SAAS_Login_dynamicCookie : ")
    print(dynamicCookie)

    return dynamicCookie

def lreUpload(dynamicCookie):

    print("LRE_SAAS_Upload ======================================================")

    url = "https://lreorgprod4-pst.saas.microfocus.com/Loadtest/rest/domains/Cloud/projects/SMDC/Scripts"

    payload = {
        'metadata': '<Script	xmlns="http://www.hp.com/PC/REST/API">	<TestFolderPath>Subject\\MMH\\MPO\\services\\scripts</TestFolderPath>	<Overwrite>true</Overwrite>	<RuntimeOnly>true</RuntimeOnly>	<KeepCheckedOut>false</KeepCheckedOut></Script>'}

    files = [
        ('filename', (
        'AIP_MAPD_Claim_ClaimsDetails.zip', open('C://EPE/AIP_MAPD_Claim_ClaimsDetails.zip', 'rb'), 'application/zip'))
    ]

    headers = {
        'Cookie': dynamicCookie
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    #print(response.request.url)
    #print(response.request.body)
    #print(response.request.headers)
    print("LRE_SAAS_Upload_Response_Status_Code : " + str(response))
    # print("Login Headers")
    #print("Headers")
    #print(response.headers)
    print("LRE_SAAS_Upload_ResponseContent : ")
    print(response.text)
def getCookie(allCookies):
    print("getCookie---------------------------------------------------------------------")
    print("allCookies")
    print(allCookies)

    remainText = str(allCookies).split('LWSSO_COOKIE_KEY')
    print("remainText")
    print(list(remainText))
    print(remainText)
    lreAuthCookie = 'LWSSO_COOKIE_KEY' + remainText[0]
    print("lreAuthCookie")
    print(lreAuthCookie)


def main():
    LRE_Cookie = lreLogin()
    lreUpload(LRE_Cookie)

main()
