# ============================================================================================================
# LIBRARIES
# ============================================================================================================

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================================================================
# LOAD DATA
# ============================================================================================================

from data_source import get_fred_rate
from data_source import get_dxy
from data_source import get_us10y
from data_source import get_pmi

# ============================================================================================================
# STREAMLIT CONFIG
# ============================================================================================================

st.set_page_config(
    page_title="Investment Framework",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Top Down Investment Dashboard")
st.caption("Macro Indicators")
st.divider()

# ============================================================================================================
# HELPER FUNCTION
# ============================================================================================================

def get_trend(change):
    """Return trend text based on value change."""
    if change > 0:
        return "↑ Uptrend"
    elif change < 0:
        return "↓ Downtrend"
    else:
        return "↔️ Sideways"

def get_latest_metric(data):
    "Return Current Value, Previous Value, and Change"
    current = float(data.iloc[-1])
    previous = float(data.iloc[-2])
    change = current - previous
    return current, previous, change

# ============================================================================================================
# FED RATE
# ============================================================================================================

st.subheader("🏦 Fed Rate")

fed_rate = get_fred_rate()

current_rate, previous_rate, rate_change = get_latest_metric(fed_rate)
peak_rate = fed_rate.max()

rate_trend = get_trend(rate_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Fed-Rate",
        f"{current_rate:.2f}%"
    )

with col2:
    st.metric(
        "Peak Fed-Rate (10Y)",
        f"{peak_rate:.2f}%"
    )

with col3:
    st.metric(
        "Last Change",
        f"{rate_change:.2f}%"
    )

with col4:
    st.metric(
        "Trend",
        rate_trend
    )

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=fed_rate.index,
        y=fed_rate,
        mode="lines",
        name="Fed Rate"
    )
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Rate (%)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Current Assessment")
if rate_change<0:
    st.success(
        """
        ### Likuiditas Global Mulai Membaik

        The Federal Reserve mulai menurunkan suku bunga acuannya. Penurunan suku bunga umumnya meningkatkan likuiditas global dan menurunkan biaya pendanaan, sehingga mendorong investor kembali ke aset yang memiliki risiko lebih tinggi.

        **Potensi Dampak ke Pasar:**
        - Arus modal berpotensi kembali ke Emerging Market.
        - Rupiah cenderung lebih stabil atau menguat.
        - IHSG berpotensi memperoleh sentimen positif.
        - Sektor teknologi dan saham dengan pertumbuhan tinggi biasanya lebih diuntungkan.
        """
    )
elif rate_change>0:
    st.warning(
        """
        ### Likuiditas Global Semakin Ketat

        The Federal Reserve masih melanjutkan kebijakan pengetatan moneter melalui kenaikan suku bunga. Kondisi ini meningkatkan biaya pinjaman dan membuat aset berdenominasi Dollar menjadi lebih menarik.

        **Potensi Dampak ke Pasar:**
        - Tekanan terhadap pasar saham global.
        - Arus modal berpotensi keluar dari Emerging Market.
        - Rupiah dapat mengalami pelemahan.
        - IHSG berpotensi bergerak lebih defensif.
        """
    )
else:
    st.info(
        """
        ### Pasar Menunggu Arah Kebijakan Berikutnya

        The Federal Reserve mempertahankan suku bunga acuannya. Pasar saat ini masih menunggu data ekonomi berikutnya sebelum menentukan ekspektasi terhadap perubahan kebijakan selanjutnya.

        **Fokus Investor Saat Ini:**
        - Data Inflasi Amerika Serikat.
        - Data Tenaga Kerja (Non-Farm Payroll).
        - Pernyataan terbaru dari The Federal Reserve.
        """
    )

st.caption("Source: Federal Reserve Economic Data (FRED)")

# ============================================================================================================
# DXY
# ============================================================================================================

st.divider()
st.subheader("💵 US Dollar Index (DXY)")

dxy_close = get_dxy()

current_dxy, previous_dxy, dxy_change = get_latest_metric(dxy_close)
peak_dxy = float(dxy_close.max())

