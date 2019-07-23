# -*- coding: utf-8 -*-

import copy
import os
from hashlib import md5

import pyperclip
from send2trash import send2trash

from wox import Wox, WoxAPI

from .constants import *


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
            if extend in EXTENDS and any([flag in name for flag in FLAGS]):
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
                elif self.getMD5(realname) == self.getMD5(pic):
                    send2trash(pic)
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

    def getMD5(self, file):
        with open(file, 'rb') as f:
            m = md5(f.read())
        return m.hexdigest()
