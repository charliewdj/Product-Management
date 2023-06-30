from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from .models import Department, History, User
from .service import (
    common_msg,
    login_service,
    part_data_repository,
    part_data_service,
    part_update_service,
    part_uploaded_file_handler,
    product_data_repository,
    product_data_service,
    product_update_service,
    product_upload_file_handler,
    tsv_column_headers,
)


def index(request):
    """ログイン画面"""

    if request.user.is_authenticated:
        login_service.logout(request)
    return render(request, "part_management/login.html")


def login(request):
    """ログイン処理"""

    if request.method == "POST":
        # 入力されたユーザコード、パスワードを取得する
        user_code = request.POST["uid"]
        password = request.POST["pass"]

        # ログイン処理
        login_succeeded = login_service.login(request, user_code, password)
        if login_succeeded == 0:
            return redirect("part_management:MainMenu")

        elif login_succeeded == 1:
            if request.user.is_authenticated:
                login_service.logout(request)
            context = {"error_message": common_msg.SVERR8000}
            return render(request, "part_management/login.html", context)

        elif login_succeeded == 2:
            context = {"error_message": common_msg.SVERR8002}
            return render(request, "part_management/login.html", context)

    return render(request, "part_management/login.html")


##def history(request):
## if request.method == "POST":
#  user_code = request.POST["uid"]
# user_name = request.user_name
# history = History(user_code = user_code, user_name = user_name)
# history.save()


def main_menu(request):
    """メインメニュー"""

    if request.user.is_authenticated:
        return render(request, "part_management/main_menu.html")
    else:
        return render(request, "part_management/no_login.html")


def product_upload(request):
    """製品情報アップロード"""

    if not request.user.is_authenticated:
        return render(request, "part_management/no_login.html")

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        user_code = request.user.user_code
        file_name = user_code + "product.tsv"

        if action_type == "Upload":

            role = request.user.role
            # アップロードボタン押下処理

            if role == 2 or role == 9:

                file = request.FILES["upload_file"]
                (
                    product_result_data,
                    err_msg,
                ) = product_upload_file_handler.validate_uploaded_file(file, file_name)
                column_head = tsv_column_headers.product_column_header()

                if len(err_msg) > 0:
                    return render(
                        request,
                        "part_management/product_upload.html",
                        {"error_message": err_msg},
                    )

                return render(
                    request,
                    "part_management/product_upload.html",
                    {"column_head": column_head, "result_data": product_result_data},
                )

            else:
                return render(
                    request,
                    "part_management/product_upload.html",
                    {"error_message": common_msg.SVERR0020},
                )

        elif action_type == "Apply":
            # 確定ボタン押下処理
            success_msg = product_update_service.apply_file_content(user_code, file_name)
            return render(
                request, "part_management/product_upload.html", {"success_message": success_msg}
            )

    return render(
        request,
        "part_management/product_upload.html",
    )


def product_info(request):
    """製品情報検索"""

    if not request.user.is_authenticated:
        return render(request, "part_management/no_login.html")

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        user_code = request.user.user_code
        file_name = user_code + "pro_info.tsv"

        if action_type == "search":
            # 検索ボタン押下処理

            # 入力された検索条件
            select_data = [
                request.POST.get("part_code"),
                request.POST.get("dept_name"),
                request.POST.get("part_name"),
                request.POST.get("user_name"),
                request.POST.get("eos_from"),
                request.POST.get("eos_to"),
            ]

            result_data, err_msg = product_data_repository.get_product_data(file_name, select_data)
            print(select_data[1])
            return render(
                request,
                "part_management/product_info.html",
                {
                    "result_data": result_data,
                    "error_message": err_msg,
                    "part_code": select_data[0],
                    "dept_name": select_data[1],
                    "part_name": select_data[2],
                    "user_name": select_data[3],
                    "eos_from": select_data[4],
                    "eos_to": select_data[5],
                },
            )

        elif action_type == "apply":

            role = request.user.role

            if role == 2 or role == 9:

                # 確定ボタン押下処理
                check_list = request.POST.getlist("applyChk")
                new_name = request.POST.getlist("updSalesItemName")
                new_eos = request.POST.getlist("updEos")
                result_data, err_msg = product_data_service.update_product_data(
                    file_name, user_code, check_list, new_name, new_eos
                )

                # 入力された検索条件保持
                select_data = [
                    request.POST.get("part_code"),
                    request.POST.get("dept_name"),
                    request.POST.get("part_name"),
                    request.POST.get("user_name"),
                    request.POST.get("eos_from"),
                    request.POST.get("eos_to"),
                ]

                return render(
                    request,
                    "part_management/product_info.html",
                    {
                        "result_data": result_data,
                        "error_message": err_msg,
                        "part_code": select_data[0],
                        "dept_name": select_data[1],
                        "part_name": select_data[2],
                        "user_name": select_data[3],
                        "eos_from": select_data[4],
                        "eos_to": select_data[5],
                    },
                )

    return render(request, "part_management/product_info.html")


def part_upload(request):
    """部品情報アップロード"""

    if not request.user.is_authenticated:
        return render(request, "part_management/no_login.html")

    if request.method == "POST":
        post = request.POST.get("action_type")
        user_code = request.user.user_code
        file_name = user_code + "part.tsv"

        if post == "Upload":

            role = request.user.role

            if role == 3 or role == 9:
                # アップロードボタン押下処理
                file = request.FILES["upload_file"]
                part_result_data, err_msg = part_uploaded_file_handler.parse_uploaded_file(
                    file, file_name
                )
                column_head = tsv_column_headers.part_column_header()
                if len(err_msg) > 0:
                    return render(
                        request, "part_management/part_upload.html", {"error_message": err_msg}
                    )

                return render(
                    request,
                    "part_management/part_upload.html",
                    {"column_head": column_head, "result_data": part_result_data},
                )

            else:
                return render(
                    request,
                    "part_management/product_upload.html",
                    {"error_message": common_msg.SVERR0021},
                )

        elif post == "Apply":
            # 確定ボタン押下処理
            part_update_service.register_by_file(user_code, file_name)
            return render(request, "part_management/part_upload.html")

    return render(request, "part_management/part_upload.html")


def part_search(request):
    """
    部品情報検索
    """

    if not request.user.is_authenticated:
        return render(request, "part_management/no_login.html")

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        user_code = request.user.user_code
        file_name = user_code + "part_info.tsv"

        if action_type == "search":
            # 検索ボタン押下処理

            # 入力された検索条件
            select_data = [
                request.POST.get("part_code"),
                request.POST.get("part_name"),
            ]

            result_data, err_msg = part_data_repository.get_part_data(file_name, select_data)
            return render(
                request,
                "part_management/part_info.html",
                {
                    "result_data": result_data,
                    "error_message": err_msg,
                    "part_code": select_data[0],
                    "part_name": select_data[1],
                },
            )

        elif action_type == "apply":

            # 確定ボタン押下処理
            check_list = request.POST.getlist("applyChk")
            new_name = request.POST.getlist("updPartsName")
            new_eos = request.POST.getlist("updEol")
            result_data, err_msg = part_data_service.update_part_data(
                file_name, user_code, check_list, new_name, new_eos
            )

            # 入力された検索条件保持
            select_data = [
                request.POST.get("part_code"),
                request.POST.get("part_name"),
            ]

            return render(
                request,
                "part_management/part_info.html",
                {
                    "result_data": result_data,
                    "error_message": err_msg,
                    "part_code": select_data[0],
                    "part_name": select_data[1],
                },
            )
    return render(request, "part_management/part_info.html")
