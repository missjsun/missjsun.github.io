import random
import statistics
import numpy as np


def mixed_groups(numStudentperGroup, grade, names, students, ban):

    try:
        nameList = list(names.keys())
    except (AttributeError, TypeError):
        nameList = names
    else: # no exception raised
        pair1 = list(names.keys())
        pair2 = list(names.values())

    verified = True
    while verified:
        nameList, grade = shuffles_students(nameList, grade)
        groups = list(chunks(grade, numStudentperGroup))
        groupNames = list(chunks(nameList, numStudentperGroup))
        if ban:
            verified = check_banned(groupNames, groups, grade, students, nameList, numStudentperGroup)
        else:
            verified = False


    # get some data
    totalGrade = sum(grade)
    numStudents = len(grade)

    numGroups = int(np.ceil(numStudents / numStudentperGroup))
    res = statistics.pstdev(grade)
    if numStudentperGroup == 2:
        pointsPerGroup = totalGrade / numGroups
        pointsRangeLow = pointsPerGroup - 1.5*res
        pointsRangeHigh = pointsPerGroup + 1.5*res
    else:
        pointsPerGroup = totalGrade / numGroups
        pointsRangeLow = pointsPerGroup - res
        pointsRangeHigh = pointsPerGroup + res


    print(f'mixed.py 41 - groups {groups}')
    print(f'mixed.py 42 - groupnames {groupNames}')

    finalizedGroups = create_mixed_groups(groups, pointsRangeLow, pointsRangeHigh, groupNames, numGroups, numStudentperGroup)
    print(f'mixed.py 45 - finalizedgroups {finalizedGroups}')
    #if rated first, then gets the pairs and puts them together.
    try:
        list(names.keys())
    except (AttributeError, TypeError):
        verified = True
        if ban:
            while verified:
                verified = check_banned(finalizedGroups, groups, grade, students, nameList, numStudentperGroup)
                if verified:
                    nameList, grade = shuffles_students(nameList, grade)
                    groups = list(chunks(grade, numStudentperGroup))
                    groupNames = list(chunks(nameList, numStudentperGroup))
                    finalizedGroups = create_mixed_groups(groups, pointsRangeLow, pointsRangeHigh, groupNames, numGroups, numStudentperGroup)

        final = finalizedGroups
        print(f'mixed.py - 61 final {final}')

    else: # no exception raised
        final = []
        templist = []
        for a in finalizedGroups:
            for b in a:
                for key in names:
                    if b == key:
                        templist.append(b)
                        templist.append(names[b])
            final.append(templist)
            templist = []
        verified = True
        counter = 0
        if ban:
            while verified:
                verified = check_banned(final, groups, grade, students, nameList, numStudentperGroup)
                if verified:
                    nameList = list(names.keys())
                    nameList, grade = shuffles_students(nameList, grade)
                    groups = list(chunks(grade, numStudentperGroup))
                    groupNames = list(chunks(nameList, numStudentperGroup))
                    finalizedGroups = create_mixed_groups(groups, pointsRangeLow, pointsRangeHigh, groupNames, numGroups, numStudentperGroup)

                    final = []
                    templist = []
                    for a in finalizedGroups:
                        for b in a:
                            for key in names:
                                if b == key:
                                    templist.append(b)
                                    templist.append(names[b])
                        final.append(templist)
                        templist = []
                counter = counter + 1
                if counter > 5:
                    break

            #final = finalizedGroups
        print(f'mixed.py - 86 -final {final}')

    return final

def shuffles_students(nameList, grade):
    #shuffles the people
    temp = list(zip(nameList, grade))
    random.shuffle(temp)
    nameList, grade = zip(*temp)
    # changing tuple to lists
    nameList = list(nameList)
    grade = list(grade)
    return nameList, grade


# Puts everyone into groups
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#recreates groups if banned together
def check_banned(groupNames, groups, grade, students, nameList, numStudentperGroup):
    verified = False
    for i in groupNames:
        check_list = i
        print(check_list)
        for check_student in check_list:
            for b,c in enumerate(students):
                if c.name==check_student:
                    if c.banned in check_list:
                        print('it shuffled')
                        verified = True
    return verified

def create_mixed_groups(groups, pointsRangeLow, pointsRangeHigh, groupNames, numGroups, numStudentperGroup):
    finalizedGroups = []
    i = 0
    # Checks for groups that fall within the pointsPerGroup range and removes them from the list
    # Adds those  groups to the finalizedGroups
    while i < numGroups:
        if (sum(groups[i]) > pointsRangeLow) and (sum(groups[i]) < pointsRangeHigh):
            finalizedGroups.append(groupNames[i])
            groups.remove(groups[i])
            groupNames.remove(groupNames[i])
            numGroups = len(groups)
        else:
            i += 1
    print('Need to sort')
    print(groups)
    print(groupNames)

    # resets i to zero. Loop to move around students in groups
    i = 0
    counter = 0

    while numGroups > 1 and sum([len(listElem) for listElem in groups]) >= numStudentperGroup:
        # moves groups with only 1 person to the end
        if len(groups[i]) == 1:
            groups.append(groups.pop(i))
        if len(groups[i]) + len(groups[i + 1]) == numStudentperGroup + 1:
            break

        # If statement for if the first group is too high, will take out a student from this group
        if ((sum(groups[i]) > pointsRangeHigh)):
            random_index = random.randrange(0, len(groups[i]) - 1)
            tempNum = groups[i][random_index]
            tempName = groupNames[i][random_index]
            groups[i].remove(groups[i][random_index])
            groupNames[i].remove(groupNames[i][random_index])
            t = 1
            print('If 1')
            print(groups[i])

            # Loops through the remaining group to find a group that is too low to switch the 2 students
            while t <= numGroups - 1:

                # if the group is not low, then goes it will increment the t counter to check the next group
                if ((sum(groups[t]) < pointsRangeLow)):
                    if len(groups[t]) == 1:
                        random_index = 0
                    else:
                        random_index = random.randrange(0, len(groups[t]) - 1)
                    tempNum2 = groups[t][random_index]
                    tempName2 = groupNames[t][random_index]
                    groups[t].remove(groups[t][random_index])
                    groupNames[t].remove(groupNames[t][random_index])
                    groups[i].append(tempNum2)
                    groupNames[i].append(tempName2)
                    groups[t].append(tempNum)
                    groupNames[t].append(tempName)

                    # Checks if this group is now within range, then move to finalized group
                    if ((sum(groups[t]) > pointsRangeLow) and (sum(groups[t]) < pointsRangeHigh)) or (numGroups == 1):
                        finalizedGroups.append(groupNames[t])
                        groups.remove(groups[t])
                        groupNames.remove(groupNames[t])
                        numGroups = len(groups)
                        t = numGroups  # breaks out of while loop

                    if ((sum(groups[i]) > pointsRangeLow) and (sum(groups[i]) < pointsRangeHigh)) or (numGroups == 1):
                        finalizedGroups.append(groupNames[i])
                        groups.remove(groups[i])
                        groupNames.remove(groupNames[i])
                        numGroups = len(groups)
                        t = numGroups

                    elif ((sum(groups[i]) < pointsRangeLow) or (sum(groups[i]) > pointsRangeHigh) or sum(
                            groups[t]) < pointsRangeLow or sum(groups[t]) > pointsRangeHigh):
                        break
                t = t + 1
            # updates the number of groups and resets index counter to start over.
            numGroups = len(groups)
            i = 0
            counter = counter + 1
            if counter > 50:
                break


        # this block of code is if the first group is too low
        else:
            t = 1
            random_index = random.randrange(0, len(groups[i]) - 1)
            tempNum = groups[i][random_index]
            tempName = groupNames[i][random_index]
            groups[i].remove(groups[i][random_index])
            groupNames[i].remove(groupNames[i][random_index])
            print('else')
            print(groups[i])
            while t <= numGroups - 1:
                if ((sum(groups[t]) > pointsRangeHigh)):
                    random_index = random.randrange(0, len(groups[t]) - 1)
                    tempNum2 = groups[t][random_index]
                    tempName2 = groupNames[t][random_index]
                    groups[t].remove(groups[t][random_index])
                    groupNames[t].remove(groupNames[t][random_index])
                    groups[i].append(tempNum2)
                    groupNames[i].append(tempName2)
                    groups[t].append(tempNum)
                    groupNames[t].append(tempName)

                    if ((sum(groups[t]) > pointsRangeLow) and (sum(groups[t]) < pointsRangeHigh)) or (numGroups == 1):
                        finalizedGroups.append(groupNames[t])
                        groups.remove(groups[t])
                        groupNames.remove(groupNames[t])
                        numGroups = len(groups)
                        t = numGroups  # breaks out of while loop

                    if ((sum(groups[i]) > pointsRangeLow) and (sum(groups[i]) < pointsRangeHigh)) or (numGroups == 1):
                        finalizedGroups.append(groupNames[i])
                        groups.remove(groups[i])
                        groupNames.remove(groupNames[i])
                        numGroups = len(groups)
                        t = numGroups

                    elif ((sum(groups[i]) < pointsRangeLow) or (sum(groups[i]) > pointsRangeHigh)):
                        break
                t = t + 1
                numGroups = len(groups)
                counter = counter + 1
                if counter > 50:
                    break

    if len(groups) != 0:
        for i in range(0, len(groupNames)):
            finalizedGroups.append(groupNames[i])
    return finalizedGroups