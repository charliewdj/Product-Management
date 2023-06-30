import csv
import logging
from typing import Any, Iterable, Tuple

from django.db import connection

from . import common_msg, input_validator
from .mappers import map_fetch_all

logger = logging.getLogger(__name__)


def get_part_data(up_file, select_data) -> Tuple[Iterable[Iterable[Any]], str]:
    """
    検索値からデータを取得
    """
    part_code = select_data[0]
    part_name = select_data[1]

    err_msg = common_msg.MessageBuilder()

    ##msg = format_check(eos_from, eos_to)
    result = ""

    # エラーが出ていたら処理を終了しメッセージ表示
    ##if msg:
    ##err_msg.add_messages(msg)
    ##return result, err_msg.build()

    try:
        with connection.cursor() as cursor:
            # 販売品目コード , 販売品目名称
            search = ["%" + part_code + "%", "%" + part_name + "%"]

            sql = (
                "SELECT "
                "    pa.part_number"
                "   ,part_name"
                "   ,part_type"
                "   ,eol"
                "   ,pa.update_user_code"
                "   ,ver.update_date "
                "FROM "
                "   part_management_partversion ver "
                "INNER JOIN "
                "   part_management_part pa "
                "ON "
                "   sid_id = pa.id "
                "WHERE "
                "   pa.part_number LIKE %s AND "
                "   part_name LIKE %s "
            )

            logger.info(sql)
            cursor.execute(sql, search)

            result = map_fetch_all(cursor)
    except Exception as e:
        err_msg.add_messages([common_msg.SVERR0009])
        logger.error(e)

    # 検索条件を保存しておく
    select = [[part_code, part_name]]

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
