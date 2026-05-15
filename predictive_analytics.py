import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Predictive Analytics Using Historical Data")

st.markdown("Predict future trends using Machine Learning.")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Select numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Dataset needs at least 2 numeric columns.")
        st.stop()

    # Feature selection
    x_col = st.selectbox(
        "Select Feature Column (X)",
        numeric_cols
    )

    y_col = st.selectbox(
        "Select Target Column (Y)",
        numeric_cols,
        index=1
    )

    # Prepare data
    X = df[[x_col]]
    y = df[y_col]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    st.subheader("📊 Model Performance")

    col1, col2 = st.columns(2)

    col1.metric("Mean Absolute Error", f"{mae:.2f}")
    col2.metric("R² Score", f"{r2:.2f}")

    # Actual vs Predicted
    results_df = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": predictions
    })

    st.subheader("Prediction Results")
    st.dataframe(results_df)

    # Scatter plot
    fig = px.scatter(
        results_df,
        x="Actual",
        y="Predicted",
        title="Actual vs Predicted Values"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Line chart
    fig2 = px.line(
        results_df,
        title="Prediction Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Please upload a CSV dataset.")