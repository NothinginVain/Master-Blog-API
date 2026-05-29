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
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    reverse = False

    if not sort and not direction:
        return jsonify(POSTS)

    if sort not in ['title', 'content']:
        return jsonify(
            {'Error': 'type a valid parameter: title or content'}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({'Error': 'type a valid parameter: asc or desc'}), 400

    if direction.lower() == 'desc':
        reverse = True

    new_list = sorted(POSTS, key=lambda k: k.get(sort).lower(), reverse=reverse)
    return jsonify(new_list)


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
            {'Error': 'Invalid post', 'missing fields': missing_fields}), 400

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
    post_to_delete = next((post for post in POSTS if post.get('id') == id), None)

    if post_to_delete is None:
        return jsonify({'Error': 'Post not found'}), 404

    POSTS.remove(post_to_delete)

    return jsonify(
        {"message": f"post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = next((post for post in POSTS if post.get('id') == id),
                          None)

    if update_post is None:
        return jsonify({'Error': 'Post not found'}), 404

    new_data = request.json

    if not new_data:
        return jsonify(
            {'Error': 'Invalid update, please add title key and/or content'}), 400

    allowed_fields = ['title', 'content']
    invalid_fields = [key for key in new_data if key not in allowed_fields]

    if invalid_fields:
        return jsonify({'Error': f'Invalid fields: {invalid_fields}'}), 400

    for field in allowed_fields:
        if field in new_data:
            post_to_update[field] = new_data[field]

    return jsonify(post_to_update), 200


@app.route('/api/posts/search')
def search_post():
    title = request.args.get('title')
    content = request.args.get('content')
    filtered_list = []

    if title:
        for post in POSTS:
            if title.lower() in post.get('title').lower():
                filtered_list.append(post)

    if content:
        for post in POSTS:
            if content.lower() in post.get('content').lower():
                filtered_list.append(post)

    return jsonify(filtered_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
