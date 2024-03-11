'''User Management System

This program provides functionalities for user registration, task assignment, task management, and report generation. 
It allows users to register, add tasks, view tasks, edit tasks, and generate reports. The program is secured with a login 
system. An admin user can access additional functionalities such as viewing all tasks, generating reports, and displaying statistics.

Notes:
1. Use the following username and password to access the admin rights
username: admin
password: password
2. Ensure you open the whole folder for this task in VS Code otherwise the
program will look in your root directory for the text files.
'''

#==== Importing Libraries ==========
import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#======= New User ================

def reg_user():
    '''Register a new user.
This function prompts the user to input a new username and password. 
It checks if the username already exists. If the password is confirmed,
it adds the user to the user.txt file.
'''
    # Request input of a new username
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return

    # Request input of a new password
    new_password = input("New Password: ")

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
            return

        # Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
        
#======= Add Tasks ================

def add_task():
    '''Add a new task.
This function prompts the user to input details of a new task, including
the username of the person assigned to the task, task title, task description,
 and due date. It saves the task details to the tasks.txt file.
'''
    # Input username to assign task
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    # Input task details included due due with datetime
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    # Try Except catch for incorrect date formatting
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Save task details as new_task variable
    curr_date = datetime.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Append new_task to task_list list
    task_list.append(new_task)

    # Open tasks.txt file - format task data and write task_file to tasks.txt
    with open("tasks.txt", "a") as task_file:
        str_attrs = [
            new_task['username'],
            new_task['title'],
            new_task['description'],
            new_task['due_date'].strftime(DATETIME_STRING_FORMAT),
            new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "No" if not new_task['completed'] else "Yes"
        ]
        # Use join function to change str_attrs list into string
        task_file.write("\n" + ";".join(str_attrs))
    print("Task successfully added.")

#======= View All ================

