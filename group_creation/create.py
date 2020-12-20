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
        groups= []
        ban = False
        selected = request.form.getlist('choice')
        if not selected:
            return render_template("upload/create.html", message="No choice selected.")

        df2 = pd.read_pickle('all_pkl')

        numStudentperGroup = int(request.form['numOfStudents'])

        students = process.create_Students()
        single = 'None'
        teacher_removed_student = 'None'


        try:
            teacher_removed_student = request.form.get('student')
            teacher_removed_student = teacher_removed_student.capitalize()
            single = teacher_removed_student
        except (ValueError, AttributeError):
            teacher_removed_student = 'None'

        for i in selected:

            if i == 'banned':
                students = process.banned_students_in_class(students)
                choices.append('Banned')
                print('banned')
                ban = True

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
                        print(f'create.py 88 groups {groups}')
                        #check if missing students or actual matches
                        if type(groups) is list:
                            return render_template('upload/errorcreate.html', missing=groups)

                except AttributeError:
                    return render_template('upload/upload.html', message="Upload file with student ratings.")

            if i == "mixed":
                choices.append('Heterogeneous Groups')

                grade = process.grade_list()
                if not grade:
                    return render_template('upload/upload.html', message="Upload file with student grades.")

                # check to make sure everyone has a grade
                for a in grade:
                    if pd.isnull(a):
                        return render_template('upload/upload.html',
                                               message="There are student(s) missing a grade. Please fill in a grade for them.")

                if 'rate' in selected:
                    if type(df2) is list:
                        if not df2:
                            return render_template('upload/upload.html', message="Upload file with student grades.")
                    elif df2.empty:
                            return render_template('upload/upload.html', message="Upload file with student grades.")
                    else:
                        grade = rating.grades_for_pair_matches(groups)
                        print(f'create.py 121 grade {grade}')
                        numStudentperGroup = 2
                else:
                    groups = process.name_list()

                groups = mixed.mixed_groups(numStudentperGroup, grade, groups, students, ban) # list
                print(f'create.py 127 groups {groups}')
                print('mixed')

            if i == 'gender':
                choices.append('Gender')
                df2 = pd.read_pickle('all_pkl')
                if type(df2) is list:
                    if not df2:
                        return render_template('upload/upload.html', message="No student gender information was uploaded.")
                elif df2.empty:
                    return render_template('upload/upload.html', message="No student gender information was uploaded.")
                else:
                    groups, single = gender.gender_groups(df2) # dict
                    groups = list(groups.items())
                print('gender')

        if not groups:
            message="Your file did not upload correctly."
            return render_template('upload/upload.html', message=message)

        try:
            groups = list(groups.items())
        except AttributeError:
            groups = groups
        #saves groups as csv file
        path = 'group_creation/downloads'
        output_file = os.path.join(path, 'finalGroup.csv')
        userdownload=pd.DataFrame(groups)
        userdownload.to_csv(output_file, index=False,header=False)
        print(userdownload)

        #saves groups as CSV file for Zoom breakout rooms
        breakout_rooms=[['Pre-assign Room Name', "Email Address"]]
        temp_list=[]
        i = 1
        for group in groups:
            for member in group:
                for a, b in enumerate(students):
                    if b.name == member:
                        temp_list = [f'room{i}', b.email]
                breakout_rooms.append(temp_list)
                temp_list=[]
            i=i+1
        output_file1 = os.path.join(path, "breakoutroom.csv")
        userdownload=pd.DataFrame(breakout_rooms)
        userdownload.to_csv(output_file1, index=False,header=False)



        #adds info for final group for output
        display = groups_with_data(groups, selected, students)
        display = pd.DataFrame(display)

        return render_template('upload/result.html', groups=display.to_html(header=False, index=False, justify="center", classes='tablestyle'), selected=choices, single=single)

    return render_template('upload/create.html')



def groups_with_data(groups, selected, students):
    for_display=[]
    temp_group_list = []
    temp_group = []
    n = 1
    if 'rate' in selected and 'mixed' in selected:
        print('groupswithdata rate and mixed')
        temp_rate =[]
        individual_rate =[]
        for_display.append(['', 'Student 1', 'Student 2', 'Student 3', 'Student 4'])
        for_display.append(['', "Student 1's rating of others","Student 2's rating of others","Student 3's rating of others","Student 4's rating of others"])
        #create a temp list for each group to get data about each member
        for group in groups:
            for member in group:
                temp_group_list.append(member)

            for i in range(len(temp_group_list)):
                for a, b in enumerate(students):
                    if b.name == temp_group_list[i]:
                        grade = b.grade
                        temp_group.append(f'{temp_group_list[i]}: {grade}')
                        for x in range(len(temp_group_list)):
                            for rate, pref in b.preferdict.items():
                                if temp_group_list[x] in pref:
                                    individual_rate.append(str(rate))
                        individual_rate.insert(i, 'X')
                        temp_rate.append(', '.join(individual_rate))
                        individual_rate=[]

            temp_group_list=[]
            temp_group.insert(0, f'Group {n}')
            n = n + 1
            temp_rate.insert(0, 'Ratings')
            for_display.append(temp_group)
            for_display.append(temp_rate)
            temp_rate=[]
            temp_group = []

    
    # for displaying printout of groups with their partner's rating number
    elif 'rate' in selected:
        print('groups with data rate only')
        for_display.append(['','Member 1', "Member 1's rating of 2", "Member 2's rating of 1", 'Member 2'])
        for group in groups:
            for member in group:
                temp_group_list.append(member)

            for a, b in enumerate(students):
                if b.name == temp_group_list[0]:
                    for rate, pref in b.preferdict.items():
                        if temp_group_list[1] in pref:
                            temp_group.append(temp_group_list[0])
                            temp_group.append(rate)
                if b.name == temp_group_list[1]:
                    for rate,pref in b.preferdict.items():
                        if temp_group_list[0] in pref:
                            temp_group.append(rate)
                            temp_group.append(member)

            temp_group_list=[]
            temp_group.insert(0, f'Group {n}')
            n = n + 1
            for_display.append(temp_group)
            temp_group = []
            
    elif 'mixed' in selected:
        #for displaying printout of groups with their grades

        print('groupswithdata mixed only')
        for group in groups:
            for member in group:
                temp_group_list.append(member)

            for i in range(len(temp_group_list)):
                for a, b in enumerate(students):
                    if b.name == temp_group_list[i]:
                        grade = b.grade
                        temp_group.append(f'{temp_group_list[i]}: { grade}')
            temp_group_list=[]
            temp_group.insert(0, f'Group {n}')
            n = n + 1
            for_display.append(temp_group)
            temp_group=[]
    else:
        for_display = groups

    return for_display




