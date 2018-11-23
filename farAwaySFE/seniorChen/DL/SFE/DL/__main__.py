# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\DL\__main__.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 147 bytes
from fire import Fire

def main(src, key, dst=None):
    from SFE.DL.BaseModel import BaseModel
    BaseModel.encrypt(src, dst, key)


Fire(main)
# okay decompiling SFE\DL\__main__.pyc
