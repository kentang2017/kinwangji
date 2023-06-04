import os, urllib
import streamlit as st
import pendulum as pdlm
import datetime, pytz
from contextlib import contextmanager, redirect_stdout
from sxtwl import fromSolar
from io import StringIO
import streamlit.components.v1 as components
from wanji import *

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write
        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        stdout.write = new_write
        yield

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/kentang2017/ichingshifa/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")
  
def kty(path):
    url = 'https://raw.githubusercontent.com/kentang2017/kinliuren/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

st.set_page_config(layout="wide",page_title="堅皇極-皇極經世排盤")
pan,update = st.tabs([' 排盤 ', ' 連結 '])
with st.sidebar:
    idate = st.text_input('輸入日期(如: 1997/8/8)', '')
    pp_time=st.time_input("時間",pdlm.now(tz='Asia/Shanghai').time())
    start = st.button('起盤')
 
with update:
    st.header('日誌')
    st.markdown(kty("update.md"))

with pan:
    st.header('堅皇極')
    st.text('暫時以明黃粵洲的皇極經世起盤公式起盤。')
    output2 = st.empty()
    with st_capture(output2.code):
        if start:
            p = str(idate).split("/")
            pp = str(pp_time).split(":")
            y = int(p[0])
            m = int(p[1])
            d = int(p[2])
            h = int(pp[0])
            min = int(pp[1])
            pan = display_pan(y,m,d,h,min)
            print(pan)
        else:
            now = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong'))
            ny = now.year
            nm = now.month
            nd = now.day
            nh = now.hour
            nmin = now.minute
            pan = display_pan(ny,nm,nd,nh,nmin)
            print(pan)

       
   
