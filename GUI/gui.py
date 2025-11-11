import customtkinter 
from CTkTable import CTkTable
import sqlite3
from datetime import datetime, timedelta






customtkinter.set_appearance_mode("dark")  # Or "light" or "system"
customtkinter.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
customtkinter.set_widget_scaling(4) 


class Sign_in_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4,5), weight=1)

        # Spacer label to push back button to the right
        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        # Place back button at top-right
        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Username label and entry field
        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Password label and password entry (masked input)
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=3, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Enter password", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Enter button
        self.enter_button = customtkinter.CTkButton(self, text="Enter", command=self.enter_action)
        self.enter_button.grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    def back(self):
        self.grid_forget()

    def login_function(self,username,password):
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                cursor = conn.cursor()

                # Check users table
                cursor.execute(
                    "SELECT username FROM users WHERE username = ? AND password = ? AND verified = 'YES'",
                    (username, password)
                )
                user_result = cursor.fetchone()

                # Check admin_users table
                cursor.execute(
                    "SELECT admin_username FROM admin_users WHERE admin_username = ? AND password = ?",
                    (username, password)
                )
                admin_result = cursor.fetchone()

            # Check results
            if user_result:
                return 1
                
            if admin_result:
                return 2
                
            else:
                return 3
                
        except sqlite3.Error:
            return 3
        except Exception:
            return 3
        

    def enter_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # print(f"Username: {username}, Password: {password}")
        self.case = self.login_function(username, password)

        self.master.username = username

        if (self.case == 1):
            self.master.log_in_frame.grid_forget()
            self.master.log_in_frame.sign_in_frame.grid_forget()
            self.master.user_frame = User_frame(self.master)
            self.master.user_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")
        elif (self.case == 2):
            self.master.log_in_frame.grid_forget()
            self.master.log_in_frame.sign_in_frame.grid_forget()
            self.master.admin_user_frame = Admin_user_frame(self.master)
            self.master.admin_user_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")
        else:
            self.spacer.configure(text="Invalid Credentials")
        
        # Add your login validation logic here

