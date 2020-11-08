from flask import (Blueprint, request, render_template)
import mixed

bp = Blueprint('create', __name__)

@bp.route('/create', methods=('GET','POST'))
def create_groups():
    if request.method == 'POST':
        selected = []
        selected = request.form.getlist('choice')

        numStudentperGroup = int(request.form['numOfStudents'])

        for i in selected:
            if "mixed":
                groups = mixed.mixed_groups(numStudentperGroup)
        return render_template('upload/mixed.html', groups=groups)

    return render_template('upload/create.html')
                        





