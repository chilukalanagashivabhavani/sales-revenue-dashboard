import streamlit as st
import pandas as pd
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")

st.markdown("Analyze sales and revenue data interactively.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read File
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully ✅")

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Preview Data
    st.subheader("📄 Dataset Preview")
    st.dataframe(df)

    # Find Numeric & Categorical Columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # Check Numeric Columns
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found in dataset.")
        st.stop()

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # Select Sales Column
    sales_col = st.sidebar.selectbox(
        "Select Sales Column",
        numeric_cols
    )

    # Select Category Column
    if len(categorical_cols) > 0:
        category_col = st.sidebar.selectbox(
            "Select Category Column",
            categorical_cols
        )
    else:
        category_col = None

    # Dynamic Filters
    filtered_df = df.copy()

    for col in categorical_cols:

        values = st.sidebar.multiselect(
            f"Filter {col}",
            df[col].dropna().unique()
        )

        if values:
            filtered_df = filtered_df[
                filtered_df[col].isin(values)
            ]

    # Filtered Data
    st.subheader("📌 Filtered Data")
    st.dataframe(filtered_df)

    # KPI Metrics
    st.subheader("📈 KPI Metrics")

    total_sales = filtered_df[sales_col].sum()
    avg_sales = filtered_df[sales_col].mean()
    max_sales = filtered_df[sales_col].max()
    min_sales = filtered_df[sales_col].min()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"{total_sales:,.2f}")
    col2.metric("Average Sales", f"{avg_sales:,.2f}")
    col3.metric("Highest Sale", f"{max_sales:,.2f}")
    col4.metric("Lowest Sale", f"{min_sales:,.2f}")

    # Charts Section
    st.subheader("📊 Charts & Visualization")

    # Bar Chart
    if category_col:

        chart_data = filtered_df.groupby(category_col)[sales_col].sum().reset_index()

        fig_bar = px.bar(
            chart_data,
            x=category_col,
            y=sales_col,
            title=f"{sales_col} by {category_col}",
            text_auto=True
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # Pie Chart
        fig_pie = px.pie(
            chart_data,
            names=category_col,
            values=sales_col,
            title=f"{sales_col} Distribution"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        filtered_df,
        y=sales_col,
        title=f"{sales_col} Trend"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # Histogram
    fig_hist = px.histogram(
        filtered_df,
        x=sales_col,
        title=f"{sales_col} Distribution Histogram"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # Download Filtered Data
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV or Excel file to begin.")