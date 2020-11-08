from flask import (Blueprint, request, render_template)
import mixed
import gender


bp = Blueprint('create', __name__)

@bp.route('/create', methods=('GET','POST'))
def create_groups():
    if request.method == 'POST':
        selected = []
        selected = request.form.getlist('choice')

        numStudentperGroup = int(request.form['numOfStudents'])


        for i in selected:
            if i == 'gender':
                groups, single = gender.gender_groups()
                return render_template('upload/gender.html', pairs=groups, single=single)

            elif i == "mixed":
                groups = mixed.mixed_groups(numStudentperGroup)
                return render_template('upload/mixed.html', groups=groups, selected=selected)



    return render_template('upload/create.html')
                        