class Register_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4,5,6,7,8,9), weight=1)

        # Spacer label to push back button to the right
        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        # Place back button at top-right
        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Username label and entry field
        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Password label and password entry (masked input)
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=3, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Enter password", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        #Contact
        contact_label = customtkinter.CTkLabel(self, text="Contact:")
        contact_label.grid(row=5, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.contact_entry = customtkinter.CTkEntry(self, placeholder_text="Enter contact")
        self.contact_entry.grid(row=6, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        #email
        email_label = customtkinter.CTkLabel(self, text="Email:")
        email_label.grid(row=7, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Enter email")
        self.email_entry.grid(row=8, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Enter button
        self.enter_button = customtkinter.CTkButton(self, text="Enter", command=self.enter_action)
        self.enter_button.grid(row=9, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        

    def back(self):
        self.grid_forget()

    def add_new_user(self, username, password, contact, email):
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                
                # Insert user with all required fields + defaults for other columns
                cursor.execute('''
                    INSERT INTO users (username, password, verified, borrowed_book_id, borrowed_book_date,
                                    approved_book, requested_bookid, contact, email, join_date)
                    VALUES (?, ?, 'PENDING', 'NIL', 'NIL', 'PENDING', 'NIL', ?, ?, datetime('now'))
                ''', (username, password, contact, email))
                
                conn.commit()
                
                return 1  # Login successful
            
        except sqlite3.IntegrityError as e:
            return 2  # Login unsuccessful
        except Exception as e:
            return 3  # Login unsuccessful

    def enter_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        
        self.case = self.add_new_user(username, password, contact, email)

        if (self.case == 1):
            self.spacer.configure(text="Request Sent")
        elif (self.case == 2):
            self.spacer.configure(text="User or email already exists")
        else:
            self.spacer.configure(text="Invalid Credentials")
        # Add your login validation logic here

class Register_as_admin_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Spacer label to push back button to the right
        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        # Place back button at top-right
        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Username label and entry field
        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Password label and password entry (masked input)
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=3, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Enter password", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        #Contact
        contact_label = customtkinter.CTkLabel(self, text="Contact:")
        contact_label.grid(row=5, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.contact_entry = customtkinter.CTkEntry(self, placeholder_text="Enter contact")
        self.contact_entry.grid(row=6, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        #email
        email_label = customtkinter.CTkLabel(self, text="Email:")
        email_label.grid(row=7, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Enter email")
        self.email_entry.grid(row=8, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        #Admin key
        admin_key_label = customtkinter.CTkLabel(self, text="Admin Key:")
        admin_key_label.grid(row=9, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.admin_key_entry = customtkinter.CTkEntry(self, placeholder_text="Enter admin key")
        self.admin_key_entry.grid(row=10, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # Enter button
        self.enter_button = customtkinter.CTkButton(self, text="Enter", command=self.enter_action)
        self.enter_button.grid(row=11, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        

    def back(self):
        self.grid_forget()

    def add_new_user(self, username, password, contact, email):
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                
                # Insert user with all required fields + defaults for other columns
                cursor.execute('''
                    INSERT INTO admin_users (admin_username, password, role, contact, email)
                    VALUES (?, ?, 'ADMIN', ?, ?)
                ''', (username, password, contact, email))
                
                conn.commit()
                return 1  # Login successful
            
        except sqlite3.IntegrityError as e:
            return 2  # Login unsuccessful
        except Exception as e:
            return 3  # Login unsuccessful

    def enter_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        admin_key = self.admin_key_entry.get()

        if (admin_key != "1111"):
            self.spacer.configure(text="Invalid Admin key")
            return
        
        self.case = self.add_new_user(username, password, contact, email)

        if (self.case == 1):
            self.spacer.configure(text="Created Admin User")
        elif (self.case == 2):
            self.spacer.configure(text="User or email already exists")
        else:
            self.spacer.configure(text="Invalid Credentials")
        # Add your login validation logic here
        
class Log_in_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2), weight=1)
        
        self.sign_in_button = customtkinter.CTkButton(self, text="Sign in", command=self.sign_in)
        self.sign_in_button.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=1, column=0, padx=10, pady=(5, 5))
        self.register_as_admin_button = customtkinter.CTkButton(self, text="Admin Register", command=self.register_as_admin)
        self.register_as_admin_button.grid(row=2, column=0, padx=10, pady=(5, 10))
        
        self.sign_in_frame = Sign_in_frame(self.master)
        self.register_frame = Register_frame(self.master)
        self.register_as_admin_frame = Register_as_admin_frame(self.master)

    def sign_in(self):
        self.register_frame.grid_forget()
        self.register_as_admin_frame.grid_forget()
        self.sign_in_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
    def register(self):
        self.sign_in_frame.grid_forget()
        self.register_as_admin_frame.grid_forget()
        self.register_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
    def register_as_admin(self):
        self.sign_in_frame.grid_forget()
        self.register_frame.grid_forget()
        self.register_as_admin_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

class Filters_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0,1), weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(2, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4), weight=1)

        # Spacer label to push back button to the right
        spacer = customtkinter.CTkLabel(self, text="")
        spacer.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Place back button at top-right
        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # 1. Biography
        # 2. Fantasy
        # 3. Fiction
        # 4. History
        # 5. Mystery
        # 6. Non-fiction
        # 7. Romance
        # 8. Science
        # 9. Self-Help
        # 10. Technology

        

        # Biography
        self.master.biography = customtkinter.StringVar(value="Y")
        self.biography_checkbox = customtkinter.CTkCheckBox(self, text="Biography", command=self.set_biography_var,
                                    variable=self.master.biography, onvalue="Y", offvalue="N")
        self.biography_checkbox.grid(row=1, column=0, padx=5, pady=(10,5), sticky="ew")

        # Fantasy
        self.master.fantasy = customtkinter.StringVar(value="Y")
        self.fantasy_checkbox = customtkinter.CTkCheckBox(self, text="Fantasy", command=self.set_fantasy_var,
                                variable=self.master.fantasy, onvalue="Y", offvalue="N")
        self.fantasy_checkbox.grid(row=1, column=1, padx=5, pady=(10,5), sticky="ew")

        self.master.fiction = customtkinter.StringVar(value="Y")
        self.fiction_checkbox = customtkinter.CTkCheckBox(self, text="Fiction", command=self.set_fiction_var,
                                     variable=self.master.fiction, onvalue="Y", offvalue="N")
        self.fiction_checkbox.grid(row=1, column=2, padx=10, pady=(10,5), sticky="ew")  # left align label

        # History
        self.master.history = customtkinter.StringVar(value="N")
        self.history_checkbox = customtkinter.CTkCheckBox(self, text="History", command=self.set_history_var,
                                variable=self.master.history, onvalue="Y", offvalue="N")
        self.history_checkbox.grid(row=2, column=0, padx=5, pady=(5,5), sticky="w")

        # Mystery
        self.master.mystery = customtkinter.StringVar(value="N")
        self.mystery_checkbox = customtkinter.CTkCheckBox(self, text="Mystery", command=self.set_mystery_var,
                                variable=self.master.mystery, onvalue="Y", offvalue="N")
        self.mystery_checkbox.grid(row=2, column=1, padx=5, pady=(5,5), sticky="w")

        # Non-fiction
        self.master.non_fiction = customtkinter.StringVar(value="N")
        self.non_fiction_checkbox = customtkinter.CTkCheckBox(self, text="Non-fiction", command=self.set_non_fiction_var,
                                    variable=self.master.non_fiction, onvalue="Y", offvalue="N")
        self.non_fiction_checkbox.grid(row=2, column=2, padx=10, pady=(5,5), sticky="w")

        # Romance
        self.master.romance = customtkinter.StringVar(value="N")
        self.romance_checkbox = customtkinter.CTkCheckBox(self, text="Romance", command=self.set_romance_var,
                                variable=self.master.romance, onvalue="Y", offvalue="N")
        self.romance_checkbox.grid(row=3, column=0, padx=5, pady=(5,5), sticky="w")

        # Science
        self.master.science = customtkinter.StringVar(value="N")
        self.science_checkbox = customtkinter.CTkCheckBox(self, text="Science", command=self.set_science_var,
                                variable=self.master.science, onvalue="Y", offvalue="N")
        self.science_checkbox.grid(row=3, column=1, padx=5, pady=(5,5), sticky="w")

        # Self-Help
        self.master.self_help = customtkinter.StringVar(value="N")
        self.self_help_checkbox = customtkinter.CTkCheckBox(self, text="Self-Help", command=self.set_self_help_var,
                                variable=self.master.self_help, onvalue="Y", offvalue="N")
        self.self_help_checkbox.grid(row=3, column=2, padx=10, pady=(5,5), sticky="w")

        # Technology
        self.master.technology = customtkinter.StringVar(value="N")
        self.technology_checkbox = customtkinter.CTkCheckBox(self, text="Technology", command=self.set_technology_var,
                                variable=self.master.technology, onvalue="Y", offvalue="N")
        self.technology_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=(5,10), sticky="w")

        self.select_all_button = customtkinter.CTkButton(self, text="Select All", command=self.select_all)
        self.select_all_button.grid(row=5, column=0, padx=10, pady=10, sticky="se")

        self.deselect_all_button = customtkinter.CTkButton(self, text="Deselect All", command=self.deselect_all)
        self.deselect_all_button.grid(row=5, column=1, padx=10, pady=10, sticky="se")

        self.master.available = customtkinter.StringVar(value="N")
        self.available_checkbox = customtkinter.CTkCheckBox(self, text="available", command=self.set_available_var,
                                variable=self.master.available, onvalue="Y", offvalue="N")
        self.available_checkbox.grid(row=5, column=2, padx=10, pady=10, sticky="w")


    

    def select_all(self):
        self.biography_checkbox.select()
        self.fantasy_checkbox.select()
        self.fiction_checkbox.select()
        self.history_checkbox.select()
        self.mystery_checkbox.select()
        self.non_fiction_checkbox.select()
        self.romance_checkbox.select()
        self.science_checkbox.select()
        self.self_help_checkbox.select()
        self.technology_checkbox.select()
        self.available_checkbox.select()

    def deselect_all(self):
        self.biography_checkbox.deselect()
        self.fantasy_checkbox.deselect()
        self.fiction_checkbox.deselect()
        self.history_checkbox.deselect()
        self.mystery_checkbox.deselect()
        self.non_fiction_checkbox.deselect()
        self.romance_checkbox.deselect()
        self.science_checkbox.deselect()
        self.self_help_checkbox.deselect()
        self.technology_checkbox.deselect() 
        self.available_checkbox.deselect()

    def set_available_var(self):
        print("checkbox toggled, current value:", self.master.available.get())

    def set_fiction_var(self):
        print("checkbox toggled, current value:", self.master.fiction.get())

    def set_biography_var(self):
        print("Biography toggled, current value:", self.master.biography.get())

    def set_fantasy_var(self):
        print("Fantasy toggled, current value:", self.master.fantasy.get())

    def set_fiction_var(self):
        print("Fiction toggled, current value:", self.master.fiction.get())

    def set_history_var(self):
        print("History toggled, current value:", self.master.history.get())

    def set_mystery_var(self):
        print("Mystery toggled, current value:", self.master.mystery.get())

    def set_non_fiction_var(self):
        print("Non-fiction toggled, current value:", self.master.non_fiction.get())

    def set_romance_var(self):
        print("Romance toggled, current value:", self.master.romance.get())

    def set_science_var(self):
        print("Science toggled, current value:", self.master.science.get())

    def set_self_help_var(self):
        print("Self-Help toggled, current value:", self.master.self_help.get())

    def set_technology_var(self):
        print("Technology toggled, current value:", self.master.technology.get())


    def back(self):
        self.grid_forget()

class Browse_books_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2), weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(3, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3), weight=1)

        # Spacer label to push back button to the right
        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")

        # Place back button at top-right
        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=3, padx=10, pady=10, sticky="ne")

        search_title_label = customtkinter.CTkLabel(self, text="Enter title:")
        search_title_label.grid(row=1, column=0, columnspan=4, padx=20, pady=(10,5), sticky="w")  # left align label

        self.search_title_entry = customtkinter.CTkEntry(self, placeholder_text="Enter book title")
        self.search_title_entry.grid(row=2, column=0, columnspan=4, padx=20, pady=(5, 10), sticky="ew")

        self.search_by_filters_button = customtkinter.CTkButton(self, text="Search by filters", command=self.search_by_filters)
        self.search_by_filters_button.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        self.search_by_title_button = customtkinter.CTkButton(self, text="Search by title", command=self.search_by_title)
        self.search_by_title_button.grid(row=3, column=2, columnspan=2, pady=20, padx=20, sticky="ew")

    def back(self):
        self.grid_forget()

        # 1. Biography
        # 2. Fantasy
        # 3. Fiction
        # 4. History
        # 5. Mystery
        # 6. Non-fiction
        # 7. Romance
        # 8. Science
        # 9. Self-Help
        # 10. Technology
    def filter_books(self, genre1=None, genre2=None, genre3=None, genre4=None, 
                 genre5=None, genre6=None, genre7=None, genre8=None, genre9=None, genre10=None,
                 available=None):
        """
        Advanced book filtering function.
        Returns formatted string, column_names, data_rows or (error message, None, [])
        """
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all available genres from database
                cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
                genres = [row[0] for row in cursor.fetchall()]
                
                if not genres:
                    error_msg = "No genres found in database."
                    return error_msg, None, []
                
                # Use direct parameters
                genre_inputs = [genre1, genre2, genre3, genre4, genre5, genre6, 
                                genre7, genre8, genre9, genre10]
                
                # Validate parameters
                if any(g not in [None, 'Y', 'N'] for g in genre_inputs):
                    error_msg = "❌ Genre parameters must be 'Y', 'N', or None!"
                    return error_msg, None, []
                
                if available not in [None, 'Y', 'N']:
                    error_msg = "❌ 'available' parameter must be 'Y', 'N', or None!"
                    return error_msg, None, []
                
                # Map parameters to actual genres (up to 10)
                selected_genres = []
                for i, genre_flag in enumerate(genre_inputs):
                    if genre_flag == 'Y' and i < len(genres):
                        selected_genres.append(genres[i])
                
                show_available = available == 'Y'
                genre_numbers = [i+1 for i, flag in enumerate(genre_inputs) if flag == 'Y']
                
                print(f"\n🔍 Direct filter: Genres {genre_numbers} | Available only: {show_available}")
                
                # Build safe parameterized query
                query_params = []
                conditions = []
                
                # Genre conditions
                if selected_genres:
                    genre_placeholders = ','.join(['?' for _ in selected_genres])
                    conditions.append(f"(genre IN ({genre_placeholders}))")
                    query_params.extend(selected_genres)
                
                # Availability condition
                if show_available:
                    conditions.append("available = 'YES'")
                
                # Build final query
                base_query = """
                    SELECT id, isbn, title, author, genre, available, available_for, check_after, quantity 
                    FROM books
                """
                where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
                order_clause = " ORDER BY genre ASC, title ASC"
                
                final_query = base_query + where_clause + order_clause
                
                print(f"\n🔍 Executing Query:")
                print(f"   {final_query}")
                print(f"   Params: {query_params}")
                
                # Execute with parameters (SQL injection safe)
                cursor.execute(final_query, query_params)
                books = cursor.fetchall()
                
                if not books:
                    error_msg = "❌ No books found matching criteria!"
                    return error_msg, None, []
                
                # Get column names in order from cursor.description
                column_names = [description[0] for description in cursor.description]
                
                # Prepare data rows
                data_rows = []
                for book in books:
                    row_data = []
                    for item in book:
                        row_data.append(item if item is not None else "")
                    data_rows.append(row_data)
                
                # Calculate column widths dynamically
                col_widths = [len(name) for name in column_names]
                
                # Find maximum width for each column including all data
                for row in data_rows:
                    for i, val in enumerate(row):
                        val_str = str(val)
                        col_widths[i] = max(col_widths[i], len(val_str))
                
                # Add padding (2 spaces on each side)
                col_widths = [width + 4 for width in col_widths]
                
                # Build format string dynamically
                format_parts = [f"{{:<{width}}}" for width in col_widths]
                fmt_string = " | ".join(format_parts)
                
                # Build header
                header_parts = [f"{name:<{width-4}}" for name, width in zip(column_names, col_widths)]
                header_line = " | ".join(header_parts)
                
                # Build separator
                separator_parts = ["-" * width for width in col_widths]
                separator_line = "-+-".join(separator_parts).replace("-", "-")
                
                # Build data rows
                data_lines = []
                for row in data_rows:
                    row_parts = [f"{str(val):<{width-4}}" for val, width in zip(row, col_widths)]
                    data_lines.append(" | ".join(row_parts))
                
                # Combine everything
                result_lines = [
                    "📖 Book Search Results",
                    f"Filter: Genres {', '.join(selected_genres) if selected_genres else 'All'} | Available only: {show_available}",
                    "",
                    header_line,
                    separator_line,
                ] + data_lines + [
                    separator_line,
                    f"Total: {len(books)} books found.",
                    ""
                ]
                
                formatted_result = "\n".join(result_lines)
                
                return formatted_result, column_names, data_rows
                
        except sqlite3.Error as e:
            error_msg = f"❌ Database error: {e}"
            return error_msg, None, []
        except Exception as e:
            error_msg = f"❌ Unexpected error: {e}"
            return error_msg, None, []

    def search_by_filters(self):
        self.books, column_names, data_rows = self.filter_books(
            self.master.biography.get(),
            self.master.fantasy.get(),
            self.master.fiction.get(),
            self.master.history.get(),
            self.master.mystery.get(),
            self.master.non_fiction.get(),
            self.master.romance.get(),
            self.master.science.get(),
            self.master.self_help.get(),
            self.master.technology.get(),
            self.master.available.get()
        )

        print(self.books)

        if not data_rows:
            customtkinter.CTkMessagebox.show_info("No Books", "No books found matching the filters.")
            return

        # Compose table values: first row for headers, following for data
        values = [column_names] + [list(map(str, row)) for row in data_rows]

        # Open new CTkToplevel
        result_win = customtkinter.CTkToplevel(self)
        result_win.geometry("2400x1300")
        result_win.title("Filtered Books Table")
        
        # Create scrollable frame in the toplevel window
        scrollable_frame = customtkinter.CTkScrollableFrame(result_win)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the table inside the scrollable frame
        table = CTkTable(
            master=scrollable_frame,
            row=len(values),
            column=len(column_names),
            values=values,
        )
        # # Create the table: plus one row for header, as many columns as there are headers
        # table.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        table.pack(expand=True, fill="both", padx=10, pady=10)

        small_font = customtkinter.CTkFont(family="Arial", size=5)

        # After creating your CTkTable instance named 'table'
        # Hypothetical: loop through all cells if accessible
        for (row, col), button in table.frame.items():
            button.configure(font=small_font)

    def search_books_by_title(self, title):
        """
        Search books by title and return results in format compatible with ctkTable.
        Returns a tuple of (column_names, data_rows) or (None, []) if no matches/errors.
        Includes all columns: id, title, available, check_after, available_for, genre, author, isbn, quantity
        """
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                cursor = conn.cursor()

                # Search for books containing the title (case-insensitive)
                cursor.execute(
                    """
                    SELECT id, title, available, check_after, available_for, genre, author, isbn, quantity
                    FROM books 
                    WHERE title LIKE ? 
                    ORDER BY title
                    """,
                    (f"%{title}%",)
                )
                results = cursor.fetchall()

                if not results:
                    return None, []

                # Define column names for CTkTable (matches table, use human-friendly for display)
                column_names = [
                    'ID', 'Title', 'Available', 'Due Date', 'Duration',
                    'Genre', 'Author', 'ISBN', 'Quantity'
                ]

                # Format data rows for CTkTable
                data_rows = []
                for row in results:
                    id_ = row[0] if row[0] is not None else ''
                    title_ = row[1] if row[1] is not None else ''
                    available = row[2] if row[2] is not None else ''
                    check_after = row[3] if row[3] is not None else ''
                    available_for = row[4] if row[4] is not None else ''
                    genre = row[5] if row[5] is not None else ''
                    author = row[6] if row[6] is not None else ''
                    isbn = row[7] if row[7] is not None else ''
                    quantity = str(row[8]) if row[8] is not None else '0'

                    # Display "Yes"/"No"
                    if available == 'YES':
                        available_display = 'Yes'
                    elif available == 'NO':
                        available_display = 'No'
                    else:
                        available_display = available

                    # Format due date or leave empty unless book is borrowed
                    if check_after and available == 'NO':
                        due_date = check_after
                    else:
                        due_date = ''

                    # duration ("available_for")—display as is
                    duration = available_for

                    data_rows.append([
                        id_,
                        title_,
                        available_display,
                        due_date,
                        duration,
                        genre,
                        author,
                        isbn,
                        quantity
                    ])

                return column_names, data_rows

        except sqlite3.Error:
            return None, []
        except Exception:
            return None, []

    def search_by_title(self):
        column_names, data_rows = self.search_books_by_title(self.search_title_entry.get())

        # print(self.books)

        if not data_rows:
            customtkinter.CTkMessagebox.show_info("No Books", "No books found matching the filters.")
            return

        # Compose table values: first row for headers, following for data
        values = [column_names] + [list(map(str, row)) for row in data_rows]

        # Open new CTkToplevel
        result_win = customtkinter.CTkToplevel(self)
        result_win.geometry("2400x1300")
        result_win.title("Searched Books Table")
        
        # Create scrollable frame in the toplevel window
        scrollable_frame = customtkinter.CTkScrollableFrame(result_win)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the table inside the scrollable frame
        table = CTkTable(
            master=scrollable_frame,
            row=len(values),
            column=len(column_names),
            values=values,
        )
        # # Create the table: plus one row for header, as many columns as there are headers
        # table.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        table.pack(expand=True, fill="both", padx=10, pady=10)

        small_font = customtkinter.CTkFont(family="Arial", size=5)

        # After creating your CTkTable instance named 'table'
        # Hypothetical: loop through all cells if accessible
        for (row, col), button in table.frame.items():
            button.configure(font=small_font)

    def enter_action(self):
        self.spacer.configure(text="Request Sent")

class Borrow_book_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4,5), weight=1)

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        book_id_label = customtkinter.CTkLabel(self, text="Book id:")
        book_id_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.book_id_entry = customtkinter.CTkEntry(self, placeholder_text="Enter book id")
        self.book_id_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        self.enter_button = customtkinter.CTkButton(self, text="Enter", command=self.enter_action)
        self.enter_button.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    def back(self):
        self.grid_forget()
        
    def borrow_book_by_id(self, book_id, username):
        """
        Function to borrow a book by ID.
        Returns 1 for success, 2 for book issue, 3 for user issue, 4 for error.
        """
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                cursor = conn.cursor()

                # Check if user exists and is verified
                cursor.execute(
                    "SELECT username FROM users WHERE username = ? AND verified = 'YES'",
                    (username,)
                )
                user_result = cursor.fetchone()

                if not user_result:
                    print("User '{}' not found or not verified".format(username))
                    return 3

                # Check if book exists and is available
                cursor.execute(
                    "SELECT id, title, author, available, quantity FROM books WHERE id = ?",
                    (book_id,)
                )
                book_result = cursor.fetchone()

                if not book_result:
                    print("Book ID '{}' not found".format(book_id))
                    return 2

                book_id_val, title, author, available, quantity = book_result

                if available != 'YES':
                    print("Book '{}' (ID: {}) is not available".format(title, book_id))
                    return 2

                if quantity <= 0:
                    print("Book '{}' is out of stock".format(title))
                    return 2

                # Check if user already has a borrowed book
                cursor.execute(
                    "SELECT borrowed_book_id FROM users WHERE username = ? AND borrowed_book_id != 'NIL'",
                    (username,)
                )
                existing_borrow = cursor.fetchone()

                if existing_borrow:
                    current_book_id = existing_borrow[0]
                    cursor.execute("SELECT title FROM books WHERE id = ?", (current_book_id,))
                    current_book = cursor.fetchone()
                    if current_book:
                        print("User '{}' already borrowed '{}' (ID: {})".format(username, current_book[0], current_book_id))
                    else:
                        print("User '{}' already has a borrowed book".format(username))
                    return 3

                # Calculate dates
                borrow_date = datetime.now().date()
                due_date = borrow_date + timedelta(days=7)
                borrow_date_str = borrow_date.strftime('%Y-%m-%d')
                due_date_str = due_date.strftime('%Y-%m-%d')

                # Update book status
                cursor.execute("""
                    UPDATE books 
                    SET available = 'NO', check_after = ?, available_for = '7 days'
                    WHERE id = ?
                """, (due_date_str, book_id))

                # Update user info
                cursor.execute("""
                    UPDATE users 
                    SET borrowed_book_id = ?, borrowed_book_date = ?
                    WHERE username = ?
                """, (book_id, borrow_date_str, username))

                # Decrement quantity
                cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book_id,))

                conn.commit()

                print("Book borrowed successfully")
                print("User: {}".format(username))
                print("Book ID: {}".format(book_id))
                print("Title: '{}' by {}".format(title, author))
                print("Borrow Date: {}".format(borrow_date_str))
                print("Due Date: {}".format(due_date_str))
                print("Duration: 7 days")
                print("Remaining Quantity: {}".format(quantity - 1))

                return 1

        except sqlite3.Error as e:
            print("Database error: {}".format(e))
            return 4
        except Exception as e:
            print("Error: {}".format(e))
            return 4

    def enter_action(self):
        self.case = self.borrow_book_by_id(self.book_id_entry.get(), self.master.username)

        if (self.case == 1):
            self.spacer.configure(text="Borrowed Book Successfully")
        else:
            self.spacer.configure(text="Invalid Credentials")
        # self.master.log_in_frame.grid_forget()
        # self.master.log_in_frame.sign_in_frame.grid_forget()

        # self.master.user_frame = User_frame(self.master)
        # self.master.user_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")     

