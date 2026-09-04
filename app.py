# ============================================================================================================
# LIBRARIES
# ============================================================================================================

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================================================================
# LOAD FUNCTIONS
# ============================================================================================================

from data_source import get_fred_rate
from data_source import get_dxy
from data_source import get_us10y
from data_source import get_pmi
from data_source import get_copper
from data_source import get_iron
from data_source import get_nickel
from data_source import get_gold
from data_source import get_oil
from data_source import get_silver
from data_source import get_natural_gas

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
        return "⬆️ Uptrend"
    elif change < 0:
        return "⬇️ Downtrend"
    else:
        return "↔️ Sideways"

def get_latest_metric(data):
    "Return Current Value, Previous Value, and Change"
    current = float(data.iloc[-1])
    previous = float(data.iloc[-2])
    change = current - previous
    return current, previous, change

def get_pmi_status(value):
    if value > 50:
        return "🟢 Expansion"
    elif value < 50:
        return "🔴 Contraction"
    else:
        return "🟡 Neutral"
    
def get_macro_overall(rate_change, dxy_change, us10y_change):
    """
    Return overall macro liquidity condition
    """
    score = 0
    if rate_change < 0:
        score += 1
    elif rate_change > 0:
        score -= 1

    if dxy_change < 0:
        score += 1
    elif dxy_change > 0:
        score -= 1

    if us10y_change < 0:
        score += 1
    elif us10y_change > 0:
        score -= 1

    if score >= 2: 
        return "🟢 Improving Liquidity"
    elif score <= -2:
        return "🔴 Tightening Liquidity"
    else:
        return "🟡 Mixed Signal"

def get_macro_summary(overall):
    """"
    Return macro summary based on overall condition
    """
    if overall == "🟢 Improving Liquidity":
        return (
            "Global liquidity condition is improving. Lower interest "
            "rates, a weeker USD, and declining Treasury yields "
            "generally create a more supportive environtment for risk assets and Emerging markets."
        )
    elif overall == "🔴 Tightening Liquidity":
        return (
            "Global liquidity condition is tightening. Higher interest "
            "rates, a stronger USD, and rising Treasury yields "
            "typically increase financial pressure and reduce investor's risk appetite."
            ""
        )
    else:
        return (
            "Macro indicators are sending mixed signals. Investors should "
            "wait for additional economic data before confirming the next market direction."
        )

