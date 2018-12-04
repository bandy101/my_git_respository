from SFE import getAuthID


def getAuthCode(auth_id: str=None):
    """ 获取授权码
    - auth_id str[None]: 授权ID, 为`None`时会获取当前机器的ID
    """
    from hashlib import md5

    if auth_id is None:
        auth_id = getAuthID()

    code = 1
    for c in auth_id.replace("f", "").replace("e", "").split("-"):
        if c:
            code *= int(c, 16)
    return md5(bin(code).encode()).hexdigest()


if __name__ == "__main__":
    from fire import Fire
    Fire({
        "getAuthID": getAuthID,
        "getAuthCode": getAuthCode
    })
