import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.ensemble import RandomForestRegressor
import numpy as np

st.set_page_config(page_title="UX Audit AI & ML", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Advanced UX Audit System for Website Analysis")
mode = st.sidebar.radio("Navigation", ["🌐 URL Analyzer", "📁 CSV Analyzer"])
st.sidebar.success("Startup Dashboard Mode ON 🔥")

# ---------- STYLING ----------
st.markdown("""
<style>
body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
.metric-card { padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #1f4037, #99f2c8); text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3); transition: transform 0.3s ease; }
.metric-card:hover { transform: translateY(-10px) scale(1.05); }
.big-title { text-align: center; font-size: 34px; font-weight: bold; color: #00f2ff; }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="big-title">🚀 UX Audit AI Dashboard</div>', unsafe_allow_html=True)

# ---------- HELPER FUNCTIONS ----------

def analyze_website(url):
    """Scrape basic features from a website"""
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        load_time = round(time.time() - start, 2)
        images = len(soup.find_all("img"))
        links = len(soup.find_all("a"))
        text = soup.get_text()
        text_length = len(text)

        # Bounce rate simulated
        bounce_rate = round(random.uniform(20, 60), 2)

        return {
            "URL": url,
            "Load Time": load_time,
            "Images": images,
            "Links": links,
            "Text Length": text_length,
            "Bounce Rate": bounce_rate
        }

    except:
        st.error(f"Error loading website: {url}")
        return None

def train_demo_ml_model(df):
    """Train a RandomForestRegressor on demo data"""
    features = ["Load Time", "Images", "Links", "Text Length", "Bounce Rate"]
    X = df[features]
    y = df["UX Score"]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_ux_score(model, data):
    features = ["Load Time", "Images", "Links", "Text Length", "Bounce Rate"]
    X = pd.DataFrame([data])[features]
    score = model.predict(X)[0]
    return round(score, 2)

def competitor_chart(your_score, comp_scores=None):
    if not comp_scores:
        comp_scores = [your_score - random.randint(5,15), your_score + random.randint(3,10)]
    fig, ax = plt.subplots()
    ax.bar(["Your Site", "Competitor A", "Competitor B"], [your_score]+comp_scores, color=["#00f2ff","#ff6f61","#ffa500"])
    st.pyplot(fig)

def ai_suggestions(data):
    """Simple feature-based suggestions"""
    suggestions = []
    if data["Load Time"] > 2:
        suggestions.append("⚡ Improve loading speed (below 2s recommended)")
    if data["Bounce Rate"] > 50:
        suggestions.append("📉 Reduce bounce rate with engaging content")
    if data["Images"] < 5:
        suggestions.append("🖼️ Add more visuals to increase engagement")
    if data["Links"] < 10:
        suggestions.append("🔗 Improve internal linking for better navigation")
    if not suggestions:
        suggestions.append("✅ Website looks optimized!")
    return suggestions

def export_pdf(data):
    doc = SimpleDocTemplate("UX_Report.pdf")
    styles = getSampleStyleSheet()
    content = [Paragraph("UX Audit AI Report", styles["Title"])]
    for k,v in data.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))
    doc.build(content)

# ---------- DEMO ML DATA ----------
# For now, we train a simple demo model on synthetic data
demo_data = pd.DataFrame({
    "Load Time": np.random.uniform(0.5,3.5,50),
    "Images": np.random.randint(1,15,50),
    "Links": np.random.randint(5,30,50),
    "Text Length": np.random.randint(500,5000,50),
    "Bounce Rate": np.random.uniform(20,60,50),
    "UX Score": np.random.uniform(50,100,50)
})
ml_model = train_demo_ml_model(demo_data)

# ---------- URL ANALYZER ----------
if mode == "🌐 URL Analyzer":
    st.header("🌐 Analyze Website")
    url = st.text_input("Enter Website URL")

    if st.button("Analyze 🚀"):
        data = analyze_website(url)
        if data:
            # ML predicted UX score
            ux_score = predict_ux_score(ml_model, data)
            data["UX Score"] = ux_score

            # Score cards
            cols = st.columns(2)
            cols[0].markdown(f'<div class="metric-card">UX Score<h2>{ux_score}</h2></div>', unsafe_allow_html=True)
            cols[1].markdown(f'<div class="metric-card">Bounce Rate<h2>{data["Bounce Rate"]}</h2></div>', unsafe_allow_html=True)

            # Competitor comparison
            st.subheader("🏆 Competitor Analysis")
            competitor_chart(ux_score)

            # AI suggestions
            st.subheader("🤖 AI Suggestions")
            for s in ai_suggestions(data):
                st.write(s)

            # CSV download
            df = pd.DataFrame([data])
            st.download_button("⬇ Download CSV", df.to_csv(index=False), "ux_results.csv")

            # PDF export
            if st.button("📄 Export PDF"):
                export_pdf(data)
                st.success("PDF Generated!")

# ---------- CSV ANALYZER ----------
elif mode == "📁 CSV Analyzer":
    st.header("📁 Upload CSV")
    file = st.file_uploader("Upload CSV with URLs", type=["csv"])

    if file:
        df = pd.read_csv(file)
        if "URL" not in df.columns:
            st.error("CSV must contain 'URL' column")
        else:
            results = []
            st.info("🔄 Running analysis on dataset...")
            for url in df["URL"]:
                with st.spinner(f"Analyzing {url}..."):
                    time.sleep(0.2)
                    data = analyze_website(url)
                    if data:
                        data["UX Score"] = predict_ux_score(ml_model, data)
                        results.append(data)
            result_df = pd.DataFrame(results)

            # Data preview
            st.subheader("📊 Data Preview")
            st.dataframe(result_df)

            # CSV download
            st.download_button("⬇ Download Full Results CSV", result_df.to_csv(index=False), "full_results.csv")

            # Average metrics
            st.subheader("📈 Average Scores")
            st.write(result_df.mean(numeric_only=True))

            # Pie chart - UX distribution
            st.subheader("🥧 UX Score Distribution")
            bins = ["Low","Medium","High"]
            ux_levels = pd.cut(result_df["UX Score"], bins=[0,50,75,100], labels=bins, include_lowest=True)
            pie_data = ux_levels.value_counts().reindex(bins, fill_value=0)
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

            # Bar chart comparison
            st.subheader("📊 Score Comparison")
            chart_data = result_df[["UX Score"]].astype(float)
            st.bar_chart(chart_data)

            # Competitor comparison (average)
            st.subheader("🏆 Competitor Analysis (Dataset Avg)")
            competitor_chart(result_df["UX Score"].mean())

            # AI suggestions (overall)
            st.subheader("🤖 AI Suggestions (Overall)")
            sample = result_df.iloc[0].to_dict()
            for s in ai_suggestions(sample):
                st.write(s)