# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

# Adds a new user to the user.txt file
def reg_user(new_username):        
        # Loops if passwords do not match
        while True:
            # Request input of a new password
            new_password = input("New Password: ")
            # Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # If they are the same, add them to the user.txt file
                print("New user added")
                username_password[new_username] = new_password
                break
            # Otherwise you present a relevant message.
            else:
                print("Passwords do no match")    

        # Stores data added by user to user.txt file        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

# Adds a new task to task.txt file
def add_task():
    counter = 0
    # Loops until a valid username has been entered
    while True:
        counter += 1
        task_username = input("Name of user assigned to task: ")
        if task_username in username_password.keys():
            break
        else:
            print("User does not exist. Please enter a valid username")
            if counter >= 2:
                # Loops if user enters a character other than 'y' or 'n'
                while True:
                    add_new_user = input('''Y = Yes \nN = No \n\
Would you like to register a new user? ''').lower()
                    if add_new_user == 'y':
                        new_username = input("New Username: ")
                        # Loops if user enters a username that already exists
                        while True:
                            with open('user.txt', 'r') as user_check:
                                if new_username not in user_check.read():
                                    break
                                else:
                                    new_username = input("This username already exists. Please enter a different username: ")
                        # Call function to register new user
                        reg_user(new_username)
                        # Autofills task username if new user registered
                        task_username = new_username
                        return
                    elif add_new_user == 'n':
                        break
                    else:
                        print("Invalid input")
    task_title = input("Title of task: ")
    task_description = input("Description of task: ")
    # Loops until a valid datetime format has been entered
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        # Custom message for error, preventing crash
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Gets the current date.
    curr_date = date.today()
    # Compiles the data as a new task and marks the task as incomplete
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Adds new task to the list of all tasks
    task_list.append(new_task)
    # Writes the new task to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

# View all tasks listed in tasks.txt
def view_all():
        # Reads each task from task.txt file
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            disp_str += f"Task Description: \n{t['description']}\n"
            # Prints each task with information in an easy to read format
            print(disp_str)

# View all tasks listed in tasks.txt assigned to current user
def view_mine():
    # If no tasks are assigned to user, task numbers list remains empty
    task_numbers = []
    # Reads each task from task.txt file, changing value of 'i'
    for i, t in enumerate(task_list, 1):
        # Sorts all tasks assigned to current user only
        if t['username'] == curr_user:
            task_numbers += str(i)
            disp_str = f"Task Number: \t\t {i}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            disp_str += f"Task Description: \n{t['description']}\n"
            # Prints each task with information in an easy to read format
            print(disp_str)
    # If list of task numbers remains unchanged, no tasks available
    if task_numbers == []:
        # Returns user to main menu
        print("User has no tasks assigned to them.")
        return
    
    while True:        
        try:
            # Select task to edit and gives option to return to menu
            task_number = input('''Which task would you like to edit? \n\
Please enter Task Number only or enter "-1" to return to main menu: ''')
            if task_number in task_numbers:
                task_number = int(task_number)
                break
            elif task_number == '-1':
                print("Returning to main menu")
                return
            else:
                print("Please select a valid task\n")
                continue
    # Handles error if a number is not entered
        except ValueError:
            print("Please enter the number only")
    
    # Loops through all tasks
    for j, t in enumerate(task_list, 1):
        # Once the task entered by the user is found in the loop
        if j == task_number:
            # If task is already completed, returns to menu
            if t['completed'] == True:
                print("Unable to edit, task already completed")
                return
            
            # Used to prevent looping once edit is complete
            amend = False
            # Loops for invalid input by user           
            while not amend:        
                while True:
                    try:
                        # Allows user to choose what they would like to edit
                        edit_option = input('''1 - Mark task as complete \n\
2 - Edit the task \nEnter number only for the option you would like: ''')
                        edit_option = int(edit_option)
                        break
                    # Handles error if a number is not entered
                    except ValueError:
                        print("Please enter the number only")

                if edit_option == 1:
                    # Performs the change requested by the user
                    t['completed'] = "Yes"
                    break
                
                elif edit_option == 2:
                    # Loops for invalid input
                    # Used to prevent looping once edit is complete
                    while not amend:
                        while True:
                            try:
                                # Gives the user an option for what to edit
                                edit_task = input('''1 - Username \n2 - Due Date
Enter number only for the option you would like: ''')
                                edit_task = int(edit_task)
                                break
                            except ValueError:
                                print("Please enter the number only")
                        
                        if edit_task == 1:
                            # Loops until valid username is entered
                            while True:
                                username_change = input('''Enter username to \
be assigned to current task: ''')
                                # Checks if username entered exists
                                if username_change in username_password.keys():
                                    break
                                else:
                                    print('''User does not exist. \
Please enter a valid username\n''')
                            # Performs change requested by the user
                            t['username'] = username_change
                            # Breaks loops allowing changes to be written to text file
                            amend = True
                            break
                        
                        elif edit_task == 2:
                            # Loops until a valid datetime format has been entered
                            while True:
                                try:
                                    task_due_date = input("Enter new due date (YYYY-MM-DD): ")
                                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                                    t['due_date'] = due_date_time
                                    # Breaks loops allowing changes to be written to text file
                                    amend = True
                                    break
                                # Custom message for error, preventing crash
                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")
                        else:
                            print("Please select a valid option\n")
                else:
                    print("Please select a valid option\n")

            # Writes the updated task to tasks.txt
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
                print("Task successfully edited")
                return

