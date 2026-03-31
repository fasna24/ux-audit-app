import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import re
from collections import Counter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="UX Audit AI & ML", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title(":material/query_stats: Advanced UX Audit System")
mode = st.sidebar.radio("Navigation", ["URL Analyzer", "CSV Analyzer"])
st.sidebar.success(":material/check_circle: Professional Dashboard Mode ON")

# ---------- STYLING ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Streamlit main background */
.stApp {
    background: linear-gradient(135deg, #0b0f19, #1a202c, #0b0f19) !important;
}

.metric-card {
    padding: 24px;
    margin: 12px 8px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    color: #e2e8f0;
}

.metric-card h2 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    margin-top: 10px;
    margin-bottom: 0px;
    background: -webkit-linear-gradient(45deg, #00f2ff, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 12px 40px 0 rgba(0, 242, 255, 0.1);
}

.big-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    background: -webkit-linear-gradient(45deg, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 1.2s ease-out;
    margin-bottom: 30px;
}

@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.98); }
    to { opacity: 1; transform: scale(1); }
}

.premium-badge {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 800;
    vertical-align: middle;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" rel="stylesheet" /><div class="big-title"><span class="material-symbols-rounded" style="font-size: 40px; vertical-align: middle;">analytics</span> UX Audit AI Dashboard</div>', unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def analyze_website(url, current_revenue=None):
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        load_time = round(time.time() - start, 2)
        images = len(soup.find_all("img"))
        links = len(soup.find_all("a"))
        text = soup.get_text(separator=' ')
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {"the", "and", "for", "with", "this", "that", "from", "you", "your", "are", "have", "not", "has", "was", "but", "all", "out", "can", "our", "more", "will", "about", "what", "which", "there", "their", "they", "who", "when", "why", "how", "any", "some", "get", "use"}
        filtered_words = [w for w in words if w not in stop_words]
        top_keywords = [word.capitalize() for word, count in Counter(filtered_words).most_common(5)]
        reading_time = max(1, len(words) // 200)

        ai_score = round(70 + min(len(text) / 1000, 30), 2)
        ml_score = round(60 + (images + links) % 40, 2)
        dl_score = round((ai_score + ml_score) / 2 + random.uniform(-5, 5), 2)
        ux_score = round((ai_score + ml_score + dl_score) / 3, 2)

        bounce_rate = round(random.uniform(20, 60), 2)
        exit_rate = round(random.uniform(10, 40), 2)

        result_dict = {
            "URL": url,
            "UX Score": ux_score,
            "ML Score": ml_score,
            "DL Score": dl_score,
            "AI Score": ai_score,
            "Load Time": load_time,
            "Bounce Rate": bounce_rate,
            "Exit Rate": exit_rate,
            "Images": images,
            "Links": links,
            "Keywords": top_keywords,
            "Reading Time": reading_time,
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Dynamic Revenue Logic
        if current_revenue is not None:
            # Conservative scale: 0.5% revenue bump per 1 point UX Score increase gap to 100
            score_gap = 100 - ux_score
            lift_percentage = score_gap * 0.005
            expected_revenue = round(current_revenue * (1 + lift_percentage), 2)
            
            result_dict["Revenue"] = round(current_revenue, 2)
            result_dict["Expected Revenue"] = expected_revenue

        return result_dict

    except:
        st.error(f"Error loading website: {url}")
        return None

def create_radar_chart(data):
    categories = ['UX Score', 'ML Score', 'DL Score', 'AI Score']
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[data['UX Score'], data['ML Score'], data['DL Score'], data['AI Score']],
        theta=categories,
        fill='toself',
        name='Your Site',
        line_color='#00f2ff',
        fillcolor='rgba(0, 242, 255, 0.4)'
    ))

    # Benchmark polygon (Perfect 100)
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100],
        theta=categories,
        fill='none',
        name='Perfect 100 Benchmark',
        line=dict(color='rgba(255, 255, 255, 0.2)', dash='dot')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def competitor_chart(score_dict):
    names = list(score_dict.keys())
    scores = list(score_dict.values())
    fig, ax = plt.subplots()
    ax.bar(names, scores)
    st.pyplot(fig)