def view_all():
    '''View all tasks.

    This function displays all tasks assigned to users, including task details
    such as title, assigned user, due date, etc.
    '''
    # Use enumerate to print out task info for one task at a time
    for index, task in enumerate(task_list, 1):
        print(f"Task {index}:")
        print(f"Title: {task['title']}")
        print(f"Assigned to: {task['username']}")
        print(f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Description: {task['description']}")
        print(f"Completed: {'Yes' if task['completed'] else 'No'}")
        print()

#======= View Mine ================
        
def mark_task_complete(task_index):
    '''View tasks assigned to the current user.

    This function displays tasks assigned to the currently logged-in user.
    '''
    # If statement to find task's assigned number
    if 0 < task_index <= len(task_list):
        task = task_list[task_index - 1]
        if not task['completed']: 
            task['completed'] = True # If not, use Boolean to mark complete
            print("Task marked as complete successfully!")
        else:
            print("This task is already marked as complete.")
    else:
        print("Invalid task index.")

# Function to edit a task
def edit_task(task_index):
    if 0 < task_index <= len(task_list):
        task = task_list[task_index - 1] # Variable for task number
        if not task['completed']:
            field_to_edit = input("Enter 'username' to edit assigned username \
or 'due_date' to edit due date: ").lower() # Request input for field to edt
            if field_to_edit == 'username':
                new_username = input("Enter new username: ")
                task['username'] = new_username
                print("Username updated successfully!")
            elif field_to_edit == 'due_date':
                new_due_date_str = input("Enter new due date (YYYY-MM-DD): ")
                try: # Try except catch for incorrect date formatting
                    new_due_date = datetime.strptime(new_due_date_str, DATETIME_STRING_FORMAT)
                    task['due_date'] = new_due_date
                    print("Due date updated successfully!")
                except ValueError:
                    print("Invalid date format. Date should be in YYYY-MM-DD format.")
            else:
                print("Invalid field to edit.")
        else:
            print("Cannot edit a completed task.")
    else:
        print("Invalid task index.")

# Function to view specific user's task
def view_mine():
    # Enumerate through numbers to find all user's specific tasks
    for index, task in enumerate(task_list, 1):
        if task['username'] == curr_user:
            # Print task details for tasks where 'username' is = to current user
            print(f"Task {index}:")
            print(f"Title: {task['title']}")
            print(f"Assigned to: {task['username']}")
            print(f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Description: {task['description']}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print()

#======= Generate Reports ================

def generate_reports():
    '''Generate reports.

    This function generates reports on task overview and user overview,
    including total tasks, completed tasks, incomplete tasks, etc.
    '''
    # Variables for task data
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    # Check for tasks not completed if task due date is less than today's date
    overdue_tasks = sum(1 for task in task_list if not task['completed'] \
and task['due_date'] < datetime.today()) 
    # Percentage calculator for incomplete and overdue tasks
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Write function for opening task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        # Write task details to txt files
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # Write function for opening user_overview.txt
    with open("user_overview.txt", "w") as user_overview_file:
        # Write initial summary of total users and tasks to txt file
        user_overview_file.write(f"Total users: {len(username_password)}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")

        # Loop through each user and summarise task details
        for user, password in username_password.items():
            tasks_assigned_to_user = sum(1 for task in task_list if task['username'] == user)
            percentage_of_total_tasks = (tasks_assigned_to_user / total_tasks) * 100
            completed_tasks_by_user = sum(1 for task in task_list if \
task['username'] == user and task['completed'])
            percentage_completed = (completed_tasks_by_user / tasks_assigned_to_user) \
* 100 if tasks_assigned_to_user != 0 else 0
            percentage_incomplete = 100 - percentage_completed
            overdue_tasks_by_user = sum(1 for task in task_list if task['username'] == \
user and not task['completed'] and task['due_date'] < datetime.today())
            percentage_overdue = (overdue_tasks_by_user / tasks_assigned_to_user) * 100 \
if tasks_assigned_to_user != 0 else 0

            # Write user summaries to txt file
            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Tasks assigned: {tasks_assigned_to_user}\n")
            user_overview_file.write(f"Percentage of total tasks: {percentage_of_total_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage completed: {percentage_completed:.2f}%\n")
            user_overview_file.write(f"Percentage incomplete: {percentage_incomplete:.2f}%\n")
            user_overview_file.write(f"Percentage overdue: {percentage_overdue:.2f}%\n")

#======= Display Statistics ================

def display_statistics():
    '''Display statistics.

    This function displays statistics based on the generated reports.
    '''
    generate_reports()  # Generate reports if not already generated
    with open("task_overview.txt", "r") as task_overview_file:
        print("Task Overview:")
        print(task_overview_file.read())

    with open("user_overview.txt", "r") as user_overview_file:
        print("User Overview:")
        print(user_overview_file.read())

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

#==== Login Section =======
    
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

# Login - ask for admin logins if not already logged in
logged_in = False
while not logged_in:
        
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user in username_password.keys() and \
username_password[curr_user] == curr_pass:
        print("Login Successful!")
        logged_in = True
    else:
        print("Invalid username or password")

# If logged in display main menu
while True:
    print()
    menu = input('''Select one of the following options below:
    r - Registering a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    # If elif else to read user selection
    if menu == 'r':
            reg_user()
    elif menu == 'a':
            add_task()
    elif menu == 'va':
            view_all()
    elif menu == 'vm':
            view_mine()
            # Request user input for task number to edit
            task_choice = input("Enter a task number to select a task to edit \
(or -1 to return to the main menu): ")
            if task_choice == '-1':
                continue # -1 user selection to exit 'vm'
            else:
                task_choice = int(task_choice)
                action_choice = input("Enter 'complete' to mark the task as \
complete or 'edit' to edit the task: ").lower() # User input's action for task
                if action_choice == 'complete':
                    mark_task_complete(task_choice) # Utilise function
                elif action_choice == 'edit':
                    edit_task(task_choice) # Utilise edit_task function
                else:
                    print("Invalid choice.")
    elif menu == 'gr':
            print("\n")
            print("Reports successfully generated. Please see below:")
            print("-----------------------------------------------\n")
            generate_reports()
    elif menu == 'ds':
            print("\n")
            display_statistics() # Call function to generate on screen report
    elif menu == 'e':
        print('Goodbye!')
        exit() # Close main menu and end program
    else:
        print("You have made a wrong choice, Please Try again")