# Khue Nhat Do
# ID 2095632

import datetime


# create a function to check that student has graduated or not
def havegraduated(graduation, currentdate):
    date = graduation.split('/')
    month = int(date[0])
    day = int(date[1])
    year = int(date[2])
    if year < currentdate.year - 2000:
        return False
    elif year > currentdate.year - 2000:
        return True
    else:
        if month > currentdate.month:
            return True
        elif month < currentdate.month:
            return False
        else:
            if day > currentdate.day:
                return True
            else:
                return False


# create a function to compare two different dates
def isolder(date1, date2):
    lst1 = date1.split('/')
    month1 = int(lst1[0])
    day1 = int(lst1[1])
    year1 = int(lst1[2])

    lst2 = date2.split('/')
    month2 = int(lst2[0])
    day2 = int(lst2[1])
    year2 = int(lst2[2])

    if year1 > year2:
        return False
    elif year1 < year2:
        return True
    else:
        if month1 > month2:
            return False
        elif month1 < month2:
            return True
        else:
            if day1 > day2:
                return False
            else:
                return True


# create a dictionary to store the students' information as {ID: [firstName(1), lastName(0), major(2), discipline(3),
# GPA(4), graduationdate(5)]}
dct = {}

# open StudentMajorsList.csv and get their information
majors_file_name = input("Enter the major's file name:\n")
majors_file = open(majors_file_name)
lastName_list = []  # store last name in the list
majors_list = []  # store majors
ID_list = []  # store IDs
disciplined_list = []  # store students who have been disciplined

for line in majors_file:
    lst = line.split(',')
    ID = lst[0]
    ID_list.append(ID)
    dct[ID] = []
    # get lastName
    dct[ID].append(lst[1])
    lastName_list.append(lst[1])
    # get firstName
    dct[ID].append(lst[2])
    # get major
    dct[ID].append(lst[3])
    if lst[3] not in majors_list:
        majors_list.append(lst[3])
    # get discipline
    dct[ID].append(lst[4].strip())
    if lst[4].strip() != "":
        disciplined_list.append(ID)

majors_file.close()

# open GPAList.csv and get their information
GPA_file_name = input("Enter GPA's file name:\n")
GPA_file = open(GPA_file_name)
scholarship_list = []  # store students' IDs have GPA > 3.8
GPA_list = []  # store GPA
for line in GPA_file:
    lst = line.split(',')
    ID = lst[0]
    # get GPA
    GPA = lst[1].strip()
    GPA_list.append(GPA)
    dct[ID].append(GPA)
    if float(GPA) > 3.8:
        scholarship_list.append(ID)

GPA_file.close()

# open GraduationDatesList.csv and get their information
Graduation_name = input("Enter Graduation's file name:\n")
Graduation_file = open(Graduation_name)

for line in Graduation_file:
    lst = line.split(',')
    ID = lst[0]
    # get graduation date
    dct[ID].append(lst[1].strip())

Graduation_file.close()

# part a
# Sort student last name alphabetically
lastName_list.sort()

# Create FullRoster.csv to store student ID, major, first name, last name, GPA, graduation date and indicate if
# disciplinary action was taken
f = open("FullRoster.csv", 'w')
for lastname in lastName_list:
    for ID in dct.keys():
        if dct[ID][0] == lastname:
            f.write(
                str(ID) + ',' + dct[ID][2] + ',' + dct[ID][1] + ',' + dct[ID][0] + ',' + dct[ID][4] + ',' + dct[ID][5])
            if dct[ID][3] != "":
                f.write(', ' + dct[ID][3])
                f.write('\n')
            else:
                f.write('\n')

f.close()

# part b
# Sort students' IDs
ID_list.sort()

# Create major files
for major in majors_list:
    fileName = major.replace(" ", "")
    f = open(fileName + '.csv', 'w')
    for ID in ID_list:
        if dct[ID][2] == major:
            f.write(str(ID) + ',' + dct[ID][0] + ',' + dct[ID][1] + ',' + dct[ID][5])
            if dct[ID][3] != "":
                f.write(', ' + dct[ID][3])
                f.write('\n')
            else:
                f.write('\n')
    f.close()

