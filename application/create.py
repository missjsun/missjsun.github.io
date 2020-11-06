from Flask import (Blueprint, request, render_template)
import upload
import mixed

@bp.route('/create', methods=('GET','POST')
def create_groups():
    gender = request.form.get('gender') != None
    rate = request.form.get('rate') != None
    mixed = request.form.get('mixed') != None
    banned = request.form.get('banned') != None

    numStudentperGroup = int(request.form['numOfStudents'])


    if mixed:
        upload.mixed_groups(numStudentperGroup)
        return render_template('upload/mixed.html')

    return render_template('upload/mixed.html')
                        





