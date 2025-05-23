
# 🛍️ Shopping Assistant AI

A conversational shopping assistant built with LangGraph, Tavily Search, and Groq’s LLaMA. This intelligent agent searches for product information, summarizes and recommends options, and integrates human feedback to refine its suggestions using Retrieval-Augmented Generation (RAG) and AI reasoning.

## 🚀 Features

- 🔎 Product search via Tavily API
- 🧠 Summary and recommendation generation using Groq’s LLaMA 3.1
- 🙋 Human-in-the-loop approval with feedback refinement
- 🔁 LangGraph-powered state management with refinement loop
- 🖥️ Streamlit interface for interactive user experience

## 📸 Demo Preview

<img width="842" alt="Screenshot 2025-05-23 at 6 50 44 PM" src="https://github.com/user-attachments/assets/0f30de03-2083-4b76-8153-273d78f51947" />




<img width="1440" alt="Screenshot 2025-05-23 at 6 51 26 PM" src="https://github.com/user-attachments/assets/2f63c64d-036e-4db7-9447-dd687ffdf63e" />







## 🛠️ Tech Stack

- **AI & LLM**: LangChain, ChatGroq (LLaMA 3.1)
- **Search**: Tavily API
- **Graph Logic**: LangGraph (StateGraph)
- **Frontend**: Streamlit
- **Language**: Python

## 📂 Project Structure

```
shopping-assistant-ai/
│
├── mini_project-1_Iwu.py                     # Main Streamlit + LangGraph implementation
├── requirements.txt
└── README.md
```

## ⚙️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/shopping-assistant-ai.git
cd shopping-assistant-ai
```

2. Set up your virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables for your API keys:

```bash
export GROQ_API_KEY=your_groq_api_key
export TAVILY_API_KEY=your_tavily_api_key
```

5. Launch the app:

```bash
streamlit run mini_project-1_Iwu.py
```

## ✅ Strengths

- Real-time product search with AI-based summarization
- Human approval workflow integrated via LangGraph
- Feedback-driven recommendation refinement
- Easy-to-use Streamlit interface

## ⚠️ Limitations

- Results depend on Tavily API search quality
- LLM-generated summaries may require user validation
- Feedback refinement relies on Groq LLM output, which may vary

## 📄 License

MIT License — free to use, modify, and share.

## 👤 Author

**Chibuike Iwu**  

# ShoppingAssistantAI
