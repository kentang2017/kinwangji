import os
import urllib.request
import datetime

import streamlit as st
import pendulum as pdlm
import pytz

from kinwangji.wanji import display_pan, wanji_four_gua, one2two
from kinwangji.jieqi import jq, gong_wangzhuai

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------

_TEXTS = {
    "zh": {
        "page_title": "堅皇極 — 皇極經世排盤",
        "sidebar_title": "堅皇極",
        "sidebar_intro": (
            "**皇極經世**是北宋邵雍所創的象數易學體系，"
            "以元會運世的時間框架推演天地萬物之變化。\n\n"
            "本工具根據明黃粵洲的皇極經世起盤公式，"
            "將任意日期時間轉換為對應的卦象排盤。"
        ),
        "language": "🌐 Language / 語言",
        "date_time": "📅 日期時間選擇",
        "select_date": "選擇日期",
        "select_time": "⏰ 選擇時間",
        "hour": "時",
        "minute": "分",
        "tab_pan": "🔮 排盤",
        "tab_detail": "📋 詳細排盤",
        "tab_links": "🔗 連結",
        "header": "堅皇極 — 排盤結果",
        "subtitle": "暫時以明黃粵洲的皇極經世起盤公式起盤。",
        "datetime_label": "起卦時間",
        "gangzhi_label": "干支",
        "solar_term": "節氣",
        "prosperous": "旺",
        "supportive": "相",
        "hui": "會",
        "yun": "運",
        "shi": "世",
        "cycle_title": "📊 元會運世定位",
        "cycle_desc": "當前日期在皇極經世時間框架中的位置",
        "hui_desc": "一元 = 12會 (每會 10,800 年)",
        "yun_desc": "一會 = 30運 (每運 360 年)",
        "shi_desc": "一運 = 12世 (每世 30 年)",
        "hexagram_title": "🔮 卦象總覽",
        "main_gua": "正卦",
        "yun_gua": "運卦",
        "shi_gua": "世卦",
        "xun_gua": "旬卦",
        "year_gua": "年卦",
        "month_gua": "月卦",
        "day_gua": "日卦",
        "hour_gua": "時卦",
        "minute_gua": "分卦",
        "cosmic_gua": "⬆ 天道卦 (宏觀)",
        "temporal_gua": "⬇ 人事卦 (微觀)",
        "changing_line": "動爻",
        "full_board": "完整排盤文本",
        "links_header": "連結",
        "project_links": "📎 相關連結",
        "github_link": "GitHub 源碼",
        "pypi_link": "PyPI 頁面",
        "wiki_link": "維基百科：皇極經世",
        "image_caption": "皇極經世示意圖",
    },
    "en": {
        "page_title": "KinWangJi — Huangji Jingshi Divination",
        "sidebar_title": "KinWangJi",
        "sidebar_intro": (
            "**Huangji Jingshi** (皇極經世) is a numerological system "
            "created by Shao Yong (1011–1077) of the Northern Song dynasty.\n\n"
            "It uses yuan-hui-yun-shi cosmic cycles to map "
            "any date/time into a set of I Ching hexagrams."
        ),
        "language": "🌐 Language / 語言",
        "date_time": "📅 Date & Time",
        "select_date": "Select date",
        "select_time": "⏰ Select time",
        "hour": "Hour",
        "minute": "Min",
        "tab_pan": "🔮 Board",
        "tab_detail": "📋 Full Text",
        "tab_links": "🔗 Links",
        "header": "KinWangJi — Divination Result",
        "subtitle": "Based on Ming-dynasty Huang Yuezhou's formula.",
        "datetime_label": "Date / Time",
        "gangzhi_label": "Stems-Branches",
        "solar_term": "Solar Term",
        "prosperous": "Prosperous",
        "supportive": "Supportive",
        "hui": "Huì (會)",
        "yun": "Yùn (運)",
        "shi": "Shì (世)",
        "cycle_title": "📊 Cosmic Cycle Position",
        "cycle_desc": "Position within the Huangji Jingshi time framework",
        "hui_desc": "1 Yuán = 12 Huì (10,800 yr each)",
        "yun_desc": "1 Huì = 30 Yùn (360 yr each)",
        "shi_desc": "1 Yùn = 12 Shì (30 yr each)",
        "hexagram_title": "🔮 Hexagram Overview",
        "main_gua": "Main (正卦)",
        "yun_gua": "Yùn (運卦)",
        "shi_gua": "Shì (世卦)",
        "xun_gua": "Xún (旬卦)",
        "year_gua": "Year (年卦)",
        "month_gua": "Month (月卦)",
        "day_gua": "Day (日卦)",
        "hour_gua": "Hour (時卦)",
        "minute_gua": "Min (分卦)",
        "cosmic_gua": "⬆ Cosmic Hexagrams (macro)",
        "temporal_gua": "⬇ Temporal Hexagrams (micro)",
        "changing_line": "Changing line",
        "full_board": "Full Divination Board (text)",
        "links_header": "Links",
        "project_links": "📎 Related Links",
        "github_link": "GitHub Source",
        "pypi_link": "PyPI Page",
        "wiki_link": "Wikipedia: Huangji Jingshi",
        "image_caption": "Huangji Jingshi Diagram",
    },
}


