from admin import Bank_admin
from log_on import Sign_in
import cx_Oracle
import sys
import datetime
admin = 'SYSTEM'
adminp = 'vishi'
con = cx_Oracle.connect(admin, adminp,'localhost')
cursor = con.cursor()
con.autocommit



def sign_up():
    name = input("Enter your Name -: ")
    address = input("Enter Your Address -: ")
    pwd = input("Enter your Password -: ")
    acc_type = input("Enter Account Type :\n C for Current account \n S for Saving Account  -: ")
    bal=0
    try:
        if acc_type.lower() == 'c':
            print("Amount to be deposited should be > 5000")
            bal =int(input("Enter Amount You Want to Deposit -: "))
            if bal < 5000:
               print("Amount is low : can't open account")
               return
        elif acc_type.lower() == 's':
            print("Amount to be deposited should be > 1000")
            bal = int(input("Enter Amount You Want to Deposit -: "))
            if bal < 1000:
                print("Amount is low : can't open account")
                return
        else:
            print("Invalid Account Type")
            return
        todate = datetime.datetime.now()
        td = str(todate.strftime('%d-%m-%Y'))
        cursor.execute("insert into bank_account values(BANK_ACCOUNT_SEQ.nextval,BANK_ACCOUNT_SEQ_NO.nextval,:1,:2,:3,:4,:5,to_date(:6,'dd/mm/yyyy'),1)" , (name , address , pwd , acc_type , bal , td))
        con.commit()
        cursor.execute("select account from  BANK_ACCOUNT")
        data = cursor.fetchall()
        print("Your Account No. is Your Customer Id : ",data[-1][0])
        cursor.execute("insert into balance_sheet values(:1,:2,null,to_date(:3,'dd/mm/yyyy'),:4)",(data[-1][0], bal, td, bal))
        con.commit()
        return
    except:
        print("Something Went Wrong !!")
        return


def main():
    while True:
        print("\tMain Menu\t")
        print("\t\tEnter : 1 to Sign In")
        print("\t\tEnter : 2 to Sign Up")
        print("\t\tEnter : 3 to Admin Sign In")
        print("\t\tEnter : 4 to Quit")

        x = int(input("\t\tEnter user's Choice -: "))
        if x == 4:
            sys.exit("Thank you")
        elif x == 3:
            Bank_admin.admin_log()
        elif x == 2:
            sign_up()
        elif x == 1:
            Sign_in.sign_in()
        else:
            print("Invalid Input")



main()
