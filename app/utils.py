import jwt
import os 
import time
from app import app
from app.models import User

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'timestamp': int(time.time())
    }
    token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
    return token

def check_token_expiry(timestamp):    
    return timestamp < int(time.time()) - 60 * 60 * 24

def verify_token(token):
    if not token:
        return 'Token is required'

    try:
        decoded_token = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        user_id = decoded_token['user_id']
        timestamp = decoded_token['timestamp']
        
        if check_token_expiry(timestamp):
            raise jwt.ExpiredSignatureError
        
        user = User.query.get(user_id)
        
        if not user:
            raise jwt.InvalidTokenError
        
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
    
    return user

def get_root_path():
    return app.root_path.replace("\\", "/").replace("app", "") + "/"

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS