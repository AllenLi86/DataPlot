from flask import Flask, request, jsonify

app = Flask(__name__)

# Basic GET only route
@app.route('/get-only')
def get_only():
    return 'This only handles GET requests'

# Test jsonify
@app.route('/JJJ', methods=['GET']) 
def index():
    response = jsonify({'maaassage': 'welcome'})
    return response

# Specify multiple methods
@app.route('/user', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        data = request.json
        return jsonify({"message": "User created", "data": data})
    return jsonify({"message": "Here's the user data"})

# POST only route
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    return jsonify({"received": data})

# Handle form data
@app.route('/form', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        print(jsonify({"received": username}))
        return f"Received: {username}, {email}"
    return '''
        <form method="post">
            <input type="text" name="username">
            <input type="email" name="email">
            <input type="submit">
        </form>
    '''

# URL parameters with both GET and POST
@app.route('/product/<id>', methods=['GET', 'POST'])
def handle_product(id):
    if request.method == 'POST':
        return f"Updating product {id}"
    return f"Viewing product {id}"

# Multiple URL parameters
@app.route('/user/<user_id>/posts/<post_id>', methods=['GET', 'POST', 'DELETE'])
def handle_user_post(user_id, post_id):
    if request.method == 'POST':
        return f"Creating post {post_id} for user {user_id}"
    elif request.method == 'DELETE':
        return f"Deleting post {post_id} for user {user_id}"
    return f"Viewing post {post_id} from user {user_id}"

if __name__ == '__main__':
    app.run(debug=True)