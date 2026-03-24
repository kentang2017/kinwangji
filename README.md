# Python Kinwangji 堅皇極經世

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package of **Huangji Jingshi** (皇極經世, Book of Supreme World Ordering Principles) by Shao Yong (邵雍).

Python 實現北宋邵雍《皇極經世》數術系統，包含元會運世、節氣推算、聲音律呂、觀物內外篇相關計算。

邵雍（1011–1077），字堯夫，號康節，北宋五子之一，以先天易學與象數哲學聞名。
《皇極經世》窮三十年觀天地之消長，建構宇宙大數：
一元 = **129,600 年**（12會 × 30運 × 12世 × 30年）
一元十二會、一會三十運、一運十二世、一世三十年，週而復始，推演古今治亂興亡。

本專案嘗試以現代 Python 重現部分核心算法，並提供互動介面，讓使用者可以輸入日期觀察「皇極」視角下的時空定位。

## 主要功能 Features

- 節氣（二十四節氣）精確計算（基於天文曆法）
- 元會運世時間框架換算
- 皇極經世大數週期定位（年 → 世 → 運 → 會 → 元）
- 聲音律呂基礎對應（待擴充）
- Streamlit 互動網頁應用（選擇日期 → 顯示皇極時空坐標）

## 安裝 Installation

需要 Python 3.8+，建議使用虛擬環境。

```bash
# 從 GitHub 安裝
pip install git+https://github.com/kentang2017/kinwangji.git

# 本地開發安裝（可編輯模式）
git clone https://github.com/kentang2017/kinwangji.git
cd kinwangji
pip install -e .

# 包含 Streamlit 應用依賴
pip install -e ".[app]"
```

## 使用方式 Usage

```python
from kinwangji import wanji_four_gua, display_pan, jq

# 取得某日的皇極經世卦象
result = wanji_four_gua(2025, 6, 15, 10, 30)
print(result)

# 取得節氣
solar_term = jq(2025, 6, 15, 10, 30)
print(solar_term)

# 顯示完整排盤
print(display_pan(2025, 6, 15, 10, 30))
```

## Streamlit 應用

```bash
pip install -e ".[app]"
streamlit run app.py
```

## 專案結構 Project Structure

```
kinwangji/
├── kinwangji/          # 主要套件
│   ├── __init__.py
│   ├── jieqi.py        # 節氣計算
│   ├── wanji.py        # 皇極經世核心算法
│   └── data/
│       └── data.pkl    # 卦象資料
├── examples/           # 使用範例
├── tests/              # 測試
├── app.py              # Streamlit 應用
├── pyproject.toml      # 專案配置
└── README.md
