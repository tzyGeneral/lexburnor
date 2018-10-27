from django.contrib import admin
from .models import *

# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
    #制定在列表页中显示的字段们
    list_display = ('title','goodsType','price','spec')
    #指定右侧显示的过滤器
    list_filter = ('goodsType',)
    #指定在上访显示的搜索字段
    search_fields = ('title',)


admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)