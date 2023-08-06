import logging, os

from typing import NewType
from .actions import *

TOKEN = NewType('Token', str)

logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

class GoFile:
    def __init__(self, token=TOKEN) -> dict:
        self._token = token
        self._server = getServer()['server']
        self._account = getAccountDetails(self._token)
        self._root_folder = self._account['rootFolder']

    def get_content(self, contentId=str) -> dict:
        if not contentId:
            contentId = self._root_folder

        return getContent(contentId, self._token)

    def create_folder(self, folderName=str, parentFolderId=str) -> dict:
        if not folderName:
            return logging.error('GoFile.create_folder: Invalid folder name')

        if not parentFolderId:
            parentFolderId = self._root_folder

        return createFolder(parentFolderId, folderName, self._token)
    
    def set_option(self, contentId=str, option=str, value=str) -> dict:
        if not contentId:
            return logging.error('GoFile.set_option: Invalid content id')
        
        if not option:
            return logging.error('GoFile.set_option: Invalid option')
        
        if not value:
            return logging.error('GoFile.set_option: Invalid value')
        
        return setOption(contentId, option, value, self._token)
    
    def copy_content(self, contentsId=str, folderIdDest=str) -> dict:
        if contentsId == str:
            return logging.error('GoFile.copy_content: Invalid contents id')

        if folderIdDest == str:
            folderIdDest = self._root_folder

        return copyContent(contentsId, folderIdDest, self._token)
    
    def delete_content(self, contentsId=str) -> dict:
        if contentsId == str:
            return logging.error('GoFile.delete_content: Invalid contents id')

        return deleteContent(contentsId, self._token)
    
    def upload_file(self, filePath=str, folderId=str) -> dict:
        if filePath == str:
            return logging.error('GoFile.upload_file: Invalid file')

        if not os.path.exists(filePath):
            return logging.error('GoFile.upload_file: No file exists')

        if folderId == str:
            folderId = self._root_folder

        return uploadFile(filePath, folderId, self._server, self._token)