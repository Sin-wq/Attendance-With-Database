#!C:\Users\SyEdM\AppData\Local\Programs\Python\Python310\python.exe
from tkinter import Grid
from wsgiref import headers
from tabulate import tabulate
import cx_Oracle
import time
import getpass
import stdiomask

con = cx_Oracle.connect("system/system@localhost/xe")
cur = con.cursor()
user = ()

def clrScr():
    for i in range(30):
        print("\n")

def loginoption():
    clrScr()
    opt = input(
        """
        1. Login as Principal
        2. Login as HOD
        3. Login as Student
        4. Exit
        select an option: """
    )

    if opt.isdigit():
        pass
    else:
        print("---Enter a number to choose option---")
        time.sleep(1)
        loginoption()

    opt = int(opt)    

    if (opt == 1):
        principalLogin()
    elif (opt == 2):
        loginHOD()
    elif (opt == 3):
        loginStudent()
    elif(opt == 4):
        exit()    
    else:
        print("---Enter correct option---")
        time.sleep(1)
        loginoption()          

def principalLogin():
    clrScr()
    Name = input("Enter your name: ")
    # password = input("Enter your password: ")
    
    password = stdiomask.getpass("Enter your password: ")
    if (Name == "" or password == ""):
        print("---Enter something!---")
        clrScr()
        time.sleep(1)
        principalLogin()
    
    if Name.isdigit():
        print("---Enter name in chars---")
        time.sleep(1)
        clrScr()
        principalLogin()

    if password.isdigit():
        pass
    else:
        print("---Enter password in numbers---")
        time.sleep(1)
        clrScr()
        principalLogin()

    Name = Name.upper()
    # print(Name)
    if (Name == "SIR" and password == "0000"):
        clrScr()
        leaveshow()

def leaveshow():
    global user
    global cur
    clrScr()
    choice = input(
        """
        1. Show All leaves
        2. Show leaves by department
        3. Logout
        4. Logout and Exit
        select an option: """
    )
    if choice.isdigit():
        pass
    else:
        print("---Enter a number to choose option---")
        time.sleep(1)
        clrScr()
        leaveshow()

    choice = int(choice)  

    if (choice == 1):
        cur.execute("select * from leaveinfo")
        leaves = cur.fetchall()
        head = ["rollno","date","no of days","reason","approved","remarks"]
        print(tabulate(leaves, headers=head, tablefmt="grid"))
        input("press any key to go back to menu ")
        clrScr()
        leaveshow()
    elif (choice == 2):
        depart = input("Enter Course Name: ")
        depart = depart.upper()
        cur.execute(f"select ROW_NUMBER() OVER (ORDER BY leavedate) serial,studentinfo.rollno , leavedate ,  noofdays ,  reason , approved  , remark    from    studentinfo,leaveinfo where studentinfo.rollno = leaveinfo.rollno  and  course = '{depart}'")        
        departleaves = cur.fetchall()
        head = ["serial","rollno","date","no of days","reason","approved","remarks"]
        print(tabulate(departleaves, headers=head, tablefmt="grid"))
        input("Press any key to go back to menu ")
        clrScr()
        leaveshow()
    elif (choice == 3):
        clrScr()
        loginoption()
    elif (choice == 4):
        clrScr()
        exit()
    else:
        print("---Enter correct option---")
        time.sleep(1)
        clrScr()
        principalLogin()

def loginHOD():
    global user 
    global cur
    clrScr()
    Name = input("Enter your name: ")
    password = stdiomask.getpass("Enter your password: ")

    if (Name == "" or password == ""):
        print("---Enter something!---")
        time.sleep(1)
        clrScr()
        loginHOD()

    if password.isdigit():
        pass
    else:
        print("---Enter password in number---")
        time.sleep(1)
        clrScr()
        loginHOD()

    # password = int(password)       

    user=cur.execute(f"Select * from HODinfo where name='{Name}' and password='{password}'")
    user = cur.fetchone()

    if(user == None): #check if user exists
        print("---enter a valid name and password---")
        time.sleep(1)
        clrScr()
        loginHOD()
    else:
        print("Logged in succesfully!")
        time.sleep(1)
        clrScr()
        menuforhod()

