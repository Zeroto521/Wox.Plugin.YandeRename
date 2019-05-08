# -*- coding: utf-8 -*-

import copy
import os
from getpass import getuser

import pyperclip

from wox import Wox, WoxAPI

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


class Main(Wox):

    def query(self, param):
        """Wox dealing programm

        Arguments:
            param {str} -- wox window key in parameter

        Returns:
            list -- wox json list
        """

        os.chdir(PATH)  # switch to main path

        result = []
        param = param.strip()

        counter = 0
        for pic in os.listdir():
            name, extend = os.path.splitext(pic)
            if extend in EXTENDS:
                if any([flag in name for flag in FLAGS]):
                    if 'yande.re' in name:
                        mark = ' ' if ' ' in name else '%'
                        # use yande.re's "id to replace raw name
                        realname = name.split(mark)[1]

                    if 'original' in name:
                        # use yande.re's "id to replace raw name
                        realname = name.split('-')[0]

                    realname += extend

                    if not os.path.exists(realname):
                        os.rename(pic, realname)  # rename it
                        counter += 1  # to count how many pictures

                    else:
                        title = 'Failed to rename {}, please to check out the picture in local folder.'.format(
                            realname)
                        subtitle = 'Click to copy picture name to clipboard.'
                        method = 'copy2clipboard'
                        result.append(
                            self.genaction(title, subtitle, method, name))

        title = "{} pictures have renamed.".format(counter)
        subtitle = 'Click to open the folder in window.'
        method = 'openFolder'
        result.insert(0, self.genaction(title, subtitle, method, PATH))

        return result

    @staticmethod
    def genformat(title, subtitle=''):
        """Generate wox json data

        Arguments:
            title {str} -- as name

        Keyword Arguments:
            subtitle {str} -- additional information (default: {''})

        Returns:
            json -- wox json
        """

        time_format = copy.deepcopy(RESULT_TEMPLATE)
        time_format['Title'] = title
        time_format['SubTitle'] = subtitle

        return time_format

    @staticmethod
    def genaction(tit, subtit, method, actparam):
        """Generate wox json data with copy action

        Arguments:
            title {str} -- as name
            actparam {str} -- the paramter which need to copy

        Returns:
            json -- wox json
        """

        res = copy.deepcopy(RESULT_TEMPLATE)
        res['Title'] = tit
        res['SubTitle'] = subtit

        action = copy.deepcopy(ACTION_TEMPLATE)
        action['JsonRPCAction']['method'] = method
        action['JsonRPCAction']['parameters'] = [actparam]
        res.update(action)

        return res

    def copy2clipboard(self, value):
        pyperclip.copy(value)

    def openFolder(self, path):
        os.startfile(path)
        WoxAPI.change_query(path)


if __name__ == '__main__':
    Main()
