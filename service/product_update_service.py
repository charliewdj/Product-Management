import csv
import os
from datetime import date

from django.db import connection

from ..models import Product
from . import common_msg


def apply_file_content(user, up_file):
    """
    読み取ったデータからDBにデータ登録
    """

    now_date = date.today().strftime("%Y-%m-%d")

    # 一時ファイルからtsvデータ読み込み
    with open(up_file, "r") as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            with connection.cursor() as cursor:
                sales_item_number = row[0]
                sales_item_name = row[1]
                owner_dept_code = row[2]
                owner_user_code = row[3]
                update_user_code = user
                update_date = now_date
                create_user_code = user
                create_date = now_date
                owner_contact = row[4]
                eos = row[5] if row[5] != "" else None

                cursor.execute(
                        "DELETE FROM part_management_product " "WHERE sales_item_number = %s",
                        [sales_item_number],
                    )

                cursor.execute(
                    "INSERT INTO part_management_product"
                    "(sales_item_number,sales_item_name,dept_code,"
                    "user_code,update_user_code,update_date,"
                    "create_user_code,create_date,owner_contact,eos) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [
                        sales_item_number,
                        sales_item_name,
                        owner_dept_code,
                        owner_user_code,
                        update_user_code,
                        update_date,
                        create_user_code,
                        create_date,
                        owner_contact,
                        eos,
                    ],
                )


    # 一時ファイルを消去
    os.remove(up_file)

    return common_msg.SVERR0025

    #common_msg.SVERR0025
