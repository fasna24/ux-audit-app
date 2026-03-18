import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="UX Audit System", layout="wide")

# Title
st.title("🚀 Hybrid Website UX & Conversion Audit System")

# Sidebar
st.sidebar.header("Navigation")
option = st.sidebar.radio("Choose Input Type", ["Upload Dataset", "Enter Website URL"])

# -------------------------------
# OPTION 1: DATASET UPLOAD
# -------------------------------
if option == "Upload Dataset":
    st.subheader("📊 Upload Website Analytics Dataset")

    file = st.file_uploader("Upload CSV File", type=["csv"])

    if file is not None:
        data = pd.read_csv(file)

        # Preview
        st.write("### Dataset Preview")
        st.dataframe(data.head())

        # -------------------------------
        # MACHINE LEARNING MODEL
        # -------------------------------
        if 'Revenue' in data.columns:
            st.write("### 🤖 AI Prediction Model")

            data['Revenue'] = data['Revenue'].astype(int)

            features = ['Administrative', 'Informational', 'ProductRelated', 'BounceRates', 'ExitRates']

            # Make sure required columns exist
            if all(col in data.columns for col in features):
                X = data[features]
                y = data['Revenue']

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

                model = RandomForestClassifier()
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)

                st.metric("Model Accuracy", round(acc, 2))

        # -------------------------------
        # BASIC STATS
        # -------------------------------
        st.write("### 📊 Basic Statistics")
        st.write(data.describe())

        # -------------------------------
        # UX METRICS
        # -------------------------------
        bounce_rate = 0
        exit_rate = 0

        if 'BounceRates' in data.columns:
            bounce_rate = data['BounceRates'].mean()
            st.metric("Average Bounce Rate", round(bounce_rate, 2))

        if 'ExitRates' in data.columns:
            exit_rate = data['ExitRates'].mean()
            st.metric("Average Exit Rate", round(exit_rate, 2))

        # -------------------------------
        # UX SCORE SYSTEM
        # -------------------------------
        score = 10
        issues = []

        if bounce_rate > 0.5:
            score -= 3
            issues.append("High Bounce Rate")

        if exit_rate > 0.5:
            score -= 2
            issues.append("High Exit Rate")

        if 'ProductRelated' in data.columns:
            if data['ProductRelated'].mean() < 20:
                score -= 2
                issues.append("Low Product Engagement")

        # Score display
        st.write("### 🎯 UX Score")
        st.metric("UX Score (out of 10)", score)

        # Issues
        if issues:
            st.error("⚠️ Issues Found:")
            for i in issues:
                st.write(f"- {i}")
        else:
            st.success("✅ Excellent UX")

        # -------------------------------
        # SOLUTIONS (UPGRADED)
        # -------------------------------
        st.write("### 💡 UX Improvement Solutions")

        if "High Bounce Rate" in issues:
            st.error("🔴 High Bounce Rate Solutions")
            st.write("- Improve page loading speed (optimize images, caching)")
            st.write("- Add strong headline & clear value proposition")
            st.write("- Improve mobile responsiveness")
            st.write("- Reduce clutter and improve layout")
            st.write("- Add clear Call-To-Action (CTA)")

        if "High Exit Rate" in issues:
            st.error("🟠 High Exit Rate Solutions")
            st.write("- Simplify checkout process")
            st.write("- Reduce form fields")
            st.write("- Add trust badges & reviews")
            st.write("- Provide offers/discounts")
            st.write("- Improve navigation flow")

        if "Low Product Engagement" in issues:
            st.error("🟡 Low Product Engagement Solutions")
            st.write("- Use high-quality product images")
            st.write("- Add detailed descriptions")
            st.write("- Show ratings & reviews")
            st.write("- Add product demo videos")
            st.write("- Recommend related products")

        if not issues:
            st.success("✅ Your UX is strong. Keep optimizing!")

        # -------------------------------
        # VISUALIZATION
        # -------------------------------
        if 'BounceRates' in data.columns:
            st.write("### 📈 Bounce Rate Distribution")
            fig, ax = plt.subplots()
            ax.hist(data['BounceRates'], bins=20)
            st.pyplot(fig)

            if bounce_rate > 0.5:
                st.error("⚠️ High Bounce Rate → Poor UX")
            else:
                st.success("✅ Users are engaging well")

# -------------------------------
# OPTION 2: WEBSITE URL
# -------------------------------
else:
    st.subheader("🌐 Analyze Website UX")

    url = st.text_input("Enter Website URL")

    if st.button("Analyze"):
        if url:
            st.write(f"Analyzing: {url}")

            # Dummy values (can upgrade later)
            load_time = 4.5
            bounce_rate = 0.65

            st.metric("Page Load Time (s)", load_time)
            st.metric("Bounce Rate", bounce_rate)

            if load_time > 3:
                st.warning("⚠️ Slow Website → Improve speed (optimize images, hosting)")

            if bounce_rate > 0.5:
                st.error("⚠️ High Bounce Rate → Improve content & UX")

            st.success("💡 Suggestions:")
            st.write("- Improve loading speed")
            st.write("- Simplify navigation")
            st.write("- Reduce clutter")