def _t(key: str) -> str:
    """Return the translated text for *key* in the current language."""
    lang = st.session_state.get("lang", "zh")
    return _TEXTS[lang][key]


# ---------------------------------------------------------------------------
# Helper – fetch remote Markdown (used by the Links tab)
# ---------------------------------------------------------------------------

def _fetch_remote_md(url: str) -> str:
    """Fetch a remote Markdown file; return empty string on failure."""
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return response.read().decode("utf-8")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    layout="wide",
    page_title="堅皇極 — Huangji Jingshi",
    page_icon="☯",
)

# Initialise language in session state
if "lang" not in st.session_state:
    st.session_state["lang"] = "zh"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    # Language toggle
    lang_choice = st.selectbox(
        "🌐 Language / 語言",
        options=["中文", "English"],
        index=0 if st.session_state["lang"] == "zh" else 1,
    )
    st.session_state["lang"] = "zh" if lang_choice == "中文" else "en"

    st.divider()

    # Project image
    img_path = os.path.join(os.path.dirname(__file__), "pic", "kwj.png")
    if os.path.isfile(img_path):
        st.image(img_path, caption=_t("image_caption"), use_container_width=True)

    # Introduction
    st.subheader(_t("sidebar_title"))
    st.markdown(_t("sidebar_intro"))
    st.divider()

    # Date / time input
    now_shanghai = pdlm.now(tz="Asia/Shanghai")
    st.subheader(_t("date_time"))
    idate = st.date_input(
        _t("select_date"),
        now_shanghai.date(),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2100, 12, 31),
    )
    st.markdown(f"**{_t('select_time')}**")
    col1, col2 = st.columns(2)
    with col1:
        sel_hour = st.number_input(
            _t("hour"), min_value=0, max_value=23,
            value=now_shanghai.hour, step=1,
        )
    with col2:
        sel_minute = st.number_input(
            _t("minute"), min_value=0, max_value=59,
            value=now_shanghai.minute, step=1,
        )
    pp_time = datetime.time(int(sel_hour), int(sel_minute))

    st.divider()

    # Project links
    st.subheader(_t("project_links"))
    st.markdown(
        "- [🐙 GitHub](https://github.com/kentang2017/kinwangji)\n"
        "- [📦 PyPI](https://pypi.org/project/kinwangji/)\n"
        "- [📖 Wikipedia](https://zh.wikipedia.org/wiki/皇極經世)"
    )

# ---------------------------------------------------------------------------
# Compute results
# ---------------------------------------------------------------------------

y, m, d = idate.year, idate.month, idate.day
h, mi = pp_time.hour, pp_time.minute

try:
    result = wanji_four_gua(y, m, d, h, mi)
    pan_text = display_pan(y, m, d, h, mi)
    solar_term = jq(y, m, d, h, mi)
    wz = gong_wangzhuai(solar_term)
except ValueError:
    now = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong"))
    y, m, d, h, mi = now.year, now.month, now.day, now.hour, now.minute
    result = wanji_four_gua(y, m, d, h, mi)
    pan_text = display_pan(y, m, d, h, mi)
    solar_term = jq(y, m, d, h, mi)
    wz = gong_wangzhuai(solar_term)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_pan, tab_detail, tab_links = st.tabs(
    [_t("tab_pan"), _t("tab_detail"), _t("tab_links")]
)

