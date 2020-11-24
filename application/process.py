import pandas as pd
import random

# create a class for each student
class Student:
    def __init__(self, name, grade, gender, banned):
        self.name = name
        self.grade = grade
        self.gender = gender
        self.banned = banned
        self.preferdict = {}

    def add_dict(self, preferdict):
        new = {k:v for k,v in preferdict.items() if pd.notnull(k)}
        self.preferdict.update(new)

    def __repr__(self):
        if not self.preferdict:
            return "< name:%s  grade:%s  gender:%s  banned:%s>" % (self.name, self.grade, self.gender, self.banned)
        else:
            for key, value in self.preferdict.items():
                return "< name:%s  grade:%s  gender:%s  banned:%s, key:%s, value:%s>" % (self.name, self.grade, self.gender, self.banned, key, value)

 # creates an instance/object of each student from all.csv. Puts each student in a list to access: students[0].name


def create_Students():
    students = []
    missing_students_wo_info = []
    all_list = change_info_to_list()
    rate, studentnames = shuffle_order()

    # creates objects using the all list
    for i in range(len(all_list)):
        if any(x.name == all_list[i][0] for x in students):
            for a, b in enumerate(students):
                if b.name == studentnames[i]:
                    index = a
                    break
            students[a] = Student(all_list[i][0], all_list[i][1], all_list[i][2], all_list[i][3])
        else:
            students.append(Student(all_list[i][0], all_list[i][1], all_list[i][2], all_list[i][3]))

    # checks the rating csv. Sees if student is already an object to add to their preference to their instance
    index = 0
    for i in range(len(studentnames)):  # iterates through rating dictionary order
        if any(x.name == studentnames[i] for x in students):  # checks if student an object
            for a, b in enumerate(students):  # finds the index number for that object
                if b.name == studentnames[i]:
                    index = a  # index number to add
                    break
            ranks_for_student = rate.loc[studentnames[i]]  # gets row for student
            ranksforstudentdict = ranks_for_student.to_dict()  # puts that row into a dictionary
            new_dict_of_rate = {}
            for key, value in ranksforstudentdict.items():  # creates new dictionary based on #rank as key; students as list values
                if value in new_dict_of_rate:
                    new_dict_of_rate[value].append(key)
                    if len(new_dict_of_rate[value])>1:
                        random.shuffle(new_dict_of_rate[value])
                else:
                    new_dict_of_rate[value] = [key]
            students[a].add_dict(new_dict_of_rate)  # adds this dictionary to the object
            #print("this is the first for loop...")

        else:

            missing_students_wo_info.append(studentnames[i])
            ranks_for_student = rate.loc[studentnames[i]] #gets all the ratings
            ranksforstudentdict = ranks_for_student.to_dict() #puts their rating to a dictionary
            new_dict_of_rate = {}
            for key, value in ranksforstudentdict.items():
                if value in new_dict_of_rate:
                    new_dict_of_rate[value].append(key)
                    if len(new_dict_of_rate[value])>1:
                        random.shuffle(new_dict_of_rate[value])
                else:
                    new_dict_of_rate[value] = [key]
            students.append(Student(studentnames[i], 0, 'n', 'None'))
            students[-1].add_dict(new_dict_of_rate)
    return students

def banned_students_in_class(students):    # changes rating for banned students to 0
    for i in range(len(students)):
        if students[i].banned != 'None':
            banned_student = students[i].banned
            for key in students[i].preferdict.values():
                try:
                    key.remove(banned_student)
                    break
                except ValueError:
                    pass
            students[i].preferdict[0.0] = [banned_student]

    return students


def name_list():
    a = pd.read_pickle('all_pkl')

    try:
        all_df = a['student'].tolist()
        all_df = [x.capitalize() for x in all_df]
        #print(all_df)
    except (AttributeError, TypeError):
        all_df = []
    return all_df


def grade_list():
    # get grade list
    a = pd.read_pickle('all_pkl')
    try:
        all_df = a['grade'].tolist()
    except (AttributeError, TypeError):
        all_df = []
    return all_df


def change_info_to_list():
    a = pd.read_pickle('all_pkl')

    try:
        all_list = a.values.tolist()
        templist = []
        all = []
        for i in all_list:
            for b in i:
                if isinstance(b, str):
                    templist.append(b.capitalize())
                else:
                    templist.append(b)
            all.append(templist)
            all_list = all
            templist = []
    except (AttributeError, TypeError):
        all_list = []

    return all_list


def shuffle_order():
    # get header and shuffle, then rearrange with new header
    rate_df = pd.read_pickle('rating_pkl')

    try:
        rate_df.columns = rate_df.columns.str.capitalize()
        rate_df.index = rate_df.index.str.capitalize()
        header = rate_df.columns.tolist()
        random.shuffle(header)
        rate_df = rate_df[header]
        studentname = rate_df.index.tolist()
        studentnames = [x.capitalize() for x in studentname]
    except AttributeError:
        rate_df=[]
        studentnames =[]
    return (rate_df, studentnames)


def dict_rate():
    dict_of_rate = pd.read_csv('rating_pkl').to_dict('index')
    return dict_of_rate