dxy_trend = get_trend(dxy_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current DXY",
        f"{current_dxy:.2f}"
    )

with col2:
    st.metric(
        "Peak DXY (5Y)",
        f"{peak_dxy:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{dxy_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        dxy_trend
    )

fig_dxy = go.Figure()

fig_dxy.add_trace(
    go.Scatter(
        x=dxy_close.index,
        y=dxy_close,
        mode="lines",
        name="DXY"
    )
)

fig_dxy.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="DXY Index",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_dxy,
    use_container_width=True
)

st.subheader("Current Assessment")
if dxy_change < 0:
    st.success(
        """
        ### Tekanan Dollar Mulai Berkurang

        Pelemahan Dollar AS menunjukkan tekanan terhadap mata uang negara berkembang mulai mereda. Kondisi ini juga biasanya memberikan dukungan terhadap harga komoditas yang diperdagangkan dalam Dollar.

        **Potensi Dampak ke Pasar*:*
        - Positif bagi Emerging Market.
        - Rupiah berpotensi menguat.
        - Harga komoditas memiliki peluang naik.
        - Mendukung sektor pertambangan dan energi.
        """
    )
elif dxy_change > 0:
    st.warning(
        """
        ### Dollar AS Semakin Dominan

        Penguatan Dollar menunjukkan investor lebih memilih aset yang dianggap aman. Kondisi ini biasanya menekan harga komoditas dan meningkatkan tekanan terhadap negara berkembang.

        **Potensi Dampak ke Pasar:**
        - Tekanan terhadap harga komoditas.
        - Rupiah berpotensi melemah.
        - Arus modal dapat berpindah ke Amerika Serikat.
        - Sentimen pasar cenderung lebih berhati-hati.
        """
    )

else:
    st.info(
        """
        ### Dollar Bergerak Stabil

        Pergerakan Dollar relatif tidak banyak berubah. Pasar masih menunggu katalis baru yang dapat menentukan arah berikutnya.

        **Fokus Investor Saat Ini:**
        - Inflasi Amerika Serikat.
        - Kebijakan The Federal Reserve.
        - Perkembangan ekonomi global.
        """)

st.caption("Source: Yahoo Finance (yfinance)")

# ============================================================================================================
# US 10Y
# ============================================================================================================

st.divider()
st.subheader("📜 US 10Y Treasury Yield")

us10y = get_us10y()

current_us10y, previous_us10y, us10y_change = get_latest_metric(us10y)
peak_us10y = float(us10y.max())

us10y_trend = get_trend(us10y_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current US10Y",
        f"{current_us10y:.2f}%"
    )


with col2:
    st.metric(
        "Peak US10Y (10Y)",
        f"{peak_us10y:.2f}%"
    )

with col3:
    st.metric(
        "Last Change",
        f"{us10y_change:.2f}%"
    )

with col4:
    st.metric(
        "Trend",
        us10y_trend
    )

fig_us10y = go.Figure()

fig_us10y.add_trace(
    go.Scatter(
        x=us10y.index,
        y=us10y,
        mode="lines",
        name="US10Y"
    )
)

fig_us10y.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Yield (%)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_us10y,
    use_container_width=True
)

st.subheader("Current Assessment")
if us10y_change < 0:
    st.success(
        """
        ### Minat terhadap Aset Berisiko Mulai Meningkat

        Penurunan imbal hasil obligasi pemerintah Amerika menunjukkan tekanan di pasar obligasi mulai mereda. Investor biasanya mulai kembali mempertimbangkan aset yang memiliki potensi imbal hasil lebih tinggi.

        **Potensi Dampak ke Pasar:**
        - Positif bagi pasar saham global.
        - Mendukung Emerging Market.
        - Biaya pendanaan perusahaan menjadi lebih rendah.
        """
    )
