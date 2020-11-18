from flask import (Blueprint, render_template, request)
import pandas as pd
import pickle
bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=("GET",'POST'))
def upload():

    if request.method == 'POST':
        uploaded_files = request.files.getlist('file[]')
        missing_students_wo_rating=[]
        empty_list = []

        with open('all_pkl','wb') as f:
            pickle.dump(empty_list, f)
        with open('rating_pkl','wb') as f:
            pickle.dump(empty_list, f)

        for f in uploaded_files:
            df = pd.read_csv(f)
            temp_col = df.columns.values.tolist()
            print(temp_col)
            col = [x.capitalize() for x in temp_col]
            
            if 'Grade' not in col:
                df = df.set_index(df.columns[0])
                temp_col_names = df.columns.values.tolist()
                col_names = [x.capitalize() for x in temp_col_names]
                temp_row_names = df.index.tolist()
                row_names = [x.capitalize() for x in temp_row_names]
                print(col_names)

                if sorted(col_names) != sorted(row_names):
                    missing_students_wo_rating.append(set(col_names).difference(row_names))

                for i in range(len(col_names)):
                    pref_list=df.iloc[i]
                    pref_list=pref_list.tolist()
                    for a in pref_list:
                        if pd.isnull(a):
                            pref_list.remove(a)

                    if len(pref_list) != len(col_names)-1:
                        missing_students_wo_rating.append(row_names[i])

                df.to_pickle('rating_pkl')

            else:
                df.to_pickle('all_pkl')

            
        if not missing_students_wo_rating:
            missing_students_wo_rating = "None"

        return render_template('upload/create.html', missing=missing_students_wo_rating)

    return render_template('upload/upload.html')

