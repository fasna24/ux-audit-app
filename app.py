import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ML
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# DL
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

st.set_page_config(page_title="UX Audit AI System", layout="wide")

st.title("🚀 Advanced UX & Conversion Audit System (ML + DL)")

# Upload file
file = st.file_uploader("📂 Upload Website Dataset (CSV)", type=["csv"])

if file is not None:

    data = pd.read_csv(file)

    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Data", "🤖 Models", "🎯 UX Insights"])

    # -------------------------------
    # TAB 1 → DATA
    # -------------------------------
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(data.head())
        st.write("### Basic Statistics")
        st.write(data.describe())

    # -------------------------------
    # TAB 2 → MODELS (ML + DL)
    # -------------------------------
    with tab2:

        if 'Revenue' in data.columns:

            data['Revenue'] = data['Revenue'].astype(int)

            features = ['Administrative', 'Informational', 'ProductRelated', 'BounceRates', 'ExitRates']

            X = data[features]
            y = data['Revenue']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            # 🔹 ML MODEL
            st.subheader("🤖 Machine Learning Model")

            rf_model = RandomForestClassifier()
            rf_model.fit(X_train, y_train)

            rf_pred = rf_model.predict(X_test)
            rf_acc = accuracy_score(y_test, rf_pred)

            st.metric("ML Accuracy (Random Forest)", round(rf_acc, 2))

            # 🔹 DL MODEL
            st.subheader("🧠 Deep Learning Model")

            X_train_dl = np.array(X_train)
            X_test_dl = np.array(X_test)

            model = Sequential()
            model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))
            model.add(Dense(8, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))

            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

            model.fit(X_train_dl, y_train, epochs=20, batch_size=10, verbose=0)

            dl_loss, dl_acc = model.evaluate(X_test_dl, y_test, verbose=0)

            st.metric("DL Accuracy (Neural Network)", round(dl_acc, 2))

            # 🔹 COMPARISON
            st.subheader("⚖️ Model Comparison")

            st.write(f"ML Accuracy: {round(rf_acc,2)}")
            st.write(f"DL Accuracy: {round(dl_acc,2)}")

            if dl_acc > rf_acc:
                st.success("Deep Learning performs better on this dataset")
            else:
                st.info("Machine Learning performs efficiently for this dataset")

        else:
            st.error("❌ Dataset must contain 'Revenue' column")

    # -------------------------------
    # TAB 3 → UX ANALYSIS
    # -------------------------------
    with tab3:

        if all(col in data.columns for col in ['BounceRates', 'ExitRates', 'ProductRelated']):

            bounce_rate = data['BounceRates'].mean()
            exit_rate = data['ExitRates'].mean()
            product_engagement = data['ProductRelated'].mean()

            score = 10
            issues = []

            # UX checks
            if bounce_rate > 0.5:
                score -= 3
                issues.append("High Bounce Rate")

            if exit_rate > 0.5:
                score -= 2
                issues.append("High Exit Rate")

            if product_engagement < 20:
                score -= 2
                issues.append("Low Product Engagement")

            # Score
            st.subheader("🎯 UX Score")
            st.metric("UX Score (out of 10)", score)
            st.progress(score / 10)

            # Issues
            if issues:
                st.error("⚠️ Issues Found:")
                for i in issues:
                    st.write(f"- {i}")
            else:
                st.success("✅ Excellent UX")

            # Suggestions
            st.subheader("💡 Suggestions")

            if "High Bounce Rate" in issues:
                st.write("✔ Improve landing page design & speed")

            if "High Exit Rate" in issues:
                st.write("✔ Simplify checkout process")

            if "Low Product Engagement" in issues:
                st.write("✔ Improve product images & descriptions")

            if not issues:
                st.write("🎉 Your UX is already strong!")

            # Graph
            st.subheader("📈 Bounce Rate Distribution")
            fig, ax = plt.subplots()
            ax.hist(data['BounceRates'], bins=20)
            st.pyplot(fig)

            # -------------------------------
            # DOWNLOAD REPORT
            # -------------------------------
            report = f"""
UX AUDIT REPORT

ML Accuracy: {round(rf_acc,2) if 'rf_acc' in locals() else 'N/A'}
DL Accuracy: {round(dl_acc,2) if 'dl_acc' in locals() else 'N/A'}

UX Score: {score}/10

Issues:
{', '.join(issues) if issues else 'None'}

Suggestions:
- Improve bounce rate
- Optimize navigation
- Enhance product engagement
"""

            st.download_button("📥 Download Report", report, file_name="ux_report.txt")

        else:
            st.error("❌ Required columns missing (BounceRates, ExitRates, ProductRelated)")