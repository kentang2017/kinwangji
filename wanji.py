# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:44:35 2023

@author: kentang
"""
from ephem import Date
from sxtwl import fromSolar
from bidict import bidict
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
wangji_gua = dict(zip(range(1,61),"復,頤,屯,益,震,噬嗑,隨,无妄,明夷,賁,既濟,家人,豐,革,同人,臨,損,節,中孚,歸妹,睽,兌,履,泰,大畜,需,小畜,大壯,大有,夬,姤,大過,鼎,恆,巽,井,蠱,升,訟,困,未濟,解,渙,蒙,師,遯,咸,旅,小過,漸,蹇,艮,謙,否,萃,晉,豫,觀,比,剝".split(",")))
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

def wanji_four_gua(year, month, day, hour, minute):
    ygz = gangzhi(year, month, day, hour, minute)[0]
    if year < 0:
        acum_year = 67017 + year + 1
    else:
        acum_year = 67017 + year #積年數
    hui  = acum_year // 10800 +1 #會
    yun = acum_year // 360 +1  #運
    shi = acum_year // 30 + 1 #世
    main_gua = wangji_gua.get(int(round((acum_year / 2160), 0)))#
    mys = list(sixtyfourgua.inverse[main_gua][0].replace("6","8").replace("9","7"))
    if yun % 6 == 0:
        yun_gua_yao = 6
    else:
        yun_gua_yao = yun % 6
    mys1 = change(mys, yun_gua_yao)
    yungua = multi_key_dict_get(sixtyfourgua, mys1)
    shi_yao = shi // 2 % 6  
    shis1 = change(mys1, shi_yao)
    shigua = multi_key_dict_get(sixtyfourgua, change(mys1, shi_yao))
    shi_shun = dict(zip("甲子,甲戌,甲申,甲午,甲辰,甲寅".split(","),range(1,7)))
    shun_yao = shi_shun.get(multi_key_dict_get(liujiashun_dict(), ygz))
    shungua1 = change(shis1,shun_yao)
    shun_gua = multi_key_dict_get(sixtyfourgua, shungua1)
    jiazi_years = [4 - 60 * i for i in range(52)]+[4 + 60 * i for i in range(52)]
    if year < 0:
        close_jiazi_year = closest1(jiazi_years, year)
    else:
        close_jiazi_year = closest(jiazi_years, year)
    yeargua = dict(zip(list(range(close_jiazi_year, close_jiazi_year+60)), new_list(list(wangji_gua.values()), shigua))).get(year)
    return {"會":hui, "運":yun, "世":shi, "運卦動爻":yun_gua_yao, "世卦動爻": shi_yao, "旬卦動爻":shun_yao ,"正卦":main_gua, "運卦":yungua, "世卦":shigua, "旬卦":shun_gua, "年卦":yeargua } 

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None


def display_pan(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    a = "起卦時間︰{}年{}月{}日{}時{}分\n".format(year, month, day, hour, minute)
    b = "農曆︰{}{}月{}日\n".format(cn2an.transform(str(year)+"年", "an2cn"), an2cn(lunar_date_d(year, month, day).get("月")), an2cn(lunar_date_d(year,month, day).get("日")))
    c = "干支︰{}年  {}月  {}日  {}時\n".format(gz[0], gz[1], gz[2], gz[3])
    j_q = jq(year, month, day, hour)
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
    g1 = "   正卦            運卦            世卦             旬卦             年卦\n"
    gg = " 【{}】         【{}】         【{}】         【{}】          【{}】\n".format(mg1, yg1, sg1, shg1, yrg1)
    g2 = " {}         {}         {}         {}         {}\n".format(mg_code[5], yg_code[5], sg_code[5], shg_code[5], yrg_code[5])
    g3 = " {}         {}         {}         {}         {}\n".format(mg_code[4], yg_code[4], sg_code[4], shg_code[4], yrg_code[4])
    g4 = " {}         {}         {}         {}         {}\n".format(mg_code[3], yg_code[3], sg_code[3], shg_code[3], yrg_code[3])
    g5 = " {}         {}         {}         {}         {}\n".format(mg_code[2], yg_code[2], sg_code[2], shg_code[2], yrg_code[2])
    g6 = " {}         {}         {}         {}         {}\n".format(mg_code[1], yg_code[1], sg_code[1], shg_code[1], yrg_code[1])
    g7 = " {}         {}         {}         {}         {}\n".format(mg_code[0], yg_code[0], sg_code[0], shg_code[0], yrg_code[0])
    yrgd = "【"+ yrg +"】卦\n" +"".join([gua_dist.get(yrg).get(i)+"\n" for i in list(range(0,6))])
    return a+b+c+c0+g+g1+gg+g2+g3+g4+g5+g6+g7+yrgd



if __name__ == '__main__':
    print( display_pan(2023,8,8,10,0))
