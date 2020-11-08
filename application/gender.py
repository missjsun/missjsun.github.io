from flask import (render_template,request)

import pandas as pd
import random
import os


#bp = Blueprint('gender', __name__)

#@bp.route('/gender', methods=('GET','POST'))
def gender_groups():

    df2 = pd.read_pickle('all_pkl')

    namelist = df2['student'].tolist()
    genderList = df2['gender'].tolist()
    pairs = {}

    # Count number of M/F
    m = genderList.count('m')
    f = genderList.count('f')
    single = "none"

    r = random.randrange(0, len(genderList))

    # IF this is an odd # of students, this section gets a singleton
    if len(genderList) % 2 == 1:
        while (genderList[r] == m and f > m) or (genderList[r] == f and m > f):
            r = random.randrange(0, len(genderList))
        else:
            single = namelist.pop(r)
            genderList.pop(r)

    # randomly pairs up students of different genders and puts them in a dictionary
    while (len(genderList) > 1):
        r1 = random.randrange(0, len(genderList))
        gender1 = genderList.pop(r1)
        name1 = namelist.pop(r1)

        r2 = random.randrange(0, len(genderList))
        gender2 = genderList[r2]

        if (m != 0) and (f != 0):
            while gender1 == gender2:
                r2 = random.randrange(0, len(genderList))
                gender2 = genderList[r2]

        gender2 = genderList.pop(r2)
        name2 = namelist.pop(r2)

        pairs[name1] = name2
        m = genderList.count('m')
        f = genderList.count('f')

    path = 'application/downloads'
    output_file = os.path.join(path, 'finalGroup.csv')

    userdownload = pd.DataFrame.from_dict(pairs,orient='index')
    userdownload.to_html()
    userdownload.to_csv(output_file, header=False)

    return pairs, single
    #return render_template('upload/gender.html', pairs=pairs, single=single)