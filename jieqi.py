# -*- coding: utf-8 -*-
"""
Created on Tue May  9 20:32:01 2023

@author: kentang
"""

import re
from math import pi
from ephem import Sun, Date, Ecliptic, Equatorial
import ephem

jieqi_name = re.findall('..', '春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水驚蟄')

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def new_list(olist, o):
    a = olist.index(o)
    res1 = olist[a:] + olist[:a]
    return res1

def ecliptic_lon(jd_utc):
    return Ecliptic(Equatorial(Sun(jd_utc).ra,Sun(jd_utc).dec,epoch=jd_utc)).lon

def sta(jd_num):
    return int(ecliptic_lon(jd_num)*180.0/pi/15)

def iteration(jd,sta):
    s1=sta(jd)
    s0=s1
    dt=1.0
    while True:
        jd+=dt
        s=sta(jd)
        if s0!=s:
            s0=s
            dt=-dt/2
        if abs(dt)<0.0000001 and s!=s1:
            break
    return jd

def find_jq_date(year, month, day, hour, jie_qi):
    jd_format=Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    e_1=ecliptic_lon(jd_format)
    n_1=int(e_1*180.0/pi/15)+1
    dzlist = []
    for i in range(24):
        if n_1>=24:
            n_1-=24
        jd_d=iteration(jd_format)
        d=Date(jd_d+1/3).tuple()
        bb_1 = {jieqi_name[n_1]: Date("{}/{}/{} {}:{}:00.00".format(str(d[0]).zfill(4), str(d[1]).zfill(2), str(d[2]).zfill(2), str(d[3]).zfill(2) , str(d[4]).zfill(2)))}
        n_1+=1
        dzlist.append(bb_1)
    return list(dzlist[list(map(lambda i:list(i.keys())[0], dzlist)).index(jie_qi)].values())[0]

def find_jq_date1(year, month, day, hour, minute):
    current = "{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2))
    changets = Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)))
    jd=Date(changets - 24 * ephem.hour *30)
    e_1=ecliptic_lon(jd)
    result1 = {}
    result = []
    e=ecliptic_lon(jd)
    n=int(e*180.0/pi/15)+1
    for i in range(24):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        dt = "{}/{}/{} {}:{}:00.00".format(d[0],d[1],d[2],str(d[3]).zfill(2),str(d[4]).zfill(2)).split(".")[0]
        time_info = {  jieqi_name[n]:dt}
        n+=1    
        result.append(time_info)
    for i in result[1:]:
        result1.update(i)
    #j = [list(i.keys())[0] for i in result]
    return result1


def gong_wangzhuai(j_q):
    wangzhuai = list("旺相胎沒死囚休廢")
    #wangzhuai_num = [3,4,9,2,7,6,1,8]
    wangzhuai_num = list("震巽離坤兌乾坎艮")
    wangzhuai_jieqi = {('春分','清明','穀雨'):'春分',
                        ('立夏','小滿','芒種'):'立夏',
                        ('夏至','小暑','大暑'):'夏至',
                        ('立秋','處暑','白露'):'立秋',
                        ('秋分','寒露','霜降'):'秋分',
                        ('立冬','小雪','大雪'):'立冬',
                        ('冬至','小寒','大寒'):'冬至',
                        ('立春','雨水','驚蟄'):'立春'}
    r1 = dict(zip(new_list(wangzhuai_num, dict(zip(jieqi_name[0::3],wangzhuai_num )).get(multi_key_dict_get(wangzhuai_jieqi, j_q))), wangzhuai))
    r2 = {v: k for k, v in r1.items()}
    return r1, r2


def xzdistance(year, month, day, hour):
    return int(find_jq_date(year, month, day, hour, "夏至") -  Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2))))

def distancejq(year, month, day, hour, jq):
    return int( Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2))) - find_jq_date(year-1, month, day, hour, jq) )

def fjqs(year, month, day, hour):
    jd_format = Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    n= int(ecliptic_lon(jd_format)*180.0/pi/15)+1
    c = []
    for i in range(1):
        if n>=24:
            n-=24
        d = Date(jd_format+1/3).tuple()
        c.append([jieqi_name[n], Date("{}/{}/{} {}:{}:00.00".format(str(d[0]).zfill(4), str(d[1]).zfill(2), str(d[2]).zfill(2), str(d[3]).zfill(2) , str(d[4]).zfill(2)))])
    return c[0]

def jq(year, month, day, hour, minute):#从当前时间开始连续输出未来n个节气的时间
    #current =  datetime.strptime("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)), '%Y/%m/%d %H:%M:%S')
    current = Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)))
    changets = Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)))
    jd=Date(changets - 24 * ephem.hour *30)
    #jd = Date("{}/{}/{} {}:{}:00.00".format(str(b.year).zfill(4), str(b.month).zfill(2), str(b.day).zfill(2), str(b.hour).zfill(2), str(b.minute).zfill(2)  ))
    result = []
    e=ecliptic_lon(jd)
    n=int(e*180.0/pi/15)+1
    for i in range(3):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        dt = Date("{}/{}/{} {}:{}:00.00".format(d[0],d[1],d[2],d[3],d[4]).split(".")[0])
        time_info = {  dt:jieqi_name[n]}
        n+=1    
        result.append(time_info)
    j = [list(i.keys())[0] for i in result]
    if current > j[0] and current > j[1] and current > j[2]:
        return list(result[2].values())[0]
    if current > j[0] and current > j[1] and current <= j[2]:
        return list(result[1].values())[0]
    if current >= j[1] and current < j[2]:
        return list(result[1].values())[0]
    if current < j[1] and current < j[2]:
        return list(result[0].values())[0]