class User_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((1,2), weight=1)
        
        self.filters_label = customtkinter.CTkLabel(self, text="Filters", text_color="grey", cursor="hand2")
        self.filters_label.bind("<Button-1>", self.filters)
        self.filters_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.browse_button = customtkinter.CTkButton(self, text="Browse Books", command=self.browse_books)
        self.browse_button.grid(row=1, column=0, padx=10, pady=(5, 5))
        self.borrow_button = customtkinter.CTkButton(self, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.grid(row=2, column=0, padx=10, pady=(5, 10))

        self.filters_frame = Filters_frame(self.master)
        self.browse_books_frame = Browse_books_frame(self.master)
        self.borrow_book_frame = Borrow_book_frame(self.master)

    def filters(self, event):
        self.browse_books_frame.grid_forget()
        self.borrow_book_frame.grid_forget()
        self.filters_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def browse_books(self):
        self.filters_frame.grid_forget()
        self.borrow_book_frame.grid_forget()
        self.browse_books_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
        # self.register_frame.grid_forget()
        # self.register_as_admin_frame.grid_forget()
        # self.sign_in_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
    def borrow_book(self):
        self.filters_frame.grid_forget()
        self.browse_books_frame.grid_forget()
        self.borrow_book_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

        # self.sign_in_frame.grid_forget()
        # self.register_as_admin_frame.grid_forget()
        # self.register_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

class Pending_requests_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        # self.grid_rowconfigure((1,2,3,4,5), weight=1)

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")


        user_label = customtkinter.CTkLabel(self, text="Username:")
        user_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username")
        self.user_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 5), sticky="ew")

        # Submit button
        self.submit_button = customtkinter.CTkButton(self, text="Approve", command=self.submit_action)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        self.show_button = customtkinter.CTkButton(self, text="Show Pending Users", command=self.show_requests)
        self.show_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

    def show_requests(self):
        column_names, data_rows = self.show_pending_requests()

        # print(self.books)

        if not data_rows:
            customtkinter.CTkMessagebox.show_info("No Books", "No books found matching the filters.")
            return

        # Compose table values: first row for headers, following for data
        values = [column_names] + [list(map(str, row)) for row in data_rows]

        # Open new CTkToplevel
        result_win = customtkinter.CTkToplevel(self)
        result_win.geometry("2400x1300")
        result_win.title("Pending Users Books Table")
        
        # Create scrollable frame in the toplevel window
        scrollable_frame = customtkinter.CTkScrollableFrame(result_win)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the table inside the scrollable frame
        table = CTkTable(
            master=scrollable_frame,
            row=len(values),
            column=len(column_names),
            values=values,
        )
        # # Create the table: plus one row for header, as many columns as there are headers
        # table.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        table.pack(expand=True, fill="both", padx=10, pady=10)

        small_font = customtkinter.CTkFont(family="Arial", size=5)

        # After creating your CTkTable instance named 'table'
        # Hypothetical: loop through all cells if accessible
        for (row, col), button in table.frame.items():
            button.configure(font=small_font)

        # self.display_frame = customtkinter.CTkFrame(master=self.master)
        # self.display_frame.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def back(self):
        self.grid_forget()

    def show_pending_requests(self):
        """
        Query pending user requests and return results in format compatible with CTkTable.
        Returns a tuple of (column_names, data_rows) or (None, []) if no matches/errors.
        """
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                
                # Get pending users (verified = 'PENDING')
                cursor.execute("""
                    SELECT id, username, email, contact, join_date 
                    FROM users 
                    WHERE verified = 'PENDING'
                    ORDER BY join_date ASC
                """)
                
                pending_users = cursor.fetchall()
                
                if not pending_users:
                    return None, []
                
                # Define column names for CTkTable display
                column_names = ['ID', 'Username', 'Email', 'Contact', 'Join Date']
                
                # Format data rows for CTkTable
                data_rows = []
                for user in pending_users:
                    user_id = str(user[0]) if user[0] is not None else ''
                    username = str(user[1]) if user[1] is not None else ''
                    email = str(user[2]) if user[2] is not None else ''
                    contact = str(user[3]) if user[3] is not None else ''
                    join_date = str(user[4]) if user[4] is not None else ''
                    
                    data_rows.append([
                        user_id,
                        username,
                        email,
                        contact,
                        join_date
                    ])
                
                print(f"📋 Found {len(data_rows)} pending user requests")
                
                return column_names, data_rows
        
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return None, []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None, []

    def approve_user_verification(self, username):
        """
        Set verified='YES' where username matches and current verified='PENDING'.
        Returns True if update succeeded, False or None if user not found or error.
        """
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()

                # Update verified to YES for matching username if currently PENDING
                cursor.execute("""
                    UPDATE users
                    SET verified = 'YES'
                    WHERE username = ? AND verified = 'PENDING'
                """, (username,))

                conn.commit()

                if cursor.rowcount == 0:
                    print(f"User '{username}' not found or not pending verification.")
                    return False

                print(f"User '{username}' verified successfully.")
                return True

        except sqlite3.Error as e:
            print(f"Database error during verification update: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during verification update: {e}")
            return False

    def submit_action(self):
        self.approve_user_verification(self.user_entry.get())

