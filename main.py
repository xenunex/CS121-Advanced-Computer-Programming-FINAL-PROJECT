import customtkinter as ctk
from PIL import Image
import re
import mysql.connector
import random
from datetime import datetime, date


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SKILLHub")
        self.geometry("1200x700")

        self.grid_rowconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(0, weight=35, uniform="equal")
        self.grid_columnconfigure(1, weight=65, uniform="equal")

        self.create_signup_frame()
        
        
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="skillhubdb"
        )


    def fetch_data(self, table_name):
        try:
            valid_tables = ["login", "user", "mentorship"] 
            if table_name not in valid_tables:
                print(f"Invalid table name: {table_name}. Please choose from {valid_tables}.")
                return
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            print(f"Fetched Data from {table_name}:")
            for row in rows:
                print(row)
            
            connection.close()
        except Exception as e:
            print(f"Error fetching data from {table_name}: {e}")


    def create_signup_frame(self):
        self.picture_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="white")
        self.picture_frame.grid(row=0, column=0, sticky="nsew")

        self.bg_ctk_image = ctk.CTkImage(
            light_image=Image.open("FINAL PROJECT/backgroundpage.png"),
            dark_image=Image.open("FINAL PROJECT/backgroundpage.png"),
            size=(600, 800)
        )
        self.bg_label = ctk.CTkLabel(self.picture_frame, image=self.bg_ctk_image, text="")
        self.bg_label.pack()

        self.signup_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#659287")
        self.signup_frame.grid(row=0, column=1, sticky="nsew")

        self.project_info = ctk.CTkLabel(self.signup_frame, text="SKILLHub", font=("Helvetica", 55, "bold"), text_color="black")
        self.project_info.pack(pady=(50, 20))

        self.project_info2 = ctk.CTkLabel(self.signup_frame, text="Let's BUILD you confidence.", font=("Arial", 25, "bold"), text_color="black")
        self.project_info2.pack(pady=(20, 60))

        self.signup_title = ctk.CTkLabel(self.signup_frame, text="Sign In", font=("Arial", 24, "bold"))
        self.signup_title.pack(pady=20)

        self.username_label = ctk.CTkLabel(self.signup_frame, text="Email:", font=("Arial", 18))
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.signup_frame, font=("Arial", 16), width=200)
        self.username_entry.pack(pady=(0, 10), ipady=7)

        self.password_label = ctk.CTkLabel(self.signup_frame, text="Password:", font=("Arial", 18))
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.signup_frame, font=("Arial", 16), show="*", width=200)
        self.password_entry.pack(ipady=7)

        self.toggle_password_button = ctk.CTkButton(self.signup_frame, text="Show Password", font=("Arial", 10), fg_color="#5A6C57", command=self.toggle_password_visibility)
        self.toggle_password_button.pack(pady=(1, 10), ipadx=0, ipady=0)

        self.signup_button = ctk.CTkButton(self.signup_frame, text="SIGN IN", font=("Verdana", 15), fg_color="#5A6C57", command=lambda: self.signup(self.username_entry.get(), self.password_entry.get()))
        self.signup_button.pack(pady=(5, 15), ipadx=20, ipady=10)
        
        self.username_label = ctk.CTkLabel(self.signup_frame, text="Don't have an account?", font=("Arial", 12))
        self.username_label.pack(pady=(5, 0))
        
        self.signup_button = ctk.CTkButton(self.signup_frame, text="REGISTER", font=("Verdana", 14), fg_color="#5A6C57", command=self.register)
        self.signup_button.pack(pady=(1, 5), ipadx=10, ipady=5)

        self.feedback_label = ctk.CTkLabel(self.signup_frame, text="", font=("Arial", 14), text_color="red")
        self.feedback_label.pack(pady=5)


    def toggle_password_visibility(self):
        current_show = self.password_entry.cget("show")
        if current_show == "*":
            self.password_entry.configure(show="")
            self.toggle_password_button.configure(text="Hide Password")
        else:
            self.password_entry.configure(show="*")
            self.toggle_password_button.configure(text="Show Password")


    def signup(self, username_entry, password_entry):
        email = username_entry
        password = password_entry
        global mentorshipidframe, userid4mentor

        mentorshipidframe = None
        userid4mentor = None

        if email == "admin" and password == "admin":
            self.adminaccess()
        elif email and password:
            try:
                connection = self.get_connection()
                cursor = connection.cursor()

                query = "SELECT userid, password FROM login WHERE email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    userid, stored_password = result

                    if password == stored_password:
                        global useridforprof, useridforsearch
                        useridforprof = userid
                        useridforsearch = userid
                        self.feedback_label.configure(text="Sign in successful!", text_color="blue")

                        query_user_type = "SELECT usertype FROM user WHERE userid = %s"
                        cursor.execute(query_user_type, (userid,))
                        result_user_type = cursor.fetchone()

                        if result_user_type:
                            usertype = result_user_type[0]
                            global userforhome
                            userforhome = usertype

                            if usertype == "Apprentice":
                                query_apprentice_id = "SELECT apprenticeid FROM user WHERE userid = %s"
                                cursor.execute(query_apprentice_id, (userid,))
                                result_apprentice_id = cursor.fetchone()

                                if result_apprentice_id:
                                    userid4mentor = result_apprentice_id[0]

                            elif usertype == "Mentor":
                                query_mentor_id = "SELECT mentorid FROM user WHERE userid = %s"
                                cursor.execute(query_mentor_id, (userid,))
                                result_mentor_id = cursor.fetchone()

                                if result_mentor_id:
                                    mentorid = result_mentor_id[0]

                                    query_mentorship_id = "SELECT mentorshipid FROM mentorship WHERE mentorid = %s"
                                    cursor.execute(query_mentorship_id, (mentorid,))
                                    result_mentorship_id = cursor.fetchone()

                                    if result_mentorship_id:
                                        mentorshipidframe = result_mentorship_id[0]

                        self.signup_frame.destroy()
                        self.show_main_application()

                    else:
                        self.feedback_label.configure(text="Incorrect password.", text_color="red")
                else:
                    self.feedback_label.configure(text="Account does not exist.", text_color="red")
            except Exception as e:
                self.feedback_label.configure(text=f"Error during sign in: {e}", text_color="red")
            finally:
                if cursor:
                    cursor.fetchall()
                    cursor.close()
                if connection:
                    connection.close()
        else:
            self.feedback_label.configure(text="Please fill in all fields.", text_color="red")


    def generate_userid(self, userid):
        
        connection = self.get_connection()
        cursor = connection.cursor()
        query =  "SELECT userid FROM login WHERE userid = %s"
        cursor.execute(query, (userid,))
        return cursor.fetchone() is not None
    
    
    def generate_mentorid(self, mentorid):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT mentorid FROM user WHERE mentorid = %s"
        cursor.execute(query, (mentorid,))
        return cursor.fetchone() is not None
    
    
    def generate_apprenticeid(self, apprenticeid):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT apprenticeid FROM user WHERE apprenticeid = %s"
        cursor.execute(query, (apprenticeid,))
        return cursor.fetchone() is not None
        
        
    def regconfirm(self, registerfname, registermidname, registersurname, genderopt, accountentry, birthdayenter, province_drop, city_drop, emailentry, passentry):
        
        testfirst_name = registerfname
        testmiddle_name = registermidname
        testlast_name =  registersurname
        testgender = genderopt
        testbirthday = birthdayenter
        testusertype = accountentry
        testprovince = province_drop
        testcity = city_drop
        testemail = str(emailentry)
        testpass = str(passentry)
   
        if (testprovince == "Select a Province" or 
            testcity == "Select a City" or 
            testfirst_name == "" or 
            testmiddle_name == "" or 
            testlast_name == "" or 
            testgender == "Select your Gender" or 
            testusertype == "Select a type" or 
            testbirthday == '' or  
            not re.match(r'^\d{4}-\d{2}-\d{2}$', testbirthday) or 
            testemail == "" or 
            not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', testemail) or 
            testpass == "" or 
            len(testpass) < 8) or self.format_birthday(testbirthday) is None:
            self.regshow_popup("Registration Failed", "Please provide all the required information \nand ensure that your details are correct.") 
        else:
            first_name = testfirst_name
            middle_name =  testmiddle_name
            last_name =  testlast_name
            gender = testgender
            birthday = self.format_birthday(testbirthday)
            usertype = testusertype
            province = testprovince
            city = testcity
            email = testemail
            password = testpass
            userid = random.randint(10000000, 99999999)
            
            today = datetime.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            
            while self.generate_userid(userid):
                userid = random.randint(10000000, 99999999)
                
            if usertype == "Apprentice":
                mentorid = None
                apprenticeid = random.randint(10000000, 99999999)
                while self.generate_apprenticeid(apprenticeid):
                    apprenticeid = random.randint(10000000, 99999999) 
            elif usertype == "Mentor":
                apprenticeid = None
                mentorid = random.randint(10000000, 99999999)
                while self.generate_apprenticeid(mentorid):
                    mentorid = random.randint(10000000, 99999999)
            else:
                mentorid = None
                apprenticeid = None
                    
            if email and password: 
                try:
                    connection = self.get_connection()
                    cursor = connection.cursor()
                    query1 = "SELECT * FROM login WHERE userid = %s"
                    cursor.execute(query1, (userid,))
                    userid_result = cursor.fetchone()
                    
                    query2 = "SELECT * FROM login WHERE email = %s"

                    cursor.execute(query2, (email,))
                    email_result = cursor.fetchone()

                    if userid_result:
                        self.regshow_popup("UserID already exists", "The UserID is already taken. \nPlease choose a different UserID.")
                    elif email_result:
                        self.regshow_popup("Email already exists", "The Email is already taken. \nPlease choose a different Email address.")
                    else:
                        try:
                            cursor.execute(
                                "INSERT INTO login (userid, email, password) VALUES (%s, %s, %s)", (userid, email, password)
                            )
                            
                            cursor.execute(
                                "INSERT INTO user (userid, mentorid, apprenticeid, firstname, middlename, lastname, gender, birthday, usertype, province, city, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (userid, mentorid, apprenticeid, first_name, middle_name, last_name, gender, birthday, usertype, province, city, age)
                            ) 
                            connection.commit()
                            self.regshow_popup("Success", "All details are filled. Registration can proceed.")
                        except Exception as e:
                            self.regshow_popup("An error occured", "Try again.")
                except Exception as e:
                    self.regshow_popup("An error occured", "Please try again later.")
                finally:
                    if connection:
                        connection.close()
                   
                        
    def format_birthday(self, birthday):
        try:
            return datetime.strptime(birthday, '%Y-%m-%d').date()
        except ValueError:
            return None
                  
                    
    def regshow_popup(self, title, message):
        self.pop_up = ctk.CTkToplevel(self)
        self.pop_up.title(title)
        self.pop_up.geometry("300x150")

        self.pop_up.lift()
        self.pop_up.grab_set()
        
        self.message_label = ctk.CTkLabel(self.pop_up, text=message, font=("Arial", 14))
        self.message_label.pack(pady=20)
        if title == ("Registration Failed" or "UserID already exists" or "Email already exists") and message == ("Please provide all the required information \nand ensure that your details are correct." or "The UserID is already taken. \nPlease choose a different UserID." or "The Email is already taken. \nPlease choose a different Email address."):
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=self.pop_up.destroy)
            self.close_button.pack()
        else:
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=lambda: [self.regback(), self.pop_up.destroy()])
            self.close_button.pack()
        
        
    def regback(self):
        self.register_frame.destroy()
        self.create_signup_frame()
        
        
    def register(self):
        self.register_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#659287")
        self.register_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.register_frame.columnconfigure(0, weight=1)
        self.register_frame.columnconfigure(1, weight=1)
        self.register_frame.columnconfigure(2, weight=1)
        self.register_frame.columnconfigure(3, weight=1)
        
        self.registertitle = ctk.CTkLabel(self.register_frame, text="CREATE ACCOUNT", font=("Verdana", 40, "bold"), text_color="black")
        self.registertitle.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        self.firname = ctk.CTkLabel(self.register_frame, text="First Name", font=("Arial", 12))
        self.firname.grid(pady=(5, 2), row=1, column=1)
        
        self.registerfname = ctk.CTkEntry(self.register_frame, font=("Arial", 12), width=200)
        self.registerfname.grid(row=2, column=1)
                
        self.midname = ctk.CTkLabel(self.register_frame, text="Middle Name", font=("Arial", 12))
        self.midname.grid(pady=(5, 2), row=3, column=1)
        self.registermidname = ctk.CTkEntry(self.register_frame, font=("Arial", 12), width=200)
        self.registermidname.grid(row=4, column=1)
        
        self.surname = ctk.CTkLabel(self.register_frame, text="Last Name", font=("Arial", 12))
        self.surname.grid(pady=(5, 2), row=5, column=1)
        self.registersurname = ctk.CTkEntry(self.register_frame, font=("Arial", 12), width=200)
        self.registersurname.grid(row=6, column=1)
        
        self.usertype = ctk.CTkLabel(self.register_frame, text="Choose an Account Type")
        self.usertype.grid(row=7, column=1)
        
        global accounttype
        accounttype = ["Select a type", "Apprentice", "Mentor", "Undecided"]
        self.accountentry = ctk.CTkOptionMenu(self.register_frame, values=accounttype)
        self.accountentry.grid(row=8, column=1)
        
        self.gender = ctk.CTkLabel(self.register_frame, text="Gender", font=("Arial", 12))
        self.gender.grid(pady=(5, 2), row=1, column=2)
        
        global genderopt
        genderopt = ["Select your Gender", "Male", "Female", "Undecided"]
        self.genderopt = ctk.CTkOptionMenu(self.register_frame, values=genderopt)
        self.genderopt.grid(row=2, column=2)
        
        def format_date_input(event):
            current_text = self.birthdayenter.get()
            current_text = ''.join([ch for ch in current_text if ch.isdigit()])
            
            if len(current_text) > 4:
                current_text = current_text[:4] + '-' + current_text[4:]
            if len(current_text) > 7:
                current_text = current_text[:7] + '-' + current_text[7:]
            if len(current_text) > 9:
                current_text = current_text[:10]
    
            self.birthdayenter.delete(0, ctk.END)  
            self.birthdayenter.insert(0, current_text) 
    
        # Para sa bday 
        self.birthdate = ctk.CTkLabel(self.register_frame, text="Birthdate(yyyy-mm-dd)", font=("Arial", 12))
        self.birthdate.grid(pady=(5, 2), row=3, column=2)
        
        self.birthdayenter = ctk.CTkEntry(self.register_frame, placeholder_text="yyyy-mm-dd")
        self.birthdayenter.grid(row=4, column=2)
        self.birthdayenter.bind("<KeyRelease>", format_date_input)

        # Para sa address
        self.address = ctk.CTkLabel(self.register_frame, text="Address", font=("Arial", 12))
        self.address.grid(pady=(5, 2), row=5, column=2)
        self.address.grid_columnconfigure(0, weight=75, minsize=100)
        
        global provinces
        provinces = ["Select a Province", "Batangas"]
        province_drop = ctk.CTkOptionMenu(self.register_frame, values=provinces)
        province_drop.grid(pady=5, row=6, column=2)
        
        global cities
        cities = ["Select a City", "Agoncillo", "Balayan", 
                "Batangas City", "Bauan", "Calaca", "Cuenca", 
                "Ibaan",  "Lemery", "Lipa City", "Nasugbu", "Rosario", 
                "San Jose", "San Juan", "Sto. Tomas City", "Taal",  
                "Tanauan City", "Taysan", "Tuy"]
        
        city_drop = ctk.CTkOptionMenu(self.register_frame, values=cities)
        city_drop.grid(pady=5, row=7, column=2)
        
        emailtext = ctk.CTkLabel(self.register_frame, text="Email", font=("Arial", 15, "bold"))
        emailtext.grid(row=9, column=0, columnspan=4, sticky="nsew")
        emailentry = ctk.CTkEntry(self.register_frame, font=("Verdana", 14))
        emailentry.grid(padx=400, row=10, column=0, columnspan=4, sticky="nsew")
        passtext = ctk.CTkLabel(self.register_frame, text="Password", font=("Arial", 15, "bold"))
        passtext.grid(row=11, column=0, columnspan=4, sticky="nsew")
        passentry = ctk.CTkEntry(self.register_frame, font=("Verdana", 14))
        passentry.grid(padx=400, row=12, column=0, columnspan=4, sticky="nsew")
        
        confirmbtn = ctk.CTkButton(self.register_frame, text="CONFIRM", fg_color="#5A6C57", command=lambda: self.regconfirm(self.registerfname.get(), self.registermidname.get(), self.registersurname.get(), self.genderopt.get(), self.accountentry.get(), self.birthdayenter.get(), province_drop.get(), city_drop.get(), emailentry.get(), passentry.get()))
        confirmbtn.grid(pady=(100,10), row=13, column=1, columnspan=2, sticky="nsew")
        
        reg_back_button = ctk.CTkButton(self.register_frame, text="BACK", fg_color="#5A6C57", command=self.regback)
        reg_back_button.grid(row=14, column=1, columnspan=2, sticky="nsew")
    
    
    def show_main_application(self):
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#D3F1DF")
        self.main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.sideframe = ctk.CTkFrame(self.main_frame, fg_color="#D3F1DF")
        self.sideframe.pack(side="left", fill="y")
        
        self.bg_ctk_image = ctk.CTkImage(
            light_image=Image.open("FINAL PROJECT/backgroundpage.png"),
            dark_image=Image.open("FINAL PROJECT/backgroundpage.png"),
            size=(120, 160)
        )
        self.bg_label = ctk.CTkLabel(self.sideframe, image=self.bg_ctk_image, text="")
        self.bg_label.pack(pady=10)

        self.profilebutton = ctk.CTkButton(self.sideframe, text="PROFILE", font=("Helvetica", 20), fg_color="#5A6C57", command=lambda: [self.show_frame(self.profileframe), self.profileframeinfo()])
        self.profilebutton.pack(padx=5, pady=15, ipady=10, fill="x")
        self.homebutton = ctk.CTkButton(self.sideframe, text="HOME", font=("Helvetica", 20), fg_color="#5A6C57", command=lambda: [self.show_frame(self.homeframe), self.homeframeinfo()])
        self.homebutton.pack(padx=5, pady=15, ipady=10, fill="x")
        self.aboutbutton = ctk.CTkButton(self.sideframe, text="SEARCH", font=("Helvetica", 20), fg_color="#5A6C57", command=lambda: [self.show_frame(self.searchframe), self.searchframeinfo()])
        self.aboutbutton.pack(padx=5, pady=15, ipady=10, fill="x")
        self.searchbutton = ctk.CTkButton(self.sideframe, text="ABOUT", font=("Helvetica", 20), fg_color="#5A6C57", command=lambda: [self.show_frame(self.aboutframe), self.aboutframeinfo()])
        self.searchbutton.pack(padx=5, pady=15, ipady=10, fill="x")
        
        if mentorshipidframe != None:
            self.mentor = ctk.CTkButton(self.sideframe, text="MENTORSHIP", font=("Helvetica", 20), fg_color="#5A6C57", command=lambda: [self.show_frame(self.mentorframe), self.mentorframeinfo()])
            self.mentor.pack(padx=5, pady=15, ipady=10, fill="x")
            
        self.profileframe = ctk.CTkFrame(self.main_frame, fg_color="#659287")
        self.profileframe.grid_columnconfigure(0, weight=1)
        self.profileframe.grid_columnconfigure(1, weight=1)
        self.profileframe.grid_columnconfigure(2, weight=1)
        self.homeframe = ctk.CTkFrame(self.main_frame, fg_color="#659287")
        self.homeframe.grid_columnconfigure(0, weight=1)
        self.searchframe = ctk.CTkFrame(self.main_frame, fg_color="#659287")
        self.searchframe.grid_columnconfigure(0, weight=1)
        self.aboutframe = ctk.CTkFrame(self.main_frame, fg_color="#659287")
        self.aboutframe.grid_columnconfigure(0, weight=1)
        self.aboutframe.grid_columnconfigure(1, weight=1)
        self.mentorframe = ctk.CTkFrame(self.main_frame, fg_color="#659287")
        self.mentorframe.grid_columnconfigure(0, weight=1)
        self.mentorframe.grid_columnconfigure(1, weight=1)
        self.mentorframe.grid_columnconfigure(2, weight=1)
        self.mentorframe.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(self.profileframe, text="Your Profile", font=("Arial", 40, "bold")).grid(ipady=20, row=0, column=0, columnspan=3, sticky="nsew")
        ctk.CTkLabel(self.homeframe, text="Home", font=("Arial", 40, "bold")).grid(ipady=20, row=0, column=0, columnspan=2, sticky="nsew")
        self.searchword = ctk.CTkLabel(self.searchframe, text="Search", font=("Arial", 40, "bold"))
        self.searchword.grid(ipady=20, row=0, column=0, columnspan=2, sticky="nsew")
        ctk.CTkLabel(self.aboutframe, text="     About", font=("Arial", 40, "bold")).grid(ipady=20, row=0, column=0, columnspan=2, sticky="nsew")
        self.mentorword = ctk.CTkLabel(self.mentorframe, text="APPRENTICES", font=("Arial", 40, "bold"))
        self.mentorword.grid(ipady=20, row=0, column=0, columnspan=2, sticky="nsew")
        
        self.show_frame(self.homeframe)
        self.homeframeinfo()
       
        logout_button = ctk.CTkButton(self.main_frame, text="Logout", fg_color="#5A6C57", command=self.logout)
        logout_button.pack(side="bottom", pady=10)
        
        
    def profileframeinfo(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT userid FROM user WHERE userid = %s", (useridforprof,)
            )
            result = cursor.fetchone()
            if result:
                resultid = result[0]
                try:
                    cursor.execute("SELECT userid, mentorid, apprenticeid, firstname, middlename, lastname, gender, birthday, usertype, province, city from user WHERE userid = %s", (resultid,)
                    )
                    row = cursor.fetchone()
                    userid, mentorid, apprenticeid, firstname, middlename, lastname, gender, birthday, usertype, province, city = row
                except Exception as e:
                    return
        except Exception as e:
            return
        
        def profilebutton():
            profpopup = ctk.CTkToplevel(self.profileframe)
            profpopup.title("Error")
            profpopup.geometry("250x150")
            profpopup.lift()
            profpopup.grab_set()
            errorlabel = ctk.CTkLabel(profpopup, text="Adding a Photo or an Image\n is not yet available", font=("Arial", 15))
            errorlabel.pack(pady=40)
        
        ctk.CTkFrame(self.profileframe, bg_color="white", width=150, height=150).grid(row=1, column=1)
        ctk.CTkButton(self.profileframe, text="Add a Photo", font=("Arial", 15), fg_color="#5A6C57", command=profilebutton).grid(pady=(5, 10), row=2, column=1)
        ctk.CTkLabel(self.profileframe, text=f"UserID: {userid}", font=("Arial", 20)).grid(pady=(10, 5), row=3, column=1, sticky="nsew")
        ctk.CTkLabel(self.profileframe, text=f"Name: {firstname} {middlename} {lastname}", font=("Arial", 20)).grid(pady=5, row=4, column=1, sticky="nsew") 
        ctk.CTkLabel(self.profileframe, text=f"Birthday: {birthday.strftime("%B %d, %Y")}", font=("Arial", 20)).grid(pady=5, row=5, column=1, sticky="nsew")
        ctk.CTkLabel(self.profileframe, text=f"Gender: {gender}", font=("Arial", 20)).grid(pady=5, row=6, column=1, sticky="nsew")
        ctk.CTkLabel(self.profileframe, text=f"User Type: {usertype}", font=("Arial", 20)).grid(pady=5, row=7, column=1, sticky="nsew")
        ctk.CTkLabel(self.profileframe, text=f"Address: {city}, {province}", font=("Arial", 20)).grid(pady=5, row=9, column=1, sticky="nsew")
        ctk.CTkButton(self.profileframe, text="Update Data", font=("Arial", 15), fg_color="#5A6C57", command=lambda: self.updateprof(userid, firstname, middlename, lastname, birthday)).grid(pady=(20, 0), row=10, column=1)
        ctk.CTkButton(self.profileframe, text="Delete Data", font=("Arial", 15), fg_color="#5A6C57", command=lambda: self.deleteprof(userid)).grid(pady=10,row=11, column=1)

        if usertype == "Apprentice":
            ctk.CTkLabel(self.profileframe, text=f"Apprentice ID: {apprenticeid}", font=("Arial", 20)).grid(pady=5, row=8, column=1, sticky="nsew")
        elif usertype == "Mentor":
            ctk.CTkLabel(self.profileframe, text=f"Mentor ID: {mentorid}", font=("Arial", 20)).grid(pady=5, row=8, column=1, sticky="nsew")
        else:
            None
            
            
    def upconfirm(self, userid, upregisterfname, upregistermidname, upregistersurname, upgenderopt, upaccountentry, upbirthdayenter, upprovince_drop, upcity_drop, upemailentry, uppassentry):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT mentorid, apprenticeid, firstname, middlename, lastname, gender, birthday, usertype, province, city FROM user WHERE userid = %s", (userid,))
            row = cursor.fetchone()
            if not row:
                self.upshow_popup("Error", "User not found.")
                return

            mentorid, apprenticeid, firstname, middlename, lastname, gender, birthday, usertype, province, city = row

            cursor.execute("SELECT email, password FROM login WHERE userid = %s", (userid,))
            row1 = cursor.fetchone()
            if not row1:
                self.upshow_popup("Error", "Login details not found.")
                return

            email, password = row1

            upfirst_name = upregisterfname if upregisterfname else firstname
            upmiddle_name = upregistermidname if upregistermidname else middlename
            uplast_name = upregistersurname if upregistersurname else lastname
            upgender = upgenderopt if upgenderopt != "Select your Gender" else gender

            try:
                upbirthday = datetime.strptime(upbirthdayenter, "%Y-%m-%d") if upbirthdayenter else birthday
            except ValueError:
                self.upshow_popup("Invalid Date", "Please provide a valid date in the format YYYY-MM-DD.")
                return

            if upaccountentry and upaccountentry != usertype:
                if upaccountentry == "Mentor":
                    upusertype = "Mentor"
                    upapprenticeid = None
                    upmentorid = random.randint(10000000, 99999999)
                    while self.generate_apprenticeid(upmentorid):
                        upmentorid = random.randint(10000000, 99999999)
                elif upaccountentry == "Apprentice":
                    upusertype = "Apprentice"
                    upmentorid = None
                    upapprenticeid = random.randint(10000000, 99999999)
                    while self.generate_apprenticeid(upapprenticeid):
                        upapprenticeid = random.randint(10000000, 99999999)
                elif upaccountentry == "Undecided":
                    upusertype = "Undecided"
                    upmentorid = None
                    upapprenticeid = None
                else:
                    self.upshow_popup("Error", "Invalid user type.")
                    return
            else:
                upusertype = usertype
                upmentorid = mentorid
                upapprenticeid = apprenticeid

            upprovince = upprovince_drop if upprovince_drop != "Select a Province" else province
            upcity = upcity_drop if upcity_drop != "Select a City" else city

            upemail = upemailentry if upemailentry else email
            uppassword = uppassentry if uppassentry else password

            today = datetime.today()
            age = today.year - upbirthday.year - ((today.month, today.day) < (upbirthday.month, upbirthday.day))

            try:
                sql_query1 = "UPDATE login SET email = %s, password = %s WHERE userid = %s"
                cursor.execute(sql_query1, (upemail, uppassword, userid))

                sql_query2 = """
                    UPDATE user
                    SET mentorid = %s, apprenticeid = %s, firstname = %s, middlename = %s, lastname = %s, gender = %s, birthday = %s, usertype = %s, province = %s, city = %s, age = %s WHERE userid = %s
                """
                cursor.execute(
                    sql_query2,
                    (upmentorid, upapprenticeid, upfirst_name, upmiddle_name, uplast_name, upgender, upbirthday, upusertype, upprovince, upcity, age, userid))
                connection.commit()
            
                self.upshow_popup("Update Success", "User details updated successfully. \nSome information will be \nupdated here after relog-in.")
            except Exception as e:
                self.upshow_popup("An error occurred", f"Error during update: {e}")
            finally:
                if connection:
                    connection.close()
        except Exception as e:
            self.upshow_popup("An error occurred", f"Unexpected error: {e}")


    def format_birthday(self, birthday):
        try:
            return datetime.strptime(birthday, '%Y-%m-%d').date()
        except ValueError:
            return None
                    
                    
    def upshow_popup(self, title, message):
        self.pop_up = ctk.CTkToplevel(self)
        self.pop_up.title(title)
        self.pop_up.geometry("300x150")

        self.pop_up.lift()
        self.pop_up.grab_set()
        
        self.message_label = ctk.CTkLabel(self.pop_up, text=message, font=("Arial", 14))
        self.message_label.pack(pady=20)
        if title == ("Update Failed" or "UserID already exists" or "Email already exists") and message == ("Please provide all the required information \nand ensure that your details are correct." or "The UserID is already taken. \nPlease choose a different UserID." or "The Email is already taken. \nPlease choose a different Email address."):
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=self.pop_up.destroy)
            self.close_button.pack()
        else:
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=lambda: [self.upback(), self.pop_up.destroy()])
            self.close_button.pack()
        
        
    def upback(self):
        self.update_frame.destroy()
        self.create_signup_frame()
        
        
    def updateprof(self, userid, firstname, middlename, lastname, birthday):
    
        self.update_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#659287")
        self.update_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=1)
        self.update_frame.columnconfigure(2, weight=1)
        self.update_frame.columnconfigure(3, weight=1)
        
        self.updatetitle = ctk.CTkLabel(self.update_frame, text="UPDATE ACCOUNT", font=("Verdana", 40, "bold"), text_color="black")
        self.updatetitle.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        self.upfirname = ctk.CTkLabel(self.update_frame, text="First Name", font=("Arial", 12))
        self.upfirname.grid(pady=(5, 2), row=1, column=1)
        
        self.upregisterfname = ctk.CTkEntry(self.update_frame, font=("Arial", 12), width=200, placeholder_text=firstname)
        self.upregisterfname.grid(row=2, column=1)
                
        self.upmidname = ctk.CTkLabel(self.update_frame, text="Middle Name", font=("Arial", 12))
        self.upmidname.grid(pady=(5, 2), row=3, column=1)
        self.upregistermidname = ctk.CTkEntry(self.update_frame, font=("Arial", 12), width=200, placeholder_text=middlename)
        self.upregistermidname.grid(row=4, column=1)
        
        self.upsurname = ctk.CTkLabel(self.update_frame, text="Last Name", font=("Arial", 12))
        self.upsurname.grid(pady=(5, 2), row=5, column=1)
        self.upregistersurname = ctk.CTkEntry(self.update_frame, font=("Arial", 12), width=200, placeholder_text=lastname)
        self.upregistersurname.grid(row=6, column=1)
        
        self.upusertype = ctk.CTkLabel(self.update_frame, text="Choose an Account Type")
        self.upusertype.grid(row=7, column=1)
        
        global upaccounttype
        upaccounttype = ["Select a type", "Apprentice", "Mentor", "Undecided"]
        self.upaccountentry = ctk.CTkOptionMenu(self.update_frame, values=upaccounttype)
        self.upaccountentry.grid(row=8, column=1)
        
        self.upgender = ctk.CTkLabel(self.update_frame, text="Gender", font=("Arial", 12))
        self.upgender.grid(pady=(5, 2), row=1, column=2)
        
        global upgenderopt
        upgenderopt = ["Select your Gender", "Male", "Female", "Undecided"]
        self.upgenderopt = ctk.CTkOptionMenu(self.update_frame, values=upgenderopt)
        self.upgenderopt.grid(row=2, column=2)
        
        def format_date_input(event):
            current_text = self.upbirthdayenter.get()
            current_text = ''.join([ch for ch in current_text if ch.isdigit()])
            
            if len(current_text) > 4:
                current_text = current_text[:4] + '-' + current_text[4:]
            if len(current_text) > 7:
                current_text = current_text[:7] + '-' + current_text[7:]
            if len(current_text) > 9:
                current_text = current_text[:10]
    
            self.upbirthdayenter.delete(0, ctk.END)  
            self.upbirthdayenter.insert(0, current_text) 
    
        # Para sa bday 
        self.upbirthdate = ctk.CTkLabel(self.update_frame, text="Birthdate(yyyy-mm-dd)", font=("Arial", 12))
        self.upbirthdate.grid(pady=(5, 2), row=3, column=2)
        
        self.upbirthdayenter = ctk.CTkEntry(self.update_frame, placeholder_text=birthday)
        self.upbirthdayenter.grid(row=4, column=2)
        self.upbirthdayenter.bind("<KeyRelease>", format_date_input)

        # Para sa address
        self.upaddress = ctk.CTkLabel(self.update_frame, text="Address", font=("Arial", 12))
        self.upaddress.grid(pady=(5, 2), row=5, column=2)
        self.upaddress.grid_columnconfigure(0, weight=75, minsize=100)
        
        global upprovinces
        upprovinces = ["Select a Province", "Batangas"]
        upprovince_drop = ctk.CTkOptionMenu(self.update_frame, values=upprovinces)
        upprovince_drop.grid(pady=5, row=6, column=2)
        
        global upcities
        upcities = ["Select a City", "Agoncillo", "Balayan", 
                "Batangas City", "Bauan", "Calaca", "Cuenca", 
                "Ibaan",  "Lemery", "Lipa City", "Nasugbu", "Rosario", 
                "San Jose", "San Juan", "Sto. Tomas City", "Taal",  
                "Tanauan City", "Taysan", "Tuy"]
        
        upcity_drop = ctk.CTkOptionMenu(self.update_frame, values=upcities)
        upcity_drop.grid(pady=5, row=7, column=2)
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT email FROM login WHERE userid = %s", (userid,)
            )
            result = cursor.fetchone()
            email = result[0]
        except Exception as e:
            self.upshow_popup("An error occured", "Please try again later.")
        
        upemailtext = ctk.CTkLabel(self.update_frame, text="Email", font=("Arial", 15, "bold"))
        upemailtext.grid(row=9, column=0, columnspan=4, sticky="nsew")
        upemailentry = ctk.CTkEntry(self.update_frame, font=("Verdana", 14), placeholder_text=email)
        upemailentry.grid(padx=400, row=10, column=0, columnspan=4, sticky="nsew")
        uppasstext = ctk.CTkLabel(self.update_frame, text="Password", font=("Arial", 15, "bold"))
        uppasstext.grid(row=11, column=0, columnspan=4, sticky="nsew")
        uppassentry = ctk.CTkEntry(self.update_frame, font=("Verdana", 14))
        uppassentry.grid(padx=400, row=12, column=0, columnspan=4, sticky="nsew")
        
        upconfirmbtn = ctk.CTkButton(self.update_frame, text="CONFIRM", fg_color="#5A6C57", command=lambda: self.upconfirm(userid, self.upregisterfname.get(), self.upregistermidname.get(), self.upregistersurname.get(), self.upgenderopt.get(), self.upaccountentry.get(), self.upbirthdayenter.get(), upprovince_drop.get(), upcity_drop.get(), upemailentry.get(), uppassentry.get()))
        upconfirmbtn.grid(pady=(100,10), row=13, column=1, columnspan=2, sticky="nsew")
        
        up_back_button = ctk.CTkButton(self.update_frame, text="BACK", fg_color="#5A6C57", command=self.upback)
        up_back_button.grid(row=14, column=1, columnspan=2, sticky="nsew")
        
        
    def deleteprof(self, userid):
        self.deletepop = ctk.CTkToplevel(self)
        self.deletepop.title("DELETE CONFIRMATION")
        self.deletepop.geometry("400x300")
        
        self.deletepop.lift()
        self.deletepop.grab_set()
        
        self.confirmdelframe = ctk.CTkFrame(self.deletepop)
        self.confirmdelframe.pack()
        
        self.confirmdel = ctk.CTkLabel(self.confirmdelframe, text="DO YOU REALLY WANT TO DELETE YOUR ACCOUNT?")
        self.confirmdel.pack(pady=20, padx=20)
        self.confirmdelbut = ctk.CTkButton(self.deletepop, text="YES", command=lambda: self.enterpassdel(userid))
        self.confirmdelbut.pack()
        
        
    def enterpassdel(self, userid):
        self.deletepop.destroy()
        
        self.deletepop1 = ctk.CTkToplevel(self)
        self.deletepop1.title("CONTINUE FOR DELETION")
        self.deletepop1.geometry("400x300")
        self.deletepop1.lift()
        self.deletepop1.grab_set()
        
        self.confirmdelframe = ctk.CTkFrame(self.deletepop1)
        self.confirmdelframe.pack()
        
        self.confirmdel = ctk.CTkLabel(self.confirmdelframe, text="ENTER PASSWORD TO CONTINUE")
        self.confirmdel.pack(pady=20, padx=20)
        
        self.entrydel = ctk.CTkEntry(self.confirmdelframe)
        self.entrydel.pack()
        
        self.confirmdelbut = ctk.CTkButton(self.confirmdelframe, text="CONFIRM DELETION", command=lambda: [self.condel(userid, self.entrydel.get()), self.deletepop1.destroy()])
        self.confirmdelbut.pack()
            
            
    def condel(self, userid, passwordentered):
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM login WHERE userid = %s", (userid,)
            ) 
            result = cursor.fetchone()
            if result:
                checkpass = result[0]
                if checkpass == passwordentered:
                    try:
                        sql_query = "DELETE FROM user WHERE userid = %s"
                        cursor.execute(sql_query, (userid,))
                        
                        sql_query2 = "DELETE FROM login WHERE userid = %s"
                        cursor.execute(sql_query2, (userid,))

                        connection.commit()
                        
                        self.delshow_popup("DELETION UPDATE", "Your account has been deleted.")
                    except Exception as e:
                        self.delshow_popup("An error occured", "Please try again later.")
                else:
                    self.delshow_popup("An error occured", "Wrong Password.")
        except Exception as e:
            self.delshow_popup("An error occured", "Please try again later.")
            
            
    def delshow_popup(self, title, message):
        self.pop_up = ctk.CTkToplevel(self)
        self.pop_up.title(title)
        self.pop_up.geometry("300x150")

        self.pop_up.lift()
        self.pop_up.grab_set()
        
        self.message_label = ctk.CTkLabel(self.pop_up, text=message, font=("Arial", 14))
        self.message_label.pack(pady=20)
        if title == "An error occured" or "Success" or message == ("Please try again later." or "Wrong Password." or "Mentorship application submitted successfully!"):
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=self.pop_up.destroy)
            self.close_button.pack()
        else:
            self.close_button = ctk.CTkButton(self.pop_up, text="OK", command=lambda: [self.logout(), self.pop_up.destroy()])
            self.close_button.pack()
            
            
    def homeframeinfo(self):
        ctk.CTkLabel(self.homeframe, text="Home", font=("Arial", 40, "bold")).grid(pady=(20, 5), row=0, column=0, columnspan=4, sticky="nsew")

        if userforhome == "Mentor":
            ctk.CTkButton(self.homeframe, text="Publish", font=("Arial", 20, "bold"), fg_color="#5A6C57", command=self.publish).grid(pady=5, row=1, column=0, columnspan=2, sticky="nsew")
            ctk.CTkLabel(self.homeframe, text="Your Published Articles", font=("Arial", 20, "bold")).grid(pady=(20, 5), row=2, column=1, columnspan=2, sticky="nsew")
        elif userforhome == "Apprentice":
            ctk.CTkLabel(self.homeframe, text="Shared by Mentors", font=("Arial", 20, "bold")).grid(pady=(20, 5), row=2, column=1, columnspan=2, sticky="nsew")
        else:
            ctk.CTkLabel(self.homeframe, text="No Contents Here", font=("Arial", 20, "bold")).grid(pady=(20, 5), row=2, column=1, columnspan=2, sticky="nsew")
        ctk.CTkButton(self.homeframe, text="Refresh", font=("Arial", 20, "bold"), fg_color="#5A6C57", command=self.refreshhome).grid(pady=5, row=1, column=1, columnspan=2, sticky="nsew")
        ctk.CTkLabel(self.homeframe, text="Available Resources", font=("Arial",20, "bold")).grid(pady=(20, 5), row=2, column=0, columnspan=2, sticky="nsew")
        
        self.home_canvas_left = ctk.CTkCanvas(self.homeframe, bg="lightgray")
        self.home_canvas_left.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        self.home_canvas_right = ctk.CTkCanvas(self.homeframe, bg="lightgray")
        self.home_canvas_right.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")

        self.scrollbar_left = ctk.CTkScrollbar(self.homeframe, command=self.home_canvas_left.yview)
        self.scrollbar_left.grid(row=3, column=1, sticky="ns", pady=20)
        self.home_canvas_left.configure(yscrollcommand=self.scrollbar_left.set)

        self.scrollbar_right = ctk.CTkScrollbar(self.homeframe, command=self.home_canvas_right.yview)
        self.scrollbar_right.grid(row=3, column=3, sticky="ns", pady=20)
        self.home_canvas_right.configure(yscrollcommand=self.scrollbar_right.set)

        self.content_frame_left = ctk.CTkFrame(self.home_canvas_left)
        self.content_frame_right = ctk.CTkFrame(self.home_canvas_right)

        self.home_canvas_left.create_window((0, 0), window=self.content_frame_left, anchor="nw")
        self.home_canvas_right.create_window((0, 0), window=self.content_frame_right, anchor="nw")
        
        connection = self.get_connection()
        cursor = connection.cursor()
        
        if userforhome == "Mentor":
            cursor.execute("""
                SELECT a.title, CONCAT(u.firstname, ' ', u.middlename, ' ', u.lastname) AS author_name, a.contents
                FROM articles a
                INNER JOIN user u ON a.authorid = u.userid
                WHERE a.authorid = %s""", (useridforprof,))
            articles_by_user = cursor.fetchall()

        elif userforhome == "Apprentice":
            cursor.execute("""
                SELECT a.title, CONCAT(u.firstname, ' ', u.middlename, ' ', u.lastname) AS author_name, 
                    a.contents
                FROM articles a
                JOIN user u ON a.authorid = u.userid
                WHERE u.userid IN (
                    SELECT u.userid
                    FROM user u
                    JOIN mentorship m ON m.mentorid = u.mentorid
                    WHERE m.apprentices = (
                        SELECT apprenticeid 
                        FROM user 
                        WHERE userid = %s
                    )
                );
            """, (useridforprof,))
            articles_by_user = cursor.fetchall()
            
        cursor.execute("""
            SELECT a.title, CONCAT(u.firstname, ' ', u.middlename, ' ', u.lastname) AS author_name, a.contents
            FROM articles a
            INNER JOIN user u ON a.authorid = u.userid
            WHERE a.authorid != %s""", (useridforprof,))  
        articles_from_others = cursor.fetchall()

        connection.close()
            
        for i, (title, author, content) in enumerate(articles_from_others):
            formatted_content = self.format_content(content)
            article_label = ctk.CTkLabel(self.content_frame_left, text=f"{title} by {author}", font=("Arial", 14))
            article_label.grid(row=i, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            
            article_label.bind("<Button-1>", lambda e, t=title, c=formatted_content: self.show_article_details(t, c))

        for i, (title, author, content) in enumerate(articles_by_user):
            formatted_content1 = self.format_content(content)
            article_label = ctk.CTkLabel(self.content_frame_right, text=f"{title} by {author}", font=("Arial", 14))
            article_label.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
            
            article_label.bind("<Button-1>", lambda e, t=title, c=formatted_content1: self.show_article_details(t, c))

        self.content_frame_left.update_idletasks()
        self.home_canvas_left.config(scrollregion=self.home_canvas_left.bbox("all"))

        self.content_frame_left.update_idletasks()
        self.content_frame_right.update_idletasks()
        self.home_canvas_left.configure(scrollregion=self.home_canvas_left.bbox("all"))
        self.home_canvas_right.configure(scrollregion=self.home_canvas_right.bbox("all"))

        self.homeframe.grid_rowconfigure(3, weight=1)
        self.homeframe.grid_columnconfigure(0, weight=1)
        self.homeframe.grid_columnconfigure(1, weight=0)
        self.homeframe.grid_columnconfigure(2, weight=1)
        self.homeframe.grid_columnconfigure(3, weight=0)
        
        self.content_frame_left.grid_columnconfigure(0, weight=1)
        
        
    def format_content(self, content):
        formatted_content = ""
        max_line_length = 100 
        
        while len(content) > max_line_length:
            formatted_content += content[:max_line_length] + "\n"
            content = content[max_line_length:] 
        
        formatted_content += content 
        return formatted_content
    

    def show_article_details(self, title, content):
        self.article_window = ctk.CTkToplevel(self)
        self.article_window.title(title)
        self.article_window.geometry("900x700")
        
        self.article_window.lift()
        self.article_window.grab_set()
        
        ctk.CTkLabel(self.article_window, text=title, font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.article_window, text=content, font=("Arial", 14)).pack(padx=20, pady=10)
        ctk.CTkButton(self.article_window, text="Close", command=self.article_window.destroy).pack(pady=10)
        
        
    def refreshhome(self):
        self.homeframeinfo()
        

    def publish(self):
        self.publishpopup = ctk.CTkToplevel(self)
        self.publishpopup.title("PUBLISH")
        self.publishpopup.geometry("900x700")
        self.publishpopup.lift()
        self.publishpopup.grab_set()

        ctk.CTkLabel(self.publishpopup, text="TITLE", font=("Arial", 18, "bold")).pack(pady=10)
        self.titleentry = ctk.CTkEntry(self.publishpopup, placeholder_text="Title", width=300)
        self.titleentry.pack(pady=10)

        ctk.CTkLabel(self.publishpopup, text="CONTENT", font=("Arial", 18, "bold")).pack(pady=10)
        self.contententry = ctk.CTkTextbox(self.publishpopup, height=10, wrap="word")
        self.contententry.pack(padx=100, pady=10, fill="both", expand=True)

        ok_button = ctk.CTkButton(self.publishpopup, text="OK", font=("Arial", 16), bg_color="#47663B", command=self.on_publish_ok)
        ok_button.pack(side="left", padx=50, pady=20)

        back_button = ctk.CTkButton(self.publishpopup, text="BACK", font=("Arial", 16), bg_color="#47663B", command=self.on_publish_back)
        back_button.pack(side="right", padx=50, pady=20)
        

    def on_publish_ok(self):
        title = self.titleentry.get()
        content = self.contententry.get("1.0", "end-1c")  
        articleid = random.randint(10000000, 99999999)
        while self.generate_articleid(articleid):
            articleid = random.randint(10000000, 99999999)

        if not title.strip() or not content.strip():
            self.show_warning("Title and Content cannot be empty!")
        else:
            try:
                connection = self.get_connection()
                cursor = connection.cursor()
                
                query = "INSERT INTO articles (articleid, authorid, title, contents) VALUES (%s, %s, %s, %s)" 
                cursor.execute(query, (articleid, useridforprof, title, content))
                connection.commit()
                
                self.show_success("Article Published Successfully!")
                self.publishpopup.destroy() 
            except:
                pass
            
            
    def on_publish_back(self):
        self.publishpopup.destroy()  
        

    def show_warning(self, message):
        warning_popup = ctk.CTkToplevel(self)
        warning_popup.title("Warning")
        warning_popup.geometry("300x150")
        warning_popup.lift()
        warning_popup.grab_set()

        label = ctk.CTkLabel(warning_popup, text=message, font=("Arial", 14), text_color="red")
        label.pack(pady=20)

        button = ctk.CTkButton(warning_popup, text="OK", command=warning_popup.destroy)
        button.pack(pady=10)
        

    def show_success(self, message):
        success_popup = ctk.CTkToplevel(self)
        success_popup.title("Success")
        success_popup.geometry("300x150")
        success_popup.lift()
        success_popup.grab_set()

        label = ctk.CTkLabel(success_popup, text=message, font=("Arial", 14), text_color="green")
        label.pack(pady=20)

        button = ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy)
        button.pack(pady=10)
        
        
    def generate_articleid(self, articleid):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT articleid FROM articles WHERE articleid = %s"
        cursor.execute(query, (articleid,))
        return cursor.fetchone() is not None
        
        
    def searchframeinfo(self):
        
        self.searchlabel = ctk.CTkLabel(self.searchframe, text="Search for users", font=("Arial", 20, "bold"))
        self.searchlabel.grid(row=1, column=0, pady=10)
        
        self.searchingframe = ctk.CTkFrame(self.searchframe, bg_color="green")
        self.searchingframe.grid(row=2, column=0)

        self.searchentry = ctk.CTkEntry(self.searchingframe, placeholder_text="USERID", width=200, font=("Arial", 15))
        self.searchentry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.searchbutton = ctk.CTkButton(self.searchingframe, text="SEARCH", fg_color="#5A6C57", font=("Arial", 15, "bold"), bg_color="#47663B", command=self.perform_search)
        self.searchbutton.grid(row=1, column=0, padx=10, sticky="nsew")
        
        self.searchbutton = ctk.CTkButton(self.searchingframe, text="BACK", fg_color="#5A6C57", font=("Arial", 15, "bold"), bg_color="#47663B", command=self.back_search)
        self.searchbutton.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
        
        self.searchlabel = ctk.CTkLabel(self.searchframe, text="Suggestions", font=("Arial", 20, "bold"))
        self.searchlabel.grid(row=3, column=0, pady=10)
        
        self.display_all_users()
        
        
    def back_search(self):
        for widget in self.searchframe.winfo_children():
            if widget not in [self.searchword, self.searchlabel, self.searchentry, self.searchbutton, self.searchingframe]:
                widget.destroy()
            
        self.searchframeinfo()  


    def perform_search(self):
        search_query = self.searchentry.get().strip()

        for widget in self.searchframe.winfo_children():
            if widget not in [self.searchlabel, self.searchentry, self.searchbutton, self.searchingframe]:
                widget.destroy()

        if search_query == "":
            self.display_all_users() 
        else:
            connection = self.get_connection()
            cursor = connection.cursor()
            query = "SELECT userid, mentorid, firstname, middlename, lastname, gender, birthday, usertype, city, province FROM user WHERE userid LIKE %s"
            cursor.execute(query, (f"%{search_query}%",))
            users = cursor.fetchall()
            
            self.search_userinfo(users) 


    def search_userinfo(self, users):

        for user in users:
            userid, mentorid, firstname, middlename, lastname, gender, birthday, usertype, city, province = user
        
            formatted_birthday = "N/A"
            
            if isinstance(birthday, str):
                try:
                    birthday = datetime.strptime(birthday, "%Y-%m-%d")
                    formatted_birthday = birthday.strftime("%B %d, %Y")
                except ValueError:
                    formatted_birthday = "Invalid date format"
            elif isinstance(birthday, datetime):
                formatted_birthday = birthday.strftime("%B %d, %Y")
            elif isinstance(birthday, date): 
                formatted_birthday = birthday.strftime("%B %d, %Y")

        ctk.CTkLabel(self.searchframe, text=f"UserID: {userid}", font=("Arial", 20)).grid(padx=150, row=4, column=0, sticky="nsew")
        ctk.CTkLabel(self.searchframe, text=f"Name: {firstname} {middlename} {lastname}", font=("Arial", 20)).grid(padx=150, row=5, column=0, sticky="nsew") 
        ctk.CTkLabel(self.searchframe, text=f"Birthday: {formatted_birthday}", font=("Arial", 20)).grid(padx=150, row=6, column=0, sticky="nsew")
        ctk.CTkLabel(self.searchframe, text=f"Gender: {gender}", font=("Arial", 20)).grid(padx=150, row=7, column=0, sticky="nsew")
        ctk.CTkLabel(self.searchframe, text=f"User Type: {usertype}", font=("Arial", 20)).grid(padx=150, row=8, column=0, sticky="nsew")
        ctk.CTkLabel(self.searchframe, text=f"Address: {city}, {province}", font=("Arial", 20)).grid(padx=150, row=9, column=0, sticky="nsew")
        if usertype == "Mentor" and userid != useridforprof:
            ctk.CTkButton(self.searchframe, text="Apply", command=lambda: self.applymentor(mentorid), bg_color="#47663B").grid(padx=150, row=10, column=0, sticky="nsew")
            
            
    def applymentor(self, mentorid):
        apprenticeid = userid4mentor 
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT mentorshipid FROM mentorship WHERE mentorid = %s and apprentices = %s"
            cursor.execute(query, (mentorid, apprenticeid))
            result = cursor.fetchone()
            
            if result:
                self.delshow_popup("An error occurred", "You already have this user a mentor.")
            else: 
                mentorshipid = random.randint(10000000, 99999999)
                insert_query = "INSERT INTO mentorship (mentorshipid, mentorid, apprentices) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (mentorshipid, mentorid, apprenticeid))
                
                connection.commit()
                self.delshow_popup("Success", "Mentorship application submitted successfully!")
        except Exception as e:
            print(f"Error in applymentor: {e}")
            self.delshow_popup("An error occurred", "Please try again later.")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            
            
    def generate_mentorshipid(self, mentorshipid):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "SELECT mentorshipid FROM mentorship WHERE mentoprshipid = %s"
        cursor.execute(query, (mentorshipid,))
        return cursor.fetchone() is not None
            
            
    def display_all_users(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = "SELECT userid, firstname, middlename, lastname, usertype FROM user WHERE userid != %s ORDER BY usertype DESC"
        cursor.execute(query, (useridforsearch,))
        users = cursor.fetchall()

        self.display_user_list(users)


    def display_user_list(self, users):
        row = 4
        for user in users:
            user_id, first_name, middle_name, last_name, user_type = user

            user_label = ctk.CTkLabel(self.searchframe, text=f"UserID: {user_id} - {first_name} {middle_name} {last_name} ({user_type})", font=("Arial", 15),  text_color="black", bg_color="#D3F1DF")
            user_label.grid(row=row, column=0, sticky="w", padx=350, pady=5, ipadx=20)
            row += 1
                
                
    def mentorframeinfo(self):
        for widget in self.mentorframe.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.mentorframe, text="Apprentices Details", font=("Arial", 40, "bold"), bg_color="#9EDF9C")
        title_label.grid(row=0, column=0, columnspan=4, pady=10, padx=0, sticky="n")

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT u.userid, u.firstname, u.middlename, u.lastname, u.city, u.province, 
                    TIMESTAMPDIFF(YEAR, u.birthday, CURDATE()) AS age
                FROM user u
                WHERE u.apprenticeid IN (
                    SELECT m.apprentices
                    FROM mentorship m
                    WHERE m.mentorid = (
                        SELECT u.mentorid
                        FROM user u
                        WHERE u.userid = %s
                    )
                );
            """
            cursor.execute(query, (useridforprof,))
            apprentices = cursor.fetchall()

            headers = ["UserID", "Full Name", "Address", "Age"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(self.mentorframe, text=header, font=("Arial", 20, "bold")).grid(row=1, column=col, sticky="nsew", padx=5, pady=5)

            row = 2
            for apprentice in apprentices:
                userid, firstname, middlename, lastname, city, province, age = apprentice
                full_name = f"{firstname} {middlename} {lastname}"
                address = f"{city}, {province}"

                ctk.CTkLabel(self.mentorframe, text=f"{userid}", font=("Arial", 15)).grid(row=row, column=0, sticky="nsew", padx=5, pady=2)
                ctk.CTkLabel(self.mentorframe, text=f"{full_name}", font=("Arial", 15)).grid(row=row, column=1, sticky="nsew", padx=5, pady=2)
                ctk.CTkLabel(self.mentorframe, text=f"{address}", font=("Arial", 15)).grid(row=row, column=2, sticky="nsew", padx=5, pady=2)
                ctk.CTkLabel(self.mentorframe, text=f"{age} years", font=("Arial", 15)).grid(row=row, column=3, sticky="nsew", padx=5, pady=2)

                row += 1

        except Exception as e:
            print(f"Error in mentorframeinfo: {e}")
            error_label = ctk.CTkLabel(self.mentorframe, text="Failed to load apprentices.", font=("Arial", 14), text_color="red")
            error_label.grid(row=2, column=0, pady=10, padx=5, sticky="w")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def aboutframeinfo(self):
        self.aboutframein = ctk.CTkLabel(self.aboutframe, text="        SKILLHUB\n\n\
        VISION\n To empower individuals through meaningful connections, \naccessible learning, and personalized career guidance, \ncreating a world where education and industry work seamlessly together \nto foster growth and innovation.\n\n\
        MISSION\n Our mission is to bridge the gap between education and industry \nby providing a collaborative platform that connects students, professionals, and mentors. \nSkillHub aims to inspire lifelong learning, support skill development,\
        \nand guide individuals toward fulfilling careers through innovative tools, \na rich resource library, and a vibrant community.", font=("Arial", 20), justify="center", anchor="center")
        self.aboutframein.grid(pady=(20, 10), row=1, column=0, columnspan=2, sticky="nsew")
        self.myname = ctk.CTkLabel(self.aboutframe, text="        PROGRAMMER\n\
        Ilagan, Marlon Jay M.\n\
        BSIT-2102", font=("Arial", 20), justify="center", anchor="center")
        self.myname.grid(pady=10, row=2, column=0, columnspan=2, sticky="nsew")
    
    
    def create_scrollable_frame(self, parent, row, col, rowspan=1, colspan=1):
        canvas = ctk.CTkCanvas(parent, bg="white", highlightthickness=0)
        canvas.grid(padx=(50, 0), row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=canvas.yview)
        scrollbar.grid(padx=(50, 0), row=row, column=col + colspan, rowspan=rowspan, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)

        return canvas, scrollable_frame


    def adminaccess(self):
        self.admin_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="white")
        self.admin_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        for i in range(16):
            self.admin_frame.columnconfigure(i, weight=1)

        self.adminlabel = ctk.CTkLabel(self.admin_frame, text="DATA OF ALL USERS", font=("Arial", 30, "bold"), text_color="black")
        self.adminlabel.grid(pady=20, row=0, column=0, columnspan=18, sticky="nsew")

        self.canvas, self.user_data_frame = self.create_scrollable_frame(self.admin_frame, row=2, col=0, colspan=18)

        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT u.userid, u.mentorid, u.apprenticeid, u.firstname, u.middlename, u.lastname,
                u.gender, u.birthday, u.usertype, u.province, u.city, l.email, l.password 
            FROM user u
            LEFT JOIN login l ON u.userid = l.userid
        """
        cursor.execute(query)
        users = cursor.fetchall()

        headers = [
            "User ID", "Mentor ID", "Apprentice ID", "First Name", "Middle Name", "Last Name",
            "Gender", "Birthday", "User Type", "Province", "City", "Email", "Password"
        ]

        for col_num, header in enumerate(headers):
            label_frame = ctk.CTkFrame(self.user_data_frame, fg_color="#D3D3D3", corner_radius=5)
            label_frame.grid(row=0, column=col_num, padx=10, pady=10, sticky="nsew")

            label = ctk.CTkLabel(label_frame, text=header, font=("Arial", 13, "bold"), text_color="black", anchor="center")
            label.grid(row=0, column=0, sticky="nsew")

        for row_num, user in enumerate(users, start=1):
            for col_num, value in enumerate(user):
                cell_frame = ctk.CTkFrame(self.user_data_frame, fg_color="#f8f8f8", corner_radius=5)
                cell_frame.grid(row=row_num, column=col_num, padx=5, pady=10, sticky="nsew")

                label = ctk.CTkLabel(cell_frame, text=value, font=("Arial", 13), text_color="black", anchor="center")
                label.grid(row=0, column=0, sticky="nsew")

        self.user_data_frame.update_idletasks()

        menquery = "SELECT COUNT(*) FROM user WHERE usertype = 'Mentor';"
        appquery = "SELECT COUNT(*) FROM user WHERE usertype = 'Apprentice';"
        menquery2 = "SELECT COUNT(mentorshipid) FROM mentorship;"

        cursor.execute(menquery)
        mentors = cursor.fetchone()[0]

        cursor.execute(appquery)
        apprentices = cursor.fetchone()[0]
        
        cursor.execute(menquery2)
        mentorships = cursor.fetchone()[0]

        self.numofmentors = ctk.CTkLabel(self.admin_frame, text=f"Active Mentors: {mentors}", font=("Arial", 13, "bold"), text_color="black")
        self.numofmentors.grid(padx=(50, 0), row=1, column=0, sticky="w")

        self.numofmentorapprentices = ctk.CTkLabel(self.admin_frame, text=f"Active Apprentices: {apprentices}", font=("Arial", 13, "bold"), text_color="black")
        self.numofmentorapprentices.grid(row=1, column=1, sticky="w")
        
        self.numofmentorapprentices = ctk.CTkLabel(self.admin_frame, text=f"Active Mentorships: {mentorships}", font=("Arial", 13, "bold"), text_color="black")
        self.numofmentorapprentices.grid(row=1, column=2, sticky="w")

        self.delete_entry = ctk.CTkEntry(self.admin_frame, placeholder_text="USERID TO DELETE", width=150)
        self.delete_entry.grid(row=1, column=13, padx=10, pady=10, sticky="e")

        self.delete_button = ctk.CTkButton(self.admin_frame, text="Delete User", text_color="black", command=lambda: self.delete_user(self.delete_entry.get()))
        self.delete_button.grid(row=1, column=14, padx=10, pady=10, sticky="e")

        self.refresh_button = ctk.CTkButton(self.admin_frame, text="REFRESH", text_color="black", command=self.refreshadmin)
        self.refresh_button.grid(row=1, column=15, padx=10, pady=10, sticky="e")
        
        self.logoutadmin_button = ctk.CTkButton(self.admin_frame, text="LOG-OUT", text_color="black", command= self.logoutadmin)
        self.logoutadmin_button.grid(row=0, column=15, padx=10, pady=10, sticky="e")

        self.adminlabel2 = ctk.CTkLabel(self.admin_frame, text="LIST OF ALL MENTORSHIPS", font=("Arial", 30, "bold"),text_color="black")
        self.adminlabel2.grid(pady=20, row=3, column=0, columnspan=18, sticky="nsew")

        self.canvas2, self.user_data_frame2 = self.create_scrollable_frame(self.admin_frame, row=4, col=0, colspan=18)

        mentorship_query = """SELECT m.mentorshipid, 
                            m.mentorid, 
                            CONCAT(u1.firstname, ' ', u1.middlename, ' ', u1.lastname) AS MentorName, 
                            m.apprentices, 
                            CONCAT(u2.firstname, ' ', u2.middlename, ' ', u2.lastname) AS ApprenticeName
                            FROM mentorship m
                            LEFT JOIN user u1 ON m.mentorid = u1.mentorid
                            LEFT JOIN user u2 ON m.apprentices = u2.apprenticeid; """
        cursor.execute(mentorship_query)
        mentorships = cursor.fetchall()
        connection.close()

        headers = ["Mentorship ID", "Mentor ID", "Mentor Name", "Apprentice ID", "Apprentice Name"]

        for col_num, header in enumerate(headers):
            label_frame = ctk.CTkFrame(self.user_data_frame2, fg_color="#D3D3D3", corner_radius=5)
            label_frame.grid(row=0, column=col_num, padx=10, pady=10, sticky="nsew")

            label = ctk.CTkLabel(label_frame, text=header, font=("Arial", 13, "bold"), text_color="black", anchor="center")
            label.grid(row=0, column=0, sticky="nsew")

        for row_num, mentorship in enumerate(mentorships, start=1):
            for col_num, value in enumerate(mentorship):
                cell_frame = ctk.CTkFrame(self.user_data_frame2, fg_color="#f8f8f8", corner_radius=5)
                cell_frame.grid(row=row_num, column=col_num, padx=5, pady=10, sticky="nsew")

                label = ctk.CTkLabel(cell_frame, text=value, font=("Arial", 13), text_color="black", anchor="center")
                label.grid(row=0, column=0, sticky="nsew")

        self.user_data_frame2.update_idletasks()
        
    
    def logoutadmin(self):
        self.admin_frame.destroy()
        self.create_signup_frame()


    def refreshadmin(self):
        self.adminaccess()


    def delete_user(self, useridtodelete):
        def confirm_deletion():
            try:
                connection = self.get_connection()
                cursor = connection.cursor()

                query_delete_login = "DELETE FROM login WHERE userid = %s"
                cursor.execute(query_delete_login, (useridtodelete,))
                
                query_delete_user = "DELETE FROM user WHERE userid = %s"
                cursor.execute(query_delete_user, (useridtodelete,))
                
                connection.commit()
                confirmation_label.configure(text=f"User with ID {useridtodelete} has been deleted.")
                
            except Exception as e:
                confirmation_label.configure(text=f"Error occurred: {e}")
            finally:
                if connection:
                    connection.close()
                confirmation_window.after(1000, confirmation_window.destroy) 

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query_check_user = "SELECT firstname, middlename, lastname FROM user WHERE userid = %s"
            cursor.execute(query_check_user, (useridtodelete,))
            user = cursor.fetchone()
            
            if not user:
                return
            
            firstname, middlename, lastname = user
            full_name = f"{firstname} {middlename} {lastname}".strip()

            confirmation_window = ctk.CTkToplevel()
            confirmation_window.title("Confirm Deletion")
            confirmation_window.geometry("400x200")
            confirmation_window.grab_set()
            
            message = f"Are you sure you want to delete the following user?\n\nUser ID: {useridtodelete}\nName: {full_name}"
            confirmation_label = ctk.CTkLabel(confirmation_window, text=message, font=("Arial", 14), wraplength=380, justify="left")
            confirmation_label.pack(pady=20)
            
            confirm_button = ctk.CTkButton(confirmation_window, text="Confirm", command=confirm_deletion)
            confirm_button.pack(side="left", padx=20, pady=20, expand=True)
            
            cancel_button = ctk.CTkButton(confirmation_window, text="Cancel", command=confirmation_window.destroy)
            cancel_button.pack(side="right", padx=20, pady=20, expand=True)
        
        except Exception as e:
            pass
        
        
    def show_frame(self, frame):
        
        for f in [self.profileframe, self.homeframe, self.aboutframe, self.searchframe, self.mentorframe]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)


    def logout(self):
        self.main_frame.destroy()
        self.create_signup_frame()


if __name__ == "__main__":
    app = App()
    app.mainloop()
