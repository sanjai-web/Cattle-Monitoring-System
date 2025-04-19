import firebase_admin
from firebase_admin import credentials, db
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred = credentials.Certificate(os.path.join(BASE_DIR, 'config/serviceAccountKey.json'))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cattle-83fee-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
