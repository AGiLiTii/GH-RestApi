from flask import Flask , jsonify, make_response, request
from github_scraper import test, get_userdata, get_repodata


app = Flask(__name__)
#config
app.config.update({
    "JSON_SORT_KEYS":False,
})


# Home page
@app.route('/')
def root():
    return jsonify({'message': 'Welcome to the GitHub API'})

# Test page
@app.route('/test')
def test_page():
    return jsonify(test())

# User data page
@app.route('/users/<username>', methods=['GET'])
def user_data(username):
    user_info = get_userdata(username)
    if user_info is None:
        return make_response(jsonify({'error': 'User not found'}), 404)
    return make_response(jsonify(user_info), 200)

# User's repository data page with query parameters
@app.route('/users/<username>/repos', methods=['GET'])
def repo_data(username):

    args = request.args
    repo_info = get_repodata(username)
    if repo_info is None:
        return make_response(jsonify({'error': 'User not found'}), 404)
    
    # Access query parameters using request.args

    # Sort
    sort_order = request.args.get('sort', default='full_name')
    # Direction
    direction = request.args.get('direction', default='asc')

    if sort_order == "pushed":
        repo_info = sorted(repo_info, key=lambda k: k.get('pushed_at', ''),reverse=True) 
    else:
        # FIXME:
        repo_info = sorted(repo_info, key=lambda k: k.get('full_name', ''))


    if direction == "desc":
        repo_info.reverse()

    # Page
    page = int(args.get("page", 1))

    # Per page
    per_page = int(args.get("per_page", 30))

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page

    # Slice
    repo_info = repo_info[start:end]

    return make_response(jsonify(repo_info), 200)


#TODO:UNdocumneted response code


if __name__ == '__main__':
    app.run(debug=True)

    