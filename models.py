from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class Menu(models.Model):
    """メニューマスタ"""

    menu_code = models.CharField("メニューコード", max_length=50, primary_key=True)
    menu_name = models.CharField("メニュー名称", max_length=50)
    menu_seq = models.IntegerField("メニュー表示順序")


class SubMenu(models.Model):
    """サブメニューマスタ"""

    main_menu_code = models.ForeignKey(
        Menu, verbose_name="メインメニューコード", on_delete=models.CASCADE, db_column="menu_code"
    )
    sub_menu_code = models.CharField("サブメニューコード", max_length=50)
    sub_menu_name = models.CharField("メニュー名称", max_length=50)
    menu_seq = models.IntegerField("メニュー表示順序")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "main_menu_code",
                    "sub_menu_code",
                ],
                name="unique_sub_menu",
            ),
        ]


class Department(models.Model):
    """部門マスタ"""

    dept_code = models.CharField("部門コード", max_length=10, primary_key=True)
    dept_name = models.CharField("部門名", max_length=50)
    delete_date = models.DateField("削除日", null=True)
    invalid = models.BooleanField("無効", help_text="無効の場合True")


class UserManager(BaseUserManager):
    def create_user(self, user_code, dept_code, password=None, **kargs):
        if not user_code:
            return None

        dept = Department.objects.get(dept_code=dept_code)
        user = self.model(user_code=user_code, dept_code=dept, **kargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_code, user_name, dept_code, password):
        prop = {
            "user_name": user_name,
            "role": 9,
            "effective_start_date": "2000-01-01",
            "effective_end_date": "2999-12-31",
        }
        suser = self.create_user(user_code, dept_code, password, **prop)
        suser.is_staff = True
        suser.is_superuser = True
        suser.save()
        return suser


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザマスタ"""

    ROLES = ((1, "guest"), (2, "製品管理者"), (3, "部品管理者"), (9, "システム管理者"))

    user_code = models.CharField("ユーザコード", max_length=10, primary_key=True)
    user_name = models.CharField("ユーザ名称", max_length=50)
    password = models.CharField("パスワード", max_length=100)
    dept_code = models.ForeignKey(
        Department, verbose_name="規定組織コード", on_delete=models.PROTECT, db_column="dept_code"
    )
    role = models.IntegerField("役割", choices=ROLES)
    constact_info = models.CharField("連絡先", max_length=50, null=True)
    effective_start_date = models.DateField("有効開始日")
    effective_end_date = models.DateField("有効終了日")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_code"
    REQUIRED_FIELDS = ["user_name", "dept_code"]

    class Meta:
        db_table = "user"

class History(models.Model):

    user_code = models.CharField("ユーザコード", max_length=10)
    user_name = models.CharField("ユーザ名称", max_length=50)
    login_time = models.DateField("ログイン日時")



class Product(models.Model):
    """製品情報"""

    sales_item_number = models.CharField("販売品目コード", max_length=17)
    sales_item_name = models.CharField("販売品目名称", max_length=100)
    owner_dept_code = models.ForeignKey(
        Department, verbose_name="担当部門", on_delete=models.PROTECT, db_column="dept_code"
    )
    owner_user_code = models.ForeignKey(
        User, verbose_name="担当者", on_delete=models.PROTECT, db_column="user_code"
    )
    owner_contact = models.CharField("担当者連絡先", max_length=50, null=True)
    update_user_code = models.CharField("更新者", max_length=10, null=True)
    update_date = models.DateField("更新日", null=True)
    create_user_code = models.CharField("作成者", max_length=10)
    create_date = models.DateField("作成日")
    eos = models.DateField("EOS", null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["sales_item_number"], name="unique_sales_item_number"),
        ]


class Part(models.Model):
    """部品情報"""

    part_number = models.CharField("部品コード", max_length=17)
    update_user_code = models.CharField("更新者", max_length=10, null=True)
    update_date = models.DateField("更新日", null=True)
    create_user_code = models.CharField("作成者", max_length=10)
    create_date = models.DateField("作成日")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["part_number"], name="unique_part_number"),
        ]


class PartVersion(models.Model):
    """部品版数情報"""

    PART_TYPES = (("A", "ASSY"), ("E", "電気電子部品"), ("p", "プリント版"))

    sid = models.ForeignKey(Part, verbose_name="部品ID", on_delete=models.CASCADE)
    revision = models.IntegerField("版数")
    part_name = models.CharField("部品名称", max_length=100)
    part_type = models.CharField("品目種別", max_length=1, choices=PART_TYPES)
    eol = models.DateField("EOL", null=True)
    update_user_code = models.CharField("更新者", max_length=10, null=True)
    update_date = models.DateField("更新日", null=True)
    create_user_code = models.CharField("作成者", max_length=10)
    create_date = models.DateField("作成日")


class PartAssy(models.Model):
    """ASSY情報"""

    sid = models.IntegerField("部品版数ID")


class PartElectricalParts(models.Model):
    """電気電子部品情報"""

    POWER_SUPPLY_SYSTEM_CHOICES = (("01", "単電源品"), ("02", "マルチ電源品"))
    PACKAGE_TYPE_CHOICES = (("01", "DIP"), ("02", "SOP(JEITA)"), ("03", "other"))
    OPERATING_TEMPATURE_CHOICES = (
        ("01", "Commercial"),
        ("02", "Industrial"),
        ("03", "Automotive"),
        ("04", "Military"),
        ("05", "other"),
    )

    sid = models.IntegerField("部品版数ID")
    function = models.CharField("機能", max_length=200, null=True)
    power_supply_system = models.CharField(
        "電源系統", max_length=2, choices=POWER_SUPPLY_SYSTEM_CHOICES, null=True
    )
    min_power_supply_voltage = models.CharField("電源電圧(MIN)[V]", max_length=50, null=True)
    max_power_supply_voltage = models.CharField("電源電圧(MAX)[V]", max_length=50, null=True)
    package_type = models.CharField("パッケージ", max_length=2, choices=PACKAGE_TYPE_CHOICES, null=True)
    temperture_type = models.CharField("温度区分", max_length=2, null=True)
    operating_temperature = models.CharField(
        "動作保証温度", max_length=50, choices=OPERATING_TEMPATURE_CHOICES, null=True
    )
    comment = models.CharField("コメント", max_length=4000, null=True)


class PartPwb(models.Model):
    MOUNTING_TYPE_CHOICES = (("01", "片面"), ("02", "両面"))

    """ プリント板情報 """
    sid = models.IntegerField("部品版数ID")
    layer_count = models.IntegerField("層数")
    mounting_type = models.CharField("実装タイプ", max_length=2, choices=MOUNTING_TYPE_CHOICES)
