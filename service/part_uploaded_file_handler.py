import csv
import datetime
import logging
from typing import Iterable, List, Tuple

from . import common_msg, input_validator

logger = logging.getLogger(__name__)


def parse_uploaded_file(upload_file, temp_file_name) -> Tuple[List[Iterable[str]], str]:
    """
    アップデートファイルの読み取り
    """

    # ファイルサイズの確認
    if not upload_file or upload_file.size == 0:
        return [], common_msg.SVERR0001

    data_list = []
    err_msg = common_msg.MessageBuilder()

    # 一時ファイルを作成しデータ出力
    with open(temp_file_name, "wb+") as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)

    # 一時ファイルからtsvデータ読み込み
    try:
        with open(temp_file_name, "r") as file:
            reader = csv.reader(file, delimiter="\t")

            for row_count, row in enumerate(reader, 1):
                msg = check_row_len(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                msg = check_null(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                msg = check_length(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                msg = check_num(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                msg = check_date_form(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                msg = check_year(row, row_count)
                if msg:
                    err_msg.add_messages(msg)
                    continue

                # データ格納
                data_list.append(row)

    except Exception as e:
        err_msg.add_messages([common_msg.SVERR9999])
        logger.error(e)

    return data_list, err_msg.build()


def check_row_len(row, row_count):
    """1行ごとの項目数チェック"""
    err_msg = []
    if not len(row) == 17:
        err_msg.append(common_msg.SVERR0011.format(row_count))

    return err_msg


def check_null(row, row_count):
    """nullチェック"""
    err_msg = []
    # 部品コード
    if row[0] == "":
        err_msg.append(common_msg.SVERR0012.format(row_count, 1))

    # 版数
    if row[1] == "":
        err_msg.append(common_msg.SVERR0012.format(row_count, 2))

    # 品目種別
    if row[3] == "":
        err_msg.append(common_msg.SVERR0012.format(row_count, 4))

    # 担当者
    if row[5] == "":
        err_msg.append(common_msg.SVERR0012.format(row_count, 6))

    # 更新日
    if row[6] == "":
        err_msg.append(common_msg.SVERR0012.format(row_count, 7))

    return err_msg


def check_length(row, row_count):
    """文字数チェック"""

    err_msg = []
    # 部品コード
    if len(row[0]) > 17:
        err_msg.append(common_msg.SVERR0013.format(row_count, 1, 17))

    valid = input_validator.validate_product_code(row[0])
    if not valid:
        err_msg.append(common_msg.SVERR0024)

    # 部品版数
    if len(row[1]) > 3:
        err_msg.append(common_msg.SVERR0013.format(row_count, 2, 3))

    # 部品名称
    if len(row[2]) > 100:
        err_msg.append(common_msg.SVERR0013.format(row_count, 3, 100))

    # 品目種別
    if len(row[3]) > 1:
        err_msg.append(common_msg.SVERR0013.format(row_count, 4, 2))

    # 品目種別が"E"のとき
    if row[3] == "E":
        # 機能（200桁）
        if len(row[7]) > 200:
            err_msg.append(common_msg.SVERR0013.format(row_count, 8, 200))

        # 電源系統（2桁）
        if len(row[8]) > 2:
            err_msg.append(common_msg.SVERR0013.format(row_count, 9, 2))

        # 電源電圧 (MIN)[V]（30桁）
        if len(row[9]) > 30:
            err_msg.append(common_msg.SVERR0013.format(row_count, 10, 30))

        # 電源電圧 (MAX)[V]（30桁）
        if len(row[10]) > 30:
            err_msg.append(common_msg.SVERR0013.format(row_count, 11, 30))

        # パッケージ（2桁）
        if len(row[11]) > 2:
            err_msg.append(common_msg.SVERR0013.format(row_count, 12, 2))

        # 温度区分（2桁）
        if len(row[12]) > 2:
            err_msg.append(common_msg.SVERR0013.format(row_count, 3, 2))

        # 動作保証温度（50桁）
        if len(row[13]) > 50:
            err_msg.append(common_msg.SVERR0013.format(row_count, 14, 50))

        # コメント（4000桁）
        if len(row[14]) > 4000:
            err_msg.append(common_msg.SVERR0013.format(row_count, 15, 4000))

    # 品目種別が"P"のとき
    if row[3] == "P":
        # 層数（4桁）
        if len(row[7]) > 4:
            err_msg.append(common_msg.SVERR0013.format(row_count, 8, 4))

        # 実装タイプ（2桁）
        if len(row[8]) > 2:
            err_msg.append(common_msg.SVERR0013.format(row_count, 9, 2))

    return err_msg


def check_num(row, row_count):
    """
    数値チェック
    """
    err_msg = []
    # 部品版数
    if not row[1].isdigit():
        err_msg.append(common_msg.SVERR0014.format(row_count, 2))

    # 品目種別が"P"のとき
    if row[3] == "P":
        # 層数
        if not row[7].isdigit():
            err_msg.append(common_msg.SVERR0014.format(row_count, 8))

    return err_msg


def check_date_form(row, row_count):
    """
    日付フォーマットチェック
    """
    err_msg = []

    # EOL (YYYY/MM/DD)
    if not row[4] == "":
        valid = input_validator.validate_date(row[4])
        if not valid:
            err_msg.append(common_msg.SVERR0015.format(row_count, 5))

    # 更新日 (YYYY/MM/DD)
    if not row[6] == "":
        valid = input_validator.validate_date(row[6])
        if not valid:
            err_msg.append(common_msg.SVERR0015.format(row_count, 7))

    return err_msg

def check_year(row, row_count):

    date_today = datetime.date.today()
    err_msg = []

    if not row[4] == "":
        date_data = row[4]
        li = date_data.split("/")
        date = datetime.date(int(li[0]), int(li[1]), int(li[2]))
        delta = date_today - date

        if delta.days >= (3 * 365):
            err_msg.append(common_msg.SVERR0023)

    return err_msg






