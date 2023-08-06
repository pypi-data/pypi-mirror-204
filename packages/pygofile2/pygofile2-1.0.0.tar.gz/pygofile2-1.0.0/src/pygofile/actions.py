import requests, logging
from urllib.parse import urlparse

BASE_URL = 'https://api.gofile.io'

Errors = {
    'error-auth': 'Invalid token provided',
    'error-notPremium': 'This endpoint is for premium users only, get premium here: https://gofile.io/myProfile#premium.'
}

def _request(req):
    try:
        res = req.json()

        if 'status' in res and res['status'] != 'ok':
            return _error(req, res['status'])
        
        return res['data']
    except Exception as error:
        return _error(req, error)
    
def _error(req, error):
    path = urlparse(req.url).path[1:]

    if error in Errors:
        logging.error('%s: %s (%s)', path, Errors[error], error)
    else:
        logging.error('%s: %s', path, error)

    return False

def getServer():
    req = requests.get(url=f'{BASE_URL}/getServer')

    return _request(req)

def getAccountDetails(token):
    req = requests.get(url=f'{BASE_URL}/getAccountDetails?token={token}')
        
    return _request(req)

def getContent(contentId, token):
    req = requests.get(url=f'{BASE_URL}/getContent?contentId={contentId}&token={token}')
        
    return _request(req)

def createFolder(parentFolderId, folderName, token):
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    payload = f"parentFolderId={parentFolderId}&folderName={folderName}&token={token}"

    req = requests.put(url=f'{BASE_URL}/createFolder', data=payload, headers=headers)

    return _request(req)

def setOption(contentId, option, value, token):
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    payload = f"contentId={contentId}&option={option}&value={value}&token={token}"

    req = requests.put(url=f'{BASE_URL}/setOption', data=payload, headers=headers)

    return _request(req)

def copyContent(contentsId, folderIdDest, token):
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    payload = f"contentsId={contentsId}&folderIdDest={folderIdDest}&token={token}"

    req = requests.put(url=f'{BASE_URL}/copyContent', data=payload, headers=headers)

    return _request(req)

def deleteContent(contentsId, token):
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    payload = f"contentsId={contentsId}&token={token}"

    req = requests.delete(url=f'{BASE_URL}/deleteContent', data=payload, headers=headers)

    return _request(req)

def uploadFile(filePath, folderId, server, token):
    files = { 'upload_file': open(filePath, 'rb') }
    payload = { 'folderId': folderId, 'token': token }

    req = requests.post(url=f'https://{server}.gofile.io/uploadFile', data=payload, files=files)

    return _request(req)