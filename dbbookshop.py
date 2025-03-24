#do install MySQL locally
import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",passwd="1234")
mc=db.cursor()
mc.execute("create database if not exists bookshop")
l=[]
def menu():
    print("\n1) Add a Book \n2) Search a Book \n3) Show Booklist \n4) Remove a Book \n5) Show CART \n6) Exit")
    print("\n\tEnter your choice: ", end="")
    n = int(input())
    if n == 1:
        insert()
    if n == 2:
        search()
    if n == 3:
        show()
    if n == 4:
        remove()
    if n == 5:
        cart()
    if n == 6:
        print("\nChanges have been made successfully !!! \n\t\t    Good bye")
    if n < 1 or n > 6:
        print("\nChoice is invalid")
        menu()

def insert():
    mc.execute("use bookshop")
    mc.execute("create table if not exists books(bookid char(8) primary key not null, name varchar(20), price int(5))")
    n=input("\nEnter the Name of the Book  : ")
    b=input("Enter the Bookid  : ")
    pr=int(input("Enter the price of the Book  : "))
    sql="insert into books values(%s,%s,%s)"
    val=(b.lower(),n.lower(),pr)
    try:
        mc.execute(sql,val)
        db.commit()
        print("The book has been added !!!")
        menu()
    except:
        print("An error has occurred try again...")
        db.rollback()
        menu()

def search():
    t=True
    mc.execute("use bookshop")
    n=input("\nEnter the Name of the book you want to search  : ")
    mc.execute("select name from books")
    cm=mc.fetchall()
    for i in range(len(cm)):
        if cm[i][0]==n.lower():
            t=False
            break
    if t==False:
        s="select bookid , price from books where name = %s"
        val=(n.lower(),)
        mc.execute(s,val)
        c=mc.fetchall()
        print("\n\tID of the Book      : ", c[0][0])
        print("\n\tName of the Book    : ", n.title())
        print("\n\tPrice of the Book   : ", c[0][1],"/-")
        q=input("\nDo you want to add it to cart ? : (y/n) : ")
        global l
        if q=='y':
            l.append(n.lower())
            q1=input("\n1) Want to continue to payment ? \n2) Want to add more books ? \n3) Back to menu \n: ")
            if q1=='1':
                payment()
            if q1=='2':
                search()
            if q1=='3':
                menu()
        else:
            menu()
    else:
        print("Such Book is not present in the list")
        menu()

def show():
    mc.execute("use bookshop")
    mc.execute("select * from books")
    cm=mc.fetchall()
    if cm==[]:
        print("\nBook list is empty")
        menu()
    else:
        print("\n\\\_______________________//|\\________________________///")
        print("\n                       BOOK LIST                         ")
        print("________________________________________________________")
        for i in range(len(cm)):
                print("\n", i + 1, ')', '\t    The Name of the Book :  ', cm[i][1].title())
                print("\t    Book ID              :  ", cm[i][0])
                print("\t    Book's Price         :  ", cm[i][2],"/-")
        print("---_______________________-----________________________---")
        menu()
def remove():
    t=True
    mc.execute("use bookshop")
    n=input("Enter the Name of the book you want to remove  : ")
    mc.execute("select name from books")
    cm=mc.fetchall()
    for i in range(len(cm)):
        if cm[i][0]==n.lower():
            t=False
            break
    if t==False:
        try:
            s="delete from books where name = %s"
            val=(n.lower(),)
            mc.execute(s,val)
            db.commit()
            print("Record has been succesfully removed")
            menu()
        except:
            print("an error has occurred try again....")
            db.rollback()
            menu()
    else:
        print("No such book was found")
        menu()

def cart():
    if l == []:
        print("\n\t------Cart is empty------")
        menu()
    else:
        tp=0
        mc.execute("use bookshop")
        s="select bookid , price from books where name = %s"
        print("----------------------------------------------------------------")
        print("                        :   CART   :                            ")
        print("----------------------------------------------------------------")
        for i in range(len(l)):
            val=(l[i],)
            mc.execute(s,val)
            c=mc.fetchall()
            print("\n\n\t",i+1,")    ID of the Book      : ", c[0][0])
            print("\n\t\tName of the Book    : ", l[i].title())
            print("\n\t\tPrice of the Book   : ", c[0][1],"/-")
            tp+=c[0][1]
        print("----------------------------------------------------------------")
        print("\t\tTOTAL AMOUNT        : ", tp, "/-")
        print("----------------------------------------------------------------")
        while True:
            q = input("\n\t1) Direct to payment \n\t2) Add more books \n\t:")
            if q == "1":
                payment()
                break
            if q == "2":
                search()
                break
            else:
                print("input invalid")
def payment():
    mc.execute("use bookshop")
    s="select bookid , price from books where name = %s"
    tp=0
    print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("                       ----:   BILL  :----                         ")
    print("╔═════════════════════════════════════════════════════════════════╗")
    for i in range(len(l)):
        val=(l[i],)
        mc.execute(s,val)
        c=mc.fetchall()
        print("\n\n\t",i+1,")    ID of the Book      : ", c[0][0])
        print("\n\t\tName of the Book    : ", l[i].title())
        print("\n\t\tPrice of the Book   : ", c[0][1],"/-")
        tp+=c[0][1]
    print("───────────────────────────────────────────────────────────────────")
    print("\t\tTOTAL AMOUNT        : ", tp, "/-")
    print("───────────────────────────────────────────────────────────────────")
    print("━━━━━━━━━━━━━━━━━━━ DO VISIT OUR BOOK SHOP AGAIN ━━━━━━━━━━━━━━━━━━")
    
menu()
