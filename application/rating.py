import pandas as pd
from matching import Player
from matching.games.stable_roommates import _make_players
from matching.algorithms import stable_roommates
import process


def change_to_dict_for_rating(students, remove_student):
    new_dict = {}
    new_list = []

    for i in range(0, len(students)):
        name = students[i].name
        print(students[i])
        print(name)
        if name != remove_student:
            for key, value in sorted(students[i].preferdict.items(), reverse=True):
                new_list.append(value)

            flat_list = [item for sublist in new_list for item in sublist]
            for a in flat_list:
                if pd.isnull(a):
                    flat_list.remove(a)
                if a == remove_student:
                    flat_list.remove(a)
            new_dict[name] = flat_list
            print('NewList')
            print(new_list)

            new_list = []
            flat_list = []
        else:
            continue
    return new_dict


def final_matches(students, remove_student):
    print(len(students))
    dictionary = change_to_dict_for_rating(students, remove_student)  # to start game
    print(dictionary)
    game = _make_players(dictionary)
    matching = stable_roommates(game)
    matching = check_final_matches(matching, remove_student)
    print('Matching')
    print(matching)

    # takes the pairs of students in dictionary and create 2 separate lists as string type.
    ls = []
    pair1 = []
    pair2 = []
    ls = list(matching.keys())
    for elem in ls:
        elem = str(elem)
        pair1.append(elem)
    st = []
    st = list(matching.values())
    for item in st:
        item = str(item)
        pair2.append(item)

    # convert back to dictionary as string type
    matching = {pair1[i]: pair2[i] for i in range(len(pair1))}

    # checks for duplicates and removes the duplicate pair of matches
    finalMatch = {}
    for key, value in matching.items():
        if key not in finalMatch.values():
            finalMatch[key] = value
    print(finalMatch)

    return finalMatch

def check_final_matches(finalMatch, remove_student):
    # checks final matches
    no_match = True
    counter = 0
    while no_match and counter < 50:
        if None in finalMatch.values() or None in finalMatch.keys():
            students = process.create_Students()
            finalMatch = final_matches(students, remove_student)
            counter = counter + 1
        else:
            no_match = False

    return finalMatch


def grades_for_pair_matches(finalMatch):
#Gets the sum of grade for each matched pair. Needed with the mixed group option.
 
    #gets the names and grades for students
    nameList = process.name_list()
    grade = process.grade_list()


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