# Pending Submissions Frame
class Pending_submissions_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure(1, weight=1)

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.show_button = customtkinter.CTkButton(self, text="Show Overdue Book", command=self.show_action)
        self.show_button.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="sew")

    def back(self):
        self.grid_forget()

    def get_overdue_borrowed_books(self):
        """
        Fetch users with borrowed books overdue by more than 7 days and approved_book = 'YES'.
        Returns tuple: (column_names, data_rows) or (None, []) on no data or error.
        """
        try:
            with sqlite3.connect('library.db') as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # SQLite query using julianday for date difference
                cursor.execute("""
                    SELECT id, username, email, contact, join_date, borrowed_book_id, borrowed_book_date, approved_book
                    FROM users
                    WHERE borrowed_book_id != 'NIL'
                    AND approved_book = 'YES'
                    AND julianday('now') - julianday(borrowed_book_date) > 7
                    ORDER BY borrowed_book_date ASC
                """)
                rows = cursor.fetchall()

                if not rows:
                    return None, []
                
                column_names = rows[0].keys()
                data_rows = []
                for row in rows:
                    data_rows.append([row[col] if row[col] is not None else "" for col in column_names])

                return list(column_names), data_rows

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None, []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, []

    def show_action(self):
        column_names, data_rows = self.get_overdue_borrowed_books()

        # print(self.books)

        if not data_rows:
            customtkinter.CTkMessagebox.show_info("No Books", "No books found matching the filters.")
            return

        # Compose table values: first row for headers, following for data
        values = [column_names] + [list(map(str, row)) for row in data_rows]

        # Open new CTkToplevel
        result_win = customtkinter.CTkToplevel(self)
        result_win.geometry("2400x1300")
        result_win.title("Overdue Books Table")
        
        # Create scrollable frame in the toplevel window
        scrollable_frame = customtkinter.CTkScrollableFrame(result_win)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the table inside the scrollable frame
        table = CTkTable(
            master=scrollable_frame,
            row=len(values),
            column=len(column_names),
            values=values,
        )
        # # Create the table: plus one row for header, as many columns as there are headers
        # table.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        table.pack(expand=True, fill="both", padx=10, pady=10)

        small_font = customtkinter.CTkFont(family="Arial", size=5)

        # After creating your CTkTable instance named 'table'
        # Hypothetical: loop through all cells if accessible
        for (row, col), button in table.frame.items():
            button.configure(font=small_font)