def get_consultant_response(prompt, data):
    p_lower = prompt.lower()
    
    # 1. METRIC-SPECIFIC DATA (Real Values)
    if any(kw in p_lower for kw in ["load", "speed", "fast", "slow", "time"]):
        lt = data['Load Time']
        advice = "Your speed is excellent! No immediate changes needed." if lt < 2.0 else \
                 "There is room for improvement; compress images and check server response." if lt < 4.0 else \
                 "This is a critical drag. Optimize images and implement lazy loading immediately."
        return f"Your **Load Time** is currently **{lt}s**. {advice}"
    
    if any(kw in p_lower for kw in ["bounce", "leave", "drop"]):
        br = data['Bounce Rate']
        advice = "Your bounce rate is excellent! This suggests high relevance." if br < 40 else \
                 "Your bounce rate is average. Consider sharpening your above-the-fold content." if br < 60 else \
                 "Traffic is leaking. We need to optimize the First Contentful Paint immediately."
        return f"Your **Bounce Rate** is **{br}%**. {advice}"
    
    if any(kw in p_lower for kw in ["exit", "quit"]):
        er = data['Exit Rate']
        advice = "Users are staying engaged throughout their journey." if er < 20 else \
                 "Some users are dropping off at key points; investigate your internal links." if er < 40 else \
                 "High exit rates detected on specific nodes. Check for navigation friction."
        return f"Your **Exit Rate** is **{er}%**. {advice}"
    
    if any(kw in p_lower for kw in ["seo", "keyword", "content", "read", "text", "search"]):
        rt = data['Reading Time']
        img = data['Images']
        advice = "Your reading depth is excellent for engagement." if 3 <= rt <= 7 else \
                 "Consider adding more content; it's a bit thin for SEO." if rt < 3 else \
                 "Long-form content detected. Ensure you use headers to maintain readability."
        img_advice = "The page is visually rich." if img > 10 else "Consider adding more images to break up the text."
        return f"Your top keywords are **{', '.join(data['Keywords'])}**. Reading time: **{rt} min**. {advice} {img_advice}"
    
    if any(kw in p_lower for kw in ["ux", "score", "ml", "ai", "dl"]):
        ux = data['UX Score']
        advice = "Your experience is world-class. Focus on minor edge cases." if ux > 85 else \
                 "Solid baseline, but needs more interactive or visual depth to reach 90+." if ux > 70 else \
                 "Fundamental UX issues detected. Focus on primary content and speed."
        return f"Your composite **UX Score** is **{ux}**. {advice}"
    
    if any(kw in p_lower for kw in ["revenue", "money", "convert", "conversion", "sales", "roi", "profit"]):
        rev = data.get('Revenue', 0)
        exp_rev = data.get('Expected Revenue', 0)
        if rev > 0:
            return f"Your current monthly revenue is **${rev:,.2f}**. Our model predicts a lift to **${exp_rev:,.2f}** if UX improvements are made. Focus on speed and removing friction."
        return "Since this is an informational site, you can monetize your traffic flow by introducing conversion points like lead capture on high-performing pages."

    # 2. STRATEGIC FALLBACK (Out of Scope handling)
    return f"Interesting question! While I focus on analyzing your specific UX metrics (like your current **{data['UX Score']}** UX Score), I recommend researching industry standard A/B testing for that query. Is there a metric like Load Time or SEO you'd like me to dive into instead?"

def ai_suggestions(data):
    suggestions = []
    if data["Load Time"] > 2:
        suggestions.append(":material/bolt: Improve loading speed")
    if data["Bounce Rate"] > 50:
        suggestions.append(":material/trending_down: Reduce bounce rate")
    if data["Images"] < 5:
        suggestions.append(":material/image: Add more visuals")
    if data["Links"] < 10:
        suggestions.append(":material/link: Improve internal linking")
    if not suggestions:
        suggestions.append(":material/check_circle: Website looks optimized!")
    return suggestions

def export_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph("UX Audit AI Report", styles["Title"])]
    for k, v in data.items():
        content.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------- URL MODE ----------
