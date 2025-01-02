from flask import Flask, render_template, request, jsonify, session


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test_post():
    if request.method == "POST":
        f = request.form["first_name"]
        l = request.form["last_name"]
        email = request.form["user_email"]
        print(f)
        print(l)
        print(email)
        return jsonify({"Name": f'{f} {l}', "Email": email})
    else:
        return render_template("index_for_post.html")


if __name__ == '__main__':
    app.run(debug=True)
