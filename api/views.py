import json,hashlib,time
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from api import models
from api import service
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from utils.security import decrypt

class APIAuthView(APIView):
    def dispatch(self, request, *args, **kwargs):
        client_sign = request.GET.get('sign')  # <= 客户端签名
        client_ctime = int(request.GET.get('ctime'))  # <= 客户端时间

        server_time = int(time.time() * 1000)  # <= 服务端时间

        if server_time - client_ctime > 120000:
            return Response({'status': False, 'data': '你在路上的时间太久了'})

        if client_sign in SIGN_RECORD:
            return Response({'status': False, 'data': '签名已经被使用过了'})

        server_sign = gen_sign(client_ctime)

        if client_sign != server_sign:
            return Response({'status': False, 'data': '签名错误'})

        SIGN_RECORD[client_sign] = client_ctime
        return super().dispatch( request, *args, **kwargs)


class AssetView(APIAuthView):
    def get(self, requset, *args, **kwargs):
        host_list = ['c1.com', 'c2.com', 'c3.com']
        # return HttpResponse(json.dumps(host_list))
        return Response(host_list)

    def post(self, request, *args, **kwargs):
        # info = json.loads(request.body.decode('utf-8'))
        # print(info)
        # 获取请求体中的数据，解密
        body = decrypt(request._request.body)
        asset_info = json.loads(body.decode('utf-8'))


        result = {'status':True, 'data':None, 'error':None}

        print(asset_info) # json格式
        asset_type = asset_info.get('type')
        if asset_type == "create":


            server_dict = {}
            server_dict.update(asset_info['basic']['data'])
            server_dict.update(asset_info['cpu']['data'])
            server_dict.update(asset_info['board']['data'])

            server = models.Server.objects.create(**server_dict)
            # 2 硬盘
            disk_info = asset_info['disk']['data']
            for k,v in disk_info.items():
                print(k,v)
                v['server'] = server
                models.Disk.objects.create(**v)
            # 3 网卡
            nic_info = asset_info['nic']['data']
            for k,v in nic_info.items():
                print(k,v)
                v['name'] = k
                v['server'] = server
                models.NIC.objects.create(**v)
            # 4 内存
            memory_info = asset_info['memory']['data']
            for k,v in memory_info.items():
                print(k,v)
                v['server'] = server
                models.Memory.objects.create(**v)

        elif asset_type == "update":
            # 更新资产
            print('资产要更新了',asset_info)

            hostname = asset_info['basic']['data']['hostname']
            print(hostname)

            # 获取数据库已有的硬盘信息
            server = models.Server.objects.get(hostname=hostname)
            ################处理基本信息##################
            service.process_basic(asset_info,hostname)

            ############处理硬盘#############
            service.process_disk(asset_info,server)


            ############处理内存#############
            service.process_memory(asset_info,server)

            ############处理网卡#############
            service.process_nic(asset_info,server)


        elif asset_type == "host_update":
            hostname = asset_info['cert']
            # 获取数据库已有的硬盘信息
            server = models.Server.objects.get(hostname=hostname)

            service.process_basic(asset_info, hostname)
            service.process_disk(asset_info, server)
            service.process_memory(asset_info, server)
            service.process_nic(asset_info, server)


        result['data'] = asset_info['basic']['data']['hostname']

        return Response(result)

def gen_sign(ctime):
    val = '%s|%s' %(settings.URL_AUTH_KEY,ctime,)
    obj = hashlib.md5()
    obj.update(val.encode('utf-8'))
    return  obj.hexdigest()

SIGN_RECORD = {}


class TestView(APIAuthView):

    def post(self, request):
        return Response({'status': True, 'data': 666})


class OrmView(APIView):
    def get(self,request):



        info = {
            'slot': '0',
            'pd_type': 'SAS',
            'capacity': '279.396',
            'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'
        }

        msg_list = []
        for k,v in info.items():
            verbose_name = models.Disk._meta.get_field(k).verbose_name
            tpl = "%s:%s"%(verbose_name,v,)
            msg_list.append(tpl)

        content = ';'.join(msg_list)
        print(content)

        return Response('...')

def detail(request):
    return HttpResponse('详细页面')