elif us10y_change > 0:
    st.warning(
        """
        ### Obligasi Amerika Semakin Menarik

        Kenaikan imbal hasil obligasi meningkatkan daya tarik aset pendapatan tetap dibandingkan saham. Investor cenderung lebih berhati-hati terhadap aset berisiko.

        **Potensi Dampak ke Pasar:**
        - Tekanan terhadap valuasi saham.
        - Arus dana menuju obligasi Amerika.
        - Meningkatkan biaya pendanaan secara global.
        """
    )
else:
    st.info(
        """
        ### Pasar Obligasi Bergerak Seimbang

        Pergerakan US Treasury Yield relatif stabil. Investor masih menunggu data ekonomi yang dapat memberikan arah baru terhadap pasar obligasi.

        **Fokus Investor Saat Ini:**
        - Inflasi.
        - Pertumbuhan ekonomi.
        - Kebijakan suku bunga The Federal Reserve.
        """
    )

st.caption("Source: Federal Reserve Economic Data (FRED)")

# ============================================================================================================
# China PMI
# ============================================================================================================

st.divider()
st.subheader("🏭 China Manufacturing PMI")

china_pmi = get_pmi("China")

current_china_pmi, prev_china_pmi, china_pmi_change = get_latest_metric(china_pmi["Value"])

if current_china_pmi > 50:
    status = "🟢 Expansion"
elif current_china_pmi < 50:
    status = "🔴 Contraction"
else:
    status = "🟡 Neutral"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current PMI",
        current_china_pmi
    )

with col2:
    st.metric(
        "Previous PMI",
        prev_china_pmi
    )

with col3:
    st.metric(
        "Monthly Change",
        f"{china_pmi_change:.2f}"
    )

with col4:
    st.metric(
        "Status",
        status
    )

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=china_pmi["Date"],
        y=china_pmi["Value"],
        mode="lines",
        name="China PMI"
    )
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="PMI Value",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

china_pmi["Date"] = pd.to_datetime(china_pmi["Date"])
fig.update_xaxes(
    dtick="M1",
    tickformat="%b %Y",
    tickangle=0
)

fig.add_hline(
    y=50,
    line_dash="dash",
    line_color="yellow",
    annotation_text="PMI = 50",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Current Assessment")

if current_china_pmi > 50:
    st.success(
        """
        ### Aktivitas Manufaktur China Sedang Bertumbuh

        PMI berada di atas level 50, yang menunjukkan aktivitas manufaktur sedang mengalami ekspansi. Peningkatan aktivitas pabrik biasanya diikuti oleh kenaikan produksi, pesanan baru, dan kebutuhan bahan baku.

        **Potensi Dampak ke Pasar:**
        - Permintaan logam industri berpotensi meningkat.
        - Positif bagi sektor pertambangan.
        - Mendukung harga Copper, Iron Ore, Nickel, dan komoditas industri lainnya.
        - Memberikan sentimen positif bagi negara pengekspor komoditas, termasuk Indonesia.
        """
    )
elif current_china_pmi < 50:
    st.warning(
        """
        ### Aktivitas Manufaktur China Mulai Melambat

        PMI berada di bawah level 50, yang mengindikasikan sektor manufaktur sedang mengalami kontraksi. Penurunan aktivitas produksi biasanya diikuti oleh melemahnya permintaan bahan baku dan aktivitas industri.

        **Potensi Dampak ke Pasar:**
        - Permintaan komoditas industri berpotensi menurun.
        - Memberikan tekanan pada sektor pertambangan.
        - Harga logam industri berpotensi melemah.
        - Sentimen terhadap negara pengekspor komoditas cenderung negatif.
        """
    )
else:
    st.info(
        """
        ### Aktivitas Manufaktur Berada di Titik Keseimbangan

        PMI berada tepat di level 50, yang menunjukkan aktivitas manufaktur belum menunjukkan ekspansi maupun kontraksi secara signifikan. Pasar masih menunggu data bulan berikutnya untuk mengonfirmasi arah tren.

        **Fokus Investor Saat Ini:**
        - Perkembangan pesanan baru.
        - Kebijakan stimulus pemerintah China.
        - Permintaan ekspor dan konsumsi domestik.
        """
    )

st.caption("Source: National Bureau of Statistics (NBS)")


# ============================================================================================================
# US PMI
# ============================================================================================================

st.divider()
st.subheader("🏭 US Manufacturing PMI")

us_pmi = get_pmi("US")

us_pmi["Date"] = pd.to_datetime(us_pmi["Date"])

current_us_pmi, prev_us_pmi, us_pmi_change = get_latest_metric(us_pmi["Value"])

if current_us_pmi > 50:
    status = "🟢 Expansion"
elif current_us_pmi < 50:
    status = "🔴 Contraction"
else:
    status = "🟡 Neutral"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current PMI",
        current_us_pmi
    )

