import os
from flask import (Flask, render_template, send_from_directory, current_app)

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

    @app.route('/mixed', methods=['GET','POST'])
    def mixed_groups():
        return render_template('upload/mixed.html', groups=finalizedGroups, names=nameList, grade=grade)

#    @app.route('/upload', methods=['GET', 'POST'])
#    def upload():
#        return render_template('upload/upload.html')

    #@app.route('/create', methods=['GET','POST'])
    #def create():


    @app.route('/downloads/<path:filename>',methods=["GET",'POST'])
    def downloads(filename):
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_PATH'])
        try:
            return send_from_directory(directory=uploads, filename=filename,as_attachment=True)
        except FileNotFoundError:
            abort(404)

    from . import gender
    app.register_blueprint(gender.bp)

 #   from . import mixed
 #   app.register_blueprint(mixed.bp)

    from . import upload
    app.register_blueprint(upload.bp)

    from . import create
    app.register_blueprint(create.bp)

    return app