def create_line_chart(data, title, yaxis_title):
    """
    Create standard plotly line chart.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data,
            mode="lines",
            name=title
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    return fig

def get_manufacturing_overall(china_pmi, us_pmi):
    """
    Return overall global manufacturing condition.
    """
    score = 0

    if china_pmi > 50:
        score += 1
    elif china_pmi < 50:
        score -= 1

    if us_pmi > 50:
        score += 1
    elif us_pmi < 50:
        score -= 1

    if score == 2:
        return "🟢 Global Expansion"
    elif score == -2:
        return "🔴 Global Contraction"
    else:
        return "🟡 Mixed Manufacturing"

def get_manufacturing_summary(overall):
    """
    Return manufacturing summary.
    """

    if overall == "🟢 Global Expansion":
        return (
            "Manufacturing activity remains in expansion across the world's "
            "largest economies. This suggests resilient industrial demand "
            "and supports the outlook for cyclical sectors."
        )

    elif overall == "🔴 Global Contraction":
        return (
            "Manufacturing activity is contracting across major economies. "
            "Weakening industrial demand may increase pressure on global "
            "growth and cyclical sectors."
        )

    else:
        return (
            "Manufacturing indicators are sending mixed signals. "
            "Investors should monitor future PMI releases to determine "
            "whether global manufacturing is strengthening or weakening."
        )
# ============================================================================================================
# LOAD DATA
# ============================================================================================================

fed_rate = get_fred_rate()
dxy_close = get_dxy()
us10y = get_us10y()

china_pmi = get_pmi("China")
us_pmi = get_pmi("US")

copper_price = get_copper()
iron_price = get_iron()
nickel_price = get_nickel()

oil_price = get_oil()
gas_price = get_natural_gas()

gold_price = get_gold()
silver_price = get_silver()

# ============================================================================================================
# CALCULATE METRICS
# ============================================================================================================

# Fed Rate
current_rate, previous_rate, rate_change = get_latest_metric(fed_rate)
peak_rate = fed_rate.max()
rate_trend = get_trend(rate_change)

# DXY
current_dxy, previous_dxy, dxy_change = get_latest_metric(dxy_close)
peak_dxy = dxy_close.max()
dxy_trend = get_trend(dxy_change)

# US10Y
current_us10y, previous_us10y, us10y_change = get_latest_metric(us10y)
peak_us10y = us10y.max()
us10y_trend = get_trend(us10y_change)

# PMI    
current_china_pmi, prev_china_pmi, china_pmi_change = get_latest_metric(china_pmi["Value"])
china_status = get_pmi_status(current_china_pmi)
current_us_pmi, prev_us_pmi, us_pmi_change = get_latest_metric(us_pmi["Value"])
us_status = get_pmi_status(current_us_pmi)

# Copper    
current_copper, prev_copper, copper_change = get_latest_metric(copper_price)
peak_copper = float(copper_price.max())
copper_trend = get_trend(copper_change)

# Iron    
current_iron, prev_iron, iron_change = get_latest_metric(iron_price["Value"])
peak_iron = float(iron_price["Value"].max())
iron_trend = get_trend(iron_change)

# Nickel    
current_nickel, prev_nickel, nickel_change = get_latest_metric(nickel_price["Value"])
peak_nickel = float(nickel_price["Value"].max())
nickel_trend = get_trend(nickel_change)

# Oil    
current_oil, prev_oil, oil_change = get_latest_metric(oil_price)
peak_oil = float(oil_price.max())
oil_trend = get_trend(oil_change)

# Gas    
current_gas, prev_gas, gas_change = get_latest_metric(gas_price)
peak_gas = float(gas_price.max())
gas_trend = get_trend(gas_change)

# Gold    
current_gold, prev_gold, gold_change = get_latest_metric(gold_price)
peak_gold = float(gold_price.max())
gold_trend = get_trend(gold_change)

# Silver    
current_silver, prev_silver, silver_change = get_latest_metric(silver_price)
peak_silver = float(silver_price.max()) 
silver_trend = get_trend(silver_change)

# ============================================================================================================
# GLOBAL MACRO ANALYSIS
# ============================================================================================================

# OVERVIEW
# --------

if "macro_selected" not in st.session_state:
    st.session_state.macro_selected = "Fed"

macro_overall = get_macro_overall(
        rate_change,
        dxy_change,
        us10y_change
    )
macro_summary = get_macro_summary(
        macro_overall
    )

st.subheader("🌍 Global Macro Analysis")
with st.container(border=True):
    st.markdown("### 🌐 Overall Outlook")
    st.success(macro_overall)

    st.markdown("### 📊 Key Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
                st.markdown("#### 🏦 Fed Rate")
                st.markdown(f"## {current_rate:.2f}%")
                st.markdown(f"**{rate_trend}**")

                #if st.session_state.macro_selected == "Fed":
                 #   st.success("✓ Viewing")
                #else:
                if st.button(
                            "Analyze",
                            key="fed_button",
                            use_container_width=True
                        ):
                        st.session_state.macro_selected = "Fed"

    with col2:
        with st.container(border=True):
                st.markdown("#### 💵 US Dollar Index")
                st.markdown(f"## {current_dxy:.2f}")
                st.markdown(f"**{dxy_trend}**")

#                if st.session_state.macro_selected == "DXY":
#                   st.success("✓ Viewing")
#                else:
                if st.button(
                            "Analyze",
                            key="dxy_button",
                            use_container_width=True
                        ):
                        st.session_state.macro_selected = "DXY"

    with col3:
            with st.container(border=True):
                st.markdown("#### 📜 US10Y Treasury")
                st.markdown(f"## {current_us10y:.2f}%")
                st.markdown(f"**{us10y_trend}**")

#                if st.session_state.macro_selected == "US10Y":
#                    st.success("✓ Viewing")
#                else:
                if st.button(
                            "Analyze",
                            key="us10y_button",
                            use_container_width=True
                        ):
                        st.session_state.macro_selected = "US10Y"

    st.markdown("### 📝 Summary")
    st.info(macro_summary)

# DETAIL ANALYSIS GLOBAL MACRO
# ----------------------------

selected_macro = st.session_state.macro_selected
if selected_macro == "Fed":
        st.subheader("🏦 Fed Rate")

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

        fig = create_line_chart(
                fed_rate,
                "Fed Rate",
                "Rate (%)"
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption("Source: Federal Reserve Economic Data (FRED)")

elif selected_macro == "DXY":
        st.subheader("💵 US Dollar Index")

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

        fig = create_line_chart(
                dxy_close,
                "DXY",
                "DXY Index"
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption("Source: Yahoo Finance (yfinance)")

else:
        st.subheader("📜 US10Y Treasury")

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

        fig = create_line_chart(
                dxy_close,
                "US10Y",
                "US10Y Index"
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption("Source: Federal Reserve Economic Data (FRED)")

st.divider()
        
# ============================================================================================================
# GLOBAL MANUFACTURING OVERVIEW
# ============================================================================================================

manufacturing_overall = get_macro_overall(rate_change, dxy_change, us10y_change)
manufacturing_summary = get_macro_summary(macro_overall)

st.header("🏭 Global Manufacturing Overview")

with st.container(border=True):
    st.markdown("### 🟢 Overall Outlook")
    st.success(manufacturing_overall)

st.markdown("### 📊 Key Indicators")
col1, col2 = st.columns(2)

with col1:
        st.metric(
            "China PMI",
            china_status
        )
with col2:
        st.metric(
            "US PMI",
            us_status
        )

st.markdown("### 📝 Summary")
st.write(manufacturing_summary)

st.divider()

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

st.caption("Source: Institute for Supply Management (ISM)")

# ============================================================================================================
# Copper
# ============================================================================================================

st.divider()
st.subheader("🟠 Copper Futures")

copper_price = get_copper()

current_copper, previous_copper, copper_change = get_latest_metric(copper_price)
peak_copper = float(copper_price.max())
copper_trend = get_trend(copper_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Copper",
        f"{current_copper:.2f}"
    )

with col2:
    st.metric(
        "Peak Copper (5Y)",
        f"{peak_copper:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{copper_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        copper_trend
    )

fig_copper = go.Figure()

fig_copper.add_trace(
    go.Scatter(
        x=copper_price.index,
        y=copper_price,
        mode="lines",
        name="Copper"
    )
)

fig_copper.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/lb)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_copper,
    use_container_width=True
)

st.caption("Source: Yahoo Finance (yfinance)")

# ============================================================================================================
# Iron ore
# ============================================================================================================

st.divider()
st.subheader("🟠 Iron Ore")

iron_price = get_iron()

current_iron, previous_iron, iron_change = get_latest_metric(iron_price["Value"])
peak_iron = float(iron_price["Value"].max())
iron_trend = get_trend(iron_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current iron",
        f"{current_iron:.2f}"
    )

with col2:
    st.metric(
        "Peak iron (5Y)",
        f"{peak_iron:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{iron_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        iron_trend
    )

fig_iron = go.Figure()

fig_iron.add_trace(
    go.Scatter(
        x=iron_price["Date"],
        y=iron_price["Value"],
        mode="lines",
        name="Iron Ore"
    )
)

fig_iron.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/dmt)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_iron,
    use_container_width=True
)

st.caption("Source: macro_dataset.xlsx")

# ============================================================================================================
# Nickle
# ============================================================================================================

st.divider()
st.subheader("🟠 Nickle")

nickle_price = get_nickel()

current_nickle, previous_nickle, nickle_change = get_latest_metric(nickle_price["Value"])
peak_nickle = float(nickle_price["Value"].max())
nickle_trend = get_trend(nickle_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current nickle",
        f"{current_nickle:.2f}"
    )

with col2:
    st.metric(
        "Peak nickle (5Y)",
        f"{peak_nickle:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{nickle_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        nickle_trend
    )

fig_nickle = go.Figure()

fig_nickle.add_trace(
    go.Scatter(
        x=nickle_price["Date"],
        y=nickle_price["Value"],
        mode="lines",
        name="Nickle"
    )
)

fig_nickle.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/MT)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_nickle,
    use_container_width=True
)

st.caption("Source: macro_dataset.xlsx")

# ============================================================================================================
# Oil
# ============================================================================================================

st.divider()
st.subheader("🛢️ Crude Oil")

oil_price = get_oil()

current_oil, previous_oil, oil_change = get_latest_metric(oil_price)
peak_oil = float(oil_price.max())
oil_trend = get_trend(oil_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Oil",
        f"{current_oil:.2f}"
    )

with col2:
    st.metric(
        "Peak Oil (5Y)",
        f"{peak_oil:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{oil_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        oil_trend
    )

fig_oil = go.Figure()

fig_oil.add_trace(
    go.Scatter(
        x=oil_price.index,
        y=oil_price,
        mode="lines",
        name="Crude Oil"
    )
)

fig_oil.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/bbl)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_oil,
    use_container_width=True
)

st.caption("Source: Yahoo Finance (yfinance)")

# ============================================================================================================
# Natural Gas
# ============================================================================================================

st.divider()
st.subheader("🛢️ Natural Gas")

natural_gas_price = get_natural_gas()

current_natural_gas, previous_natural_gas, natural_gas_change = get_latest_metric(natural_gas_price)
peak_natural_gas = float(natural_gas_price.max())
natural_gas_trend = get_trend(natural_gas_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Natural Gas",
        f"{current_natural_gas:.2f}"
    )

with col2:
    st.metric(
        "Peak Natural Gas (5Y)",
        f"{peak_natural_gas:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{natural_gas_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        natural_gas_trend
    )

fig_natural_gas = go.Figure()

fig_natural_gas.add_trace(
    go.Scatter(
        x=natural_gas_price.index,
        y=natural_gas_price,
        mode="lines",
        name="Natural Gas"
    )
)

fig_natural_gas.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/MMBtu)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_natural_gas,
    use_container_width=True
)

st.caption("Source: Yahoo Finance (yfinance)")

# ============================================================================================================
# Gold
# ============================================================================================================

st.divider()
st.subheader("Gold")

gold_price = get_gold()

current_gold, previous_gold, gold_change = get_latest_metric(gold_price)
peak_gold = float(gold_price.max())
gold_trend = get_trend(gold_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Gold",
        f"{current_gold:.2f}"
    )

with col2:
    st.metric(
        "Peak Gold (5Y)",
        f"{peak_gold:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{gold_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        gold_trend
    )

fig_gold = go.Figure()

fig_gold.add_trace(
    go.Scatter(
        x=gold_price.index,
        y=gold_price,
        mode="lines",
        name="Gold"
    )
)

fig_gold.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/oz)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_gold,
    use_container_width=True
)

st.caption("Source: Yahoo Finance (yfinance)")

# ============================================================================================================
# Silver
# ============================================================================================================

st.divider()
st.subheader("Gold")

silver_price = get_silver()

current_silver, previous_silver, silver_change = get_latest_metric(silver_price)
peak_silver = float(silver_price.max())
silver_trend = get_trend(silver_change)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Silver",
        f"{current_silver:.2f}"
    )

with col2:
    st.metric(
        "Peak Silver (5Y)",
        f"{peak_silver:.2f}"
    )

with col3:
    st.metric(
        "Last Change",
        f"{silver_change:.2f}"
    )

with col4:
    st.metric(
        "Trend",
        silver_trend
    )

fig_silver = go.Figure()

fig_silver.add_trace(
    go.Scatter(
        x=silver_price.index,
        y=silver_price,
        mode="lines",
        name="Silver"
    )
)

fig_silver.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Price (USD/oz)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_silver,
    use_container_width=True
)

st.caption("Source: Yahoo Finance (yfinance)")