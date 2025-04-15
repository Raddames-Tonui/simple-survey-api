import firebase_admin
from firebase_admin import credentials, storage
import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load base64 credentials from environment
firebase_credentials_b64 = os.getenv("FIREBASE_CREDENTIALS_B64")
if not firebase_credentials_b64:
    raise ValueError("FIREBASE_CREDENTIALS_B64 is not set in .env")

# Decode and load JSON
firebase_credentials_json = json.loads(base64.b64decode(firebase_credentials_b64).decode("utf-8"))

# Initialize Firebase app
cred = credentials.Certificate(firebase_credentials_json)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sheria-365.appspot.com'
})
