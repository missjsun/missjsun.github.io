from flask import (Blueprint, render_template, request)
import pandas as pd

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=("GET",'POST'))
def upload():

    if request.method == 'POST':
        uploaded_files = request.files.getlist('file[]')
        missing_students_wo_rating=[]

        for f in uploaded_files:
            df = pd.read_csv(f)
            col = df.columns.values.tolist()
            if 'grade' not in col:
                df = df.set_index('names')
                col_names = df.columns.values.tolist()
                row_names = df.index.tolist()

                if sorted(col_names) != sorted(row_names):
                    missing_students_wo_rating.append(set(col_names).difference(row_names))
                df.to_pickle('rating_pkl')

            else:
                df.to_pickle('all_pkl')

            if not missing_students_wo_rating:
                missing_students_wo_rating = "None"

            return render_template('upload/create.html', missing=missing_students_wo_rating)

    return render_template('upload/upload.html')