# Submit Book Frame
class Submit_book_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4), weight=1)

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Book ID input
        book_id_label = customtkinter.CTkLabel(self, text="Book id:")
        book_id_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")  # left align label

        self.book_id_entry = customtkinter.CTkEntry(self, placeholder_text="Enter book id")
        self.book_id_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 5), sticky="ew")

        # Submit button
        self.submit_button = customtkinter.CTkButton(self, text="Submit Book", command=self.submit_action)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

    def back(self):
        self.grid_forget()

    def return_borrowed_book(self, book_id):
        """
        Return a book by setting user's borrowed_book_id to 'NIL', borrowed_book_date to 'NIL', 
        and approved_book to 'NO' where borrowed_book_id matches the given book_id.
        Returns True if update succeeded, False if no user found or error occurred.
        """
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                
                # Update user's record to return the book
                cursor.execute("""
                    UPDATE users
                    SET borrowed_book_id = 'NIL',
                        borrowed_book_date = 'NIL',
                        approved_book = 'NO'
                    WHERE borrowed_book_id = ? AND borrowed_book_id != 'NIL'
                """, (book_id,))
                
                conn.commit()
                
                if cursor.rowcount == 0:
                    print(f"Book ID '{book_id}' not found in any active borrowing record.")
                    return False
                
                print(f"Book ID '{book_id}' successfully returned. {cursor.rowcount} user record updated.")
                return 1
                
        except sqlite3.Error as e:
            print(f"Database error during book return: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during book return: {e}")
            return False

    def submit_action(self):
        book_id = self.book_id_entry.get()
        self.case = self.return_borrowed_book(book_id)

        if (self.case == 1):
            self.spacer.configure(text=f"Book {book_id} submission done")
        else:
            self.spacer.configure(text="Invalid Book id")

