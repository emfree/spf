import time
from flask import Flask, request, jsonify, render_template
from spf.util import parse


app = Flask(__name__)
app.config['DEBUG'] = True



d = parse('/home/emfree/inbox/profile')


@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json(force=True)
    timestamp = time.time()
    return ''


@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/example')
def example():
    return jsonify(d)


if __name__ == '__main__':
    app.run(port=5556)
