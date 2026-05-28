from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json

    missing_fields = []

    if not data.get('title'):
        missing_fields.append('title')

    if not data.get('content'):
        missing_fields.append('content')

    if missing_fields:
        return jsonify(
            {'error': 'Invalid post', 'missing fields': missing_fields}), 400

    if POSTS:
        new_id = max(post['id'] for post in POSTS) + 1
    else:
        new_id = 1

    title = data.get('title')
    content = data.get('content')

    new_post = {
        'id': new_id,
        'title': title,
        'content': content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    delete_post = next((post for post in POSTS if post.get('id') == id), None)

    if delete_post is None:
        return jsonify({'Error': 'Post not found'}), 404

    POSTS.remove(delete_post)

    return jsonify(
        {"message": f"post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = next((post for post in POSTS if post.get('id') == id), None)

    if update_post is None:
        return jsonify({'Error': 'Post not found'}), 404

    new_data = request.json

    if not new_data:
        return jsonify({'Error': 'Invalid update, please add title key and/or content'})

    allowed_fields = ['title','content']
    invalid_fields = [key for key in new_data if key not in allowed_fields]

    if invalid_fields:
        return jsonify({'Error': f'Invalid fields: {invalid_fields}'}), 400


    for field in allowed_fields:
        if field in new_data:
            post_to_update[field] = new_data[field]

    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
