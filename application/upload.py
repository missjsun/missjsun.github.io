from flask import (Blueprint, render_template, request)
import pandas as pd

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=("GET",'POST'))
def upload():
    missing_students_wo_rating = "None"
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file[]')
        filenames = []
        for f in uploaded_files:
            df = pd.read_csv(f)
            col = df.columns.values.tolist()
            if 'grades' not in col:
                missing_students_wo_rating = []
                col_names = df.columns.values.tolist()
                row_names = df.index.tolist()

                if sorted(col_names) != sorted(row_names):
                    missing_students_wo_rating.append(set(col_names).difference(row_names))

                df = df.set_index('names')
                df.to_pickle('rating')

            else:
                df.to_pickle('all')

    return render_template('upload/upload.html', missing=missing_students_wo_rating)

