import datetime
from prettytable import PrettyTable as pt
import itertools as it

"""This function creates a new list for an individual"""


def indi_list():
    op_list = [0 for i in range(7)]
    op_list[5] = []
    return op_list


"""This function creates a new list for a family"""


def fam_list():
    op_list = [0 for i in range(6)]
    op_list[5] = []
    return op_list


import datetime

"""This function draws a pretty table for the individuals list"""


def draw_indi_table(ip_list):
    x = pt(['Individual_ID', 'Name', 'Sex', 'Birth Date', 'Death Date', 'Spouse In', 'Child In'])
    for i in ip_list:
        death = 'NA'
        spouse = 'NA'
        child = 'NA'
        if (i[4] != 0):
            death = i[4]
        if (i[5] != []):
            spouse = i[5]
        if (i[6] != 0):
            child = i[6]
        x.add_row([i[0], i[1], i[2], i[3], death, spouse, child])
    print(x)


"""This function draws a pretty table for the families list"""


def draw_fam_table(ip_list):
    x = pt(['Family_ID', 'Husband ID', 'Wife ID', 'Marriage Date', 'Divorce Date', 'Children'])
    for i in ip_list:
        div = 'NA'
        child = 'NA'
        if (i[4] != 0):
            div = i[4]
        if (i[5] != []):
            child = i[5]
        x.add_row([i[0], i[1], i[2], i[3], div, child])
    print(x)


"""This function takes input '/Last_Name/' and returns 'Last_Name' as output (removes the slashes in .ged file)"""


def getLastName(str):
    temp = ''
    for i in str:
        if (i != '/'):
            temp += i
    return temp


"""This function prints the contents of the input list"""


def print_list(ip_list):
    print("\n")
    for i in ip_list:
        print(i)


def getCurrDate():
    curr_date = str(datetime.date.today())
    return curr_date


"""This function converts the Date Format from '2000 JAN 5' to '2000-01-05' while parsing"""


def convertDateFormat(date):
    temp = date.split()
    if (temp[1] == 'JAN'): temp[1] = '01';
    if (temp[1] == 'FEB'): temp[1] = '02';
    if (temp[1] == 'MAR'): temp[1] = '03';
    if (temp[1] == 'APR'): temp[1] = '04';
    if (temp[1] == 'MAY'): temp[1] = '05';
    if (temp[1] == 'JUN'): temp[1] = '06';
    if (temp[1] == 'JUL'): temp[1] = '07';
    if (temp[1] == 'AUG'): temp[1] = '08';
    if (temp[1] == 'SEP'): temp[1] = '09';
    if (temp[1] == 'OCT'): temp[1] = '10';
    if (temp[1] == 'NOV'): temp[1] = '11';
    if (temp[1] == 'DEC'): temp[1] = '12';
    if (temp[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        temp[2] = '0' + temp[2]
    return (temp[0] + '-' + temp[1] + '-' + temp[2])



def CorrectGenderRoles(list_indi, list_fam):
    bad_list = []
    for i in list_fam:
        if (getSexByID(list_indi, i[1]) != 'M'):
            bad_list.append(i[1])
            print("US21: The Individual " + i[1] + " in family " + i[0] + " has incorrect Gender role.")
        if (getSexByID(list_indi, i[2]) != 'F'):
            bad_list.append(i[2])
            print("US21: The Individual " + i[2] + " in family " + i[0] + " has incorrect Gender role.")
    if (len(bad_list) == 0):
        print("US21: The Individuals in all the Families have correct gender roles.")
        print()
    else:
        print("US21: The following Individual(s) have incorrect gender role: ", end='')
        print(bad_list)
        print()


def getSexByID(list_indi, id):
    for i in list_indi:
        if (i[0] == id):
            return i[2]


"""This function parses the GEDCOM File and returns 2 lists: one for individuals and another for families"""


def parse(file_name):
    f = open(file_name, 'r')
    indi_on = 0
    fam_on = 0
    list_indi = []
    list_fam = []
    indi = indi_list()
    fam = fam_list()
    for line in f:
        str = line.split()
        if (str != []):
            if (str[0] == '0'):
                if (indi_on == 1):
                    list_indi.append(indi)
                    indi = indi_list()
                    indi_on = 0
                if (fam_on == 1):
                    list_fam.append(fam)
                    fam = fam_list()
                    fam_on = 0
                if (str[1] in ['NOTE', 'HEAD', 'TRLR']):
                    pass
                else:
                    if (str[2] == 'INDI'):
                        indi_on = 1
                        indi[0] = (str[1])
                    if (str[2] == 'FAM'):
                        fam_on = 1
                        fam[0] = (str[1])
            if (str[0] == '1'):
                if (str[1] == 'NAME'):
                    indi[1] = str[2] + " " + getLastName(str[3])
                if (str[1] == 'SEX'):
                    indi[2] = str[2]
                if (str[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']):
                    date_id = str[1]
                if (str[1] == 'FAMS'):
                    indi[5].append(str[2])
                if (str[1] == 'FAMC'):
                    indi[6] = str[2]
                if (str[1] == 'HUSB'):
                    fam[1] = str[2]
                if (str[1] == 'WIFE'):
                    fam[2] = str[2]
                if (str[1] == 'CHIL'):
                    fam[5].append(str[2])
            if (str[0] == '2'):
                if (str[1] == 'DATE'):
                    date = str[4] + " " + str[3] + " " + str[2]
                    if (date_id == 'BIRT'):
                        indi[3] = convertDateFormat(date)
                    if (date_id == 'DEAT'):
                        indi[4] = convertDateFormat(date)
                    if (date_id == 'MARR'):
                        fam[3] = convertDateFormat(date)
                    if (date_id == 'DIV'):
                        fam[4] = convertDateFormat(date)
    return list_indi, list_fam


def main(file_name):
    list_indi, list_fam = parse(file_name)
    list_indi.sort()
    list_fam.sort()

    # print_list(list_indi)
    # print_list(list_fam)

    draw_indi_table(list_indi)
    draw_fam_table(list_fam)

    CorrectGenderRoles(list_indi, list_fam)


main('My_Fam.ged')