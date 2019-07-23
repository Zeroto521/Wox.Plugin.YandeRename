# -*- coding: utf-8 -*-

from getpass import getuser

USERNAME = getuser()
PATH = r'C:\Users\{}\Pictures\舔图猫'.format(USERNAME)

RESULT_TEMPLATE = {
    'Title': '',
    'SubTitle': '',
    'IcoPath': 'Images/favicon.ico',
}

ACTION_TEMPLATE = {
    'JsonRPCAction': {
        'method': '',
        'parameters': [],
    }
}

FLAGS = ['yande.re', 'original']
EXTENDS = [".png", '.jpg', '.jpeg', '.gif']
