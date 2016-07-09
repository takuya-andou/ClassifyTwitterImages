#!/usr/bin/env python2
import json
import os
import tempfile

# pip install flask
from flask import Flask, request, make_response, abort
from labellio import Classifier, Config, ImageLoader, Label

# Flask Settings
DEBUG = True
UPLOAD_FOLDER = "tmp"
MODEL_FOLDER = "model"
SUPPORT_EXTENSIONS = set([".jpg", ".jpeg", ".png"])
app = Flask(__name__)
app.config.from_object(__name__)

# Labellio Settings
labellio_config = Config(app.config['MODEL_FOLDER'])
labellio_label = Label(labellio_config)
labellio_image_loader = ImageLoader(labellio_config)
labellio_classifier = Classifier(labellio_config)
with open(labellio_config.label_file) as fp:
    labellio_label_dict = json.load(fp)


def images(image_dir):
    for base, _, files in os.walk(image_dir):
        for f in files:
            yield os.path.join(base, f)


def exec_batch(batch, classifier, label):
    paths, data = zip(*batch)
    result = {"label_name": labellio_label_dict}
    for i, output in enumerate(classifier.forward_iter(data)):
        result[i] = {
            "label": label.label(output.best), "score": output.values.tolist()}
    return result


def labellio_exec(image):
    global labellio_config, labellio_label, labellio_image_loader, labellio_classifier
    batch = []
    i=0
    batch.append((image, labellio_image_loader.load(image)))
    return exec_batch(batch, labellio_classifier, labellio_label)

# URL


@app.route('/', methods=['GET'])
def help():
    return """POST your image as "image" parameter to /classify.
(ex. curl -F "image=@test.png" http://{0}/classify)
""".format(request.host)


@app.route('/classify', methods=['POST'])
def classify():
    print request.form['url']

    #root, ext = os.path.splitext(uploaded_file.filename)
    root, ext = os.path.splitext(request.form['url'])
    temp_dir = ""
    print ext
    if ext in app.config['SUPPORT_EXTENSIONS']:
        pass
    else:
        abort(400)

    result = labellio_exec('images/'+request.form['url'])
    response = make_response()
    response.data = json.dumps(result)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')