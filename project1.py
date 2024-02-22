from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from PIL import Image, ImageTk
from mysql.connector import connect

conn = connect(
    host = 'localhost',
    user = 'root', #depends on your sql username
    password = 'hima@772005',
    database = 'demo'
)
conn2 = connect(
    host = 'localhost',
    user = 'root', #depends on your sql username
    password = 'hima@772005',
    database = 'demo3'
)

cursor = conn.cursor()
cursor2 = conn2.cursor()
class Home:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root, width=550, height= 350, bd= 4, relief= 'ridge', bg= 'black')
        self.frame.place(x = 0,y = 0)

        self.bg   = Image.open('..\\wise\\assests\\doctor.jpg')
        self.bg = self.bg.resize((550, 350))
        self.bg = ImageTk.PhotoImage(self.bg)

        self.bg_lbl = Label(self.frame, image= self.bg)
        self.bg_lbl.place(x= 0, y = 0)

        self.lbl=  Label(self.frame, text= 'select the option', bg = 'white', fg = 'steel blue', font=('Courier New', 20, 'bold'))
        self.lbl.place(x = 150, y = 80)

        self.btn_1=  Button(self.frame, text= 'Doctor',font=('Courier New', 20, 'bold'), bg = 'white', cursor = 'hand2', command= self.login)
        self.btn_1.place(x = 150, y = 150)
        #self.btn_1.bind("Button-2",self.warden)

        self.btn_2=  Button(self.frame, text= 'Patient',font=('Courier New', 20, 'bold'), bg = 'white', cursor = 'hand2', command= self.login_s)
        self.btn_2.place(x = 300, y = 150)

        self.goto_register = Label(self.frame, text= 'NOT A MEMBER YET? SIGNUP!', font=('Courier New', 10, 'bold'))
        self.goto_register.place(x = 5, y = 300)
        self.goto_register.bind("<Button-1>", self.change_page)


    def change_page(self,event):
        self.frame.destroy()
        register = Register(root)

    def login_s(self):
        self.bg_lbl = Label(self.frame, image= self.bg)
        self.bg_lbl.place(x= 0, y = 0)

        self.lbl=  Label(self.frame, text= 'PATIENT LOGIN DETAILS', bg = 'white', fg = 'steel blue', font=('Courier New', 18, 'bold'))
        self.lbl.place(x = 130, y = 100)

        self.lbl=  Label(self.frame, text= 'USER NAME', bg = 'white', fg = 'steel blue', font=('Courier New', 20, 'bold'))
        self.lbl.place(x = 50, y = 150)

        self.stu_entry = Entry(self.frame, width = 20, font=('Courier New', 18, 'bold'), bg = 'white')
        self.stu_entry.place(x = 220, y = 150)

        self.lbl=  Label(self.frame, text= 'PASSWORD', bg = 'white', fg = 'steel blue', font=('Courier New', 20, 'bold'))
        self.lbl.place(x = 50, y = 200)

        self.stu_p = Entry(self.frame, width = 20, font=('Courier New', 18, 'bold'), bg = 'white')
        self.stu_p.place(x = 220, y = 200)
        
        self.btn = Button(self.frame, text = 'LOGIN',font=('Courier New', 18, 'bold'), bg = 'white', cursor = 'hand2', command= self.stu)
        self.btn.place(x=250,y=250)

    def login(self):
        self.bg_lbl = Label(self.frame, image= self.bg)
        self.bg_lbl.place(x= 0, y = 0)

        self.lbl=  Label(self.frame, text= 'DOCTOR LOGIN DETAILS', bg = 'white', fg = 'black', font=('Courier New', 18, 'bold'))
        self.lbl.place(x = 150, y = 100)

        self.lbl=  Label(self.frame, text= 'USER NAME', bg = 'white', fg = 'steel blue', font=('Courier New', 20, 'bold'))
        self.lbl.place(x = 50, y = 150)

        self.War_u_entry = Entry(self.frame, width = 20, font=('Courier New', 18, 'bold'), bg = 'white')
        self.War_u_entry.place(x = 220, y = 150)

        self.lbl=  Label(self.frame, text= 'PASSWORD', bg = 'white', fg = 'steel blue', font=('Courier New', 20, 'bold'))
        self.lbl.place(x = 50, y = 200)

        self.entry_p = Entry(self.frame, width = 20, font=('Courier New', 18, 'bold'), bg = 'white')
        self.entry_p.place(x = 220, y = 200)
        
        self.btn = Button(self.frame, text = 'LOGIN',font=('Courier New', 18, 'bold'), bg = 'white', cursor = 'hand2', command= self.Admin)
        self.btn.place(x=250,y=250) 

    def back_to_main(self):
        self.home = Home(root)

    def stu(self):
        self.stu_u = self.stu_entry.get()
        self.stu_p = self.stu_p.get()
        cursor.execute('select * from user_details;')
        self.data = cursor.fetchall()
        self.names = [name[0] for name in self.data]
        if self.stu_u in self.names:
            cursor.execute(f"select roll from user_details where Name = '{self.stu_u}'")
            self.pasw = cursor.fetchall()
            self.pasw = [passw[0] for passw in self.pasw]
        else:
            messagebox.showinfo('Login failed',f'INCORRECT USERNAME')
            self.back_to_main()
            return
        if self.stu_p in self.pasw:
            messagebox.showinfo('Login Succesfull',f'Welcome {self.stu_u}')
            self.student()
        else:
            messagebox.showinfo('Login failed',f'INCORRECT PASSWORD')
            self.back_to_main()
        

    def Admin(self):
        self.War_u = self.War_u_entry.get()
        self.War_p = self.entry_p.get()
        cursor.execute('select * from user_details;')
        self.data = cursor.fetchall()
        self.names = [name[0] for name in self.data]
        if self.War_u in self.names:
            cursor.execute(f"select roll from user_details where Name = '{self.War_u}'")
            self.pasw = cursor.fetchall()
            self.pasw = [passw[0] for passw in self.pasw]
        else:
            messagebox.showinfo('Login failed',f'INCORRECT USERNAME')
            return
        if self.War_p in self.pasw:
            messagebox.showinfo('Login Succesfull',f'Welcome {self.War_u}')
            self.warden()
        else:
            messagebox.showinfo('Login failed',f'INCORRECT PASSWORD')
            self.back_to_main()

    def back_to_main2(self,event):
        self.home = Home(root)
        
    def warden(self):
        self.msg_frame = Frame(self.root, width=550, height= 350, bd= 4, relief= 'ridge', bg= 'white')
        self.msg_frame.place(x = 0,y = 0)

        self.msg = Label(self.msg_frame, text = 'View details of a student', bg = 'white', fg = 'green', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 130, y = 40)

        self.msg = Label(self.msg_frame, text = 'Patient name : ----------------', bg = 'white', fg = 'orange', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 20, y = 80)

        self.msg = Label(self.msg_frame, text = 'Registration number : ------------', bg = 'white', fg = 'orange', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 20, y = 130)

        self.msg = Label(self.msg_frame, text = 'Patient Details, Room number : --------------', bg = 'white', fg = 'orange', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 20, y = 180)

        self.msg = Label(self.msg_frame, text = 'Phone number : -----------', bg = 'white', fg = 'orange', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 20, y = 230)

        self.bck_lbl = Label(self.msg_frame, text = 'Back To Main Page', bg = 'white', fg = 'steel blue', font=('Courier New', 14, 'bold'), cursor = 'hand2')
        self.bck_lbl.place(x = 0, y = 320)
        self.bck_lbl.bind("<Button - 1>", self.back_to_main2)


    def student(self):
        font = ('Courier New', 16, 'bold')
        self.msg_frame = Frame(self.root, width=550, height= 350, bd= 4, relief= 'ridge', bg= 'white')
        self.msg_frame.place(x = 0,y = 0)
        self.msg = Label(self.msg_frame, text = 'Enter your details', bg = 'white', fg = 'red', font=('Times New Roman', 20, 'bold'))
        self.msg.place(x = 150, y = 40)

        self.name_lbl = Label(self.msg_frame, text = "NAME", bg = 'white', fg = 'blue', font=('Courier New', 16, 'bold'))
        self.name_lbl.place(x = 10, y = 100)
        self.name_entry = Entry(self.msg_frame, font=font, width= 15)
        self.name_entry.place(x = 230, y = 100)
        
        self.regno_lbl = Label(self.msg_frame, text='Regnum', bg = 'white', fg = 'blue', font=('Courier New', 16, 'bold'))
        self.regno_lbl.place(x = 10, y = 150)
        self.regno_entry = Entry(self.msg_frame, font= font, width= 15)
        self.regno_entry.place(x = 230, y = 150)

        self.hostel_name_lbl = Label(self.msg_frame, text='Room No',bg = 'white', fg = 'blue', font=('Courier New', 16, 'bold'))
        self.hostel_name_lbl.place(x = 10, y = 200)
        self.hostel_name_entry = Entry(self.msg_frame, font= font, width= 15)
        self.hostel_name_entry.place(x = 230, y = 200)

        self.phonenum_lbl = Label(self.msg_frame, text='Phonenum', bg = 'white', fg = 'blue', font=('Courier New', 16, 'bold'))
        self.phonenum_lbl.place(x = 10, y = 250)
        self.phonenum_entry = Entry(self.msg_frame, font= font, width= 15)
        self.phonenum_entry.place(x = 230, y = 250)

        self.btn = Button(self.msg_frame, text = 'SUBMIT',font=('Courier New', 18, 'bold'), bg = 'white', command= self.student_details, cursor = 'hand2')
        self.btn.place(x=250,y=300) 

        self.bck_lbl = Label(self.msg_frame, text = 'Back To Main Page', bg = 'white', fg = 'steel blue', font=('Courier New', 14, 'bold'), cursor = 'hand2')
        self.bck_lbl.place(x = 0, y = 320)
        self.bck_lbl.bind("<Button - 1>", self.back_to_main2)

        #self.sun_btn = Button(self.msg_frame, text= 'REGISTER', font = font, width= 10, command= self.register_user)
        #self.register_btn.place(x = 200, y = 240)
    
    def student_details(self):
        self.name  = self.name_entry.get()
        self.hostel_name = self.hostel_name_entry.get() 
        self.phonenum = self.phonenum_entry.get()
        self.regno = self.regno_entry.get()
        self.query = "insert into student_detail(name,regno , hostel_name, phonenum) values(%s,%s,%s,%s)"
        self.values = (self.name,self.regno,self.hostel_name, self.phonenum)
        cursor2.execute(self.query,self.values)
        conn2.commit()
        messagebox.showinfo('Account Created',f'UserName = "{self.name}"\n Password = "{self.regno}"')
    
    def submit(self):
        self.lbl=  Label(self.msg_frame, text= 'Your details are saved Sucessfully', bg = 'white', fg = 'green', font=('Courier New', 18, 'bold'))
        self.lbl.place(x = 50, y = 250)

    
    