def menuforhod():
    global user
    clrScr()
    print(f"Welcome {user[0]}\n")
    option = input(
        """
        1. View and edit leave requests
        2. View approved or disapproved leave requests 
        3. logout
        4. logout and exit
        select an option: """
    )

    if option.isdigit():
        pass
    else:
        print("---Enter a number to choose option---")
        time.sleep(1)
        clrScr()
        menuforhod()

    option = int(option)    

    if(option < 1 or option > 4):
        print("---Enter a valid option---")
        time.sleep(1)
        clrScr()
        menuforhod()
    
    if(option == 1):
        editHistoryforhod()
    elif(option == 2):
        viewHistoryforhod()
    elif(option >= 3):
        user=()
        print("You logged out!")
        time.sleep(1)
        clrScr()
    
        if(option==3):
            loginoption()
        elif(option==4):
            exit()

def editHistoryforhod():
    global cur
    global user
    clrScr()
    cur.execute(f"SELECT ROW_NUMBER() OVER (ORDER BY leavedate) serial, rollno,leavedate,noofdays,reason,approved,remark FROM leaveinfo where approved is null")
    leaves = cur.fetchall()
    head = ["serial","rollno","date","no of days","reason","approved","remarks"]
    print(tabulate(leaves,headers=head,tablefmt="grid"))
    serial = (input("enter the serial number you want to approve or reject or press any key to go to main menu:"))
    if (serial == ""):
        menuforhod()
       

    if serial.isdigit():
        serial = int(serial)
        for leave in leaves:
            if(serial > leave[0]):
                print("---enter correct serial---")
                time.sleep(1)
                editHistoryforhod() 
        rol = leaves[serial-1][1]
        approved = input(f"Press Y to approve or N to reject: ")
        if (approved != "Y" and approved != "y" and approved != "N" and approved !="n"):
            print("---Try again. Enter Y or N---")
            time.sleep(1)
            editHistoryforhod()

        remarks = input("Enter remark:")
        if (len(remarks) > 150):
            print("---Try again. Enter remarks in less than 150 chars---")
            time.sleep(1)
            editHistoryforhod()

        query = f"update leaveinfo set approved='{approved}',remark='{remarks}' where rollno={rol} and leavedate=to_DATE('{leaves[serial-1][2]}','yyyy-mm-dd hh24:mi:ss')"
        cur.execute(query)
        con.commit()
        editHistoryforhod()
        clrScr()
    else:
        time.sleep(1)
        menuforhod()

    input("press any key to go back to menu")
    menuforhod()

def viewHistoryforhod():
    global cur
    global user
    clrScr()
    cur.execute(f"select rollno, name, leavedate, noofdays, reason from (select * from leaveinfo inner join studentinfo using(rollno)) where approved is not null")
    leaves = cur.fetchall()
    head = ["rollno","Name","date","no of days","reason"]
    print(tabulate(leaves,headers=head,tablefmt="grid"))
    input("press any key to go back to menu: ")    
    menuforhod()

def loginStudent():
    global user
    global cur
    clrScr()
    rollno = input("Enter your rollno: ")
    passwd = stdiomask.getpass("Enter your password: ")

    if(rollno == "" or passwd == "" ):
        print("---Enter something!---")
        time.sleep(1)
        clrScr()
        loginStudent()

    if rollno.isdigit():
        pass
    else:
        print("---Enter in numbers---")
        time.sleep(1)
        clrScr()
        loginStudent()       
    
    rollno = int(rollno)

    if rollno < 1: #check if rollno is positve 
        print("---enter a valid rollno---")
        time.sleep(1)
        clrScr()
        loginStudent()
    else:
        user=cur.execute(f"Select * from studentinfo where rollno={rollno} and password='{passwd}'")
        user = cur.fetchone()
        if(user == None): #check if user exists
            print("---enter a valid rollno and password---")
            time.sleep(1)
            clrScr()
            loginStudent()
        else:
            menu()

