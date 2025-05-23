from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults


import requests
import streamlit as st






import os
os.environ["GROQ_API_KEY"] = ""



os.environ["TAVILY_API_KEY"] = ""

response = requests.post(
    "https://api.tavily.com/search",
    headers={
        "Authorization": f"Bearer {os.getenv('TAVILY_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={"query": "test", "max_results": 1}
)
print(response.status_code, response.json())


from langchain_community.tools.tavily_search import TavilySearchResults


# ---- State Definition ----
class ShoppingState(TypedDict):
    query: str
    product_data: Optional[list]
    summary: Optional[str]
    user_decision: Optional[str]
    feedback: Optional[str]  # For user feedback


# ---- Tavily Product Search Node ----
def search_products(state: ShoppingState) -> ShoppingState:
    """Search for products using Tavily API."""
    query = state["query"]
    api_key = os.getenv("TAVILY_API_KEY")
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json" }
    payload = {"query": query,
               "max_results": 3,
               "search_depth": "basic",
               "include_answer": False
               }


    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json().get("results", [])
    except requests.RequestException as e:
        results = ["API Error: " + str(e)]
        print(f"API Error: {e}")

    return {**state, "product_data": results}


# ---- Summary Generation using Groq ----
def generate_summary(state: ShoppingState) -> ShoppingState:
    """Generate a summary and recommendation using Groq."""
    client = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")
    products = state["product_data"]
    prompt = ChatPromptTemplate.from_template("""
    Based on the following product search results, summarize and recommend the best option: {products}
    """)
    chain = prompt | client
    result = chain.invoke({"products": str(products)})
    return {**state, "summary": result.content}


# ---- Human Approval Node ----
def human_approval(state: ShoppingState) -> ShoppingState:
    """Collect user decision and feedback."""
    print(f"\n*** Human Review ***\nQuery: {state['query']}\nSummary: {state['summary']}\n")

    decision = input("Approve recommendation? (y/n): ").lower().strip()
    feedback = input("Provide feedback (press enter to skip): ") if decision == 'n' else ""

    return {
        "user_decision": decision == "y",
        "feedback": feedback
    }


# ---- Refine Recommendation Node ----
def refine_recommendation(state: ShoppingState) -> ShoppingState:
    """Improve recommendation using user feedback."""
    prompt = ChatPromptTemplate.from_template(
        "Improve this product recommendation using human feedback:\n"
        "Original Query: {query}\n"
        "Initial Summary: {summary}\n"
        "Feedback: {feedback}\n"
        "Revised Recommendation:"
    )

    client = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")
    chain = prompt | client

    refined = chain.invoke({
        "query": state.get("query", ""),
        "summary": state.get("summary", ""),
        "feedback": state.get("feedback", "")
    }).content

    return {
        "summary": refined
    }


# ---- LangGraph Construction ----
graph = StateGraph(ShoppingState)

# Add nodes
graph.add_node("search", RunnableLambda(search_products))
graph.add_node("summarize", RunnableLambda(generate_summary))
graph.add_node("human_approval", RunnableLambda(human_approval))
graph.add_node("refine_recommendation", RunnableLambda(refine_recommendation))

# Set up main flow
graph.set_entry_point("search")
graph.add_edge("search", "summarize")
graph.add_edge("summarize", "human_approval")


# Conditional edges for approval routing
def route_approval(state: ShoppingState) -> str:
    """Decide next step based on user decision."""
    if state["user_decision"]:
        return "approve"
    else:
        return "refine"


graph.add_conditional_edges(
    "human_approval",
    route_approval,
    {
        "approve": END,
        "refine": "refine_recommendation"
    }
)

# Refinement loop
graph.add_edge("refine_recommendation", "human_approval")

app = graph.compile()

# ---- Streamlit UI ----
st.set_page_config(page_title="Shopping Assistant AI", page_icon=" ")
st.title(" Shopping Assistant AI")

query = st.text_input("Enter a product to search for:")
run_search = st.button("Search and Recommend")

if run_search and query:
    with st.spinner("Analyzing products using Tavily and Groq..."):
        final_state = app.invoke({"query": query})

    st.subheader(" AI Recommendation")
    st.write(final_state["summary"])

    decision = st.radio("Do you want to proceed with this recommendation?", ["Yes", "No"])
    st.success(f"Final Decision: {decision}")

    # Store user feedback for future improvements
    if decision == "No":
        feedback = st.text_input("Please provide feedback")
        st.write("Feedback recorded.")
