# Python Kinwangji 
Python 皇極經世　堅皇極　元會運世推步  

A python package of **Huangji Jingshi** (皇極經世, Book of Supreme World Ordering Principles) by Shao Yong (邵雍).  
Python 實現北宋邵雍《皇極經世》數術系統，包含元會運世、節氣推算、聲音律呂、觀物內外篇相關計算。

邵雍（1011–1077），字堯夫，號康節，北宋五子之一，以先天易學與象數哲學聞名。  
《皇極經世》窮三十年觀天地之消長，建構宇宙大數：  
一元 = **129,600 年**（12會 × 30運 × 12世 × 30年）  
一元十二會、一會三十運、一運十二世、一世三十年，週而復始，推演古今治亂興亡。

本專案嘗試以現代Python重現部分核心算法，並提供互動介面，讓使用者可以輸入日期觀察「皇極」視角下的時空定位。

## 主要功能 Features

- 節氣（二十四節氣）精確計算（基於天文曆法）
- 元會運世時間框架換算
- 皇極經世大數週期定位（年 → 世 → 運 → 會 → 元）
- 聲音律品基礎對應（待擴充）
- Streamlit 互動網頁應用（選擇日期 → 顯示皇極時空坐標）

## 安裝 Installation

需要 Python 3.8+，建議使用虛擬環境。

```bash
# 基本依賴（天文計算使用 pyephem 或 skyfield）
pip install -r requirements.txt

# 或直接從 github 安裝（開發中）
pip install git+https://github.com/kentang2017/kinwangji.git
