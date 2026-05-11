import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Customer Segmentation Project")

st.markdown("Segment customers based on income and spending patterns.")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Select columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    x_col = st.selectbox(
        "Select X-axis Column",
        numeric_cols
    )

    y_col = st.selectbox(
        "Select Y-axis Column",
        numeric_cols,
        index=1 if len(numeric_cols) > 1 else 0
    )

    # KMeans Clustering
    X = df[[x_col, y_col]]

    kmeans = KMeans(
        n_clusters=4,
        random_state=42
    )

    df["Cluster"] = kmeans.fit_predict(X)

    st.subheader("Clustered Data")
    st.dataframe(df)

    # Scatter Plot
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=df["Cluster"].astype(str),
        title="Customer Segments",
        hover_data=df.columns
    )

    st.plotly_chart(fig, use_container_width=True)

    # Cluster Counts
    st.subheader("Customers per Segment")

    cluster_counts = df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]

    fig_bar = px.bar(
        cluster_counts,
        x="Cluster",
        y="Count",
        text_auto=True,
        title="Cluster Distribution"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("Please upload a customer dataset.")