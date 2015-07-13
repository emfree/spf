import time
from flask import Flask, request, jsonify, render_template
from spf.data import from_file, PersistentNode, Tag


app = Flask(__name__)
app.config['DEBUG'] = True


d = from_file('/home/emfree/stats')

root = PersistentNode('root')


@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json(force=True)
    client_id = data['client_id']
    stats = data['stats']
    timestamp = time.time()
    tag = Tag(client_id=client_id, timestamp=timestamp)
    for stack, value in stats.items():
        frames = stack.split(';')
        root.add_tagged_stack(frames, value, tag)
    print root.values
    return ''


@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/data')
def data():
    threshold = float(request.args.get('threshold', 0))
    threshold_abs = threshold * root.value()
    return jsonify(d.serialize(threshold=threshold_abs))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556)
