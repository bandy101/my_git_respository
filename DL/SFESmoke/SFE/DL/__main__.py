from fire import Fire


def main(src, key, dst=None):
    from SFE.DL.BaseModel import BaseModel
    BaseModel.encrypt(src, dst, key)


Fire(main)
