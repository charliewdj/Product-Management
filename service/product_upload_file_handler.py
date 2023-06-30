"""製品情報アップロードでアップロードされたファイルを処理するモジュール"""

import csv
import datetime
import logging
from typing import Iterable, List, Tuple

from django.core.files.uploadedfile import UploadedFile

from . import common_msg, input_validator

logger = logging.getLogger(__name__)


def validate_uploaded_file(
    upload_file: UploadedFile, temp_file_name: str
) -> Tuple[List[Iterable[str]], str]:
    """アップロードされたファイルの内容をチェックします

    Args:
        upload_file (UploadedFile): アップロードされたファイル
        temp_file_name (str): アップロードファイル一時保存ファイル名

    Returns:
        Tuple[List[Iterable[str]], str]:
            アップロードされたファイルを読み込んだ内容とエラーメッセージのタプル
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

                msg = check_code_form(row, row_count)
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

                data_list.append(row)

    except Exception as e:
        err_msg.add_messages([common_msg.SVERR9999])
        logger.error(e)

    return data_list, err_msg.build()


def check_row_len(row: Iterable[str], row_count: int) -> List[str]:
    """1行ごとの項目数チェック

    Args:
        row (Iteable[str]): 項目数チェックを行う行
        row_count (int): チェックを行う行が何行目か

    Returns:
        List[str] エラーのリスト
                  エラーがない場合、空のリストが返されます。
    """

    err_msg = []
    if len(row) != 6:
        err_msg.append(common_msg.SVERR0002.format(row_count))

    return err_msg


def check_null(row: Iterable[str], row_count: int) -> List[str]:
    """必須項目チェック

    Args:
        row (Iterable[str]): 項目数チェックを行う行
        row_count (int): チェックを行う行が何行目か

    Returns:
        List[str] エラーのリスト
                  エラーがない場合、空のリストが返されます。
    """

    err_msg = []
    # 販売品目コード
    if row[0] == "":
        err_msg.append(common_msg.SVERR0003.format(row_count))

    return err_msg


def check_length(row: Iterable[str], row_count: int) -> List[str]:
    """文字数チェック

    Args:
        row (Iterable[str]): 必須項目チェックを行う行
        row_count (int): チェックを行う行が何行目か

    Returns:
        List[str] エラーのリスト
                  エラーがない場合、空のリストが返されます。

    """

    err_msg = []
    # 販売品目コード(17桁)
    if len(row[0]) > 17:
        err_msg.append(common_msg.SVERR0004.format(row_count, 1, 17))

    # 販売品目名称(100桁)
    if len(row[1]) > 100:
        err_msg.append(common_msg.SVERR0005.format(row_count, 2, 100))

    # 担当部門コード(10桁)
    if len(row[2]) > 10:
        err_msg.append(common_msg.SVERR0006.format(row_count, 3, 10))

    # ユーザコード(10桁)
    if len(row[3]) > 10:
        err_msg.append(common_msg.SVERR0007.format(row_count, 4, 10))

    # 担当者連絡先(50桁)
    if len(row[4]) > 50:
        err_msg.append(common_msg.SVERR0008.format(row_count, 5, 50))

    return err_msg

def check_code_form(row: Iterable[str], row_count: int) -> List[str]:

    err_msg = []

    valid = input_validator.validate_product_code(row[0])

    if not valid:
        err_msg.append(common_msg.SVERR0026)

    return err_msg


def check_date_form(row: Iterable[str], row_count: int) -> List[str]:
    """日付フォーマットチェック

    Args:
        row (Iterable[str]): 日付フォーマットチェックを行う行
        row_count (int): チェックを行う行が何行目か

    Returns:
        List[str] エラーのリスト
                  エラーがない場合、空のリストが返されます。
    """

    err_msg = []

    # EOS (YYYY/MM/DD)
    if not row[5] == "":
        valid = input_validator.validate_date(row[5])
        if not valid:
            err_msg.append(common_msg.SVERR0009.format(row_count, "6"))

    return err_msg


def check_year(row: Iterable[str], row_count: int) -> List[str]:

    date_today = datetime.date.today()
    ##year_today = date_today.split("-")
    ##year_today = date_today.year

    err_msg = []

    if not row[5] == "":
        date_data = row[5]
        li = date_data.split("/")
        date_data = datetime.date(int(li[0]), int(li[1]), int(li[2]))
        delta = date_today - date_data

        if delta.days >= (3 * 365):
            err_msg.append(common_msg.SVERR0022)

    return err_msg
