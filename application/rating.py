from flask import render_template
import pandas as pd
import collections
import os
import random
from matching import Player
from matching.games.stable_roommates import _make_players
from matching.algorithms import stable_roommates
import process
import upload

def rating(df2):
    '''Gets the students preferences and finds the best pairs based 
    on their preferences'''

    #removes NaN spots
    df3 = {k1:{k:v for k,v in v1.items() if pd.notnull(v)} for k1, v1 in df2.items()}

    #sorts each student by their preference in decreasing order
    df4 = {key:dict(sorted(val.items(),key=lambda x:x[1], reverse=True))
        for key, val in df3.items()}

    #creates a new dictionary with just the student name and their preference.
    new_dict={}
    new_list=[]

    for k1, v1 in df4.items():
        for subk in v1.keys():
            new_list.append(subk)
        new_dict[k1] = new_list
        new_list=[]

    #finds the best matches
    game = _make_players(new_dict)
    matching = stable_roommates(game)

    #takes the pairs of students in dictionary and create 2 separate lists as string type.
    ls = []
    pair1=[]
    pair2=[]
    ls = list(matching.keys())
    for elem in ls:
        elem = str(elem)
        pair1.append(elem)
    st = []
    st = list(matching.values())
    for item in st:
        item = str(item)
        pair2.append(item)
        
    #convert back to dictionary as string type
    matching = {pair1[i]: pair2[i] for i in range(len(pair1))} 
    #checks for duplicates and removes the duplicate pair of matches
    finalMatch = {}
    for key, value in matching.items():
        if key not in finalMatch.values():
            finalMatch[key]=value     
    return finalMatch


def check_matches():
#keeps running matches until everyone has a pair.

    df = process.shuffle_order()
    df2 = df.to_dict('index')

    finalMatch = rating(df2)
    no_match = True
    while no_match:
        if "None" in finalMatch.values() or "None" in finalMatch.keys():
            finalMatch = rating(df2)
        else:
            no_match = False

    #path = 'application/downloads'
    #output_file = os.path.join(path, 'finalGroup.csv')

    #userdownload = pd.DataFrame(finalMatch)
    #userdownload.to_csv(output_file, index=False, header=False)
    return finalMatch


def grades_for_pair_matches(finalMatch):
#Gets the sum of grade for each matched pair. Needed with the mixed group option.
 
    #gets the names and grades for students
    nameList = upload.name_list()
    grade = upload.grade_list()


    #find the sum of grade for each pair of student matches.
    pairGrade = []
    grade1=0
    grade2=0
    pair1 = list(finalMatch.keys())
    pair2 = list(finalMatch.values())
    for i in range(0, len(pair1)):
        student1 = pair1[i]
        for x in range(0, len(nameList)):
            if nameList[x] == student1:
                grade1 = grade[x]
                break

        student2 = pair2[i]
        for x in range(0, len(nameList)):
            if nameList[x] == student2:
                grade2 = grade[x]
                break

        total=grade1+grade2
        pairGrade.append(total)

    return pairGrade


