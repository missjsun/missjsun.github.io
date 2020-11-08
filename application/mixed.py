import random
import statistics
import numpy as np
import pandas as pd
import process
import os

def mixed_groups(numberofstudents):
  #  if request.method =='POST':

        numStudentperGroup = numberofstudents
        nameList = process.name_list()
        grade = process.grade_list()

    # shuffles the lists together
        temp = list(zip(nameList, grade))
        random.shuffle(temp)
        nameList, grade = zip(*temp)

    # changing tuple to lists
        nameList = list(nameList)
        grade = list(grade)

    # get some data
        totalGrade = sum(grade)
        numStudents = len(grade)

        numGroups = int(np.ceil(numStudents / numStudentperGroup))
        res = statistics.pstdev(grade)
        if numStudentperGroup == 2:
            pointsPerGroup = totalGrade / numGroups
            pointsRangeLow = pointsPerGroup - 2*res
            pointsRangeHigh = pointsPerGroup + 2*res
        else:
            pointsPerGroup = totalGrade / numGroups
            pointsRangeLow = pointsPerGroup - res
            pointsRangeHigh = pointsPerGroup + res

    # Puts everyone into groups randomly
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        groups = list(chunks(grade, numStudentperGroup))
        groupNames = list(chunks(nameList, numStudentperGroup))

        finalizedGroups = []
        tempNum = 0
        tempNum2 = 0
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

        path = 'application/downloads'
        output_file = os.path.join(path, 'finalGroup.csv')
        userdownload=pd.DataFrame(finalizedGroups)
        userdownload.to_csv(output_file, index=False,header=False)

        return (finalizedGroups)
