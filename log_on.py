import sys
import datetime
import cx_Oracle
import getpass


con = cx_Oracle.connect('SYSTEM', 'vishi','localhost')
cursor = con.cursor()
con.autocommit


class Sign_in:


    def obtaint_date():
        isValid = False
        while not isValid:
            userIn = input("Type Date dd/mm/yyyy -: ")
            try:  # strptime throws an exception if the input doesn't match the pattern
                d = datetime.datetime.strptime(userIn, "%d/%m/%Y")
                isValid = True
            except:
                print(" try again!\n")
        return d


    def closure(cust_id):
        cursor.execute("update bank_account set closure = 0 where account = :1 ", {'1': cust_id})
        con.commit()
        print("ACCOUNT IS CLOSED !!")



    def addr(cust_id):
        ad = input("Enter New Address -: ")
        # print(cust_id)
        cursor.execute("update bank_account set address =:1 where account =:2", (ad, cust_id))
        con.commit()
        print("ADDRESS UPDATED !!")


    def deposit(cust_id):
        x = int(input("Enter Amount You Want to Deposit -: "))
        todate = datetime.datetime.now()
        cursor.execute("select balance from bank_account where account = :1", {'1': cust_id})
        data = cursor.fetchall()
        td = str(todate.strftime('%d-%m-%Y'))
        cursor.execute("insert into balance_sheet values(:1,:2,null,to_date(:3,'dd/mm/yyyy'),:4)",
                       (cust_id, x, td, x + data[0][0]))
        con.commit()
        print("Your Amount Has been Deposited ")
        x = x + int(data[0][0])
        cursor.execute("update bank_account set balance = :1 where account = :2", (x, cust_id))
        con.commit()
        print("all done")


    def withdraw(cust_id):
        x = int(input("Enter Amount You Want to withdraw -:"))
        todate = datetime.datetime.now()
        cursor.execute("select balance,type from bank_account where account = :1", {'1': cust_id})
        data = cursor.fetchall()
        if data[0][1] == 's':
            if (data[0][0] - x) >= 0:
                td = str(todate.strftime('%d-%m-%Y'))
                cursor.execute("insert into balance_sheet values(:1,null,:2,to_date(:3,'dd/mm/yyyy'),:4)",
                               (cust_id, x, td,  data[0][0] - x))
                con.commit()
                print("Your Amount Has been Withdrawn ")
                x =  int(data[0][0]) - x
                cursor.execute("update bank_account set balance = :1 where account = :2", (x, cust_id))
                con.commit()
                print("all done")
            else:
                print("Can't withdraw the Amount Minimum balance of account should be Rs1000")

        elif data[0][1] == 'c':
            if (data[0][0] - x) >= 0:
                td = str(todate.strftime('%d-%m-%Y'))
                cursor.execute("insert into balance_sheet values(:1,null,:2,to_date(:3,'dd/mm/yyyy'),:4)",
                               (cust_id, x, td, data[0][0] - x))
                con.commit()
                print("Your Amount Has been Withdrawn ")
                x = int(data[0][0]) - x
                cursor.execute("update bank_account set balance = :1 where account = :2", (x, cust_id))
                con.commit()
                print("all done")
            else:
                print("Can't withdraw the Amount Minimum balance of account should be Rs5000")


    def transfer(cust_id):
        todate = datetime.datetime.now()
        acc_no = int(input("Enter Account No. You want to Transfer money To -: "))
        amt = int(input("Enter Amount you Want to Transfer -: "))
        cursor.execute("select balance, type from bank_account where account =:1", {'1':cust_id})
        data = cursor.fetchall()

        try:
            cursor.execute("select balance from bank_account where account = :1", {'1':acc_no})
        except:
            print("Enter valid Account No.")
            return
        data1 = cursor.fetchall()
        try:
            if data[0][1] == 's':
                if (data[0][0] - amt) >= 0:
                    cursor.execute("update bank_account set balance = :1 where account = :2", (data[0][0] - amt, cust_id))
                    con.commit()
                    td = str(todate.strftime('%d-%m-%Y'))
                    cursor.execute("insert into balance_sheet values(:1,null,:2,to_date(:3,'dd/mm/yyyy'),:4)",
                                   (cust_id, amt, td, data[0][0] - amt))
                    con.commit()
                    cursor.execute("update bank_account set balance = :1 where account = :2", (data1[0][0] + amt, acc_no))
                    con.commit()
                    cursor.execute("insert into balance_sheet values(:1,:2,null,to_date(:3,'dd/mm/yyyy'),:4)",
                                   (acc_no, amt, td, data1[0][0] + amt))
                    con.commit()
                    print("Transfer Succesfull !!")
                else:
                    print("Transfer Can't Be Performed Insufficient Balance")
            elif data[0][1] == 'c':
                if (data[0][0] - amt) >= 0:
                    cursor.execute("update bank_account set balance = :1 where account = :2", (data[0][0] - amt, cust_id))
                    con.commit()
                    td = str(todate.strftime('%d-%m-%Y'))
                    cursor.execute("insert into balance_sheet values(:1,null,:2,to_date(:3,'dd/mm/yyyy'),:4)",
                                   (cust_id, amt, td, data[0][0] - amt))
                    con.commit()
                    cursor.execute("update bank_account set balance = :1 where account = :2", (data1[0][0] + amt, acc_no))
                    con.commit()
                    cursor.execute("insert into balance_sheet values(:1,:2,null,to_date(:3,'dd/mm/yyyy'),:4)",
                                   (acc_no, amt, td, data1[0][0] + amt))
                    con.commit()
                    print("Transfer Succesfull !!")
                else:
                    print("Transfer Can't Be Performed Insufficient Balance")
        except:
            print("Something Went Wrong !!")
            return

    def mini_state(cust_id):
        date1 = Sign_in.obtaint_date()
        date2 = Sign_in.obtaint_date()
        if date1 < date2:
            cursor.execute("Select * from balance_sheet where account = :1 and dot >= :2 and dot <=:3",
                           (cust_id, date1, date2))
            data = cursor.fetchall()
            print("\tAccount No.\t Deposit\t Withdraw\t Balance\tdate")
            for d in data:
                print('\t', d[0],'\t\t', d[1],'\t\t', d[2],'\t\t', d[4],'\t\t', d[3].strftime("%d-%m-%Y"))
        else:
            print("First Date Should be Less Than Second Date")

    def log_in(cust_id):
        while True:
            print("\t\tmenu")
            print("\t\tEnter : 1 to Address Change")
            print("\t\tEnter : 2 to Money Deposit")
            print("\t\tEnter : 3 to Money Withdraw")
            print("\t\tEnter : 4 to Print Statement")
            print("\t\tEnter : 5 to Transfer Money")
            print("\t\tEnter : 6 to Account Closure")
            print("\t\tEnter : 7 to Log Out")
            ch = int(input("\t\tEnter Your Choice -: "))
            if ch == 7:
                return

            elif ch == 6:
                Sign_in.closure(cust_id)
            elif ch == 5:
                Sign_in.transfer(cust_id)
            elif ch == 4:
                Sign_in.mini_state(cust_id)
            elif ch == 3:
                Sign_in.withdraw(cust_id)
            elif ch == 2:
                Sign_in.deposit(cust_id)
            elif ch == 1:
                Sign_in.addr(cust_id)
            else:
                print("Enter Valid Value")

    def sign_in():
        cust_id = int(input("Enter Your Customer ID -: "))
        pwd = 0
        c = 3
        try:

            while c != 0:
                pwd = input("Enter Your Password -:")
                cursor.execute("select pass , closure from BANK_ACCOUNT where account = :1", {'1': cust_id})
                data = cursor.fetchall()
                if data[0][1] == 1:
                    if data[0][0] == pwd:
                       Sign_in.log_in(cust_id)
                       return
                        ##sys.exit("Thank You ")
                    else:
                        --c
                        print("TRY AGAIN")
                        print("Only %s Trials Left" % c)
                else:
                    print("This Account has been Closed")


            sys.exit("Try Again After Some Time ")
        except:
            print("Invalid Login Credentials !")
            Sign_in.sign_in()