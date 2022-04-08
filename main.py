# Khue Nhat Do
# ID 2095632

import datetime

# create a function to check that student has graduated or not
def haveGraduated(graduatedDate, currentDate):
    date = graduatedDate.split('/')
    month = int(date[0])
    day = int(date[1])
    year = int(date[2])
    if year < currentDate.year - 2000:
        return False
    elif year > currentDate.year - 2000:
        return True
    else:
        if month > currentDate.month:
            return True
        elif month < currentDate.month:
            return False
        else:
            if day > currentDate.day:
                return True
            else:
                return False

# create a function to compare two different dates
def isOlder(date1, date2):
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
            if day1 > day2 :
                return False
            else:
                return True

# create a dictionary to store the students' information as {ID: [firstName(0), lastName(1), major(2), discipline(3), GPA(4), graduationdate(5)]}
dct = {}

# open StudentMajorsList.csv and get their information
majors_file_name = input("Enter the major's file name:\n")
majors_file = open(majors_file_name)
lastName_list = []  # store last name in the list
majors_list = []   # store majors
ID_list = []   # store IDs
disciplined_list = []   # store students who have been disciplined

for line in majors_file:
    lst = line.split(',')
    ID = lst[0]
    ID_list.append(ID)
    dct[ID] = []
    # get firstName
    dct[ID].append(lst[1])
    # get lastName
    dct[ID].append(lst[2])
    lastName_list.append(lst[2])
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

for line in GPA_file:
    lst = line.split(',')
    ID = lst[0]
    # get GPA
    GPA = lst[1].strip()
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

# Create FullRoster.csv to store student ID, major, first name, last name, GPA, graduation date and indicate if disciplinary action was taken
f = open("FullRoster.csv", 'w')
for lastname in lastName_list:
    for ID in dct.keys():
        if dct[ID][1] == lastname:
            f.write(str(ID)+','+dct[ID][2]+','+dct[ID][0]+','+dct[ID][1]+','+dct[ID][4]+','+dct[ID][5])
            if dct[ID][3] != "":
                f.write(', '+dct[ID][3])
                f.write('\n')
            else:
                f.write('\n')

f.close()


# part b
# Sort students' IDs
ID_list.sort()

# Create major files
for major in majors_list:
    fileName = major.replace(" ","")
    f = open(fileName+'.csv','w')
    for ID in ID_list:
        if dct[ID][2] == major:
            f.write(str(ID)+','+dct[ID][1]+','+dct[ID][0]+','+dct[ID][5])
            if dct[ID][3] != "":
                f.write(', '+dct[ID][3])
                f.write('\n')
            else:
                f.write('\n')
    f.close()


# part c
currentDate = datetime.datetime.now()
# create ScholarshipCandiates.csv file to store students who are eligible for scholarship
f = open("ScholarshipCandiates.csv","w")
for ID in scholarship_list:
    if haveGraduated(dct[ID][5], currentDate) and dct[ID][3] == "":
        f.write(str(ID)+','+dct[ID][1]+','+dct[ID][0]+','+dct[ID][2]+','+dct[ID][4])
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
        if isOlder(olderDate,dct[currentID][5]) is False:
            olderDate = dct[currentID][5]
            currentIndex = i
    sorted_list.append(disciplined_list[currentIndex])
    disciplined_list.pop(currentIndex)
    currentIndex = 0
    olderDate = dct[disciplined_list[0][5]]

f = open("DisciplinedStudents.csv", "w")
for ID in sorted_list:
    f.write(str(ID)+","+dct[ID][1]+','+dct[ID][0]+','+dct[ID][5])
    f.write('\n')
f.close()

