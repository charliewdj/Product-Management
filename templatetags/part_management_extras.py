from dataclasses import dataclass
from itertools import groupby

from django import template
from django.db import connection

from ..service.mappers import dictfetchall

register = template.Library()


@dataclass
class MenuItem:
    """メニュー項目

    Attributes:
        name (str): HTMLに表示されるメニュー名
        url (str): URL(urlテンプレートタグで変換できる値)
    """

    name: str
    url: str


class MenuList:
    """メニューリスト メニューとサブメニューを表します

    Attributes:
        parent (str): 親メニュー名
        child (List[str]): 親メニューが持つメニュー
    """

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child


@register.filter()
def make_menu(dummy):
    """メニューアイテム作成"""

    result = []
    menus = None
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                 M.menu_code AS MainMenuCode
                ,M.menu_name AS MainMenuName
                ,S.sub_menu_code AS SubMenuCode
                ,S.sub_menu_name AS SubMenuName
            FROM
                part_management_menu AS M
            LEFT OUTER JOIN
                part_management_submenu AS S
            ON
                M.menu_code = S.menu_code
            ORDER BY
                M.menu_seq ASC
                ,S.menu_seq ASC
            """
        )
        menus = dictfetchall(cursor)

    for name, group in groupby(menus, key=lambda m: m["MainMenuCode"]):
        item = []
        for g in group:
            name = g["MainMenuName"]

            # サブメニューが存在しない場合
            if g["SubMenuCode"] is None:
                item.append(MenuItem(g["MainMenuName"], "part_management:" + g["MainMenuCode"]))
                break

            item.append(MenuItem(g["SubMenuName"], "part_management:" + g["SubMenuCode"]))

        result.append(MenuList(name, item))

    return result
