from flask import (Blueprint, request, render_template)
import mixed
import gender
import rating
import pandas as pd
import process
import os

bp = Blueprint('create', __name__)

@bp.route('/create', methods=('GET', 'POST'))
def create_groups():
    if request.method == 'POST':
        choices = []
        selected = request.form.getlist('choice')

        numStudentperGroup = int(request.form['numOfStudents'])

        students = process.create_Students()
        single = 'None'

        for i in selected:

            if i == 'banned':
                students = process.banned_students_in_class(students)
                choices.append('Banned')
                print('banned')

            if i == 'rate':
                choices.append('Student Preferences')
                missing = []
                print('rate')

                df = pd.read_pickle('rating_pkl')

                try:
                    df.sort_index(inplace=True)
                    df.sort_index(axis=1, inplace=True)
                    temp_col_names = df.columns.values.tolist()
                    print (temp_col_names)
                    col_names = [x.capitalize() for x in temp_col_names]
                    temp_row_names = df.index.tolist()
                    print(temp_row_names)

                    row_names = [x.capitalize() for x in temp_row_names]

                    print(col_names)

                    if sorted(col_names) != sorted(row_names):
                        missing.append(set(col_names).difference(row_names))
                    for i in range(len(col_names)):
                        pref_list=df.iloc[i]
                        pref_list=pref_list.tolist()
                        print(pref_list)
                        pref_list.pop(i)
                        
                        for a in pref_list:
                            if pd.isnull(a):
                                pref_list.remove(a)
  
                        if len(pref_list) != len(col_names)-1:
                            missing.append(row_names[i])
                    if len(missing) != 0:
                        student = missing
                        return render_template('upload/error.html', missing=student)
                    else:
                        groups = rating.final_matches(students) # in dict
                except AttributeError:
                    student=["There are no ratings."]
                    return render_template('upload/error.html', missing=student)


            if i == "mixed":
                choices.append('Heterogeneous Groups')
                if 'rate' in selected:
                    grade = rating.grades_for_pair_matches(groups)
                    numStudentperGroup = 2
                else:
                    grade = process.grade_list()
                    groups = process.name_list()
                    if not grade:
                        student = ['No information for students.']
                        return render_template('upload/error.html', missing=student)

                groups = mixed.mixed_groups(numStudentperGroup, grade, groups) # list
                print('mixed')

            if i == 'gender':
                choices.append('Gender')
                groups, single = gender.gender_groups() # dict
                groups = list(groups.items())
                print('gender')

        try:
            groups = list(groups.items())
        except AttributeError:
            groups = groups

        path = 'application/downloads'
        output_file = os.path.join(path, 'finalGroup.csv')
        userdownload=pd.DataFrame(groups)
        userdownload.to_csv(output_file, index=False,header=False)
        print(userdownload)


        return render_template('upload/result.html', groups=userdownload.to_html(header=False, justify="center", classes='tablestyle'), selected=choices, single=single)

    return render_template('upload/create.html')