with col2:
    st.metric(
        "Previous PMI",
        prev_us_pmi
    )

with col3:
    st.metric(
        "Monthly Change",
        f"{us_pmi_change:.2f}"
    )

with col4:
    st.metric(
        "Status",
        status
    )

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=us_pmi["Date"],
        y=us_pmi["Value"],
        mode="lines",
        name="US PMI"
    )
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="PMI Value",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

fig.update_xaxes(
    dtick="M1",
    tickformat="%b %Y",
    tickangle=0
)

fig.add_hline(
    y=50,
    line_dash="dash",
    line_color="yellow",
    annotation_text="PMI = 50",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Current Assessment")

if current_us_pmi > 50:
    st.success(
        """
        ### Aktivitas Manufaktur Amerika Sedang Bertumbuh

        PMI berada di atas level 50, yang menunjukkan sektor manufaktur Amerika sedang mengalami ekspansi. Peningkatan aktivitas ini mencerminkan pertumbuhan produksi, pesanan baru, dan optimisme pelaku industri terhadap kondisi ekonomi.

        **Potensi Dampak ke Pasar:**
        - Mengindikasikan pertumbuhan ekonomi Amerika yang masih kuat.
        - Meningkatkan kepercayaan investor terhadap aktivitas bisnis.
        - Berpotensi mendukung kinerja pasar saham apabila pertumbuhan tetap terkendali.
        - Perlu diwaspadai apabila ekspansi terlalu kuat karena dapat meningkatkan tekanan inflasi dan memengaruhi kebijakan suku bunga The Fed.
        """
    )
elif current_us_pmi < 50:
    st.warning(
        """
        ### Aktivitas Manufaktur Amerika Mulai Melambat

        PMI berada di bawah level 50, yang menunjukkan sektor manufaktur sedang mengalami kontraksi. Penurunan aktivitas ini dapat mengindikasikan melemahnya permintaan, berkurangnya produksi, serta meningkatnya kehati-hatian pelaku usaha.

        **Potensi Dampak ke Pasar:**
        - Mengindikasikan perlambatan pertumbuhan ekonomi Amerika.
        - Menekan sentimen terhadap pasar saham apabila kontraksi berlangsung berkelanjutan.
        - Dapat mengurangi tekanan inflasi sehingga membuka peluang pelonggaran kebijakan moneter di masa mendatang.
        - Investor perlu memantau data ekonomi lainnya untuk memastikan apakah perlambatan bersifat sementara atau mulai membentuk tren yang lebih panjang.
        """
    )
else:
    st.info(
        """
        ### Aktivitas Manufaktur Berada di Titik Keseimbangan

        PMI berada tepat pada level 50, yang menunjukkan aktivitas manufaktur belum mengalami ekspansi maupun kontraksi secara signifikan. Kondisi ini mencerminkan fase transisi di mana pasar masih menunggu arah ekonomi yang lebih jelas.

        **Fokus Investor Saat Ini:**
        - Data inflasi Amerika Serikat.
        - Kebijakan suku bunga The Federal Reserve.
        - Data tenaga kerja dan tingkat konsumsi masyarakat.
        - Perkembangan pesanan baru pada sektor manufaktur.
        """
    )

st.caption("Source: Institute for Supply Management (ISM)")