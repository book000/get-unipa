class UnipaInternalError(Exception):
    """
    処理に失敗した
    """


class UnipaLoginError(Exception):
    """
    ログインに失敗した
    """


class UnipaNotLoggedIn(Exception):
    """
    UNIPA にログインしている必要があるがしていない
    """
