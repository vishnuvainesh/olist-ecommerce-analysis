import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import queries
from utils import run_query, get_value, format_currency, format_number


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OLIST | Marketplace Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: #08100d;
        color: #edf4ef;
    }

    [data-testid="stHeader"] {
        background: #08100d;
    }

    [data-testid="stSidebar"] {
        background: #0b1511;
        border-right: 1px solid #1d2b25;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    .block-container {
        max-width: 1450px;
        padding: 2.2rem 3rem 4rem 3rem;
    }

    /* Sidebar */

    .brand {
        padding: 10px 8px 28px 8px;
        border-bottom: 1px solid #1d2b25;
        margin-bottom: 25px;
    }

    .brand-title {
        color: #f2f6f3;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -1px;
    }

    .brand-title span {
        color: #9ee6bd;
    }

    .brand-subtitle {
        color: #63746b;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1.7px;
        margin-top: 7px;
    }

    .side-label {
        color: #53645b;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1.5px;
        margin: 0 8px 10px 8px;
    }

    /* Main */

    .eyebrow {
        color: #7ea58e;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    .page-title {
        color: #f1f5f2;
        font-family: 'Fraunces', serif;
        font-size: clamp(38px, 4.5vw, 68px);
        line-height: 0.98;
        font-weight: 400;
        letter-spacing: -2px;
        margin: 0;
    }

    .page-description {
        color: #87968e;
        font-size: 14px;
        line-height: 1.7;
        max-width: 760px;
        margin-top: 18px;
    }

    .section-number {
        color: #638074;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }

    .section-title {
        color: #e9efeb;
        font-size: 21px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    /* KPI */

    .kpi-card {
        background: #0d1814;
        border: 1px solid #1d2c25;
        border-radius: 5px;
        padding: 22px 22px 20px 22px;
        min-height: 135px;
    }

    .kpi-label {
        color: #64756c;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 13px;
    }

    .kpi-value {
        color: #f2f6f3;
        font-size: 29px;
        font-weight: 600;
        letter-spacing: -1px;
    }

    .kpi-accent {
        color: #9ee6bd;
    }

    .kpi-small {
        color: #728179;
        font-size: 11px;
        margin-top: 8px;
    }

    /* Cards */

    .chart-heading {
        color: #e9efeb;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 2px;
    }

    .chart-subheading {
        color: #617169;
        font-size: 10px;
        margin-bottom: 8px;
    }

    .insight-card {
        background: #0d1814;
        border: 1px solid #1d2c25;
        border-left: 2px solid #8bd7aa;
        border-radius: 4px;
        padding: 20px 22px;
        margin-top: 12px;
    }

    .insight-title {
        color: #a7e8c1;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .insight-text {
        color: #b8c4be;
        font-size: 13px;
        line-height: 1.65;
    }

    .empty-card {
        background: #0d1814;
        border: 1px dashed #26382f;
        border-radius: 5px;
        padding: 30px;
        text-align: center;
        color: #63746b;
    }

    .footer {
        border-top: 1px solid #1d2b25;
        margin-top: 60px;
        padding-top: 18px;
        color: #4d5e55;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1px;
    }

    /* Streamlit controls */

    .stSelectbox label,
    .stRadio label {
        color: #718078 !important;
        font-size: 11px !important;
    }

    div[data-baseweb="select"] > div {
        background: #0d1814;
        border-color: #25372e;
        color: #dce6e0;
    }

    button[kind="secondary"] {
        border-color: #25372e;
    }

    [data-testid="stMetric"] {
        background: #0d1814;
        border: 1px solid #1d2c25;
        padding: 15px;
    }

    /* Hide Streamlit chrome */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe_query(query):
    """Run SQL safely and return an empty DataFrame on failure."""
    try:
        if not query:
            return pd.DataFrame()

        df = run_query(query)

        if df is None:
            return pd.DataFrame()

        return df

    except Exception:
        return pd.DataFrame()


def safe_value(query, column, default=0):
    """Get a scalar SQL value safely."""
    try:
        value = get_value(query, column)

        if pd.isna(value):
            return default

        return value

    except Exception:
        return default


def money(value):
    try:
        return format_currency(float(value))
    except Exception:
        try:
            return f"₹{float(value):,.0f}"
        except Exception:
            return "₹0"


def number(value):
    try:
        return format_number(int(float(value)))
    except Exception:
        return "0"


def decimal(value, digits=2):
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "0.00"


def clean_columns(df):
    if df.empty:
        return df

    result = df.copy()

    # --------------------------------------------------------
    # IMPORTANT:
    # Make duplicate SQL column names unique.
    # This prevents Plotly/Narwhals DuplicateError.
    # --------------------------------------------------------

    new_columns = []
    seen = {}

    for col in result.columns:

        col = str(col).strip().lower().replace(" ", "_")

        if col in seen:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_columns.append(col)

    result.columns = new_columns

    return result


def first_column(df, possible_names):
    """Return first matching column name."""
    if df.empty:
        return None

    for name in possible_names:
        if name in df.columns:
            return name

    return df.columns[0] if len(df.columns) > 0 else None


def numeric_column(df, possible_names=None):
    if df.empty:
        return None

    if possible_names:

        for name in possible_names:
            if name in df.columns:
                return name

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            return col

    return None


def style_chart(fig, height=340):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Space Grotesk",
            color="#91a098",
            size=11,
        ),
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#84938b"),
        ),
        hoverlabel=dict(
            bgcolor="#101b17",
            font_color="#edf4ef",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#24352c",
        tickfont=dict(color="#65756d"),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#17251f",
        zeroline=False,
        linecolor="#24352c",
        tickfont=dict(color="#65756d"),
    )

    return fig


