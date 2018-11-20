#-*- coding:utf-8 -*-
# author: Wang Xu
from api import models

def process_basic(asset_info,hostname):
    basic_dict = {}
    basic_dict.update(asset_info['basic']['data'])
    basic_dict.update(asset_info['cpu']['data'])
    basic_dict.update(asset_info['board']['data'])

    obj = models.Server.objects.filter(hostname=hostname).first()
    record_list = []
    for name,new_value in basic_dict.items():
        # print(name,new_value)
        if name in ["cpu_count","cpu_physical_count"]:
            old_value = int(getattr(obj, name))
        else:
            old_value = str(getattr(obj,name))
        if old_value != new_value:
            setattr(obj,name,new_value)
            msg = "[基本信息变更] 主机 %s: %s由%s 变更为%s"%(hostname,name,old_value,new_value)
            record_list.append(msg)
    obj.save()
    if record_list:
        server = models.Server.objects.get(hostname=hostname)
        models.AssetRecord.objects.create(server=server, content=';'.join(record_list))


    # for name,new_value in basic_dict:
    #     pass


    # models.Server.objects.filter(hostname=hostname).update(**basic_dict)

def process_disk(asset_info,server):
    # 1.1 获取数据库中的硬盘信息
    disk_queryset = models.Disk.objects.filter(server=server)
    disk_queryset_set = {row.slot for row in disk_queryset}

    # 1.2 最新汇报来的硬盘信息
    disk_info = asset_info['disk']['data']
    disk_info_set = set(disk_info)

    add_disk_slot_list = disk_info_set - disk_queryset_set

    del_disk_slot_list = disk_queryset_set - disk_info_set

    update_disk_slot_list = disk_info_set & disk_queryset_set

    # 更新

    for slot in update_disk_slot_list:
        # models.Disk.objects.filter(slot=slot, server=server).update(**disk_info[slot])
        obj = models.Disk.objects.filter(slot=slot, server=server).first()
        row_dict = disk_info[slot]
        record_list = []
        for name, new_value in row_dict.items():
            old_value = str(getattr(obj, name))
            if old_value != new_value:
                setattr(obj, name, new_value)
                verbose_name = models.Disk._meta.get_field(name).verbose_name
                msg = "【硬盘变更】槽位%s：%s由%s变更为%s" % (slot, verbose_name, old_value, new_value)
                record_list.append(msg)
        obj.save()
        if record_list:
            models.AssetRecord.objects.create(server=server, content=';'.join(record_list))

    # 删除
    models.Disk.objects.filter(server=server, slot__in=del_disk_slot_list).delete()
    if del_disk_slot_list:
        msg = "【硬盘变更】移除槽位%s上的硬盘"%(';'.join(del_disk_slot_list),)
        models.AssetRecord.objects.create(server=server,content=msg)

    # 添加
    for slot in add_disk_slot_list:
        row_dict = disk_info[slot]
        row_record_list = []
        for name,new_value in row_dict.items():
            verbose_name = models.Disk._meta.get_field(name).verbose_name
            tpl = "%s:%s"%(verbose_name,new_value,)
            row_record_list.append(tpl)

        msg = "【硬盘变更】槽位%s新增硬盘,硬盘信息：%s"%(slot,";".join(row_record_list),)
        models.AssetRecord.objects.create(server=server,content=msg)


        row_dict['server'] = server
        models.Disk.objects.create(**row_dict)