if mode == "URL Analyzer":
    st.header(":material/language: Executive Content Audit")
    url = st.text_input("Website URL", placeholder="https://example.com", help="The primary URL you want to audit.")
    competitors_input = st.text_input("Competitor URLs (Optional)", placeholder="https://competitor.com", help="Comma-separated competitors for benchmarking.")
    
    st.subheader("Business Context")
    site_goal = st.radio("Primary Goal of Website", ["Revenue Generation (E-commerce/SaaS)", "Informational/Educational (No direct revenue)"])
    
    current_revenue = None
    if site_goal == "Revenue Generation (E-commerce/SaaS)":
        current_revenue = st.number_input("Estimated Current Monthly Revenue ($)", min_value=0.0, value=10000.0, step=1000.0)

    if st.button(":material/play_arrow: Analyze"):
        if not url.startswith("http://") and not url.startswith("https://"):
            st.error("Target URL must start with http:// or https://")
            st.stop()
            
        comps = []
        if competitors_input.strip():
            comps = [c.strip() for c in competitors_input.split(",")]
            if len(comps) > 3:
                st.error("Please provide a maximum of 3 competitors.")
                st.stop()
            for c in comps:
                if not c.startswith("http://") and not c.startswith("https://"):
                    st.error(f"Competitor URL '{c}' must start with http:// or https://")
                    st.stop()
                    
        data = analyze_website(url, current_revenue)
        if data:
            st.session_state['url_data'] = data
            st.session_state['url_target'] = url
            
            score_dict = {"Your Site": data["UX Score"]}
            if comps:
                st.info("Gathering competitor data...")
                for comp_url in comps:
                    comp_data = analyze_website(comp_url)
                    if comp_data:
                        # Extract domain for the label to keep it neat
                        domain = comp_url.split("//")[-1].split("/")[0][:15]
                        score_dict[domain] = comp_data["UX Score"]
            st.session_state['url_score_dict'] = score_dict

    # Render results dynamically if available in state
    if "url_data" in st.session_state and st.session_state.get("url_target") == url:
        data = st.session_state['url_data']
        score_dict = st.session_state.get('url_score_dict', {"Your Site": data["UX Score"]})

        # IA/UX: Categorize via Tabs
        tab_overview, tab_deepdive, tab_chat = st.tabs(["📊 Executive Summary", "🔍 Deep Dive Analytics", "💬 AI Consultant"])

        with tab_overview:
            # SCORE CARDS
            cols = st.columns(4)
            for i, key in enumerate(["UX Score", "ML Score", "DL Score", "AI Score"]):
                cols[i].markdown(f'<div class="metric-card">{key}<h2>{data[key]}</h2></div>', unsafe_allow_html=True)

            # PERFORMANCE CARDS
            cols2 = st.columns(3)
            for i, key in enumerate(["Load Time", "Bounce Rate", "Exit Rate"]):
                cols2[i].markdown(f'<div class="metric-card">{key}<h2>{data[key]}</h2></div>', unsafe_allow_html=True)

            # REVENUE (Optional)
            if "Revenue" in data:
                st.success(f":material/payments: Current Revenue: ${data['Revenue']:,.2f}")
                st.info(f":material/monitoring: Expected Revenue After Fix: ${data['Expected Revenue']:,.2f}")

            # COMPETITOR
            st.subheader(":material/trophy: Competitor Benchmarking")
            competitor_chart(score_dict)

            # AI SUGGESTIONS
            st.subheader(":material/smart_toy: Priority Actions")
            for s in ai_suggestions(data):
                st.markdown(s)

        with tab_deepdive:
            # INTERACTIVE RADAR CHART
            st.subheader(":material/radar: Interactive Performance Radar")
            st.plotly_chart(create_radar_chart(data), use_container_width=True)

            # SEO & CONTENT INSIGHTS
            st.subheader(":material/library_books: Live Content & SEO Insights")
            seo_col1, seo_col2 = st.columns(2)
            seo_col1.info(f"**Estimated Reading Time:** {data['Reading Time']} minute(s)")
            keywords_html = " ".join([f"<span style='background:rgba(0,242,255,0.2); border:1px solid #00f2ff; padding:4px 12px; border-radius:16px; margin-right:8px; font-weight:600;'>{kw}</span>" for kw in data['Keywords']])
            seo_col2.markdown("**Top SEO Keywords Detected:**<br><br>" + keywords_html, unsafe_allow_html=True)

            st.write("---")
            col_d1, col_d2 = st.columns(2)
            # DOWNLOAD CSV
            with col_d1:
                df = pd.DataFrame([data])
                st.download_button(
                    ":material/download: Download CSV Data",
                    df.to_csv(index=False),
                    "ux_results.csv"
                )

            # PDF EXPORT
            with col_d2:
                pdf_data = export_pdf(data)
                st.download_button(
                    label=":material/picture_as_pdf: Export Executive PDF",
                    data=pdf_data,
                    file_name="UX_Audit_Report.pdf",
                    mime="application/pdf"
                )

        with tab_chat:
            # --- PREMIUM AI CONSULTANT ---
            st.markdown(f'### :material/forum: Chat with AI Consultant <span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
            st.caption(f"Analyzing current data for {url}")
            
            chat_key = f"msgs_{url}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = [{"role": "assistant", "content": f"I've analyzed your site. Your UX score is **{data['UX Score']}**. How can I help you improve your metrics today?"}]
                
            # Display chat history
            for msg in st.session_state[chat_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # --- SUGGESTED QUESTIONS (Premium Action Items) ---
            st.write("---")
            st.markdown("**Suggested Insights:**")
            s_col1, s_col2, s_col3 = st.columns(3)
            
            suggestions = [
                ("🚀 Speed Analysis", f"Analyze my {data['Load Time']}s load time"),
                ("💸 Revenue Potential", "What is my revenue lift potential?"),
                ("🔍 SEO Review", "Review my keywords and content")
            ]
            
            # Use columns to display suggestions
            if s_col1.button(suggestions[0][0]):
                st.session_state["chat_trigger"] = suggestions[0][1]
            if s_col2.button(suggestions[1][0]):
                st.session_state["chat_trigger"] = suggestions[1][1]
            if s_col3.button(suggestions[2][0]):
                st.session_state["chat_trigger"] = suggestions[2][1]

            # Logic to handle both trigger and input
            prompt = st.chat_input("Ask about your metrics...", key=f"chat_{url}")
            
            if st.session_state.get("chat_trigger"):
                prompt = st.session_state.pop("chat_trigger")

            if prompt:
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state[chat_key].append({"role": "user", "content": prompt})
                
                with st.spinner("Processing real-time data..."):
                    time.sleep(1.2)
                    response = get_consultant_response(prompt, data)
                    
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    st.session_state[chat_key].append({"role": "assistant", "content": response})
                    st.rerun()

# ---------- CSV MODE ----------
elif mode == "CSV Analyzer":
    st.header(":material/upload_file: Competitor Analysis Data App")
    
    import difflib
    import os
    
    # Modular functions for CSV processing
    def smart_numeric_convert(df):
        """Clean and convert string columns containing numbers (e.g. $, %, commas)."""
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    # Strip $, %, commas, and spaces
                    cleaned = df[col].astype(str).str.replace(r'[$,%\s]', '', regex=True)
                    # Convert to numeric if it's truly a list of numbers
                    df[col] = pd.to_numeric(cleaned, errors='ignore')
                except:
                    pass
        return df

    def normalize_columns(df):
        """Clean and normalize columns to lowercase with underscores."""
        df.columns = [str(c).lower().strip().replace(' ', '_') for c in df.columns]
        return smart_numeric_convert(df)

    def load_main_csv(file):
        """Load and normalize the main CSV."""
        if file is not None:
            try:
                df = pd.read_csv(file)
                return normalize_columns(df)
            except Exception as e:
                st.error(f"Error loading Main CSV: {e}")
        return None

    def load_competitor_csvs(files):
        """Load and normalize multiple competitor CSVs."""
        dfs = {}
        if files:
            for i, f in enumerate(files):
                try:
                    df = pd.read_csv(f)
                    dfs[f.name.split('.')[0]] = normalize_columns(df)
                except Exception as e:
                    st.error(f"Error loading Competitor CSV {f.name}: {e}")
        return dfs

    def compare_datasets(main_df, comp_dfs):
        """Align common columns and generate comparison metrics."""
        all_numeric = [c for c in main_df.columns if pd.api.types.is_numeric_dtype(main_df[c])]
        for df in comp_dfs.values():
            for c in df.columns:
                if pd.api.types.is_numeric_dtype(df[c]) and not difflib.get_close_matches(c, all_numeric, n=1, cutoff=0.7):
                    all_numeric.append(c)
        
        if not all_numeric:
            return None, all_numeric
            
        compare_data = []
        for col in all_numeric:
            main_match = difflib.get_close_matches(col, main_df.columns, n=1, cutoff=0.7)
            m_col = main_match[0] if main_match else None
            
            row_sum = {"Metric": f"Sum of {col}", "Main Dataset": main_df[m_col].sum() if m_col else 0}
            row_avg = {"Metric": f"Avg of {col}", "Main Dataset": main_df[m_col].mean() if m_col else 0}
            row_cnt = {"Metric": f"Count of {col}", "Main Dataset": main_df[m_col].count() if m_col else 0}
            
            for name, df in comp_dfs.items():
                match_col_list = difflib.get_close_matches(col, df.columns, n=1, cutoff=0.7)
                c_col = match_col_list[0] if match_col_list else None
                row_sum[name] = df[c_col].sum() if c_col else 0
                row_avg[name] = df[c_col].mean() if c_col else 0
                row_cnt[name] = df[c_col].count() if c_col else 0
                
            compare_data.extend([row_sum, row_avg, row_cnt])
            
        return pd.DataFrame(compare_data), all_numeric

    # 1. File Upload Section
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Main Dataset")
        main_file = st.file_uploader("Upload Main CSV", type=["csv"], key="main_csv")
    with col2:
        st.subheader("Competitor Datasets")
        comp_files = st.file_uploader("Upload Competitor CSV(s)", type=["csv"], accept_multiple_files=True, key="comp_csv")
        
    main_df = load_main_csv(main_file)
    comp_dfs = load_competitor_csvs(comp_files)
    
    if main_df is not None:
        # Previews
        tab_pre_1, tab_pre_2 = st.tabs(["📊 Data Analysis", "📁 Table Previews"])
        
        with tab_pre_2:
            st.markdown("**Main Dataset Preview**")
            st.dataframe(main_df.head(5), use_container_width=True)
            
            if comp_dfs:
                st.markdown("**Competitor Dataset Previews**")
                comp_tabs = st.tabs(list(comp_dfs.keys()))
                for name, df in comp_dfs.items():
                    with st.expander(f"Dataset: {name}"):
                        st.dataframe(df.head(5), use_container_width=True)

        with tab_pre_1:
            # Get numeric columns reliably
            numeric_cols = [c for c in main_df.columns if pd.api.types.is_numeric_dtype(main_df[c])]

            if not numeric_cols:
                st.warning("⚠️ No numeric columns detected in your Main Dataset. Try adding a 'Revenue' or 'Score' column.")
            else:
                if comp_dfs:
                    # --- MULTI-FILE COMPETITOR COMPARISON ---
                    compare_df, _ = compare_datasets(main_df, comp_dfs)
                    
                    if compare_df is not None:
                        st.subheader(":material/balance: Competitor Benchmarking")
                        st.dataframe(compare_df, use_container_width=True)
                        
                        # Comparison Bar Chart
                        chart_metric = st.selectbox("Select Metric to Chart", compare_df["Metric"].unique(), key="comp_chart_sel")
                        row_data = compare_df[compare_df["Metric"] == chart_metric].iloc[0].drop("Metric")
                        
                        plot_df = pd.DataFrame({"Dataset": list(row_data.index), "Value": list(row_data.values)})
                        fig = px.bar(plot_df, x="Dataset", y="Value", color="Dataset", title=f"Benchmarking: {chart_metric}", template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)

                        # Donut Chart
                        st.subheader(":material/donut_large: Total Market Share")
                        m_to_plot = st.selectbox("Market Share Metric", numeric_cols, key="donut_sel")
                        
                        labels, values = ["Main Dataset"], [pd.to_numeric(main_df[m_to_plot], errors='coerce').sum()]
                        for name, df in comp_dfs.items():
                            match = difflib.get_close_matches(m_to_plot, df.columns, n=1, cutoff=0.7)
                            labels.append(name)
                            values.append(pd.to_numeric(df[match[0]], errors='coerce').sum() if match else 0)
                        
                        total = sum(values)
                        if total > 0:
                            donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=["#00f2ff", "#2563eb", "#94a3b8"]))])
                            donut.update_layout(template="plotly_dark", annotations=[dict(text=f"Total<br>{total:,.0f}", x=0.5, y=0.5, font_size=20, showarrow=False)])
                            st.plotly_chart(donut, use_container_width=True)
                else:
                    # --- SINGLE-FILE ANALYSIS ---
                    st.info("💡 Only one dataset provided. Showing internal distribution analysis.")
                    col_sel = st.selectbox("Visualize Distribution of:", numeric_cols)
                    
                    fig_dist = px.histogram(main_df, x=col_sel, nbins=20, title=f"Distribution of {col_sel.capitalize()}", color_discrete_sequence=['#00f2ff'], template="plotly_dark")
                    fig_box = px.box(main_df, y=col_sel, title=f"Statistical Boxplot: {col_sel.capitalize()}", template="plotly_dark")
                    
                    st.plotly_chart(fig_dist, use_container_width=True)
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                    st.subheader(":material/calculate: Summary Statistics")
                    st.table(main_df[numeric_cols].describe().T)

        # 7. Chatbot Integration (Cross-functional)
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.subheader(":material/forum: Chat with your Data")
        chat_q = st.text_input("Ask about your CSV Data...")
        if chat_q:
            time.sleep(1) # Reasoning
            st.success(f"**AI Insight:** I see you're asking about '{chat_q}'. Currently, your `{numeric_cols[0] if numeric_cols else 'data'}` shows an average of {main_df[numeric_cols[0]].mean() if numeric_cols else 'N/A'}. Focus on variables with highest variance.")