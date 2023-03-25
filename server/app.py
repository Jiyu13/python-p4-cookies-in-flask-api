from flask import Flask, request, session, jsonify, make_response

app = Flask(__name__)
app.json.compact = False

# Set the secret key to some random bytes. Keep this really secret!
# used to sign session cookies for protection against cookie data tampering.
# user can't modify the contents unless they know this secret key used for signing
# in order to use session, need to set a secret key
app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

# or use os module to generate a good secret key from command line
# $ python -c 'import os; print(os.urandom(16))'

@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    # Flask takes the values in session obj and seializes them into a cookie
    # use ternary operator to set values for session
    # can be session.get("hello")/"World"
    session["hello"] = session.get("hello") or "World"  # ??? why or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"

    response = make_response(jsonify({
        # session cookie cannot be changed from brower
        # will have no effect thanks to Flask security features
        'session': {
            'session_key': key,
            'session_value': session[key],
            'session_accessed': session.accessed,
        },
        # can be changed from browser, dev tools->Application->Cookies section
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
    }), 200)
    
    # for cookie in request.cookies:
    #     print(request.cookies[cookie]) 

    response.set_cookie('mouse', 'Cookie')
    return response

if __name__ == '__main__':
    app.run(port=5555)
    