import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="E-Commerce BI Dashboard", layout="wide")

st.title("📊 E-Commerce Business Intelligence Dashboard")
st.markdown("Project 2 – Dashboard Analytics using Streamlit")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\sande\OneDrive\Desktop\project2ds\cleaning_data\combined.csv")  # 🔴 change filename
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

# year_filter = st.sidebar.multiselect(
#     "Select Year",
#     options=sorted(df['order_year'].unique()),
#     default=sorted(df['order_year'].unique())
# )

# category_filter = st.sidebar.multiselect(
#     "Select Category",
#     options=df['category'].unique(),
#     default=df['category'].unique()
# )

all_years = sorted(df['order_year'].unique())
all_categories = sorted(df['category'].unique())

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=all_years,
    default=all_years
)


category_filter = st.sidebar.multiselect(
    "Select Category",
    options=all_categories,
    default=all_categories
)


df_filt = df[
    (df['order_year'].isin(year_filter)) &
    (df['category'].isin(category_filter))
]

# -----------------------------
# Tabs
# -----------------------------
tab,tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "project",
    "🏢 Executive",
    "💰 Revenue",
    "👥 Customer",
    "📦 Product",
    "🚚 Operations",
    "📈 Advanced"
])

# =============================
# TAB : projject details: 
# =============================
with tab :
    st.markdown("### 📝 About This Project")
    st.info("""
    This is my second project and this project presents an end-to-end Business Intelligence dashboard developed using Streamlit.
            
    Features include:
    -The dashboard analyzes e-commerce transaction data to provide executive insights
    revenue trends, customer behavior, product performance, operational efficiency, and predictive business trends.
    -Interactive filters and visualizations enable stakeholders to make data-driven decisions effectively.

    """)

    st.markdown("### 📌 Skills & Domain")
    col1, col2 = st.columns(2)

    with col1:
        st.success("💡 Skills Learned")
        st.write("""
        - Data Cleaning  
        - Statistical Analysis
        - Python Programming
        - Pandas
        - Streamlit Web App Development
        """)

    with col2:
        st.success("🏷️ Domain")
        st.write("""
        - E-Commerce Analytics
        """)

    st.subheader("Link To Project Documentation 📁")
    st.link_button(
        "Open Project Document 📂",
        "https://docs.google.com/document/d/1g-i00t4ZX2sMF8FGmbPGPU26hYCGm06ysbnZDMu9h2k/edit?pli=1&tab=t.0"
    )

# TAB 1: EXECUTIVE (Q1–Q5)
# =============================
with tab1:
    st.subheader("Executive Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue (₹)", f"{df_filt['final_amount_inr'].sum():,.0f}")
    col2.metric("Active Customers", df_filt['customer_id'].nunique())
    col3.metric("Avg Order Value (₹)", f"{df_filt['final_amount_inr'].mean():,.0f}")
    col4.metric("Total Orders", df_filt['transaction_id'].nunique())

    st.write("### Monthly Revenue Trend")
    rev_month = df_filt.groupby('order_month')['final_amount_inr'].sum()

    fig, ax = plt.subplots()
    rev_month.plot(kind='line', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

# =============================
# TAB 2: REVENUE (Q6–Q10)
# =============================
with tab2:
    st.subheader("Revenue Analytics")

    st.write("### Revenue by Category")
    rev_cat = df_filt.groupby('category')['final_amount_inr'].sum().sort_values()

    fig, ax = plt.subplots()
    rev_cat.plot(kind='barh', ax=ax)
    ax.set_xlabel("Revenue")
    st.pyplot(fig)

    st.write("### Discount vs Revenue")
    fig, ax = plt.subplots()
    ax.scatter(df_filt['discount_percent'], df_filt['final_amount_inr'], alpha=0.3)
    ax.set_xlabel("Discount %")
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

# =============================
# TAB 3: CUSTOMER (Q11–Q15)
# =============================
with tab3:
    st.subheader("Customer Analytics")

    st.write("### Customer Spending Tier")
    tier = df_filt['customer_spending_tier'].value_counts()

    fig, ax = plt.subplots()
    tier.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    st.write("### Revenue by Age Group")
    age_rev = df_filt.groupby('customer_age_group')['final_amount_inr'].sum()

    fig, ax = plt.subplots()
    age_rev.plot(kind='bar', ax=ax)
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

# =============================
# TAB 4: PRODUCT (Q16–Q20)
# =============================
with tab4:
    st.subheader("Product & Inventory")

    st.write("### Top 10 Products by Revenue")
    top_prod = (
        df_filt.groupby('product_name')['final_amount_inr']
        .sum().sort_values(ascending=False).head(10)
    )

    fig, ax = plt.subplots()
    top_prod.plot(kind='bar', ax=ax)
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

    st.write("### Product Rating vs Revenue")
    rating_rev = df_filt.groupby('product_rating')['final_amount_inr'].mean()

    fig, ax = plt.subplots()
    rating_rev.plot(kind='line', ax=ax)
    st.pyplot(fig)

# =============================
# TAB 5: OPERATIONS (Q21–Q25)
# =============================
with tab5:
    st.subheader("Operations & Logistics")

    st.write("### Average Delivery Days by Type")
    deliv = df_filt.groupby('delivery_type')['delivery_days'].mean()

    fig, ax = plt.subplots()
    deliv.plot(kind='bar', ax=ax)
    ax.set_ylabel("Days")
    st.pyplot(fig)

    st.write("### Payment Method Distribution")
    pay = df_filt['payment_method'].value_counts()

    fig, ax = plt.subplots()
    pay.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# =============================
# TAB 6: ADVANCED (Q26–Q30)
# =============================
with tab6:
    st.subheader("Advanced / Predictive Insights")

    st.write("### Yearly Revenue Trend (Forecast Base)")
    year_rev = df.groupby('order_year')['final_amount_inr'].sum()

    fig, ax = plt.subplots()
    year_rev.plot(kind='line', ax=ax)
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

    st.info(
        "Predictive insights are derived from historical trends. "
        "These trends support revenue forecasting, demand planning, "
        "and strategic business decisions."
    )
