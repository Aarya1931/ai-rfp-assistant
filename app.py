import streamlit as st
import os
import tempfile
from rag_pipeline import run_all
from utils.save_output import save_proposal_to_docx, convert_docx_to_pdf
from utils.document_loader import read_pdf, read_docx

st.set_page_config(page_title="AI RFP Assistant", layout="wide")
st.title("📄 AI RFP Assistant (LangChain + Ollama + RAG)")

st.markdown("Upload the **RFP Document** (PDF/DOCX) and **Company Info** (DOCX):")

# File Uploads
rfp_file = st.file_uploader("Upload RFP Document", type=["pdf", "docx"])
company_file = st.file_uploader("Upload Company Profile", type=["docx"])

if st.button("🚀 Run Analysis") and rfp_file and company_file:
    with st.spinner("Reading files..."):

        # Save temp files
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(rfp_file.name)[1]) as tmp_rfp:
            tmp_rfp.write(rfp_file.read())
            rfp_path = tmp_rfp.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_company:
            tmp_company.write(company_file.read())
            company_path = tmp_company.name

        # Read content
        rfp_text = read_pdf(rfp_path) if rfp_path.endswith(".pdf") else read_docx(rfp_path)
        company_text = read_docx(company_path)

    with st.spinner("Running RAG pipeline..."):
        results = run_all(rfp_text, company_text)  # <- We’ll modify this function next

        st.subheader("📌 RFP Summary")
        st.markdown(results["summary"])

        st.subheader("✅ Eligibility")
        st.markdown(results["eligibility"])

        st.subheader("📋 Structure Check")
        st.markdown(results["structure"])

        st.subheader("💡 Improvements")
        st.markdown(results["improvement"])

        st.subheader("🎯 Strategy Recommendations")
        st.markdown(results["recommendations"])

        st.subheader("📝 Final Polished Proposal")
        st.markdown(results["final_proposal"]['text'])

        docx_file = save_proposal_to_docx(results["final_proposal"]['text'])
        convert_docx_to_pdf(docx_file)

        with open("polished_proposal.docx", "rb") as f:
            st.download_button("📥 Download Proposal (DOCX)", f, file_name="proposal.docx")

        with open("polished_proposal.pdf", "rb") as f:
            st.download_button("📥 Download Proposal (PDF)", f, file_name="proposal.pdf")
