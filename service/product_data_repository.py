import csv
import logging
from typing import Any, Iterable, Tuple

from django.db import connection

from . import common_msg, input_validator
from .mappers import map_fetch_all

logger = logging.getLogger(__name__)


def get_product_data(up_file, select_data) -> Tuple[Iterable[Iterable[Any]], str]:
    """
    検索値からデータを取得
    """
    part_code = select_data[0]
    dept_name = select_data[1]
    part_name = select_data[2]
    user_name = select_data[3]
    eos_from = select_data[4]
    eos_to = select_data[5]

    err_msg = common_msg.MessageBuilder()

    msg = format_check(eos_from, eos_to)
    result = ""

    # エラーが出ていたら処理を終了しメッセージ表示
    if msg:
        err_msg.add_messages(msg)
        return result, err_msg.build()

    try:
        with connection.cursor() as cursor:
            # 販売品目コード , 販売品目名称
            search = ["%" + part_code + "%", "%" + part_name + "%"]

            sql = (
                "SELECT "
                "    pro.sales_item_number"
                "   ,pro.sales_item_name"
                "   ,dep.dept_name"
                "   ,user.user_name"
                "   ,pro.owner_contact"
                "   ,pro.eos"
                "   ,pro.update_user_code"
                "   ,pro.update_date "
                "FROM "
                "   part_management_product pro "
                "INNER JOIN "
                "   part_management_department dep "
                "ON "
                "   pro.dept_code = dep.dept_code "
                "INNER JOIN "
                "   user "
                "ON "
                "   pro.user_code = user.user_code "
                "WHERE "
                "   pro.sales_item_number LIKE %s AND "
                "   pro.sales_item_name LIKE %s "
            )

            # 担当部門 (条件入力時)
            if dept_name:
                sql += "AND dep.dept_name = %s "
                search.append(dept_name)

            # 担当者　(条件入力時)
            if user_name:
                sql += "AND user.user_name = %s "
                search.append(user_name)

            # EOS(From)　(条件入力時)
            if eos_from:
                sql += "AND pro.eos >= %s "
                search.append(eos_from)

            # EOS(to)　(条件入力時)
            if eos_to:
                sql += "AND pro.eos <= %s "
                search.append(eos_to)

            cursor.execute(sql, search)

            result = map_fetch_all(cursor)
    except Exception as e:
        err_msg.add_messages([common_msg.SVERR0009])
        logger.error(e)

    # 検索条件を保存しておく
    select = [[part_code, dept_name, part_name, user_name, eos_from, eos_to]]

    # 一時ファイルを作成しデータ出力
    with open(up_file, "w", newline="") as file:
        file_writer = csv.writer(file, delimiter=",")
        file_writer.writerows(select)
        file_writer.writerows(result)

    return result, err_msg.build()


def format_check(eos_from, eos_to):
    """
    日付書式チェック
    """
    err_msg = []

    # EOS_from (YYYY/MM/DD)
    if not eos_from == "":
        valid = input_validator.validate_date(eos_from)
        if not valid:
            err_msg.append(common_msg.SVERR0017)

    # EOS_to (YYYY/MM/DD)
    if not eos_to == "":
        valid = input_validator.validate_date(eos_to)
        if not valid:
            err_msg.append(common_msg.SVERR0018)

    return err_msg
