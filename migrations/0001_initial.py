# Generated by Django 4.0.6 on 2022-08-15 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_code', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='ユーザコード')),
                ('user_name', models.CharField(max_length=50, verbose_name='ユーザ名称')),
                ('password', models.CharField(max_length=100, verbose_name='パスワード')),
                ('role', models.IntegerField(choices=[(1, 'guest'), (2, '製品管理者'), (3, '部品管理者'), (9, 'システム管理者')], verbose_name='役割')),
                ('constact_info', models.CharField(max_length=50, null=True, verbose_name='連絡先')),
                ('effective_start_date', models.DateField(verbose_name='有効開始日')),
                ('effective_end_date', models.DateField(verbose_name='有効終了日')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_code', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='部門コード')),
                ('dept_name', models.CharField(max_length=50, verbose_name='部門名')),
                ('delete_date', models.DateField(null=True, verbose_name='削除日')),
                ('invalid', models.BooleanField(help_text='無効の場合True', verbose_name='無効')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('menu_code', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='メニューコード')),
                ('menu_name', models.CharField(max_length=50, verbose_name='メニュー名称')),
                ('menu_seq', models.IntegerField(verbose_name='メニュー表示順序')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=17, verbose_name='部品コード')),
                ('update_user_code', models.CharField(max_length=10, null=True, verbose_name='更新者')),
                ('update_date', models.DateField(null=True, verbose_name='更新日')),
                ('create_user_code', models.CharField(max_length=10, verbose_name='作成者')),
                ('create_date', models.DateField(verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='PartAssy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField(verbose_name='部品版数ID')),
            ],
        ),
        migrations.CreateModel(
            name='PartElectricalParts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField(verbose_name='部品版数ID')),
                ('function', models.CharField(max_length=200, null=True, verbose_name='機能')),
                ('power_supply_system', models.CharField(choices=[('01', '単電源品'), ('02', 'マルチ電源品')], max_length=2, null=True, verbose_name='電源系統')),
                ('min_power_supply_voltage', models.CharField(max_length=50, null=True, verbose_name='電源電圧(MIN)[V]')),
                ('max_power_supply_voltage', models.CharField(max_length=50, null=True, verbose_name='電源電圧(MAX)[V]')),
                ('package_type', models.CharField(choices=[('01', 'DIP'), ('02', 'SOP(JEITA)'), ('03', 'other')], max_length=2, null=True, verbose_name='パッケージ')),
                ('temperture_type', models.CharField(max_length=2, null=True, verbose_name='温度区分')),
                ('operating_temperature', models.CharField(choices=[('01', 'Commercial'), ('02', 'Industrial'), ('03', 'Automotive'), ('04', 'Military'), ('05', 'other')], max_length=50, null=True, verbose_name='動作保証温度')),
                ('comment', models.CharField(max_length=4000, null=True, verbose_name='コメント')),
            ],
        ),
        migrations.CreateModel(
            name='PartPwb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField(verbose_name='部品版数ID')),
                ('layer_count', models.IntegerField(verbose_name='層数')),
                ('mounting_type', models.CharField(choices=[('01', '片面'), ('02', '両面')], max_length=2, verbose_name='実装タイプ')),
            ],
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_menu_code', models.CharField(max_length=50, verbose_name='サブメニューコード')),
                ('sub_menu_name', models.CharField(max_length=50, verbose_name='メニュー名称')),
                ('menu_seq', models.IntegerField(verbose_name='メニュー表示順序')),
                ('main_menu_code', models.ForeignKey(db_column='menu_code', on_delete=django.db.models.deletion.CASCADE, to='part_management.menu', verbose_name='メインメニューコード')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_item_number', models.CharField(max_length=17, verbose_name='販売品目コード')),
                ('sales_item_name', models.CharField(max_length=100, verbose_name='販売品目名称')),
                ('owner_contact', models.CharField(max_length=50, null=True, verbose_name='担当者連絡先')),
                ('update_user_code', models.CharField(max_length=10, null=True, verbose_name='更新者')),
                ('update_date', models.DateField(null=True, verbose_name='更新日')),
                ('create_user_code', models.CharField(max_length=10, verbose_name='作成者')),
                ('create_date', models.DateField(verbose_name='作成日')),
                ('eos', models.DateField(null=True, verbose_name='EOS')),
                ('owner_dept_code', models.ForeignKey(db_column='dept_code', on_delete=django.db.models.deletion.PROTECT, to='part_management.department', verbose_name='担当部門')),
                ('owner_user_code', models.ForeignKey(db_column='user_code', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='担当者')),
            ],
        ),
        migrations.CreateModel(
            name='PartVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField(verbose_name='版数')),
                ('part_name', models.CharField(max_length=100, verbose_name='部品名称')),
                ('part_type', models.CharField(choices=[('A', 'ASSY'), ('E', '電気電子部品'), ('p', 'プリント版')], max_length=1, verbose_name='品目種別')),
                ('eol', models.DateField(null=True, verbose_name='EOL')),
                ('update_user_code', models.CharField(max_length=10, null=True, verbose_name='更新者')),
                ('update_date', models.DateField(null=True, verbose_name='更新日')),
                ('create_user_code', models.CharField(max_length=10, verbose_name='作成者')),
                ('create_date', models.DateField(verbose_name='作成日')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='part_management.part', verbose_name='部品ID')),
            ],
        ),
        migrations.AddConstraint(
            model_name='part',
            constraint=models.UniqueConstraint(fields=('part_number',), name='unique_part_number'),
        ),
        migrations.AddField(
            model_name='user',
            name='dept_code',
            field=models.ForeignKey(db_column='dept_code', on_delete=django.db.models.deletion.PROTECT, to='part_management.department', verbose_name='規定組織コード'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='submenu',
            constraint=models.UniqueConstraint(fields=('main_menu_code', 'sub_menu_code'), name='unique_sub_menu'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('sales_item_number',), name='unique_sales_item_number'),
        ),
    ]