def menu():
    global user
    global cur
    clrScr()
    print(f"Welcome {user[2]}, rollno: {user[0]}, {user[3]}\n")
    option = int(input(
        """
        1. Apply for leave
        2. View leave status/history
        3. Change Password
        4. logout
        5. logout and exit
        select an option: """
    ))
    if(option < 1 or option > 5):
        print("---Enter valid option---")
        time.sleep(1)
        clrScr()
        menu()
    
    if(option == 1):
        applyForLeave()    
    elif(option == 2):
        viewHistory()
    elif(option == 3):
        password()                    
    elif(option >=4):
        user=()
        print("you logged out")
        time.sleep(1)
        clrScr()
    
        if(option==4):
            loginoption()
        elif(option==5):
            exit()
             
    else:
        print("---Enter correct option!---")
        time.sleep(1)
        clrScr()
        menu()        
            
def applyForLeave():
    clrScr()
    global user
    global cur
    checks = cur.execute(f"select sum(noofdays) from leaveinfo where rollno={user[0]}")
    checks = cur.fetchall()
    if (checks[0][0] >= 10):
        print("You can not apply for leaves anymore")    
        time.sleep(1)
        menu()
    leaveDate = input("enter leave date as dd-mm-yy: ")
    noOfDays = (input("enter no of days: "))
    reason = input("enter reason(under 150 chars): ")
    
    splitDate = leaveDate.split("-")

    if(len(splitDate) != 3):
        print("---enter a valid date---")
        time.sleep(1)
        clrScr()
        applyForLeave()
        return

    for i in range(3):
        split = int(splitDate[i])
        if(i == 0): #validate day
            if(split < 1 or split > 31):
                print("---enter a valid day---")
                time.sleep(1)
                clrScr()
                applyForLeave()
                return
        elif(i==1):
            if(split < 1 or split > 12):
                print("---enter a valid month---")
                time.sleep(1)
                clrScr()
                applyForLeave()
                return
        elif(i==2):
            if(split < 21):
                print("---enter a valid year---")
                time.sleep(1)
                clrScr()
                applyForLeave()
                return

    if noOfDays.isdigit():
        noOfDays = int(noOfDays)
    else:
        print("---Enter valid number of days---")
        time.sleep(1)
        clrScr()
        applyForLeave()
        
    if(noOfDays < 1):
        print("---enter a valid date---")
        time.sleep(1)
        clrScr()
        applyForLeave()
        return
    
    if reason.isdigit():
        print("---Enter reason in characters---")
        time.sleep(1)
        clrScr()
        applyForLeave()
        
    if(len(reason) > 150):
        print("---specify reason in less than 150 chars---")
        time.sleep(1)
        clrScr()
        applyForLeave()
    
    query = f"insert into leaveinfo values({user[0]}, TO_DATE('{leaveDate}','dd-mm-yy'), {noOfDays}, '{reason}', NULL, NULL)"
    cur.execute(query)
    con.commit()
    print("---Entered successfully---")
    time.sleep(1)
    clrScr()
    menu()

def viewHistory():
    global cur
    global user
    clrScr()
    cur.execute(f"select * from leaveinfo where rollno={user[0]}")
    leaves = cur.fetchall()
    for leave in leaves:
        head = ["rollno","date","no of days","reason","approved","remarks"]
        print(tabulate(leaves,headers=head,tablefmt="grid"))
        # print(f"rollno: {leave[0]} \t | date: {leave[1]} \t | no of days: {leave[2]} \t | reason: {leave[3]} \t | approved: {leave[4]} \t | remarks: {leave[5]} \t |")
    input("press any key to go back to menu")
    menu()

def mainmenu():
    opt2 = input("Press 'M' if you want to enter main menu else press any key to continue: ")
    if (opt2 == "M" or opt2 == "m"):
        time.sleep(1)
        clrScr()
        menuforhod()
    elif(opt2 != "M" and opt2 != "m"):
        pass
        
def password():
    global user
    global cur
    pasword = input("Enter password you want to keep: ")
    if (pasword == ""):
        print("---Enter something---")
        time.sleep(1)
        password()
    # print(user)
    # print(type(user))    
    query = f"update studentinfo set password = '{pasword}' where rollno={user[0]}"
    cur.execute(query)
    con.commit()
    print("Updated succesfully")
    time.sleep(1)
    clrScr()
    menu()
        


    


loginoption()
