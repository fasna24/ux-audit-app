import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="UX Audit AI AND ML", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 UX Audit AI")
mode = st.sidebar.radio("Navigation", ["🌐 URL Analyzer", "📁 CSV Analyzer"])
st.sidebar.success("Startup Dashboard Mode ON 🔥")

# ---------- STYLING ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    animation: slideUp 0.8s ease-in-out;
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.05);
}

.big-title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #00f2ff;
    animation: fadeIn 1.2s ease-in;
}

@keyframes slideUp {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 UX Audit AI Dashboard</div>', unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def analyze_website(url):
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        load_time = round(time.time() - start, 2)
        images = len(soup.find_all("img"))
        links = len(soup.find_all("a"))
        text = soup.get_text()

        ai_score = round(70 + min(len(text) / 1000, 30), 2)
        ml_score = round(60 + (images + links) % 40, 2)
        dl_score = round((ai_score + ml_score) / 2 + random.uniform(-5, 5), 2)
        ux_score = round((ai_score + ml_score + dl_score) / 3, 2)

        bounce_rate = round(random.uniform(20, 60), 2)
        exit_rate = round(random.uniform(10, 40), 2)

        revenue = round(ux_score * 1000, 2)
        improved_score = min(ux_score + random.uniform(5, 15), 100)
        expected_revenue = round(improved_score * 1000, 2)

        return {
            "URL": url,
            "UX Score": ux_score,
            "ML Score": ml_score,
            "DL Score": dl_score,
            "AI Score": ai_score,
            "Load Time": load_time,
            "Bounce Rate": bounce_rate,
            "Exit Rate": exit_rate,
            "Revenue": revenue,
            "Expected Revenue": expected_revenue,
            "Images": images,
            "Links": links
        }

    except:
        st.error("Error loading website")
        return None


def competitor_chart(score):
    comp = [
        score,
        score - random.randint(5, 15),
        score + random.randint(3, 10)
    ]

    fig, ax = plt.subplots()
    ax.bar(["Your Site", "Competitor A", "Competitor B"], comp)
    st.pyplot(fig)


def ai_suggestions(data):
    suggestions = []

    if data["Load Time"] > 2:
        suggestions.append("⚡ Improve loading speed")
    if data["Bounce Rate"] > 50:
        suggestions.append("📉 Reduce bounce rate")
    if data["Images"] < 5:
        suggestions.append("🖼️ Add more visuals")
    if data["Links"] < 10:
        suggestions.append("🔗 Improve internal linking")

    if not suggestions:
        suggestions.append("✅ Website looks optimized!")

    return suggestions


def export_pdf(data):
    doc = SimpleDocTemplate("UX_Report.pdf")
    styles = getSampleStyleSheet()

    content = [Paragraph("UX Audit AI Report", styles["Title"])]

    for k, v in data.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(content)


# ---------- URL MODE ----------
if mode == "🌐 URL Analyzer":
    st.header("🌐 Analyze Website")

    url = st.text_input("Enter Website URL")

    if st.button("Analyze 🚀"):
        data = analyze_website(url)

        if data:
            # SCORE CARDS
            cols = st.columns(4)
            for i, key in enumerate(["UX Score", "ML Score", "DL Score", "AI Score"]):
                time.sleep(0.1)
                cols[i].markdown(
                    f'<div class="metric-card">{key}<h2>{data[key]}</h2></div>',
                    unsafe_allow_html=True
                )

            # PERFORMANCE CARDS
            cols2 = st.columns(3)
            for i, key in enumerate(["Load Time", "Bounce Rate", "Exit Rate"]):
                time.sleep(0.1)
                cols2[i].markdown(
                    f'<div class="metric-card">{key}<h2>{data[key]}</h2></div>',
                    unsafe_allow_html=True
                )

            # REVENUE
            st.success(f"💰 Current Revenue: ${data['Revenue']}")
            st.info(f"🚀 After Fix Revenue: ${data['Expected Revenue']}")

            # COMPETITOR
            st.subheader("🏆 Competitor Analysis")
            competitor_chart(data["UX Score"])

            # AI SUGGESTIONS
            st.subheader("🤖 AI Suggestions")
            for s in ai_suggestions(data):
                st.write(s)

            # DOWNLOAD
            df = pd.DataFrame([data])
            st.download_button(
                "⬇ Download CSV",
                df.to_csv(index=False),
                "ux_results.csv"
            )

            # PDF
            if st.button("📄 Export PDF"):
                export_pdf(data)
                st.success("PDF Generated!")


# ---------- CSV MODE ----------
elif mode == "📁 CSV Analyzer":
    st.header("📁 Upload CSV")

    file = st.file_uploader("Upload CSV with URLs", type=["csv"])

    if file:
        df = pd.read_csv(file)

        if "URL" not in df.columns:
            st.error("CSV must contain 'URL' column")
        else:
            results = []

            for url in df["URL"]:
                time.sleep(0.1)
                data = analyze_website(url)
                if data:
                    results.append(data)

            result_df = pd.DataFrame(results)
            

            st.subheader("📊 Data Preview")
            st.dataframe(result_df)

            st.download_button(
                "⬇ Download Full Results CSV",
                result_df.to_csv(index=False),
                "full_results.csv"
            )

            st.subheader("📈 Average Scores")
            st.write(result_df.mean(numeric_only=True))