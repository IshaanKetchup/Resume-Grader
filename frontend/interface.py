import streamlit as st
import requests

st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("Resume Match Percentage Calculator")

job_desc = st.text_area("Paste Job Description Here:")
uploaded_files = st.file_uploader("📁 Upload Resumes", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

if st.button("Calculate"):
    if job_desc and uploaded_files:
        files = [('resumes', (f.name, f, f.type)) for f in uploaded_files]
        try:
            response = requests.post("https://resume-grader-r6xh.onrender.com", data={'job_desc': job_desc}, files=files)
            response.raise_for_status()
            results = response.json()

            for res in results:
                st.subheader(f"{res['filename']}")
                st.metric(label="Overall Match", value=f"{res['match_percent']}%")

                with st.expander("🔎 Section-wise Breakdown"):
                    section_scores = res.get("section_scores", {})
                    for section, score in section_scores.items():
                        st.write(f"**{section}**: {score}%")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except requests.exceptions.JSONDecodeError:
            st.error("Server response was not valid JSON.")
            st.text(response.text)
    else:
        st.warning("Please provide both a job description and at least one resume file.")
