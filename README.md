# Point7 real AI workflow prototype

This Streamlit app makes a live call to a provider that supports the OpenAI-compatible Chat Completions API. It classifies a customer enquiry, drafts a reply, recommends a next action, validates required fields, and allows JSON export. It does not send emails or connect to a real inbox/CRM.

## Configure Streamlit Community Cloud

In your app's Streamlit Community Cloud page, open **App settings → Secrets** and add values from your provider dashboard:

```toml
API_KEY = "your-secret-key"
API_BASE_URL = "https://api.openai.com/v1"
MODEL_NAME = "your-exact-model-id"
```

- `API_KEY`: your provider's secret API key. Never commit it to GitHub or put it in app code.
- `API_BASE_URL`: provider's API base URL, usually ending in `/v1` for OpenAI-compatible services. Do not include `/chat/completions` at the end.
- `MODEL_NAME`: exact model identifier from the provider dashboard.

The example URL is for OpenAI only. If you do not know the provider, check the website where the key was created and its API documentation. This build does not automatically support every provider. Anthropic's native API, for example, needs a different request adapter unless you use an OpenAI-compatible gateway.

## Deploy the code

1. Back up the existing GitHub repository first.
2. Replace the app's `app.py` with this `app.py` and update `requirements.txt` from this folder.
3. Commit/push to the same branch and path used by Streamlit Community Cloud.
4. Add the three Secrets values in the Streamlit app settings, then reboot/redeploy the app.
5. Test with a sample customer enquiry. Confirm the app shows a real provider/model and a live result.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local development, put the same TOML keys in `.streamlit/secrets.toml` (do not commit that file) or export environment variables named `API_KEY`, `API_BASE_URL`, and `MODEL_NAME`.