def process_nic(asset_info,server):
    # 3.1 获取数据库中的硬盘信息
    nic_queryset = models.NIC.objects.filter(server=server)
    nic_queryset_set = {row.name for row in nic_queryset}

    # 3.2 最新汇报来的硬盘信息
    nic_info = asset_info['nic']['data']
    nic_info_set = set(nic_info)

    add_nic_name_list = nic_info_set - nic_queryset_set

    del_nic_name_list = nic_queryset_set - nic_info_set

    update_nic_name_list = nic_info_set & nic_queryset_set


    # 更新
    for name in update_nic_name_list:
        # models.NIC.objects.filter(name=name, server=server).update(**nic_info[name])
        obj = models.NIC.objects.filter(name=name,server=server).first()
        nic_dict = nic_info[name]
        record_list = []
        for name, new_value in nic_dict.items():
            if name == "up":
                old_value = getattr(obj, name)
                print(type(old_value))
                print(type(new_value))
            else:
                old_value = str(getattr(obj, name))


            if old_value != new_value:
                setattr(obj,name,new_value)
                verbose_name = models.NIC._meta.get_field(name).verbose_name
                msg = "【网卡变更】网卡%s：%s由%s变更为%s" % (name, verbose_name, old_value, new_value)
                record_list.append(msg)
        obj.save()
        if record_list:
            models.AssetRecord.objects.create(server=server, content=';'.join(record_list))


    # 删除
    models.NIC.objects.filter(server=server, name__in=del_nic_name_list).delete()
    if del_nic_name_list:
        msg = "【网卡变更】移除网卡%s"%(';'.join(del_nic_name_list),)
        models.AssetRecord.objects.create(server=server,content=msg)

    # 添加
    for name in add_nic_name_list:
        row_dict = nic_info[name]
        row_record_list = []
        row_dict['name'] = name
        for name,new_value in row_dict.items():
            verbose_name = models.NIC._meta.get_field(name).verbose_name
            tpl = "%s:%s"%(verbose_name,new_value,)
            row_record_list.append(tpl)

        msg = "【网卡变更】新增网卡%s,网卡信息：%s"%(row_dict['name'],";".join(row_record_list),)
        models.AssetRecord.objects.create(server=server,content=msg)

        row_dict['server'] = server
        models.NIC.objects.create(**row_dict)

def process_memory(asset_info,server):
    # 2.1 获取数据库中的内存信息
    memory_queryset = models.Memory.objects.filter(server=server)
    memory_queryset_set = {row.slot for row in memory_queryset}

    # 2.2 最新汇报来的内存信息
    memory_info = asset_info['memory']['data']
    memory_info_set = set(memory_info)

    add_memory_slot_list = memory_info_set - memory_queryset_set

    del_memory_slot_list = memory_queryset_set - memory_info_set

    update_memory_slot_list = memory_info_set & memory_queryset_set

    # 更新
    for slot in update_memory_slot_list:
        obj = models.Memory.objects.filter(slot=slot,server=server).first()
        row_dict = memory_info[slot]
        record_list = []
        for name, new_value in row_dict.items():
            if name == 'capacity':
                old_value = getattr(obj, name)
            else:
                old_value = str(getattr(obj,name))
            if old_value != new_value:
                setattr(obj,name,new_value)
                verbose_name = models.Memory._meta.get_field(name).verbose_name
                msg = "【内存变更】槽位%s：%s由%s变更为%s" % (slot, verbose_name, old_value, new_value)
                record_list.append(msg)
        obj.save()
        if record_list:
            models.AssetRecord.objects.create(server=server, content=';'.join(record_list))

        # models.Memory.objects.filter(slot=slot, server=server).update(**memory_info[slot])
    # 删除
    models.Memory.objects.filter(server=server, slot__in=del_memory_slot_list).delete()
    if del_memory_slot_list:
        msg = "【内存变更】移除内存%s"%(';'.join(del_memory_slot_list),)
        models.AssetRecord.objects.create(server=server,content=msg)

    # 添加

    for slot in add_memory_slot_list:
        row_dict = memory_info[slot]
        row_record_list = []
        for name,new_value in row_dict.items():
            verbose_name = models.Memory._meta.get_field(name).verbose_name
            tpl = "%s:%s"%(verbose_name,new_value,)
            row_record_list.append(tpl)

        msg = "【内存变更】槽位%s新增内存,内存信息：%s"%(slot,";".join(row_record_list),)
        models.AssetRecord.objects.create(server=server,content=msg)


        row_dict['server'] = server
        models.Memory.objects.create(**row_dict)

