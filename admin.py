import cx_Oracle
admin = 'SYSTEM'
adminp = 'vishi'
import getpass

con = cx_Oracle.connect(admin, adminp,'localhost')
cursor = con.cursor()
con.autocommit

class Bank_admin:


    def admenu():
          while True:
                print("\t\t menu")
                print("\t Enter : 1 to see Closed Account History")
                print("\tEnter : 2 Log Out")
                x = int(input("Enter Your choice -: "))
                if x == 1:
                    cursor.execute("select * from bank_account where closure = 0")
                    data = cursor.fetchall()
                    for d in data:

                        date=str(d[7])
                        print(d[1], d[2], d[3], d[5], d[6],date[:11])
                if x == 2:
                    return


    def admin_log():
        aduser = input("Enter admin User Name -: ")
        adpass = input("Enter admin Password -:")
        if aduser == admin:
            if adpass == adminp:
                Bank_admin.admenu()
            else:
                print("Password Incorrect !")
        else:
            print("User Name Is Incorrect !")