# ---- Tab 1: Visual Board -------------------------------------------------
with tab_pan:
    st.header(_t("header"))
    st.caption(_t("subtitle"))

    # -- Basic info row (date, gangzhi, solar term) -------------------------
    info_cols = st.columns(3)
    with info_cols[0]:
        st.metric(_t("datetime_label"), f"{y}-{m:02d}-{d:02d}  {h:02d}:{mi:02d}")
    with info_cols[1]:
        gz = result["干支"]
        st.metric(_t("gangzhi_label"), "  ".join(gz))
    with info_cols[2]:
        # gong_wangzhuai returns (trigram_to_state, state_to_trigram)
        _, state_to_trigram = wz
        wang_str = state_to_trigram.get("旺", "")
        xiang_str = state_to_trigram.get("相", "")
        term_display = f"{solar_term}  ({_t('prosperous')}: {wang_str}, {_t('supportive')}: {xiang_str})"
        st.metric(_t("solar_term"), term_display)

    st.divider()

    # -- Yuan-Hui-Yun-Shi cycle visualization -------------------------------
    st.subheader(_t("cycle_title"))
    st.caption(_t("cycle_desc"))

    hui_val = result["會"]
    yun_val = result["運"]
    shi_val = result["世"]

    # Compute positions within their parent cycle
    hui_in_yuan = ((hui_val - 1) % 12) + 1       # 1–12
    yun_in_hui = ((yun_val - 1) % 30) + 1        # 1–30
    shi_in_yun = ((shi_val - 1) % 12) + 1         # 1–12

    cyc_cols = st.columns(3)
    with cyc_cols[0]:
        st.metric(_t("hui"), f"{hui_val}  ({hui_in_yuan}/12)")
        st.progress(hui_in_yuan / 12)
        st.caption(_t("hui_desc"))
    with cyc_cols[1]:
        st.metric(_t("yun"), f"{yun_val}  ({yun_in_hui}/30)")
        st.progress(yun_in_hui / 30)
        st.caption(_t("yun_desc"))
    with cyc_cols[2]:
        st.metric(_t("shi"), f"{shi_val}  ({shi_in_yun}/12)")
        st.progress(shi_in_yun / 12)
        st.caption(_t("shi_desc"))

    st.divider()

    # -- Hexagram overview --------------------------------------------------
    st.subheader(_t("hexagram_title"))

    # Cosmic-level hexagrams (macro)
    with st.expander(_t("cosmic_gua"), expanded=True):
        gcols = st.columns(4)
        gua_keys = [
            ("main_gua", "正卦", None),
            ("yun_gua", "運卦", "運卦動爻"),
            ("shi_gua", "世卦", "世卦動爻"),
            ("xun_gua", "旬卦", "旬卦動爻"),
        ]
        for col, (label_key, gua_key, line_key) in zip(gcols, gua_keys):
            with col:
                gua_name = one2two(result[gua_key])
                st.markdown(
                    f"<div style='text-align:center;'>"
                    f"<span style='font-size:2rem;'>☰</span><br>"
                    f"<b style='font-size:1.3rem;'>{gua_name}</b><br>"
                    f"<span style='color:gray;'>{_t(label_key)}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if line_key:
                    st.caption(f"{_t('changing_line')}: {result[line_key]}")

    # Temporal hexagrams (micro)
    with st.expander(_t("temporal_gua"), expanded=True):
        tcols = st.columns(5)
        temporal_keys = [
            ("year_gua", "年卦"),
            ("month_gua", "月卦"),
            ("day_gua", "日卦"),
            ("hour_gua", "時卦"),
            ("minute_gua", "分卦"),
        ]
        for col, (label_key, gua_key) in zip(tcols, temporal_keys):
            with col:
                gua_name = one2two(result[gua_key])
                st.markdown(
                    f"<div style='text-align:center;'>"
                    f"<span style='font-size:2rem;'>☷</span><br>"
                    f"<b style='font-size:1.3rem;'>{gua_name}</b><br>"
                    f"<span style='color:gray;'>{_t(label_key)}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

# ---- Tab 2: Full text board -----------------------------------------------
with tab_detail:
    st.subheader(_t("full_board"))
    st.code(pan_text, language=None)

# ---- Tab 3: Links ---------------------------------------------------------
with tab_links:
    st.header(_t("links_header"))
    content = _fetch_remote_md(
        "https://raw.githubusercontent.com/kentang2017/kinliuren/master/update.md"
    )
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("Unable to load remote content. Check your internet connection.")

