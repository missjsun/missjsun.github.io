from flask import (Blueprint, request, render_template)
import mixed
import gender
import rating
import pandas as pd


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

            elif i == 'rate':
                missing = []

                df = pd.read_pickle('rating_pkl')
                col_names = df.columns.values.tolist()
                row_names = df.index.tolist()

                if sorted(col_names) != sorted(row_names):
                    missing.append(set(col_names).difference(row_names))
                if len(missing) != 0:
                    student = missing
                    return render_template('upload/error.html', missing=student)
                else:
                    groups = rating.check_matches()
                    return render_template('upload/mixed.html', groups=groups)

            elif i == ['rate', 'mixed']:
                missing = []

                df = pd.read_pickle('rating_pkl')
                col_names = df.columns.values.tolist()
                row_names = df.index.tolist()

                if sorted(col_names) != sorted(row_names):
                    missing.append(set(col_names).difference(row_names))
                if len(missing) != 0:
                    student = missing
                    return render_template('upload/error.html', missing=student)
                else:
                    match = rating.check_matches()
                    grades = rating.grades_for_pair_matches(match)
                    return render_template('upload/mixed.html', groups=groups)


    return render_template('upload/create.html')
                        





