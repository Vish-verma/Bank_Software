import cx_Oracle
con = cx_Oracle.connect('SYSTEM','vishi','localhost')
cursor = con.cursor()
try :
    cursor.execute("CREATE table BANK_ACCOUNT (ID NUMBER(5) NOT NULL, ACCOUNT NUMBER(10) NOT NULL, NAME VARCHAR2(20) NOT NULL, ADDRESS VARCHAR2(100) NOT NULL, PASS VARCHAR2(10) NOT NULL, TYPE VARCHAR2(2) NOT NULL, BALANCE NUMBER(30) NOT NULL, DOC DATE NOT NULL,CLOSURE NUMBER(1), constraint  BANK_ACCOUNT_PK primary key (ID))")
except Exception :
    print()

try:
    cursor.execute("alter table BANK_ACCOUNT add constraint BANK_ACCOUNT_UK1 unique (ACCOUNT)")
except Exception:
    print()

try:
    cursor.execute("create sequence BANK_ACCOUNT_SEQ start with 1 increment by 1 nocache nocycle noorder")

except Exception:
    print()

try :
    cursor.execute(" CREATE trigger BI_BANK_ACCOUNT  before insert on BANK_ACCOUNT for each row begin  if :NEW.ID is null then select BANK_ACCOUNT_SEQ.nextval into :NEW.ID from dual;end if;end;")
except Exception:
    print()

try:
    cursor.execute("create sequence BANK_ACCOUNT_SEQ_NO start with 1000 increment by 1 nocache nocycle noorder")

except Exception:
    print()

try:
    cursor.execute(" CREATE trigger BI_BANK_ACCOUNT_NO  before insert on BANK_ACCOUNT for each row begin  if :NEW.ACCOUNT is null then select BANK_ACCOUNT_SEQ_NO.nextval into :NEW.ACCOUNT from dual;end if;end;")
except Exception:
    print()

try:
    cursor.execute("CREATE table BALANCE_SHEET (ACCOUNT NUMBER(10,0) NOT NULL,DEPOSIT NUMBER(30,0),WITHDRAW NUMBER(30,0),DOT DATE NOT NULL,BALANCE NUMBER(30))")
except Exception:
    print()