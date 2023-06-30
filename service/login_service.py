"""ログイン処理モジュール"""

import datetime

from django.contrib import auth

from ..models import History


def login(request, user_code: str, password: str) -> int:
    """ユーザをログインします。

    Arguments:
        request: リクエスト
        user_code (str): ユーザコード
        password (str): パスワード

    Returns:
        bool: ログインに成功した場合True、失敗した場合Falseを返します。
    """
    date_today = datetime.date.today()

    user = auth.authenticate(user_code=user_code, password=password)
    if not user:
        return 1

    if not (user.effective_start_date <= date_today <= user.effective_end_date):
        return 2

    auth.login(request, user)

    history = History(
        user_code=user.user_code, user_name=user.user_name, login_time=user.last_login
    )
    history.save()

    return 0


def logout(request) -> None:
    """ユーザをログアウトします。

    Arguments:
        request: リクエスト
    """

    auth.logout(request)
