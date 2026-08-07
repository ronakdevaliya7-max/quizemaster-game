from app import app, db
from models import User
from flask_login import login_user
with app.test_request_context():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    
    with client.session_transaction() as sess:
        sess['lang'] = 'gu'
        sess['_user_id'] = '1' # Assuming user ID 1 is admin
    
    response = client.get('/quiz/1')
    print("Status code:", response.status_code)
    if response.status_code == 302:
        print("Redirect Location:", response.headers['Location'])
    else:
        print("Length:", len(response.data))
        print(response.data.decode('utf-8')[:500])
