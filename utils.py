def extract_features(url, vectorizer=None):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()
        images = len(soup.find_all("img"))
        links = len(soup.find_all("a"))

        lh_metrics = run_lighthouse(url)

        # --- MAP to MODEL FEATURES ---
        session_duration = len(text) / 50  # proxy
        ctr = min(links / 10, 100)  # proxy %
        bounce_rate = max(100 - lh_metrics["Performance"], 0)  # inverse proxy
        pages_viewed = max(1, links // 5)

        features = pd.DataFrame([{
            "Session_Duration (seconds)": session_duration,
            "CTR (%)": ctr,
            "Bounce_Rate (%)": bounce_rate,
            "Pages_Viewed": pages_viewed
        }])
        return features, {
            "URL": url,
            "Images": images,
            "Links": links,
            **lh_metrics,
            "TextLength": len(text)
        }

    except Exception as e:
        print(f"Error extracting features for {url}: {e}")
        return None, None