from dotenv import load_dotenv
import os
load_dotenv()
pem = os.getenv("PEM_FILE")
app_id = os.getenv("GITHUB_APP_ID")
open_ai_api_key = os.getenv("OPENAI_API_KEY")