# part c
currentDate = datetime.datetime.now()
# create ScholarshipCandiates.csv file to store students who are eligible for scholarship
f = open("ScholarshipCandiates.csv", "w")
for ID in scholarship_list:
    if havegraduated(dct[ID][5], currentDate) and dct[ID][3] == "":
        f.write(str(ID) + ',' + dct[ID][0] + ',' + dct[ID][1] + ',' + dct[ID][2] + ',' + dct[ID][4])
        f.write('\n')
f.close()

# part d
# create DisciplinedStudents.csv file to store students that have been disciplined

sorted_list = []  # store students' ID in oder of graduation date from oldest to most recent
currentIndex = 0
olderDate = dct[disciplined_list[0]][5]

while len(disciplined_list) != 0:
    for i in range(len(disciplined_list)):
        currentID = disciplined_list[i]
        if isolder(olderDate, dct[currentID][5]) is False:
            olderDate = dct[currentID][5]
            currentIndex = i
    sorted_list.append(disciplined_list[currentIndex])
    disciplined_list.pop(currentIndex)
    currentIndex = 0

f = open("DisciplinedStudents.csv", "w")
for ID in sorted_list:
    f.write(str(ID) + "," + dct[ID][0] + ',' + dct[ID][1] + ',' + dct[ID][5])
    f.write('\n')
f.close()


# Part 2
# create a function to get a list of students with GPA within requested GPA
def eligible_student(gpa_input, num):
    gpa_valid = []  # create a list to store GPA within num
    for gpa in GPA_list:
        if (float(gpa) <= gpa_input + num) and (float(gpa) >= gpa_input - num):
            gpa_valid.append(gpa)

    id_valid = []  # store IDs that have GPA within 0.1 of the requested GPA
    for id_num in ID_list:
        if dct[id_num][4] in gpa_valid:
            id_valid.append(id_num)
    return id_valid


while True:
    user_input = input("Enter major and GPA: \n")
    # v. allow the user to quit
    if user_input == 'q':
        break

    # i. check that the student in Roster or not
    have_Student = False
    for major in majors_list:
        if major in user_input:
            have_Student = True
            break
    if not have_Student:
        print("No such student")
    else:
        # ii. print the information of student who has GPA within 0.1 and have not graduated or did not have
        # disciplinary action
        GPA_input = float(user_input.split(' ')[-1])
        for ID in eligible_student(GPA_input, 0.1):
            # check student have not graduated or did not disciplinary action
            if havegraduated(dct[ID][5], currentDate) and dct[ID][3] == "":
                print("Your students:")
                print(ID, dct[ID][1], dct[ID][0], dct[ID][4])

        # iii. GPA within 0.25
        for ID in eligible_student(GPA_input, 0.25):
            # check student have not graduated or did not disciplinary action
            if ID not in eligible_student(GPA_input, 0.1):
                if havegraduated(dct[ID][5], currentDate) and dct[ID][3] == "":
                    print("You may, also, consider:")
                    print(ID, dct[ID][1], dct[ID][0], dct[ID][4])

        # iv closest GPA to that requested
        if eligible_student(GPA_input, 0.1) == [] and eligible_student(GPA_input, 0.25) == []:
            closest_GPA = GPA_list[0]
            dif = abs(GPA_input - float(GPA_list[0]))
            for GPA in GPA_list:
                current_dif = abs(GPA_input - float(GPA))
                if current_dif < dif:
                    current_dif = dif
                    closest_GPA = GPA
            for ID in ID_list:
                if dct[ID][4] == closest_GPA:
                    if havegraduated(dct[ID][5], currentDate) and dct[ID][3] == "":
                        print("Student in the requested major has closest GPA to the requested GPA:")
                        print(ID, dct[ID][1], dct[ID][0], dct[ID][4])
