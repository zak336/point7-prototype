# Point7 — Natural-language workflow builder (early prototype)

This version upgrades the Gemini-powered enquiry demo into a small reusable workflow builder.

## What works
- User describes an agent in natural language.
- Gemini creates a structured workflow plan.
- Point7 validates plan shape, supported operations, unique IDs, and sequential dependencies.
- A reusable executor calls Gemini for each supported step and passes step outputs to downstream steps.
- Step results/errors are shown and can be exported as JSON.

## Supported operations
`classify_text`, `detect_urgency`, `analyze_sentiment`, `summarize_text`, `extract_fields`, `draft_reply`, `recommend_action`.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Configure Streamlit Secrets or environment variables:
```toml
GEMINI_API_KEY = "your-key"
MODEL_NAME = "gemini-3.1-flash-lite"
```

## Deploy to Streamlit Community Cloud
Replace `app.py` and `requirements.txt` in the GitHub repository connected to your Streamlit app, commit/push to the configured branch, and let Streamlit redeploy. Keep the key in Streamlit Secrets, never in GitHub.

## Important limitations
This is an early prototype. It only processes text pasted by the user and only executes the allowlisted operations. It does not connect to inboxes, send emails, execute arbitrary code, persist agents, or integrate external tools. Planning uses one Gemini request and every step uses another request; quotas and costs may apply. Review outputs for accuracy before use.
