import os
from flask import (Flask, render_template, send_from_directory, current_app)
import pandas as pd

def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_PATH'] = "downloads"

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('upload/index.html')

    @app.route("/form", methods=['GET', 'POST'])
    def form():
        return render_template('upload/form.html')

    @app.route('/index', methods=["GET", "POST"])
    def input():
        return render_template('upload/index.html')

    @app.route('/downloads/<path:filename>',methods=["GET",'POST'])
    def downloads(filename):
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_PATH'])
        try:
            return send_from_directory(directory=uploads, filename=filename,as_attachment=True)
        except FileNotFoundError:
            abort(404)

    @app.route('/templates', methods=["GET","POST"])
    def templates():

        path = 'application/downloads'
        output_file = os.path.join(path, 'all_template.csv')
        emptydata=[['type in student names in this column','  ','  ',' students to keep apart']]
        all_template = pd.DataFrame(emptydata, columns=['student','grade','gender','banned'])
        all_template.to_csv(output_file, index=False)
        return render_template('upload/templates.html')


    from . import upload
    app.register_blueprint(upload.bp)

    from . import create
    app.register_blueprint(create.bp)

    return app
