"""入力バリデーションモジュール"""

import datetime
import re


def validate_date(date: str) -> bool:
    """引数がyyyy/mm/ddの日付かチェックを行います

    Args:
        date (str): チェックする日付

    Returns:
        bool: 引数がyyyy/mm/ddの日付の場合True,そうでない場合False
    """

    if not date:
        return False

    pattern = r"\d{4}/\d{2}/\d{2}(?!\d)"
    boolean = bool(re.match(pattern, date))

    if boolean is False:
        return boolean

    li = date.split("/")
    try:
        datetime.date(int(li[0]), int(li[1]), int(li[2]))
    except ValueError:
        boolean = False

    return boolean

def validate_product_code(code: str) -> bool:

    if not code:
        return False

    pattern = r"\w{3}-\w{6}-\w{3}-\w{2}(?!\w)"
    return bool(re.match(pattern, code))


