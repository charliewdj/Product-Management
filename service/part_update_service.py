"""部品情報登録モジュール"""

import csv
import os
from datetime import date

from django.db import connection

from ..models import Part


def register_by_file(user_code: str, up_file: str) -> None:
    """ファイルから部品情報を登録します

    Args:
        user (str):
        up_file (str): 部品情報を登録するファイル名
    """

    now_date = date.today().strftime("%Y-%m-%d")

    # 一時ファイルからtsvデータ読み込み
    with open(up_file, "r") as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            with connection.cursor() as cursor:
                sel_id = ""
                sel_sid = ""

                part_number = row[0]
                revision = row[1]
                part_name = row[2]
                part_type = row[3]
                eol = row[4] if row[4] != "" else None
                update_user_code = row[5]
                update_date = row[6] if row[6] != "" else None
                part_function = row[7]
                power_supply = row[8]
                max_power = row[9]
                min_power = row[10]
                package_type = row[11]
                temperature_type = row[12]
                operating_temperature = row[13]
                comment = row[14]

                create_user_code = user_code
                create_date = now_date

                # ID取得
                for sel_data in Part.objects.raw(
                    """
                    SELECT
                         part.id
                        ,ver.sid_id
                    FROM
                        part_management_part part
                    INNER JOIN
                        part_management_partversion ver
                    ON
                        part.id = ver.sid_id
                    WHERE
                        part.part_number = %s
                      AND
                        ver.revision = %s
                    """,
                    [part_number, revision],
                ):
                    sel_id = sel_data.id
                    sel_sid = sel_data.sid_id

                # データ削除
                cursor.execute(
                    """
                    DELETE FROM
                        part_management_partversion
                    WHERE
                        revision = %s
                      AND
                        sid_id = %s
                    """,
                    [revision, sel_sid],
                )

                cursor.execute("DELETE FROM part_management_partassy WHERE sid = %s", [sel_sid])

                cursor.execute(
                    "DELETE FROM part_management_partelectricalparts WHERE sid = %s", [sel_sid]
                )

                cursor.execute("DELETE FROM part_management_partpwb WHERE sid = %s", [sel_sid])

                for sel_data in Part.objects.raw(
                    "SELECT id FROM part_management_part part WHERE part_number = %s",
                    [part_number],
                ):
                    sel_id = sel_data.id

                # データが無い場合登録
                if not sel_id:
                    cursor.execute(
                        """
                        INSERT INTO
                            part_management_part
                        (part_number, update_user_code, update_date, create_user_code, create_date)
                        VALUES
                        (%s,%s,%s,%s,%s)
                        """,
                        [part_number, user_code, now_date, create_user_code, create_date],
                    )

                # ID取得
                for sel_part in Part.objects.raw(
                    "SELECT part.id FROM part_management_part part WHERE part.part_number = %s",
                    (part_number,),
                ):
                    new_sel_id = sel_part.id

                # データ登録
                cursor.execute(
                    """
                    INSERT INTO
                        part_management_partversion
                    (sid_id, revision, part_name, part_type, eol, update_user_code, update_date,
                     create_user_code, create_date)
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    [
                        new_sel_id,
                        revision,
                        part_name,
                        part_type,
                        eol,
                        update_user_code,
                        update_date,
                        create_user_code,
                        create_date,
                    ],
                )

                # Assy情報登録
                if part_type == "A":
                    cursor.execute(
                        "INSERT INTO part_management_partassy(sid) VALUES (%s)", [new_sel_id]
                    )

                # 電気電子部品情報登録
                elif part_type == "E":
                    cursor.execute(
                        """
                        INSERT INTO
                            part_management_partelectricalparts
                        (sid, function, power_supply_system, min_power_supply_voltage,
                         max_power_supply_voltage, package_type, temperture_type,
                         operating_temperature, comment)
                        VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        [
                            new_sel_id,
                            part_function,
                            power_supply,
                            max_power,
                            min_power,
                            package_type,
                            temperature_type,
                            operating_temperature,
                            comment,
                        ],
                    )

                # プリント板情報登録
                elif part_type == "P":
                    cursor.execute(
                        """
                        INSERT INTO
                            part_management_partpwb
                        (sid, layer_count, mounting_type)
                        VALUES
                        (%s,%s,%s)
                        """,
                        [new_sel_id, part_function, power_supply],
                    )

    # 一時ファイルを消去
    os.remove(up_file)