# Add Book Frame
class Add_book_frame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3,4,5,6,7,8,9,10), weight=1)  # Extended for more rows

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Book title
        title_label = customtkinter.CTkLabel(self, text="Book Title:")
        title_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")

        self.title_entry = customtkinter.CTkEntry(self, placeholder_text="Enter book title")
        self.title_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # Author
        author_label = customtkinter.CTkLabel(self, text="Author:")
        author_label.grid(row=3, column=0, padx=20, pady=(10,5), sticky="w")

        self.author_entry = customtkinter.CTkEntry(self, placeholder_text="Enter author name")
        self.author_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # ISBN
        isbn_label = customtkinter.CTkLabel(self, text="ISBN:")
        isbn_label.grid(row=5, column=0, padx=20, pady=(10,5), sticky="w")

        self.isbn_entry = customtkinter.CTkEntry(self, placeholder_text="Enter ISBN")
        self.isbn_entry.grid(row=6, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # Genre - Using CTkOptionMenu for predefined options
        genre_label = customtkinter.CTkLabel(self, text="Genre:")
        genre_label.grid(row=7, column=0, padx=20, pady=(10,5), sticky="w")

        # Common book genres as predefined options
        genres = ["Biography", "Fantasy", "Fiction", "History", "Mystery", 
                 "Non-fiction", "Romance", "Science", "Self-Help", "Technology", "Other"]
        
        self.genre_var = customtkinter.StringVar(value="Fiction")  # Default genre
        self.genre_option = customtkinter.CTkOptionMenu(
            self, 
            values=genres, 
            variable=self.genre_var,
            width=200
        )
        self.genre_option.grid(row=8, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # Quantity - Numeric input
        quantity_label = customtkinter.CTkLabel(self, text="Quantity:")
        quantity_label.grid(row=9, column=0, padx=20, pady=(10,5), sticky="w")

        self.quantity_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Quantity")
        self.quantity_entry.grid(row=10, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # Add button
        self.add_button = customtkinter.CTkButton(self, text="Add Book", command=self.add_action)
        self.add_button.grid(row=11, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    def back(self):
        self.grid_forget()

    def add_book(self, title, author, isbn, genre, quantity):
        conn = None
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            if not title:
                print("Title cannot be empty!")
                return False

            if not author:
                print("❌ Author cannot be empty!")
                return False

            if not genre:
                print("❌ Genre cannot be empty!")
                return False

            if isbn:
                cursor.execute("SELECT id FROM books WHERE isbn = ?", (isbn,))
                if cursor.fetchone():
                    print("❌ ISBN already exists!")
                    return False
            else:
                isbn = None  # store NULL if no ISBN provided


            # Insert new book
            cursor.execute('''
                INSERT INTO books (title, available, genre, author, isbn, quantity)
                VALUES (?, 'YES', ?, ?, ?, ?)
            ''', (title, genre, author, isbn, quantity))

            conn.commit()

            print("✅ Book added successfully!")
            print(f"📖 Title: {title}")
            print(f"✍️  Author: {author}")
            print(f"🎯 Genre: {genre}")
            print(f"📦 Quantity: {quantity}")
            if isbn:
                print(f"🆔 ISBN: {isbn}")

            return 1

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: books.isbn" in str(e):
                print("❌ ISBN already exists!")
            else:
                print(f"❌ IntegrityError: {e}")
        except ValueError:
            print("❌ Invalid quantity! Must be a positive integer.")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if conn:
                conn.close()

    def add_action(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        genre = self.genre_var.get()
        quantity = self.quantity_entry.get()

        self.case = self.add_book(title, author, isbn, author, quantity)

        if (self.case == 1):
            self.spacer.configure(text=f"Book '{title}' by {author} added successfully")
        else:
            self.spacer.configure(text="Invalid Credentials")

# Delete Book Frame
class Delete_book_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable to fill space
        self.grid_columnconfigure(1, weight=0)  # Button column fixed width
        self.grid_rowconfigure((1,2,3), weight=1)

        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=0, column=0, sticky="ew")
        self.spacer.configure(font=customtkinter.CTkFont(size=10, weight="bold"), text_color="yellow")

        self.back_button = customtkinter.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Book ID
        book_id_label = customtkinter.CTkLabel(self, text="Book id to delete:")
        book_id_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")

        self.book_id_entry = customtkinter.CTkEntry(self, placeholder_text="Enter book id")
        self.book_id_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")

        # Delete button
        self.delete_button = customtkinter.CTkButton(self, text="Delete Book", command=self.delete_action)
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        self.show_button = customtkinter.CTkButton(self, text="Show All Book", command=self.show_action)
        self.show_button.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    def back(self):
        self.grid_forget()

    def delete_action(self):
        book_id = self.book_id_entry.get()
        self.spacer.configure(text=f"Book ID {book_id} deleted successfully")
        print(f"Deleting book ID: {book_id}")

    def get_all_books(self):
        """
        Fetch all rows from the books table, including all columns,
        and returns a tuple (column_names, data_rows).
        Returns (None, []) if no data or on error.
        """
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enables access by column name
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM books ORDER BY genre ASC, title ASC")
                rows = cursor.fetchall()
                
                if not rows:
                    return None, []
                
                # Get column names from cursor description or row keys
                column_names = rows[0].keys() if rows else []
                
                # Convert rows to list of lists (compatible with CTkTable)
                data_rows = []
                for row in rows:
                    data_rows.append([row[col] if row[col] is not None else "" for col in column_names])
                
                return list(column_names), data_rows
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None, []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, []

    def show_action(self):
        
        column_names, data_rows = self.get_all_books()

        # print(self.books)

        if not data_rows:
            customtkinter.CTkMessagebox.show_info("No Books", "No books found matching the filters.")
            return

        # Compose table values: first row for headers, following for data
        values = [column_names] + [list(map(str, row)) for row in data_rows]

        # Open new CTkToplevel
        result_win = customtkinter.CTkToplevel(self)
        result_win.geometry("2400x1300")
        result_win.title("All Books Table")
        
        # Create scrollable frame in the toplevel window
        scrollable_frame = customtkinter.CTkScrollableFrame(result_win)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the table inside the scrollable frame
        table = CTkTable(
            master=scrollable_frame,
            row=len(values),
            column=len(column_names),
            values=values,
        )
        # # Create the table: plus one row for header, as many columns as there are headers
        # table.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        table.pack(expand=True, fill="both", padx=10, pady=10)

        small_font = customtkinter.CTkFont(family="Arial", size=5)

        # After creating your CTkTable instance named 'table'
        # Hypothetical: loop through all cells if accessible
        for (row, col), button in table.frame.items():
            button.configure(font=small_font)
    

class Admin_user_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)  # Extended for more buttons
        
        self.pending_requests_button = customtkinter.CTkButton(self, text="Pending Requests", 
                                                               command=self.pending_requests)
        self.pending_requests_button.grid(row=0, column=0, padx=10, pady=(10, 5))

        self.pending_submissions_button = customtkinter.CTkButton(self, text="Pending Submissions", 
                                                                  command=self.pending_submissions)
        self.pending_submissions_button.grid(row=1, column=0, padx=10, pady=(5, 5))

        self.submit_book_button = customtkinter.CTkButton(self, text="Submit Book", 
                                                          command=self.submit_book)
        self.submit_book_button.grid(row=2, column=0, padx=10, pady=(5, 5))

        self.add_book_button = customtkinter.CTkButton(self, text="Add Book", 
                                                       command=self.add_book)
        self.add_book_button.grid(row=3, column=0, padx=10, pady=(5, 5))

        self.delete_book_button = customtkinter.CTkButton(self, text="Delete Book", 
                                                          command=self.delete_book)
        self.delete_book_button.grid(row=4, column=0, padx=10, pady=(5, 10))

        # Initialize all frames
        self.pending_requests_frame = Pending_requests_frame(self.master)
        self.pending_submissions_frame = Pending_submissions_frame(self.master)
        self.submit_book_frame = Submit_book_frame(self.master)
        self.add_book_frame = Add_book_frame(self.master)
        self.delete_book_frame = Delete_book_frame(self.master)

    # Frame switching methods
    def pending_requests(self):
        self.pending_requests_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def pending_submissions(self):
        self.pending_submissions_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def submit_book(self):
        self.submit_book_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def add_book(self):
        self.add_book_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

    def delete_book(self):
        self.delete_book_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_path='library.db'

        self.title("Library Management System")
        self.geometry("2400x1200")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.log_in_frame = Log_in_frame(self)
        self.log_in_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")

        self.toplevel_window = None

    def hello(self):
        print("hello")

    # # def open_toplevel(self):
    #     # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
    #     self.toplevel_window = Log_in_window(self)  # create window if its None or destroyed
    #     # else:
    #     self.toplevel_window.focus()  # if window exists focus it
    

app = App()
app.mainloop()

