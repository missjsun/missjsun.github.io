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
        print('upload.py - 18')
        print(uploaded_files)
        if request.files['file[]'].filename=='':
            return render_template('upload/upload.html', message='No file selected')
        else:
            for f in uploaded_files:
                df = pd.read_csv(f)
                temp_col = df.columns.values.tolist()
                print('upload.py - temp_col - 26')
                print(temp_col)
                col = [x.capitalize() for x in temp_col]
                print('upload.py - col cap -29')
                print(col)

                if 'Grade' not in col:
                    df = df.set_index(df.columns[0])
                    print(f'upload.py 34 df {df}')
                    temp_col_names = df.columns.values.tolist()
                    col_names = [x.capitalize() for x in temp_col_names]
                    temp_row_names = df.index.tolist()
                    row_names = [x.capitalize() for x in temp_row_names]
                    print('upload.py - col_names and row names- 36')
                    print(col_names)
                    print(row_names)

                    if sorted(col_names) != sorted(row_names):
                        missing_students_wo_rating.append(set(col_names).difference(row_names))
                        print('upload.py-missingstudents 44')
                        print(missing_students_wo_rating)

                    for student in temp_row_names:
                        pref_list = df.loc[student]
                        print(f'upload.py - pref_list 50 {pref_list}')
                        pref_list = pref_list.drop(labels=student)

                        pref_list = pref_list.tolist()
                        print(f'upload.py - 51 to list {pref_list}')
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

    return render_template('upload/upload.html', message=' ')
