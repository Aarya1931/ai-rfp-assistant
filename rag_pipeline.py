from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

from langchain_core.prompts import PromptTemplate

def load_prompt(path):
    with open(path, encoding="utf-8") as f:
        return PromptTemplate.from_template(f.read())


def run_all(rfp_text, company_text):
    results = {}

    summary_prompt = load_prompt("prompts/summary_prompt.txt")
    results["summary"] = (summary_prompt | llm).invoke({"rfp": rfp_text, "company": company_text})

    eligibility_prompt = load_prompt("prompts/eligibility_prompt.txt")
    results["eligibility"] = (eligibility_prompt | llm).invoke({"rfp": rfp_text, "company": company_text})

    structure_prompt = load_prompt("prompts/structure_prompt.txt")
    results["structure"] = (structure_prompt | llm).invoke({"rfp": rfp_text, "company": company_text})

    improvement_prompt = load_prompt("prompts/improvement_prompt.txt")
    results["improvement"] = (improvement_prompt | llm).invoke({"rfp": rfp_text, "company": company_text})

    recommendations_prompt = load_prompt("prompts/recommendations_prompt.txt")
    results["recommendations"] = (recommendations_prompt | llm).invoke({"rfp": rfp_text, "company": company_text})

    proposal_prompt = load_prompt("prompts/proposal_prompt.txt")
    results["proposal_draft"] = (proposal_prompt | llm).invoke({
        "summary": results["summary"],
        "rfp": rfp_text,
        "improvements": results["improvement"],
        "company": company_text
    })

    polish_prompt = load_prompt("prompts/polish_prompt.txt")
    results["final_proposal"] = (polish_prompt | llm).invoke({
    "agency": agency,
    "rfp_number": rfp_number,
    "title": title,
    "rfp_instructions": rfp_instructions,
    "company": company_profile,
    "improvements": results["improvements"]
})



    return results