def chart_title(title, subtitle=None):

    html = f'<div class="chart-heading">{title}</div>'

    if subtitle:
        html += f'<div class="chart-subheading">{subtitle}</div>'

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def empty_message(message="No data available"):

    st.markdown(
        f"""
        <div class="empty-card">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(number_text, title):

    st.markdown(
        f"""
        <div style="margin-top:34px;">
            <div class="section-number">{number_text}</div>
            <div class="section-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(number_text, title, description):

    st.markdown(
        f"""
        <div class="eyebrow">OLIST / {number_text}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi(label, value, note=""):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-small">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(title, text):

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_sort(df, column, ascending=False):

    if df.empty or column not in df.columns:
        return df

    return df.sort_values(
        column,
        ascending=ascending,
        na_position="last"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">◆ <span>OLIST</span></div>
            <div class="brand-subtitle">
                MARKETPLACE INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-label">ANALYTICS</div>',
        unsafe_allow_html=True,
    )

    pages = [
        "Overview",
        "Sales",
        "Customers",
        "Sellers & Products",
        "Delivery",
        "Reviews",
        "Insights",
    ]

    page = st.radio(
        "Navigation",
        pages,
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div style="height:35px;"></div>

        <div class="side-label">
            DATA SOURCE
        </div>

        <div style="
            color:#718078;
            font-size:11px;
            line-height:1.6;
            padding:0 8px;
        ">
            MySQL<br>
            Olist Brazilian Marketplace
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW
# ============================================================

def render_overview():

    page_header(
        "01",
        "Marketplace at a glance",
        "A high-level view of revenue, customers, orders and marketplace scale."
    )

    section(
        "01",
        "Marketplace scale"
    )

    revenue = safe_value(
        getattr(
            queries,
            "TOTAL_REVENUE",
            ""
        ),
        "total_revenue",
        0,
    )

    orders = safe_value(
        getattr(
            queries,
            "TOTAL_ORDERS",
            ""
        ),
        "total_orders",
        0,
    )

    customers = safe_value(
        getattr(
            queries,
            "TOTAL_CUSTOMERS",
            ""
        ),
        "total_customers",
        0,
    )

    sellers = safe_value(
        getattr(
            queries,
            "TOTAL_SELLERS",
            ""
        ),
        "total_sellers",
        0,
    )

    aov = safe_value(
        getattr(
            queries,
            "AVERAGE_ORDER_VALUE",
            ""
        ),
        "average_order_value",
        0,
    )

    review = safe_value(
        getattr(
            queries,
            "AVERAGE_REVIEW_SCORE",
            ""
        ),
        "average_review_score",
        0,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi(
            "Total Revenue",
            money(revenue),
            "Marketplace sales value"
        )

    with c2:
        kpi(
            "Total Orders",
            number(orders),
            "Orders in connected database"
        )

    with c3:
        kpi(
            "Customers",
            number(customers),
            "Unique marketplace customers"
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        kpi(
            "Active Sellers",
            number(sellers),
            "Sellers represented in marketplace"
        )

    with c5:
        kpi(
            "Average Order Value",
            money(aov),
            "Average value per order"
        )

    with c6:
        kpi(
            "Average Review Score",
            f"{decimal(review)} / 5",
            "Customer satisfaction"
        )

    section(
        "02",
        "Revenue movement"
    )

    monthly = clean_columns(
        safe_query(
            getattr(
                queries,
                "MONTHLY_REVENUE",
                ""
            )
        )
    )

    if not monthly.empty:

        date_col = first_column(
            monthly,
            [
                "month",
                "order_month",
                "month_year",
                "order_purchase_month",
                "date",
            ],
        )

        revenue_col = numeric_column(
            monthly,
            [
                "revenue",
                "total_revenue",
                "monthly_revenue",
                "sales",
            ],
        )

        if date_col and revenue_col:

            fig = px.area(
                monthly,
                x=date_col,
                y=revenue_col,
            )

            fig.update_traces(
                line_width=2,
                fill="tozeroy",
                hovertemplate="Revenue: ₹%{y:,.0f}<extra></extra>",
            )

            style_chart(
                fig,
                380
            )

            chart_title(
                "Monthly revenue",
                "Marketplace revenue trend over time"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

        else:
            empty_message(
                "Monthly revenue columns could not be identified."
            )

    else:
        empty_message(
            "Monthly revenue data is unavailable."
        )

    section(
        "03",
        "Marketplace composition"
    )

    left, right = st.columns(2)

    with left:

        category = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "REVENUE_BY_CATEGORY",
                    ""
                )
            )
        )

        if not category.empty:

            x = first_column(
                category,
                [
                    "category",
                    "product_category_name",
                    "product_category",
                    "category_name",
                ],
            )

            y = numeric_column(
                category,
                [
                    "revenue",
                    "total_revenue",
                    "sales",
                ],
            )

            if x and y:

                category_plot = category.nlargest(
                    10,
                    y
                )

                fig = px.bar(
                    category_plot,
                    x=y,
                    y=x,
                    orientation="h",
                )

                fig.update_traces(
                    hovertemplate="₹%{x:,.0f}<extra></extra>"
                )

                fig.update_layout(
                    yaxis=dict(
                        categoryorder="total ascending"
                    )
                )

                style_chart(
                    fig,
                    390
                )

                chart_title(
                    "Top categories",
                    "Revenue contribution by product category"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

        else:
            empty_message(
                "Category revenue data is unavailable."
            )

    with right:

        review_data = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "REVIEW_SCORE_DISTRIBUTION",
                    ""
                )
            )
        )

        if not review_data.empty:

            score_col = first_column(
                review_data,
                [
                    "review_score",
                    "score",
                    "rating",
                ],
            )

            count_col = numeric_column(
                review_data,
                [
                    "total_reviews",
                    "reviews",
                    "count",
                ],
            )

            if score_col and count_col:

                fig = px.bar(
                    review_data,
                    x=score_col,
                    y=count_col,
                )

                fig.update_traces(
                    hovertemplate="%{y:,.0f} reviews<extra></extra>"
                )

                style_chart(
                    fig,
                    390
                )

                chart_title(
                    "Review distribution",
                    "Number of reviews by customer score"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

        else:
            empty_message(
                "Review distribution is unavailable."
            )

    insight(
        "What this means",
        f"The marketplace contains {number(orders)} orders across "
        f"{number(sellers)} sellers, with an average order value of "
        f"{money(aov)} and an average customer review score of "
        f"{decimal(review)} out of 5."
    )


# ============================================================
# SALES
# ============================================================

def render_sales():

    page_header(
        "02",
        "Sales performance",
        "Understand revenue momentum, category contribution and geographic sales."
    )

    revenue = safe_value(
        getattr(
            queries,
            "TOTAL_REVENUE",
            ""
        ),
        "total_revenue",
        0,
    )

    orders = safe_value(
        getattr(
            queries,
            "TOTAL_ORDERS",
            ""
        ),
        "total_orders",
        0,
    )

    aov = safe_value(
        getattr(
            queries,
            "AVERAGE_ORDER_VALUE",
            ""
        ),
        "average_order_value",
        0,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi(
            "Revenue",
            money(revenue),
            "Total marketplace revenue"
        )

    with c2:
        kpi(
            "Orders",
            number(orders),
            "Total orders"
        )

    with c3:
        kpi(
            "Average Order Value",
            money(aov),
            "Revenue per order"
        )

    section(
        "01",
        "Revenue trend"
    )

    monthly = clean_columns(
        safe_query(
            getattr(
                queries,
                "MONTHLY_REVENUE",
                ""
            )
        )
    )

    if not monthly.empty:

        x = first_column(
            monthly,
            [
                "month",
                "order_month",
                "month_year",
                "date",
            ],
        )

        y = numeric_column(
            monthly,
            [
                "revenue",
                "total_revenue",
                "monthly_revenue",
                "sales",
            ],
        )

        if x and y:

            fig = px.line(
                monthly,
                x=x,
                y=y,
                markers=True,
            )

            fig.update_traces(
                line_width=2,
                hovertemplate="₹%{y:,.0f}<extra></extra>",
            )

            style_chart(
                fig,
                400
            )

            chart_title(
                "Monthly revenue",
                "Revenue trajectory across the marketplace"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    section(
        "02",
        "Category economics"
    )

    category = clean_columns(
        safe_query(
            getattr(
                queries,
                "CATEGORY_PERFORMANCE",
                ""
            )
        )
    )

    if category.empty:

        category = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "REVENUE_BY_CATEGORY",
                    ""
                )
            )
        )

    if not category.empty:

        category_col = first_column(
            category,
            [
                "category",
                "product_category_name",
                "product_category",
                "category_name",
            ],
        )

        revenue_col = numeric_column(
            category,
            [
                "revenue",
                "total_revenue",
                "sales",
            ],
        )

        if category_col and revenue_col:

            top = category.nlargest(
                15,
                revenue_col
            )

            fig = px.bar(
                top,
                x=revenue_col,
                y=category_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            fig.update_traces(
                hovertemplate="₹%{x:,.0f}<extra></extra>"
            )

            style_chart(
                fig,
                470
            )

            chart_title(
                "Revenue by category",
                "Highest-value product categories"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Category performance data is unavailable."
        )

    section(
        "03",
        "Geographic sales"
    )

    location = clean_columns(
        safe_query(
            getattr(
                queries,
                "SALES_BY_LOCATION",
                ""
            )
        )
    )

    if not location.empty:

        state_col = first_column(
            location,
            [
                "state",
                "customer_state",
                "seller_state",
                "customer_city",
            ],
        )

        value_col = numeric_column(
            location,
            [
                "revenue",
                "total_revenue",
                "sales",
                "orders",
                "total_orders",
            ],
        )

        if state_col and value_col:

            top = location.nlargest(
                15,
                value_col
            )

            fig = px.bar(
                top,
                x=state_col,
                y=value_col,
            )

            style_chart(
                fig,
                400
            )

            chart_title(
                "Sales by location",
                "Geographic concentration of marketplace activity"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Location sales data is unavailable."
        )


# ============================================================
# CUSTOMERS
# ============================================================

def render_customers():

    page_header(
        "03",
        "Customer intelligence",
        "Explore customer distribution, spending behaviour and repeat purchasing."
    )

    customers = safe_value(
        getattr(
            queries,
            "TOTAL_CUSTOMERS",
            ""
        ),
        "total_customers",
        0,
    )

    customer_distribution = clean_columns(
        safe_query(
            getattr(
                queries,
                "CUSTOMER_DISTRIBUTION",
                ""
            )
        )
    )

    repeat_data = clean_columns(
        safe_query(
            getattr(
                queries,
                "REPEAT_VS_NEW_CUSTOMERS",
                ""
            )
        )
    )

    top_customers = clean_columns(
        safe_query(
            getattr(
                queries,
                "TOP_CUSTOMERS",
                ""
            )
        )
    )

    repeat_count = 0

    if not repeat_data.empty:

        count_col = numeric_column(
            repeat_data,
            [
                "customers",
                "customer_count",
                "total_customers",
                "count",
            ],
        )

        label_col = first_column(
            repeat_data,
            [
                "customer_type",
                "type",
                "segment",
                "customer_segment",
            ],
        )

        if count_col and label_col:

            mask = repeat_data[
                label_col
            ].astype(str).str.lower().str.contains(
                "repeat"
            )

            if mask.any():

                repeat_count = repeat_data.loc[
                    mask,
                    count_col
                ].iloc[0]

    repeat_percentage = (
        float(repeat_count) /
        float(customers) *
        100
        if customers
        else 0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        kpi(
            "Total Customers",
            number(customers),
            "Unique customer accounts"
        )

    with c2:
        kpi(
            "Repeat Customers",
            number(repeat_count),
            "Customers with multiple purchases"
        )

    with c3:
        kpi(
            "Repeat Rate",
            f"{repeat_percentage:.1f}%",
            "Share of customers returning"
        )

    section(
        "01",
        "Customer distribution"
    )

    left, right = st.columns(2)

    with left:

        if not customer_distribution.empty:

            state_col = first_column(
                customer_distribution,
                [
                    "state",
                    "customer_state",
                    "customer_unique_id",
                ],
            )

            count_col = numeric_column(
                customer_distribution,
                [
                    "customers",
                    "customer_count",
                    "total_customers",
                    "count",
                ],
            )

            if state_col and count_col:

                top = customer_distribution.nlargest(
                    15,
                    count_col
                )

                fig = px.bar(
                    top,
                    x=count_col,
                    y=state_col,
                    orientation="h",
                )

                fig.update_layout(
                    yaxis=dict(
                        categoryorder="total ascending"
                    )
                )

                style_chart(
                    fig,
                    430
                )

                chart_title(
                    "Customer distribution",
                    "Customer concentration across locations"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

        else:
            empty_message(
                "Customer distribution is unavailable."
            )

    with right:

        if not repeat_data.empty:

            label_col = first_column(
                repeat_data,
                [
                    "customer_type",
                    "type",
                    "segment",
                    "customer_segment",
                ],
            )

            count_col = numeric_column(
                repeat_data,
                [
                    "customers",
                    "customer_count",
                    "total_customers",
                    "count",
                ],
            )

            if label_col and count_col:

                fig = px.pie(
                    repeat_data,
                    names=label_col,
                    values=count_col,
                    hole=0.62,
                )

                fig.update_traces(
                    textposition="inside",
                    hovertemplate="%{label}: %{value:,.0f}<extra></extra>",
                )

                style_chart(
                    fig,
                    430
                )

                chart_title(
                    "New vs repeat",
                    "Customer retention profile"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

        else:
            empty_message(
                "Repeat customer data is unavailable."
            )

    section(
        "02",
        "Customer spending"
    )

    spending = clean_columns(
        safe_query(
            getattr(
                queries,
                "CUSTOMER_SPENDING",
                ""
            )
        )
    )

    if not spending.empty:

        # ----------------------------------------------------
        # The current CUSTOMER_SPENDING query returns:
        # customer_unique_id + total_spending.
        #
        # Therefore display top customers rather than treating
        # customer IDs as spending segments.
        # ----------------------------------------------------

        customer_col = first_column(
            spending,
            [
                "customer_unique_id",
                "customer_id",
                "customer",
            ],
        )

        spending_col = numeric_column(
            spending,
            [
                "total_spending",
                "spending",
                "customer_spending",
            ],
        )

        if customer_col and spending_col:

            top_spending = spending.nlargest(
                15,
                spending_col
            )

            fig = px.bar(
                top_spending,
                x=spending_col,
                y=customer_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            fig.update_traces(
                hovertemplate="₹%{x:,.0f}<extra></extra>"
            )

            style_chart(
                fig,
                450
            )

            chart_title(
                "Highest customer spending",
                "Customers with the highest total purchase value"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Customer spending data is unavailable."
        )

    section(
        "03",
        "Highest-value customers"
    )

    if not top_customers.empty:

        st.dataframe(
            top_customers.head(15),
            width="stretch",
            hide_index=True,
        )

    else:
        empty_message(
            "Top customer data is unavailable."
        )

    insight(
        "Customer signal",
        f"The marketplace has approximately "
        f"{number(customers)} customers. "
        f"The current customer dataset indicates a "
        f"repeat-customer rate of approximately "
        f"{repeat_percentage:.1f}%."
    )


# ============================================================
# SELLERS & PRODUCTS
# ============================================================

def render_sellers_products():

    page_header(
        "04",
        "Sellers & products",
        "Identify leading sellers, high-volume products and category performance."
    )

    sellers = safe_value(
        getattr(
            queries,
            "TOTAL_SELLERS",
            ""
        ),
        "total_sellers",
        0,
    )

    seller_data = clean_columns(
        safe_query(
            getattr(
                queries,
                "TOP_SELLERS",
                ""
            )
        )
    )

    product_data = clean_columns(
        safe_query(
            getattr(
                queries,
                "TOP_SELLING_PRODUCTS",
                ""
            )
        )
    )

    category_data = clean_columns(
        safe_query(
            getattr(
                queries,
                "CATEGORY_PERFORMANCE",
                ""
            )
        )
    )

    section(
        "01",
        "Seller scale"
    )

    top_seller_name = "—"

    if not seller_data.empty:

        seller_col = first_column(
            seller_data,
            [
                "seller_id",
                "seller",
                "seller_unique_id",
            ],
        )

        if seller_col:

            top_seller_name = str(
                seller_data.iloc[0][seller_col]
            )

    c1, c2 = st.columns(2)

    with c1:

        kpi(
            "Total Sellers",
            number(sellers),
            "Seller accounts in marketplace"
        )

    with c2:

        kpi(
            "Leading Seller",
            top_seller_name[:24],
            "Highest-volume seller in result set"
        )

    section(
        "02",
        "Seller performance"
    )

    if not seller_data.empty:

        seller_col = first_column(
            seller_data,
            [
                "seller_id",
                "seller",
                "seller_unique_id",
            ],
        )

        metric_col = numeric_column(
            seller_data,
            [
                "units_sold",
                "total_orders",
                "orders",
                "revenue",
                "seller_revenue",
                "total_revenue",
            ],
        )

        if seller_col and metric_col:

            top = seller_data.nlargest(
                15,
                metric_col
            )

            fig = px.bar(
                top,
                x=metric_col,
                y=seller_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            style_chart(
                fig,
                470
            )

            chart_title(
                "Top sellers",
                "Leading sellers by marketplace activity"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Seller performance data is unavailable."
        )

    section(
        "03",
        "Product performance"
    )

    if not product_data.empty:

        product_col = first_column(
            product_data,
            [
                "product_id",
                "product",
                "product_category_name",
            ],
        )

        metric_col = numeric_column(
            product_data,
            [
                "units_sold",
                "total_orders",
                "orders",
                "revenue",
                "total_revenue",
            ],
        )

        if product_col and metric_col:

            top = product_data.nlargest(
                15,
                metric_col
            )

            fig = px.bar(
                top,
                x=metric_col,
                y=product_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            style_chart(
                fig,
                470
            )

            chart_title(
                "Top-selling products",
                "Products generating the highest marketplace volume"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Product performance data is unavailable."
        )

    section(
        "04",
        "Category performance"
    )

    if not category_data.empty:

        st.dataframe(
            category_data.head(20),
            width="stretch",
            hide_index=True,
        )

    else:
        empty_message(
            "Category performance data is unavailable."
        )


# ============================================================
# DELIVERY
# ============================================================

def render_delivery():

    page_header(
        "05",
        "Delivery performance",
        "Measure delivery speed, delays and their relationship with customer satisfaction."
    )

    avg_delivery = safe_value(
        getattr(
            queries,
            "AVERAGE_DELIVERY_TIME",
            ""
        ),
        "average_delivery_time",
        0,
    )

    on_time = clean_columns(
        safe_query(
            getattr(
                queries,
                "ON_TIME_VS_DELAYED",
                ""
            )
        )
    )

    delivery_location = clean_columns(
        safe_query(
            getattr(
                queries,
                "DELIVERY_BY_LOCATION",
                ""
            )
        )
    )

    delivery_review = clean_columns(
        safe_query(
            getattr(
                queries,
                "DELIVERY_DELAY_VS_REVIEW",
                ""
            )
        )
    )

    section(
        "01",
        "Delivery health"
    )

    c1, c2 = st.columns(2)

    with c1:

        kpi(
            "Average Delivery Time",
            f"{decimal(avg_delivery, 1)} days",
            "Average order delivery duration")

    with c2:

        delayed_count = 0

        if not on_time.empty:

            label_col = first_column(
                on_time,
                [
                    "delivery_status",
                    "status",
                    "type",
                ],
            )

            value_col = numeric_column(
                on_time,
                [
                    "orders",
                    "order_count",
                    "count",
                    "total_orders",
                ],
            )

            if label_col and value_col:

                delayed_mask = on_time[
                    label_col
                ].astype(str).str.lower().str.contains(
                    "delay"
                )

                if delayed_mask.any():

                    delayed_count = on_time.loc[
                        delayed_mask,
                        value_col
                    ].sum()

        kpi(
            "Delayed Orders",
            number(delayed_count),
            "Orders classified as delayed"
        )

    section(
        "02",
        "Delivery reliability"
    )

    if not on_time.empty:

        label_col = first_column(
            on_time,
            [
                "delivery_status",
                "status",
                "type",
            ],
        )

        value_col = numeric_column(
            on_time,
            [
                "orders",
                "order_count",
                "count",
                "total_orders",
            ],
        )

        if label_col and value_col:

            fig = px.pie(
                on_time,
                names=label_col,
                values=value_col,
                hole=0.62,
            )

            fig.update_traces(
                hovertemplate="%{label}: %{value:,.0f}<extra></extra>"
            )

            style_chart(
                fig,
                400
            )

            chart_title(
                "On-time vs delayed",
                "Order delivery reliability"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Delivery reliability data is unavailable."
        )

    section(
        "03",
        "Delivery by location"
    )

    if not delivery_location.empty:

        location_col = first_column(
            delivery_location,
            [
                "state",
                "customer_state",
                "seller_state",
                "location",
            ],
        )

        value_col = numeric_column(
            delivery_location,
            [
                "delivery_days",
                "average_delivery_time",
                "avg_delivery_days",
                "days",
            ],
        )

        if location_col and value_col:

            top = delivery_location.nlargest(
                15,
                value_col
            )

            fig = px.bar(
                top,
                x=value_col,
                y=location_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            style_chart(
                fig,
                450
            )

            chart_title(
                "Delivery time by location",
                "Locations with the highest average delivery duration"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Location delivery data is unavailable."
        )

    section(
        "04",
        "Delivery & customer experience"
    )

    if not delivery_review.empty:

        # ----------------------------------------------------
        # DELIVERY_DELAY_VS_REVIEW returns:
        #
        # review_score
        # total_reviews
        # average_delivery_delay
        #
        # Therefore we compare review score against delay.
        # ----------------------------------------------------

        x = numeric_column(
            delivery_review,
            [
                "average_delivery_delay",
                "delivery_delay",
                "average_delivery_time",
                "delivery_days",
            ],
        )

        y = numeric_column(
            delivery_review,
            [
                "review_score",
                "average_review_score",
                "avg_review_score",
                "rating",
            ],
        )

        if x and y:

            plot_data = delivery_review[
                [x, y]
            ].copy()

            plot_data[x] = pd.to_numeric(
                plot_data[x],
                errors="coerce"
            )

            plot_data[y] = pd.to_numeric(
                plot_data[y],
                errors="coerce"
            )

            plot_data = plot_data.dropna()

            if not plot_data.empty:

                fig = px.scatter(
                    plot_data,
                    x=x,
                    y=y,
                )

                fig.update_traces(
                    hovertemplate=(
                        "Delay: %{x:.2f} days"
                        "<br>Review: %{y:.2f} / 5"
                        "<extra></extra>"
                    )
                )

                style_chart(
                    fig,
                    400
                )

                chart_title(
                    "Delivery delay vs review score",
                    "Relationship between delivery delay and customer rating"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

            else:
                empty_message(
                    "Delivery and review values contain no usable numeric data."
                )

        else:
            empty_message(
                "Delivery and review columns could not be identified."
            )

    else:
        empty_message(
            "Delivery and review relationship data is unavailable."
        )

    insight(
        "Delivery signal",
        f"The marketplace currently shows an average delivery "
        f"duration of approximately "
        f"{decimal(avg_delivery, 1)} days. "
        f"Delivery performance should be monitored alongside "
        f"review scores because delays can affect customer experience."
    )


# ============================================================
# REVIEWS
# ============================================================

def render_reviews():

    page_header(
        "06",
        "Customer reviews",
        "Understand rating distribution, category satisfaction and the relationship between delivery and reviews."
    )

    avg_review = safe_value(
        getattr(
            queries,
            "AVERAGE_REVIEW_SCORE",
            ""
        ),
        "average_review_score",
        0,
    )

    review_distribution = clean_columns(
        safe_query(
            getattr(
                queries,
                "REVIEW_SCORE_DISTRIBUTION",
                ""
            )
        )
    )

    reviews_category = clean_columns(
        safe_query(
            getattr(
                queries,
                "REVIEWS_BY_CATEGORY",
                ""
            )
        )
    )

    rating_delivery = clean_columns(
        safe_query(
            getattr(
                queries,
                "RATING_VS_DELIVERY",
                ""
            )
        )
    )

    section(
        "01",
        "Customer satisfaction"
    )

    c1, c2 = st.columns(2)

    with c1:

        kpi(
            "Average Review Score",
            f"{decimal(avg_review)} / 5",
            "Marketplace-wide average"
        )

    with c2:

        five_star = 0

        if not review_distribution.empty:

            score_col = first_column(
                review_distribution,
                [
                    "review_score",
                    "score",
                    "rating",
                ],
            )

            count_col = numeric_column(
                review_distribution,
                [
                    "total_reviews",
                    "reviews",
                    "count",
                ],
            )

            if score_col and count_col:

                try:

                    mask = (
                        pd.to_numeric(
                            review_distribution[
                                score_col
                            ],
                            errors="coerce"
                        ) == 5
                    )

                    five_star = review_distribution.loc[
                        mask,
                        count_col
                    ].sum()

                except Exception:
                    five_star = 0

        kpi(
            "Five-Star Reviews",
            number(five_star),
            "Reviews with a score of 5"
        )

    section(
        "02",
        "Rating distribution"
    )

    if not review_distribution.empty:

        score_col = first_column(
            review_distribution,
            [
                "review_score",
                "score",
                "rating",
            ],
        )

        count_col = numeric_column(
            review_distribution,
            [
                "total_reviews",
                "reviews",
                "count",
            ],
        )

        if score_col and count_col:

            fig = px.bar(
                review_distribution,
                x=score_col,
                y=count_col,
            )

            fig.update_traces(
                hovertemplate=(
                    "%{x} stars: %{y:,.0f} reviews"
                    "<extra></extra>"
                )
            )

            style_chart(
                fig,
                390
            )

            chart_title(
                "Review score distribution",
                "Number of reviews by rating"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

    else:
        empty_message(
            "Review distribution is unavailable."
        )

    section(
        "03",
        "Reviews by category"
    )

    if not reviews_category.empty:

        category_col = first_column(
            reviews_category,
            [
                "category",
                "product_category_name",
                "product_category",
                "category_name",
            ],
        )

        score_col = numeric_column(
            reviews_category,
            [
                "average_review_score",
                "average_rating",
                "avg_review_score",
                "review_score",
                "rating",
            ],
        )

        if category_col and score_col:

            top = reviews_category.nlargest(
                15,
                score_col
            )

            fig = px.bar(
                top,
                x=score_col,
                y=category_col,
                orientation="h",
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            fig.update_traces(
                hovertemplate=(
                    "Rating: %{x:.2f} / 5"
                    "<extra></extra>"
                )
            )

            style_chart(
                fig,
                460
            )

            chart_title(
                "Category satisfaction",
                "Average rating by product category"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                },
            )

        else:
            empty_message(
                "Category review columns could not be identified."
            )

    else:
        empty_message(
            "Category review data is unavailable."
        )

    section(
        "04",
        "Rating vs delivery"
    )

    if not rating_delivery.empty:

        # ----------------------------------------------------
        # FIXED:
        #
        # RATING_VS_DELIVERY returns:
        #
        # review_score
        # total_reviews
        # average_delivery_delay
        #
        # We explicitly use:
        #
        # X = average_delivery_delay
        # Y = review_score
        #
        # This prevents Plotly/Narwhals duplicate-column
        # problems and correctly represents the SQL output.
        # ----------------------------------------------------

        x = numeric_column(
            rating_delivery,
            [
                "average_delivery_delay",
                "delivery_delay",
                "average_delivery_time",
                "delivery_days",
            ],
        )

        y = numeric_column(
            rating_delivery,
            [
                "review_score",
                "average_review_score",
                "avg_review_score",
                "rating",
            ],
        )

        if x and y:

            plot_data = rating_delivery[
                [x, y]
            ].copy()

            # Convert explicitly to numeric
            plot_data[x] = pd.to_numeric(
                plot_data[x],
                errors="coerce"
            )

            plot_data[y] = pd.to_numeric(
                plot_data[y],
                errors="coerce"
            )

            # Remove NULL / invalid values
            plot_data = plot_data.dropna()

            if not plot_data.empty:

                fig = px.scatter(
                    plot_data,
                    x=x,
                    y=y,
                )

                fig.update_traces(
                    hovertemplate=(
                        "Average Delay: %{x:.2f} days"
                        "<br>Review Score: %{y:.2f} / 5"
                        "<extra></extra>"
                    )
                )

                style_chart(
                    fig,
                    420
                )

                chart_title(
                    "Delivery delay vs review score",
                    "How delivery delays relate to customer ratings"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    },
                )

            else:

                empty_message(
                    "Rating and delivery data contains no usable values."
                )

        else:

            empty_message(
                "Delivery and review columns could not be identified."
            )

    else:

        empty_message(
            "Rating vs delivery data is unavailable."
        )

    insight(
        "Review signal",
        f"The marketplace currently has an average review score "
        f"of {decimal(avg_review)} out of 5. Review distribution "
        f"and delivery performance should be considered together "
        f"when evaluating customer experience."
    )


# ============================================================
# INSIGHTS
# ============================================================

def render_insights():

    page_header(
        "07",
        "Executive insights",
        "A concise decision layer built from the marketplace's sales, customer, seller, delivery and review data."
    )

    revenue = safe_value(
        getattr(
            queries,
            "TOTAL_REVENUE",
            ""
        ),
        "total_revenue",
        0,
    )

    orders = safe_value(
        getattr(
            queries,
            "TOTAL_ORDERS",
            ""
        ),
        "total_orders",
        0,
    )

    customers = safe_value(
        getattr(
            queries,
            "TOTAL_CUSTOMERS",
            ""
        ),
        "total_customers",
        0,
    )

    sellers = safe_value(
        getattr(
            queries,
            "TOTAL_SELLERS",
            ""
        ),
        "total_sellers",
        0,
    )

    aov = safe_value(
        getattr(
            queries,
            "AVERAGE_ORDER_VALUE",
            ""
        ),
        "average_order_value",
        0,
    )

    avg_review = safe_value(
        getattr(
            queries,
            "AVERAGE_REVIEW_SCORE",
            ""
        ),
        "average_review_score",
        0,
    )

    avg_delivery = safe_value(
        getattr(
            queries,
            "AVERAGE_DELIVERY_TIME",
            ""
        ),
        "average_delivery_time",
        0,
    )

    section(
        "01",
        "Executive scorecard"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        kpi(
            "Revenue",
            money(revenue),
            "Marketplace sales"
        )

    with c2:

        kpi(
            "Orders",
            number(orders),
            "Marketplace orders"
        )

    with c3:

        kpi(
            "AOV",
            money(aov),
            "Average order value"
        )

    with c4:

        kpi(
            "Review Score",
            f"{decimal(avg_review)} / 5",
            "Customer rating"
        )

    section(
        "02",
        "What the data says"
    )

    insight(
        "Scale",
        f"The Olist marketplace dataset represents approximately "
        f"{number(orders)} orders, {number(customers)} customers "
        f"and {number(sellers)} sellers. This provides a broad "
        f"base for analysing marketplace behaviour."
    )

    insight(
        "Revenue",
        f"Total marketplace revenue is approximately "
        f"{money(revenue)}, with an average order value of "
        f"{money(aov)}. Category and seller-level analysis can "
        f"be used to identify where revenue is concentrated."
    )

    insight(
        "Customer experience",
        f"The average customer review score is "
        f"{decimal(avg_review)} out of 5. This should be "
        f"evaluated alongside delivery performance to identify "
        f"operational factors affecting satisfaction."
    )

    insight(
        "Operations",
        f"Average delivery duration is approximately "
        f"{decimal(avg_delivery, 1)} days. Monitoring delayed "
        f"orders and geographic delivery differences can help "
        f"identify operational improvement opportunities."
    )

    section(
        "03",
        "Supporting analysis"
    )

    tabs = st.tabs(
        [
            "Top Customers",
            "Top Sellers",
            "Top Products",
        ]
    )

    with tabs[0]:

        data = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "TOP_CUSTOMERS",
                    ""
                )
            )
        )

        if not data.empty:

            st.dataframe(
                data.head(15),
                width="stretch",
                hide_index=True,
            )

        else:

            empty_message(
                "Top customer data unavailable."
            )

    with tabs[1]:

        data = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "TOP_SELLERS",
                    ""
                )
            )
        )

        if not data.empty:

            st.dataframe(
                data.head(15),
                width="stretch",
                hide_index=True,
            )

        else:

            empty_message(
                "Top seller data unavailable."
            )

    with tabs[2]:

        data = clean_columns(
            safe_query(
                getattr(
                    queries,
                    "TOP_SELLING_PRODUCTS",
                    ""
                )
            )
        )

        if not data.empty:

            st.dataframe(
                data.head(15),
                width="stretch",
                hide_index=True,
            )

        else:

            empty_message(
                "Top product data unavailable."
            )

    section(
        "04",
        "Recommended focus areas"
    )

    rec1, rec2 = st.columns(2)

    with rec1:

        insight(
            "01 / Revenue growth",
            "Prioritise the categories and sellers producing "
            "the highest revenue, then compare their performance "
            "with order volume to identify high-value opportunities."
        )

        insight(
            "02 / Customer retention",
            "Track repeat purchasing behaviour and customer "
            "spending segments to understand which customers "
            "contribute the greatest long-term marketplace value."
        )

    with rec2:

        insight(
            "03 / Delivery optimisation",
            "Investigate locations and orders with longer "
            "delivery times. Reducing delays can improve "
            "operational efficiency and potentially customer satisfaction."
        )

        insight(
            "04 / Seller quality",
            "Combine seller volume, revenue and review "
            "performance to distinguish high-volume sellers "
            "from consistently high-quality sellers."
        )


# ============================================================
# ROUTER
# ============================================================

if page == "Overview":

    render_overview()

elif page == "Sales":

    render_sales()

elif page == "Customers":

    render_customers()

elif page == "Sellers & Products":

    render_sellers_products()

elif page == "Delivery":

    render_delivery()

elif page == "Reviews":

    render_reviews()

elif page == "Insights":

    render_insights()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        OLIST MARKETPLACE INTELLIGENCE&nbsp;&nbsp;•&nbsp;&nbsp;
        MYSQL ANALYTICS&nbsp;&nbsp;•&nbsp;&nbsp;
        BUSINESS INTELLIGENCE DASHBOARD
    </div>
    """,
    unsafe_allow_html=True,
)