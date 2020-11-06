# create a class for each student
class Student:
    def __init__(self, name, grade, gender, banned):
        self.name = name
        self.grade = grade
        self.gender = gender
        self.banned = banned
        self.preferdict = {}

    def add_dict(self, preferdict):
        self.preferdict.update(preferdict)

    def display(self):
        print("Name: ", self.name, ", Grade: ", self.grade, ", Gender: ", self.gender, ",Banned: ", self.banned)
        print(self.preferdict)

        # creates an instance/object of each student from all.csv. Puts each student in a list to access: students[0].name


def create_Students():
    students = []
    all_list = change_info_to_list()
    rate = shuffle_order()
    studentnames = rate.index.tolist()

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
    index = -1
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
                else:
                    new_dict_of_rate[value] = [key]
            students[a].add_dict(new_dict_of_rate)  # adds this dictionary to the object

        else:
            missing_students_wo_info = []
            students.append(Student(studentnames[i], 0, 'n', 'None'))
            missing_students_wo_info.append(studentnames[i])
            ranks_for_student = rate.loc[studentnames[i]]
            ranksforstudentdict = ranks_for_student.to_dict()
            new_dict_of_rate = {}
            for key, value in ranksforstudentdict.items():
                if value in new_dict_of_rate:
                    new_dict_of_rate[value].append(key)
                else:
                    new_dict_of_rate[value] = [key]

            students[i].add_dict(new_dict_of_rate)
            break

    # changes rating for banned students to 1
    for i in range(len(students)):
        if students[i].banned != 'None':
            banned_student = students[i].banned
            for key in students[i].preferdict.values():
                try:
                    key.remove(banned_student)
                except ValueError:
                    pass
            if 1.0 in students[i].preferdict:
                students[i].preferdict[1.0].append(banned_student)
            else:
                students[i].preferdict[1.0] = banned_student

    return students


def name_list():
    a = pd.read_pickle('all')
    all_df = a['student'].tolist()
    return all_df


def grade_list():
    # get grade list
    a = pd.read_pickle('all')
    all_df = a['grade'].tolist()
    return all_df


def change_info_to_list():
    a = pd.read_pickle('all')
    all_list = a.values.tolist()
    return all_list


def shuffle_order():
    # get header and shuffle, then rearrange with new header
    rate_df = pd.read_pickle('ratings')
    header = rate_df.columns.tolist()
    random.shuffle(header)
    rate_df = rate_df[header]
    return rate_df


def dict_rate():
    dict_of_rate = pd.read_csv('ratings').to_dict('index')
    return dict_of_rate
