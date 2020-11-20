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
        print(len(students))
        single = 'None'
        teacher_removed_student = 'None'
        print('before')
        print(teacher_removed_student)

        try:
            teacher_removed_student = request.form.get('student')
            teacher_removed_student = teacher_removed_student.capitalize()
            print('try')
            print(teacher_removed_student)
            single = teacher_removed_student
        except (ValueError, AttributeError):
            print('value error')
            teacher_removed_student = 'None'

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
                    col_names = [x.capitalize() for x in temp_col_names]
                    temp_row_names = df.index.tolist()
                    row_names = [x.capitalize() for x in temp_row_names]
                    print(row_names)
                    print(col_names)

                    if sorted(col_names) != sorted(row_names):
                        missing.append(set(col_names).difference(row_names))
                    for i in range(len(col_names)):
                        pref_list=df.iloc[i]
                        pref_list=pref_list.tolist()
                        pref_list.pop(i)

                        for a in pref_list:
                            if pd.isnull(a):
                                pref_list.remove(a)

                        if len(pref_list) != len(col_names)-1:
                            missing.append(row_names[i])
                    if len(missing) != 0:
                        student = missing
                        return render_template('upload/error.html', missing=student)

                    if teacher_removed_student in row_names:
                        row_names.remove(teacher_removed_student)
                    if len(row_names) % 2 == 1:
                        return render_template('upload/remove.html')
                    else:
                        groups = rating.final_matches(students, teacher_removed_student) # in dict
                except AttributeError:
                    student=["There are no ratings."]
                    return render_template('upload/error.html', missing=student)

            if i == "mixed":
                choices.append('Heterogeneous Groups')
                df2 = pd.read_pickle('all_pkl')
                if 'rate' in selected:
                    if type(df2) is list:
                        if not df2:
                            student=["Student grades are missing."]
                            return render_template('upload/error.html', missing=student)
                    elif df2.empty:
                            student=["Student grades are missing."]
                            return render_template('upload/error.html', missing=student)
                    else:
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

        #adds info for final group for output
        display = groups_with_data(groups)

        return render_template('upload/result.html', groups=userdownload.to_html(header=False, justify="center", classes='tablestyle'), selected=choices, single=single)

    return render_template('upload/create.html')



def groups_with_data(groups):



