# Point7 — Gemini-powered customer enquiry prototype

This Streamlit prototype makes a real call to the Google Gemini Developer API to classify a customer enquiry, draft a reply, recommend a next action, and return structured JSON. No emails are sent and no inbox/CRM is connected.

## Recommended model

Default: `gemini-3.1-flash-lite`, selected for cost efficiency and routine classification/drafting. Model availability and free-tier limits can change; verify the model is available in your Google AI Studio account. If unavailable, set `MODEL_NAME` to a supported Flash-Lite model shown in the official Gemini API model list.

## Deploy on Streamlit Community Cloud

1. Extract this ZIP.
2. In the GitHub repository connected to your Streamlit app, replace `app.py` and `requirements.txt` with the files in `Point7_Real_Prototype/`.
3. In Streamlit Community Cloud, open **App settings → Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your-Gemini-API-key"
   MODEL_NAME = "gemini-3.1-flash-lite"
   ```

4. Save secrets. Commit and push the updated files to the branch used by the app, then wait for redeployment.
5. Run a test enquiry. Confirm the app shows a live result and model name.

Create/check the API key in Google AI Studio: https://aistudio.google.com/apikey

## Security and limitations

- Never commit the API key to GitHub or paste it into chat.
- Free tier has quotas/rate limits and may change; a free-tier key is not a guarantee of unlimited use.
- Google documents that content on the Gemini API free tier may be used to improve its products. Do not submit real sensitive customer data on the free tier; use anonymized demo enquiries.
- The app makes one model call per enquiry and validates the output structure. It does not verify factual correctness.
- No email sending, inbox/CRM integration, order lookup, persistent database, multi-agent execution, or automatic model routing is implemented.
- Keep human review before using any drafted reply.
