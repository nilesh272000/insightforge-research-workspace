# InsightForge — Multi-Agent Research Workspace

InsightForge is a multi-agent AI research workspace built with Python,
Streamlit, and LangChain.

It uses a structured research pipeline to search for information,
extract useful source content, generate a research report, and evaluate
the resulting report.

## Features

- 🔎 Automated research and web search
- 📄 Source content extraction
- ✍️ AI-generated research reports
- 🧐 Automated report quality review
- 📥 Markdown report download
- 🎨 Streamlit-based research workspace

## Architecture

The application follows a four-stage pipeline:

1. **Search Agent** — discovers relevant information
2. **Reader Agent** — extracts useful source content
3. **Writer Chain** — generates the research report
4. **Critic Chain** — reviews the generated report

## Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph / agent-based workflow
- LLM APIs
- Web search and content extraction

## Project Structure

```text
insightforge-research-workspace/
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.mdgit status