def generate_reports():
    # Generate Task Overview
    total_tasks = len(task_list)
    # Each variable will be updated with a total once loop is finished
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    
    # Loops through every task.
    for t in task_list:
        # If completed, plus 1 to the count
        if t['completed'] == True:
            completed_tasks += 1
        # If not completed and past due date, plus 1 to count
        elif t['due_date'] < datetime.now():
            overdue_tasks += 1
        # If not completed, plus 1 to count
        else:
            uncompleted_tasks += 1
    
    # Error handled if trying to divide zero
    try:
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100
    except ZeroDivisionError:
        incomplete_percentage = 0
        overdue_percentage = 0

    # Write overview of tasks in an easy to read manner
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(f'''{"-" * 40}
Total Tasks: {total_tasks}
Completed Tasks: {completed_tasks}
Uncompleted Tasks: {uncompleted_tasks}
Overdue Tasks: {overdue_tasks}
Incomplete Percentage: {round(incomplete_percentage, 2)}%
Overdue Percentage: {round(overdue_percentage, 2)}%
{"-" * 40}\n''')

    # Generate User Overview
    total_users = len(user_data)
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(f'''Total Users: {total_users}
Total Tasks: {total_tasks}
{"-" * 40}\n''')
        
        # Loops through each user
        for user in user_data:
            username_only = user.split(';')[0]
            assigned = 0
            completed = 0
            incomplete = 0
            overdue = 0
            
            # For each user, loops through every task
            for t in task_list:
                if t['username'] == username_only:
                    assigned += 1
                    # If completed, plus 1 to the count
                    if t['completed'] == True:
                        completed += 1
                    # If not completed and past due date, plus 1 to count
                    elif t['due_date'] < datetime.now():
                        overdue += 1
                    # If not completed, plus 1 to count
                    else:
                        incomplete += 1
            
            # Error handled if trying to divide zero
            try:
                user_assigned_percent = (assigned / total_tasks) * 100
                user_completed_percent = (completed / assigned) * 100
                user_incomplete_percent = (incomplete / assigned) * 100
                user_overdue_percent = (overdue / assigned) * 100
            except ZeroDivisionError:
                user_assigned_percent = 0
                user_completed_percent = 0
                user_incomplete_percent = 0
                user_overdue_percent = 0
 
            # Write overview of users in an easy to read manner
            user_overview.write(f'''User: {username_only}
Tasks Assigned: {assigned}
Tasks Assigned Percentage: {round(user_assigned_percent, 2)}%
Completed Percentage: {round(user_completed_percent, 2)}%
Incomplete Percentage: {round(user_incomplete_percent, 2)}%
Overdue Percentage: {round(user_overdue_percent, 2)}%
{"-" * 40}\n''')
    
    print("Reports generated")

def display_statistics():
    # Checks if reports have been generated, if not, generates them
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()
    
    # Displays the contents of task_overview file
    with open("task_overview.txt", "r") as display_task_overview:
        print(f"Task Overview:\n{display_task_overview.read()}")

    # Displays the contents of user_overview file
    with open("user_overview.txt", "r") as display_user_overview:
        print(f"User Overview:\n{display_user_overview.read()}")

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Admin has more options available
if curr_user == 'admin':
    while True:
        '''Presenting the menu to the user and making sure
        that the user input is converted to lower case'''
        print()
        menu = input('''Select one of the following options below:
r  - Register a new user
a  - Add a new task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e  - Exit
: ''').lower()

        if menu == 'r':
            new_username = input("New Username: ")
            # Loops if user enters a username that already exists
            while True:
                with open('user.txt', 'r') as user_check:
                    if new_username not in user_check.read():
                        break
                    else:
                        new_username = input("This username already exists. Please enter a different username")
            reg_user(new_username)

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()
        
        elif menu == 'gr':
            generate_reports()

        elif menu == 'ds': 
            display_statistics() 

        elif menu == 'e':
            print('Goodbye, have a nice day!')
            exit()

        else:
            print("Incorrect input, please select a valid option")
# If user is not admin, they have less options available
else:
    while True:
        '''Presenting the menu to the user and making sure
        that the user input is converted to lower case'''
        print()
        menu = input('''Select one of the following options below:
r  - Register a new user
a  - Add a new task
va - View all tasks
vm - View my tasks
gr - Generate reports
e  - Exit
: ''').lower()

        if menu == 'r':
            new_username = input("New Username: ")
            # Loops if user enters a username that already exists
            while True:
                with open('user.txt', 'r') as user_check:
                    if new_username not in user_check.read():
                        break
                    else:
                        new_username = input("This username already exists. Please enter a different username")
            reg_user(new_username)

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()

        elif menu == 'gr':
            generate_reports()

        elif menu == 'e':
            print('Goodbye, have a nice day!')
            exit()

        else:
            print("Incorrect input, please select a valid option")
