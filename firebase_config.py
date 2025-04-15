import firebase_admin
from firebase_admin import credentials, storage
import os

# Absolute path to the service account
cred_path = os.path.join(os.path.dirname(__file__), 'secrets', 'jazaform_firebase_secrets.json')

# Initialize Firebase app
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sheria-365.appspot.com'
})
