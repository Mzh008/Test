from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusqa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'missing fields'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'user exists'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'success': True})
    return jsonify({'error': 'invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/api/account', methods=['GET'])
@login_required
def account():
    return jsonify({'username': current_user.username})


@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    message = data.get('message', '')
    # Placeholder response: echo message
    response = {
        'reply': f"You said: {message}"
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
