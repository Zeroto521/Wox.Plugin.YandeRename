# -*- coding: utf-8 -*-

import copy
import os
from getpass import getuser

import pyperclip
from wox import Wox, WoxAPI

username = getuser()
PATH = r'C:\Users\{}\Pictures\舔图猫'.format(username)

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
            try:
                name, extend = os.path.splitext(pic)
                if extend in [".png", '.jpg', '.jpeg']:
                    mark = ' ' if ' ' in name else '%'
                    name_list = name.split(mark)
                    if name_list[0] == 'yande.re':
                        # use yande.re's "id + extend" to rename
                        realname = name_list[1] + extend
                        os.rename(pic, realname)  # rename it

                        counter += 1  # to count how many pictures
            except:
                # void the same picture problem.
                title = 'Error: {}'.format(name)
                subtitle = 'Click to copy picture name to clipboard.'
                method = 'copy2clipboard'
                result.append(self.genaction(title, subtitle, method, name))
                continue
        else:
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
