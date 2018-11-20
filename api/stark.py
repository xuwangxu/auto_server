#-*- coding:utf-8 -*-
# author: Wang Xu
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render
from stark.service.stark import site,StarkConfig,get_choice_text,Option,StarkModelForm
from api import models

# 业务线管理的配置
class BusinessUnitConfig(StarkConfig):
    # 定制页面显示的列
    # def test_checkbox(self, row=None, header=False):
    #     if header:
    #         return "测试列"
    #     return 'alex - %s'%row.name

    # list_display = [StarkConfig.display_checkbox,'id','name',test_checkbox]
    list_display = [StarkConfig.display_checkbox,'id','name']
    # 定制模糊搜索
    search_list = ['name']
    # 排序
    order_by = ['-id',]
    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.BusinessUnit.objects.filter(id__in=pk_list).delete()

        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        return redirect('http://www.baidu.com')
        # 有返回值，

    multi_delete.text = '批量删除'
    action_list = [multi_delete,]

"""
http://127.0.0.1:8000/stark/api/businessunit/list/          BusinessUnitConfig.changelist_view
http://127.0.0.1:8000/stark/api/businessunit/add/           BusinessUnitConfig.add_view
http://127.0.0.1:8000/stark/api/businessunit/2/change/      BusinessUnitConfig.change_view
http://127.0.0.1:8000/stark/api/businessunit/1/del/         BusinessUnitConfig.delete_view
"""

#<= 将要处理Models类和该类操作的配置类打包成ModelConfigMapping对象，将对象在放入到_registry = []
site.register(models.BusinessUnit,BusinessUnitConfig)



# IDC管理
class IDCConfig(StarkConfig):
    list_display = ['name','floor',]
    search_list = ['name','floor']


"""
http://127.0.0.1:8000/stark/api/idc/list/          IDCConfig.changelist_view
http://127.0.0.1:8000/stark/api/idc/add/           IDCConfig.add_view
http://127.0.0.1:8000/stark/api/idc/2/change/      IDCConfig.change_view
http://127.0.0.1:8000/stark/api/idc/1/del/         IDCConfig.delete_view
"""

site.register(models.IDC, IDCConfig)

from django import forms
from stark.forms.widgets import DatePickerInput

# 主机管理
class ServerModelForm(StarkModelForm):
    class Meta:
        model = models.Server
        fields = "__all__"
        # exclude = ['sn','manufacturer','model']
        widgets = {
            'latest_date': DatePickerInput(attrs={'class':'date-picker'})
        }

class ServerConfig(StarkConfig):
    # def display_status(self, row=None, header=False):
    #     if header:
    #         return "状态"
    #     from django.utils.safestring import mark_safe
    #     data =  row.get_device_status_id_display()
    #     tpl = "<span style='color:green'>%s</span>"%data
    #     return mark_safe(tpl)

    def display_detail(self,row=None,header=False):
        if header:
            return "查看详细"
        return mark_safe("<a href='/stark/api/server/%s/detail/'>查看详细</a>"%row.id)

    def display_record(self,row=None,header=False):
        if header:
            return "变更记录"
        return mark_safe("<a href='/stark/api/server/%s/record/'>变更记录</a>"%row.id)

    list_display = [
                    # StarkConfig.display_checkbox,
                    'hostname',
                    'os_platform',
                    'os_version',
                    #display_status,
                    'business_unit',
                    get_choice_text('device_status_id','状态'),
                    display_detail,
                    display_record,
                    ]

    search_list = ['hostname','os_platform','business_unit__name',]

    list_filter = [
        # Option('business_unit',condition={'id__gt':3},is_choice=False,text_func=lambda x:x.name,value_func=lambda x:x.id),
        Option('device_status_id',is_choice=True,text_func=lambda x:x[1],value_func=lambda x:x[0],is_multi=True),
    ]

    # 自定义modelForm
    model_form_class = ServerModelForm

    action_list = [
        # StarkConfig.multi_delete
    ]

    def extra_url(self):
        """
        扩展URL
        :return:
        """
        from django.conf.urls import url
        patterns = [
            url(r'^(?P<nid>\d+)/detail/$',self.detail_view ),
            url(r'^(?P<nid>\d+)/record/$', self.record_view),
        ]
        return patterns

    def detail_view(self, request,nid):
        """
        详细页面的视图函数
        :param request:
        :param nid:
        :return:
        """
        nic_list = models.NIC.objects.filter(server_id=nid)
        memory_list = models.Memory.objects.filter(server_id=nid)
        disk_list = models.Disk.objects.filter(server_id=nid)
        context = {
            'nic_list':nic_list,
            'memory_list':memory_list,
            'disk_list':disk_list,
        }
        return  render(request,'server_detail.html',context)

    def record_view(self,request,nid):
        record_list = models.AssetRecord.objects.filter(server_id=nid)
        context = {'record_list':record_list}
        return  render(request,'server_record.html',context)


"""
http://127.0.0.1:8000/stark/server/idc/list/          StarkConfig.changelist_view
http://127.0.0.1:8000/stark/server/idc/add/           StarkConfig.add_view
http://127.0.0.1:8000/stark/server/idc/2/change/      StarkConfig.change_view
http://127.0.0.1:8000/stark/server/idc/1/del/         StarkConfig.delete_view
"""

site.register(models.Server,ServerConfig)