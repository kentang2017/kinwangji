# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:44:35 2023

@author: kentang
"""
from ephem import Date
import sxtwl
from sxtwl import fromSolar, fromLunar
from bidict import bidict
from datetime import datetime, timedelta
import datetime
from itertools import cycle, repeat
import cn2an
from cn2an import an2cn
import os
import pickle
from jieqi import *

base = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(base, 'data.pkl')
data = pickle.load(open(path, "rb"))
sixtyfourgua = bidict(data.get("數字排六十四卦"))
gua_dist = data.get("易經卦爻詳解")
wangji_gua = dict(zip(range(1,61),"復,頤,屯,益,震,噬嗑,隨,無妄,明夷,賁,既濟,家人,豐,革,同人,臨,損,節,中孚,歸妹,睽,兌,履,泰,大畜,需,小畜,大壯,大有,夬,姤,大過,鼎,恆,巽,井,蠱,升,訟,困,未濟,解,渙,蒙,師,遯,咸,旅,小過,漸,蹇,艮,謙,否,萃,晉,豫,觀,比,剝".split(",")))
wangji_gua2 = dict(zip(range(1,65),"復,頤,屯,益,震,噬嗑,隨,無妄,明夷,賁,既濟,家人,豐,離,革,同人,臨,損,節,中孚,歸妹,睽,兌,履,泰,大畜,需,小畜,大壯,大有,夬,乾,姤,大過,鼎,恆,巽,井,蠱,升,訟,困,未濟,解,渙,坎,蒙,師,遯,咸,旅,小過,漸,蹇,艮,謙,否,萃,晉,豫,觀,比,剝,坤".split(",")))
#干支
tian_gan = '甲乙丙丁戊己庚辛壬癸'
di_zhi = '子丑寅卯辰巳午未申酉戌亥'
#換算干支
def gangzhi(year, month, day, hour, minute):
    if year == 0:
        return ["無效"]
    if year < 0:
        year = year + 1 
    if hour == 23:
        d = Date(round((Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day+1).zfill(2), str(0).zfill(2)))), 3))
    else:
        d = Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG,mTG,dTG,hTG = "{}{}".format(tian_gan[cdate.getYearGZ().tg], di_zhi[cdate.getYearGZ().dz]), "{}{}".format(tian_gan[cdate.getMonthGZ().tg],di_zhi[cdate.getMonthGZ().dz]), "{}{}".format(tian_gan[cdate.getDayGZ().tg], di_zhi[cdate.getDayGZ().dz]), "{}{}".format(tian_gan[cdate.getHourGZ(dd[3]).tg], di_zhi[cdate.getHourGZ(dd[3]).dz])
    if year < 1900:
        mTG1 = find_lunar_month(yTG).get(lunar_date_d(year, month, day).get("月"))
    else:
        mTG1 = mTG
    hTG1 = find_lunar_hour(dTG).get(hTG[1])
    gangzhi_minute = minutes_jiazi_d().get(str(hour)+":"+str(minute))
    return [yTG, mTG1, dTG, hTG1, gangzhi_minute]
#五虎遁，起正月
def find_lunar_month(year):
    fivetigers = {
    tuple(list('甲己')):'丙寅',
    tuple(list('乙庚')):'戊寅',
    tuple(list('丙辛')):'庚寅',
    tuple(list('丁壬')):'壬寅',
    tuple(list('戊癸')):'甲寅'
    }
    if multi_key_dict_get(fivetigers, year[0]) == None:
        result = multi_key_dict_get(fivetigers, year[1])
    else:
        result = multi_key_dict_get(fivetigers, year[0])
    return dict(zip(range(1,13),new_list(jiazi(), result)[:12]))

#五鼠遁，起子時
def find_lunar_hour(day):
    fiverats = {
    tuple(list('甲己')):'甲子',
    tuple(list('乙庚')):'丙子',
    tuple(list('丙辛')):'戊子',
    tuple(list('丁壬')):'庚子',
    tuple(list('戊癸')):'壬子'
    }
    if multi_key_dict_get(fiverats, day[0]) == None:
        result = multi_key_dict_get(fiverats, day[1])
    else:
        result = multi_key_dict_get(fiverats, day[0])
    return dict(zip(list(di_zhi), new_list(jiazi(), result)[:12]))

def repeat_list(n, thelist):
    return [repetition for i in thelist for repetition in repeat(i,n)]

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

#分干支
def minutes_jiazi_d():

    t = [f"{h}:{m}" for h in range(24) for m in range(60)]
    minutelist = dict(zip(t, cycle(repeat_list(2, jiazi()))))
    return minutelist
#農曆
def lunar_date_d(year, month, day):
    day = fromSolar(year, month, day)
    return {"年":day.getLunarYear(),  "月": day.getLunarMonth(), "日":day.getLunarDay()}

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))-1]

def closest1(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))+1]

def closest2(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
#旬
def liujiashun_dict():
    return dict(zip(list(map(lambda x: tuple(x), list(map(lambda x:new_list(jiazi(), x)[0:10] ,jiazi()[0::10])))), jiazi()[0::10]))

def jiazi():
    Gan, Zhi = '甲乙丙丁戊己庚辛壬癸', '子丑寅卯辰巳午未申酉戌亥'
    return list(map(lambda x: "{}{}".format(Gan[x % len(Gan)], Zhi[x % len(Zhi)]), list(range(60))))

def new_list(olist, o):
    a = olist.index(o)
    res1 = olist[a:] + olist[:a]
    return res1

def change(g, yao):
    y = {6: 5, 5: 4, 4: 3, 3: 2, 2: 1, 1: 0}.get(yao)
    if g[y] == "7":
        a = "8"
    if g[y] == "8":
        a = "7"
    return "".join([a if i == y else g[i] for i in range(len(g))])

def one2two(gua):
    if len(gua) == 1:
        return gua + "　"
    else:
        return gua

def generate_month_lists(year):
    month_lists = []
    for i in range(1, 13, 2):
        start = sxtwl.fromLunar(year, i, 1, True)
        end = sxtwl.fromLunar(year, min(i+1, 12), 31, True)
        start_date = datetime.datetime(start.getSolarYear(), start.getSolarMonth(), start.getSolarDay())
        end_date = datetime.datetime(end.getSolarYear(), end.getSolarMonth(), end.getSolarDay())
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date)
            current_date += datetime.timedelta(days=1)
        month_lists.append(date_list)
    return month_lists
    
def get_datelist(datelist):
    result = []
    for i in range(len(datelist) - 1):
        start_date = datetime.datetime.strptime(datelist[i], '%Y/%m/%d %H:%M:%S')
        end_date = datetime.datetime.strptime(datelist[i + 1], '%Y/%m/%d %H:%M:%S')
        dates_between = []
        current_date = start_date
        while current_date < end_date:
            dates_between.append(current_date)
            current_date += timedelta(days=1)
        result.append(dates_between)
    return result

def wanji_four_gua(year, month, day, hour, minute):
    j_q = jq(year, month, day, hour, minute)
    lmonth = lunar_date_d(year, month, day).get("月")
    yearlist = dict(zip(range(1,7), generate_month_lists(year))).get(multi_key_dict_get({(1, 2): 1, (3, 4): 2, (5, 6): 3, (7, 8): 4, (9, 10): 5, (11, 12): 6}, lmonth))
    fd = generate_month_lists(year)[0][0]
    fd1 = find_jq_date1(fd.year, fd.month, fd.day, fd.hour, fd.minute)
    spring = datetime.datetime.strptime( fd1.get("立春"), '%Y/%m/%d %H:%M:%S')
    cyear = lunar_date_d(year, month, day).get("年")
    if year == 0:
        year = 1
    ygz = gangzhi(year, month, day, hour, minute)[0]
    if year < 0:
        acum_year = 67017 + year + 1
    else:
        acum_year = 67017 + year #積年數
    hui  = acum_year // 10800 +1 #會
    yun = acum_year // 360 + 1  #運
    if year < 0:
        shi = acum_year // 30 + 2#世
    else:
        shi = acum_year // 30 + 1
    main_gua = wangji_gua.get(int(round((acum_year / 2160), 0)))#
    mys = list(sixtyfourgua.inverse[main_gua][0].replace("6","8").replace("9","7"))
    if yun % 6 == 0:
        yun_gua_yao = 6
    else:
        yun_gua_yao = yun % 6
    mys1 = change(mys, yun_gua_yao)
    yungua = multi_key_dict_get(sixtyfourgua, mys1)
    shi_yao = shi // 2 % 6  
    if shi_yao == 0:
        shi_yao = 6
    shis1 = change(mys1, shi_yao)
    list(wangji_gua.values())
    shigua = multi_key_dict_get(sixtyfourgua, change(mys1, shi_yao))
    shi_shun = dict(zip("甲子,甲戌,甲申,甲午,甲辰,甲寅".split(","),range(1,7)))
    shun_yao = shi_shun.get(multi_key_dict_get(liujiashun_dict(), ygz))
    shungua1 = change(shis1,shun_yao)
    shun_gua = multi_key_dict_get(sixtyfourgua, shungua1)
    jiazi_years = sorted([-56 - 60 * i for i in range(100)]+[4 + 60 * i for i in range(100)])
    if year < 0:
        close_jiazi_year = closest(jiazi_years, year)
    if year > 64:
        close_jiazi_year = closest(jiazi_years, year)
    if year - close_jiazi_year > 60:
        close_jiazi_year = closest(jiazi_years, year)
    if year < 64 and year > 0 :
        close_jiazi_year = closest2(jiazi_years, year)
    if year in jiazi_years:
        close_jiazi_year = jiazi_years[jiazi_years.index(year)]
    if year not in jiazi_years and year - close_jiazi_year > 60:
        close_jiazi_year = closest2(jiazi_years, year)
    yeargua = None
    try:
        if datetime.datetime(year, month, day, hour, minute) < spring:
            yeargua = dict(zip(list(range(close_jiazi_year, close_jiazi_year+60)), new_list(list(wangji_gua.values()), shigua))).get(cyear-1)
        else:
            yeargua = dict(zip(list(range(close_jiazi_year, close_jiazi_year+60)), new_list(list(wangji_gua.values()), shigua))).get(cyear)
    except ValueError:
        yeargua = dict(zip(list(range(close_jiazi_year, close_jiazi_year+60)), wangji_gua.values())).get(cyear)
    ygua = sixtyfourgua.inverse[yeargua][0]
    nygua = "".join([{"9":"7", "6":"8","7":"7", "8":"8"}.get(i) for i in ygua])
    firstmonthgua1 = {"7":"8", "8":"7"}.get(nygua[0]) + nygua[1:]
    secondmonthgua1 =  {"7":"8", "8":"7"}.get(firstmonthgua1[0]) +  {"7":"8", "8":"7"}.get(firstmonthgua1[1]) + firstmonthgua1[2:]
    thirdmonthgua1 =   secondmonthgua1[0] + {"7":"8", "8":"7"}.get(secondmonthgua1[1]) + {"7":"8", "8":"7"}.get(secondmonthgua1[2]) + secondmonthgua1[3:]
    forthmonthgua1 =   thirdmonthgua1[0] + thirdmonthgua1[1] + {"7":"8", "8":"7"}.get(thirdmonthgua1[2]) +  {"7":"8", "8":"7"}.get(thirdmonthgua1[3]) + thirdmonthgua1[4:]            
    fifthmonthgua1 =   forthmonthgua1[0] + forthmonthgua1[1] + forthmonthgua1[2] + {"7":"8", "8":"7"}.get(forthmonthgua1[3]) + {"7":"8", "8":"7"}.get(forthmonthgua1[4]) + forthmonthgua1[5]        
    sixthmonthgua1 =   fifthmonthgua1[0] + fifthmonthgua1[1] + fifthmonthgua1[2] + fifthmonthgua1[3] + {"7":"8", "8":"7"}.get(fifthmonthgua1[4]) +  {"7":"8", "8":"7"}.get(fifthmonthgua1[5])                 
    mlist = [firstmonthgua1,firstmonthgua1, secondmonthgua1,secondmonthgua1, thirdmonthgua1,thirdmonthgua1, forthmonthgua1,forthmonthgua1, fifthmonthgua1, fifthmonthgua1, sixthmonthgua1, sixthmonthgua1]
    mgua_list =  dict(zip(range(1,13),[multi_key_dict_get(sixtyfourgua, i) for i in mlist]))
    lmonth_yaos = dict(zip(range(1, 13),mlist)).get(1)
    final = generate_month_lists(year)[5][-1]

    middle_qi = [fd1.get(i) for i in "雨水,春分,穀雨,小滿,夏至,大暑,處暑,秋分,霜降,小雪,冬至,大寒".split(",")][0::2] + [final.strftime('%Y/%m/%d 0:00:00')] 
    #middle = [tuple("雨水","春分"),tuple("穀雨","小滿"),tuple("夏至","大暑"),tuple("處暑","秋分"),tuple("霜降","小雪"),tuple("冬至","大寒")]
    mgua = mgua_list.get(lmonth)
    new_gua_list = [sixtyfourgua.inverse[mgua][0], change(lmonth_yaos, 1), change(lmonth_yaos, 2), change(lmonth_yaos, 3), change(lmonth_yaos, 4), change(lmonth_yaos, 5)]
    
    daygua_list = [multi_key_dict_get(sixtyfourgua, i) for i in new_gua_list]
    #gualist = dict(zip(daygua_list,yearlist))
    ml = get_datelist(middle_qi)
    ml = [
    [dt.date() if isinstance(dt, datetime.datetime) else dt for dt in sublist]
    for sublist in ml
    ]
    gualist = {tuple(ml[0]): daygua_list[0],
           tuple(ml[1]): daygua_list[1],
           tuple(ml[2]): daygua_list[2],
           tuple(ml[3]): daygua_list[3],
           tuple(ml[4]): daygua_list[4],
           tuple(ml[5]): daygua_list[5]}
    #day_gua = multi_key_dict_get(gualist, datetime.date(year, month, day))
    
    day_gua = multi_key_dict_get( {
    ("雨水", "驚蟄","春分","清明"): daygua_list[0],
    ("穀雨", "立夏","小滿","芒種"): daygua_list[1],
    ("夏至", "小暑", "大暑","立秋"): daygua_list[2],
    ("處暑", "白露", "秋分","寒露"): daygua_list[3],
    ("霜降","立冬","小雪","大雪"): daygua_list[4],
    ("冬至", "小寒", "大寒","立春",): daygua_list[5]
    }, j_q)
    return {"會":hui, "運":yun, "世":shi, "運卦動爻":yun_gua_yao, "世卦動爻": shi_yao, "旬卦動爻":shun_yao ,"正卦":main_gua, "運卦":yungua, "世卦":shigua, "旬卦":shun_gua, "年卦":yeargua, "月卦":mgua, "日卦":day_gua}, spring 

def display_pan(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    a = "起卦時間︰{}年{}月{}日{}時{}分\n".format(year, month, day, hour, minute)
    b = "農曆︰{}{}月{}日\n".format(cn2an.transform(str(lunar_date_d(year, month, day).get("年"))+"年", "an2cn"), an2cn(lunar_date_d(year, month, day).get("月")), an2cn(lunar_date_d(year,month, day).get("日")))
    c = "干支︰{}年  {}月  {}日  {}時\n".format(gz[0], gz[1], gz[2], gz[3])
    j_q = jq(year, month, day, hour, minute)
    c0 = "節氣︰{} | 旺︰{} | 相︰{}\n".format(j_q, gong_wangzhuai(j_q)[1].get("旺"), gong_wangzhuai(j_q)[1].get("相"))
    guayaodict = {"6":"▅▅ ▅▅ X", "7":"▅▅▅▅▅  ", "8":"▅▅ ▅▅  ", "9":"▅▅▅▅▅ O"}
    wj = wanji_four_gua(year, month, day, hour, minute)
    g = "{}會    {}運   {}世\n\n".format(an2cn(wj.get("會")), an2cn(wj.get("運")), an2cn(wj.get("世")))
    mg = wj.get("正卦")
    mg1 = one2two(mg)
    mg_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[mg][0].replace("6","8").replace("9","7")]
    yg =  wj.get("運卦")
    yg1 =  one2two(yg)
    ygd =  wj.get("運卦動爻")
    yg_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[yg][0].replace("6","8").replace("9","7")]
    sg =  wj.get("世卦")
    sg1 =  one2two(sg)
    sgd = wj.get("世卦動爻")
    sg_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[sg][0].replace("6","8").replace("9","7")]
    shg =  wj.get("旬卦")
    shg1 =  one2two(shg)
    shd = wj.get("旬卦動爻")
    shg_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[shg][0].replace("6","8").replace("9","7")]
    yrg =  wj.get("年卦")
    yrg1 =  one2two(yrg)
    yrg_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[yrg][0].replace("6","8").replace("9","7")]
    month_g =  wj.get("月卦")
    month_g1 =  one2two(month_g)
    month_g_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[month_g][0].replace("6","8").replace("9","7")]
    day_g =  wj.get("日卦")
    day_g1 =  one2two(day_g)
    day_g_code = [guayaodict.get(i) for i in sixtyfourgua.inverse[day_g][0].replace("6","8").replace("9","7")]
    
    
    g1 = "   正卦            運卦            世卦             旬卦             年卦             月卦             日卦\n"
    gg = " 【{}】         【{}】         【{}】          【{}】          【{}】         【{}】         【{}】\n".format(mg1, yg1, sg1, shg1, yrg1, month_g1, day_g1)
    g2 = "  {}         {}         {}         {}         {}         {}         {}\n".format(mg_code[5], yg_code[5], sg_code[5], shg_code[5], yrg_code[5],month_g_code[5], day_g_code[5])
    g3 = "  {}         {}         {}         {}         {}         {}         {}\n".format(mg_code[4], yg_code[4], sg_code[4], shg_code[4], yrg_code[4],month_g_code[4], day_g_code[4])
    g4 = "  {}         {}         {}         {}         {}         {}         {}\n".format(mg_code[3], yg_code[3], sg_code[3], shg_code[3], yrg_code[3],month_g_code[3], day_g_code[3])
    g5 = "  {}         {}         {}         {}         {}         {}         {}\n".format(mg_code[2], yg_code[2], sg_code[2], shg_code[2], yrg_code[2],month_g_code[2], day_g_code[2])
    g6 = "  {}         {}         {}         {}         {}         {}         {}\n".format(mg_code[1], yg_code[1], sg_code[1], shg_code[1], yrg_code[1],month_g_code[1], day_g_code[1])
    g7 = "  {}         {}         {}         {}         {}         {}         {}\n\n".format(mg_code[0], yg_code[0], sg_code[0], shg_code[0], yrg_code[0],month_g_code[0], day_g_code[0])
    yrgd = "【"+ yrg +"】卦\n" +"".join([gua_dist.get(yrg).get(i)+"\n" for i in list(range(0,7))])
    return a+b+c+c0+g+g1+gg+g2+g3+g4+g5+g6+g7+yrgd



if __name__ == '__main__':
    #print( wanji_four_gua(2025,1,30,14,54))
    print( wanji_four_gua(2025,1,29,10,0))
