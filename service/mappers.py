"""SQLで取得した結果セットを変換する関数群モジュール"""

import datetime
from typing import Any, Dict, Iterable


def map_fetch_all(cursor) -> Iterable[Iterable[Any]]:
    """結果セットの変換を行います。

    結果セットの日付をyyyy/MM/ddに変換します。

    Args:
        cursor: SQL実行結果カーソル

    Returns:
        Iterable[Iterable[Any]]: 日付がyyyy/MM/ddに変換された結果

    """

    def convert_row(*row):
        def convert_col(col):
            if isinstance(col, datetime.datetime) or isinstance(col, datetime.date):
                return col.strftime("%Y/%m/%d")
            else:
                return col

        return [convert_col(col) for col in row]

    return [convert_row(*row) for row in cursor.fetchall()]


def dictfetchall(cursor) -> Iterable[Dict[str, Any]]:
    """結果セットを列名、値の辞書で返します

    Args:
       cursor: SQL実行結果カーソル

    Returns:
      Iterable[Dict[str, Any]]: 日付がyyyy/MM/ddに変換された結果
    """

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