class Register:
    def _init_(self, root) -> None:
        self.root = root
        font = ('Courier New', 18, 'bold')
        self.main_frame = Frame(self.root, width= 550, height= 350, bg = 'steel blue')
        self.main_frame.place(x = 0, y = 0)
        self.name_lbl = Label(self.main_frame, text = "USER NAME", font = font, width= 10)
        self.name_lbl.place(x = 10, y = 50)
        self.name_entry = Entry(self.main_frame, font=font, width= 15)
        self.name_entry.place(x = 230, y = 50)
        
        self.pass_lbl = Label(self.main_frame, text='DEPARTMENT', font = font, width= 10)
        self.pass_lbl.place(x = 10, y = 100)
        self.pass_entry = Entry(self.main_frame, font= font, width= 15)
        self.pass_entry.place(x = 230, y = 100)

        self.roll_lbl = Label(self.main_frame, text='ROLL NO.', font = font, width= 10)
        self.roll_lbl.place(x = 10, y = 150)
        self.roll_entry = Entry(self.main_frame, font= font, width= 15)
        self.roll_entry.place(x = 230, y = 150)

        
        self.register_btn = Button(self.main_frame, text= 'REGISTER', font = font, width= 10, command= self.register_user)
        self.register_btn.place(x = 200, y = 240)

        '''self.bck_lbl = Label(self.main_frame, text = 'Back To Main Page', bg = 'white', fg = 'steel blue', font=('Courier New', 14, 'bold'), cursor = 'hand2')
        self.bck_lbl.place(x = 0, y = 320)
        self.bck_lbl.bind("<Button - 1>", self.back_to_main)'''

        self.goto_register = Label(self.main_frame, text= 'Already a member LOGIN!', font=('Courier New', 10, 'bold'))
        self.goto_register.place(x = 5, y = 300)
        self.goto_register.bind("<Button-1>", self.change_page)

    def back_to_main(self):
        self.main_frame.destroy()
        

    def register_user(self):
        self.name  = self.name_entry.get()
        self.roll = self.roll_entry.get()
        self.dept = self.pass_entry.get() 
        self.query = "insert into user_details(Name, Dept, Roll) values(%s,%s,%s)"
        self.values = (self.name, self.dept,self.roll)
        cursor.execute(self.query, self.values)
        conn.commit()
        messagebox.showinfo('Account Created',f'UserName = "{self.name}"\nPassword = "{self.roll}"')
    def change_page(self,event):
        self.main_frame.destroy()
        home = Home(root)

root = Tk()
root.title('MY-APP')
root.geometry('550x350+550+200')
home = Home(root)
root.mainloop()