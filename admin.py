from django.contrib import admin

from .models import (
    Department,
    History,
    Menu,
    Part,
    PartAssy,
    PartElectricalParts,
    PartPwb,
    PartVersion,
    Product,
    SubMenu,
    User,
)

# admin管理サイトで編集できるモデルを追加する

admin.site.register(Menu)
admin.site.register(SubMenu)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Product)
admin.site.register(Part)
admin.site.register(PartVersion)
admin.site.register(PartAssy)
admin.site.register(PartElectricalParts)
admin.site.register(PartPwb)
admin.site.register(History)
