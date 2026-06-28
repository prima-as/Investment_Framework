import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import yfinance as yf
from fredapi import fred

FRED_API_KEY = "6abeb7518f0f481c5e35b4a45f609f30"

st.set_page_config(
    page_title="Top Down Investment Dashboard",
    page_icon="📈",
    layout="wide"
)

fred = fred.Fred(api_key=FRED_API_KEY)

fed_rate = fred.get_series(
    "FEDFUNDS",
    observation_start="2015-01-01"
    )

fed_df = pd.DataFrame(
    {
        "Date": fed_rate.index,
        "Fed Rate": fed_rate.values
    }
)

latest_rate = fed_df["Fed Rate"].iloc[-1]
peak_rate = fed_df["Fed Rate"].max()
last_change = (
    fed_df["Fed Rate"].iloc[-1] - fed_df["Fed Rate"].iloc[-2]
)
if last_change<0:
    trend="↓ Downtrend"
    sentiment="🟢 Positive for Emerging Market"
elif last_change>0:
    trend="↑ Uptrend"
    sentiment="🔴 Negative for Emerging Market"
else:
    trend="↔️ Flat"
    sentiment="🟡 Neutral for Emerging Market"

st.title("📈 Top Down Investment Dashboard")
st.caption(
    "Macro Indicators"
)
st.divider()
st.subheader("🏦 Fed Rate")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Fed Rate",
        f"{latest_rate:.2f}%"
    )

with col2:
    st.metric(
        "Peak Rate (10Y)",
        f"{peak_rate:.2f}%"
    )

with col3:
    st.metric(
        "Last Change",
        f"{last_change:.2f}%"
    )

with col4:
    st.metric(
        "Trend",
        trend
    )

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=fed_df["Date"],
        y=fed_df["Fed Rate"],
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

st.divider()
st.subheader("Current Assessment")
if last_change<0:
    st.success(
        """
        Fed Rate sedang menurun.
        Likuiditas Global mulai membaik.
        Kondisi ini biasanya positif untuk:
        - Emerging Market
        - Rupiah
        - IHSG
        """
    )
elif last_change>0:
    st.error(
        """
        Fed Rate sedang meningkat.
        Likuiditas Global mengetat.
        Kondisi ini biasanya kurang baik untuk:
        - Emerging Market
        - Rupiah
        - IHSG
        """
    )
else:
    st.info(
        """
        Fed Rate relatif stabil.
        Pasar sedang menunggu arah kebijakan berikutnya.
        """
    )

st.caption("Source: Federal Reserve Economic Data (FRED)")
st.divider()
st.subheader("💵 US Dollar Index (DXY)")

dxy = yf.download(
    "DX-Y.NYB",
    period= "5y",
    auto_adjust=True,
    progress=False
)

dxy_close = dxy["Close"].squeeze()

latest_dxy = float(dxy_close.iloc[-1])
peak_dxy = float(dxy_close.max())
dxy_change = float(
    dxy_close.iloc[-1]
    - dxy_close.iloc[-2]
)

if dxy_change > 0:
    dxy_trend = "↑ Uptrend"
elif dxy_change < 0:
    dxy_trend = "↓ Downtrend"
else:
    dxy_trend = "↔️ Sideways"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current DXY",
        f"{latest_dxy:.2f}"
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
    title="DXY - Last 5 Years",
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="DXY Index"
)

st.plotly_chart(
    fig_dxy,
    use_container_width=True
)

st.subheader("Current Assessment")
if dxy_change < 0:
    st.success(
        """
        DXY sedang melemah.
        Kondisi ini biasanya positif untuk:
        - Emerging Market
        - Rupiah
        - IHSG
        """
    )

elif dxy_change > 0:
    st.warning(
        """
        DXY sedang menguat.
        Kondisi ini biasanya memberi tekanan pada:
        - Emerging Market
        - Rupiah
        - IHSG
        """
    )

else:
    st.info(
        """
        DXY relatif stabil.
        Pasar sedang menunggu katalis berikutnya.
        """
    )

st.divider()
st.subheader("📜 US 10Y Treasury Yield")

us10y = fred.get_series(
    "DGS10",
    observation_start="2015-01-01"
    )

us10y = us10y.dropna()

latest_us10y = float(us10y.iloc[-1])
peak_us10y = float(us10y.max())
change_us10y = float(
    us10y.iloc[-1] - us10y.iloc[-2]
)

if change_us10y > 0:
    us10y_trend = "↑ Uptrend"
elif change_us10y < 0:
    us10y_trend = "↓ Downtrend"
else:
    us10y_trend = "↔️ Sideways"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "CURRENT US 10Y",
        f"{latest_us10y:.2f}%"
    )


with col2:
    st.metric(
        "Peak US10Y (10Y)",
        f"{peak_us10y:.2f}%"
    )

with col3:
    st.metric(
        "Last Change",
        f"{change_us10y:.2f}%"
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
    title="US 10Y Treasury Yield - Last 10 Years",
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Yield (%)"
)

st.plotly_chart(
    fig_us10y,
    use_container_width=True
)

st.subheader("Current Assessment")

if change_us10y < 0:
    st.success(
        """
        US10Y sedang menurun.
        Investor cenderung lebih tertarik ke aset berisiko.
        Kondisi ini biasanya positif untuk:
        - Saham Global
        - Emerging Market
        - IHSG
        """
    )
elif change_us10y > 0:
    st.warning(
        """
        US10Y sedang meningkat.
        Obligasi AS menjadi lebih menarik.
        Kondisi ini biasanya memberi tekanan pada:
        - Saham Global
        - Emerging Market
        - IHSG
        """
    )
else:
    st.info(
        """
        US10Y relatif stabil.
        Pasar sedang menunggu arah berikutnya.
        """
    )
