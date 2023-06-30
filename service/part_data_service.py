import csv
import logging
import os
from datetime import date

from django.db import connection

from . import common_msg, part_data_repository
from .input_validator import validate_date

logger = logging.getLogger(__name__)


def update_part_data(file_name, user, check_list, new_name, new_eos):
    """
    選択された行のアップデート処理
    """

    result = ""
    err_msg = common_msg.MessageBuilder()
    msg = format_check(check_list, new_eos)
    now_date = date.today().strftime("%Y-%m-%d")

    # エラーが出ていたら処理を終了しメッセージ表示
    if msg:
        err_msg.add_messages(msg)
        return result, err_msg.build()

    try:
        # 一時ファイル読み取り
        with open(file_name, "r") as file:
            reader = csv.reader(file)

            row_count = 0
            check_count = 0
            select_list = []
            for row in reader:

                # 検索条件
                if row_count == 0:
                    select_list = row[0], row[1]

                # チェックボックスで選択した行のUpdate
                if int(check_list[check_count]) == row_count:
                    check_count += 1
                    up_name = new_name[row_count - 1]
                    up_eos = new_eos[row_count - 1]
                    item_number = row[1]

                    # 空文字の場合Nullに変換する
                    if not up_eos:
                        up_eos = None

                    # UPDATE実行
                    sql = f"""
                        UPDATE
                           part_management_partversion
                        SET
                           part_name = '{up_name}'
                          ,eol = { f"'{up_eos}'" if up_eos is not None else "NULL" }
                        WHERE
                           part_name = '{item_number}'
                    """

                    with connection.cursor() as cursor:
                        cursor.execute(sql)

                    # チェックボックスで選択した数分を処理したら終了
                    if check_count == len(check_list):
                        break

                row_count += 1

    except Exception as e:
        err_msg.add_messages([common_msg.SVERR9999])
        logger.error(e)

    # 一時ファイルを消去
    os.remove(file_name)

    result, err_msg = part_data_repository.get_part_data(file_name, select_list)

    return result, err_msg


def format_check(check_list, new_eos):
    """
    日付書式チェック
    """
    err_msg = []

    row_count = 0
    check_count = 0
    for eos in new_eos:
        row_count += 1

        if int(check_list[check_count]) == row_count:
            check_count += 1
            # EOS (YYYY/MM/DD)
            if not (eos == "" or eos == "None"):
                valid = validate_date(eos)
                if not valid:
                    err_msg.append(common_msg.SVERR0019.format(row_count, eos))

            if check_count == len(check_list):
                break

    return err_msg
