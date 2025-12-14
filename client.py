import requests
import sys

is_running = True 

def get_all_transcripts():
    response = requests.get('http://127.0.0.1:5000/all_transcripts')
        
    if response.status_code == 200:
        data = response.json()
    
    return data

def send_transcript(transcript):
    response = requests.post('http://127.0.0.1:5000/create', json=transcript)
    if response.status_code == 200:
        print("Status: Successful")
    else: 
        print(f"End Point has errored. Error Code:{response.status_code}")
    
    return response

while is_running: 
    print("1.View All Students\n" \
    "2.Choose Student  \n" \
    "3.Add Student \n" \
    "4.Edit Student\n" \
    "5.Exit")
    menu_item = int(input("Please enter a number for the task you want executed:"))

    # View all Students
    if menu_item == 1:
        
        all_transcripts = get_all_transcripts()
        
        print("\n--- All Students ---")
        for i in range(len(all_transcripts)):
            print(f"Student Name: {all_transcripts[i]["firstname"]} {all_transcripts[i]["lastname"]}")

    # Choose Student 
    elif menu_item == 2:
        student_selected = True
        
        student_id = int(input("Please enter a Student ID: \n"))
        
        while student_selected:
            get_transcript = requests.get(f'http://127.0.0.1:5000/transcript/{student_id}')
            
            if get_transcript.status_code == 200: 
                data = get_transcript.json()
                
                print("1.List Courses\n" \
                    "2.Check Status\n" \
                    "3.Back To Main Menu \n")
                
                student_menu_options = int(input("Please select what you wish to view: "))
                
                # Listing all courses
                if student_menu_options == 1:
                    print("\n--- Student Courses ---")
                    
                    for i in range(len(data["grades"])):
                        print(f"Course: {data["grades"][i]["course"]} Mark: {data["grades"][i]["mark"]}")
                
                # Checking the Status of Pass or Fail
                if student_menu_options == 2:
                    print("\n--- Student Status ---")

                    sum_grades = 0
                    length = len(data["grades"])

                    for i in range(length):
                        sum_grades += int(data["grades"][i]["mark"])
                    
                    avg_grade = int(sum_grades / length)
                    if avg_grade >= 50:
                        print("Passing, no worries here!")
                    elif avg_grade < 50:
                        print("Boo, do better!") 
                
                # Back to Main Menu
                if student_menu_options == 3:
                    student_selected = False
            
            # Inputting invalid ID
            else:
                print("This is not a valid transcript id")
                student_selected = False

    # Add/Edit Student
    elif menu_item == 3:
        # Adding a new student
        new_transcript = {}
        # generate id that increments the highest existing transcript by one
        all_transcripts = get_all_transcripts()
        
        biggest_id = 0
        # Finding the biggest id and add one, append to dictionary
        for transcript in all_transcripts:
            current_id = int(transcript["transcript_id"])

            if current_id > biggest_id:
                biggest_id = current_id
            
        new_transcript["transcript_id"] = str(biggest_id + 1)


        # Prompt for first name
        new_transcript["firstname"] = input("Please enter a first name: ").capitalize()
        # Prompt for last name
        new_transcript["lastname"] = input("Please enter a last name: ").capitalize()
        
        # Prompt for Courses (Min:2)
        inputting_courses = True
        minimum_courses = 0

        grades = []
        while inputting_courses: 
            
            new_course_grade = {}
            # Ask for course name
            new_course_grade["course"] = input("Please enter a course name: ")
            # Ask for course mark
            new_course_grade["mark"] = int(input("What mark is being achieved? "))
            minimum_courses += 1

            # Append Grades with Course Information
            grades.append(new_course_grade)

            if minimum_courses >= 2:
                finished_inputting_courses = input("Would you like to add another course? (Y/N) ").upper()
                
                if finished_inputting_courses == "N":
                    inputting_courses = False
            
        new_transcript["grades"] = grades
        
        # Send new_transcript to .json
        send_transcript(new_transcript)

    # Editing a Student 
    elif menu_item == 4:
        all_transcripts = get_all_transcripts()
        
        # Check the ID number 
        id_num = int(input("What is the ID number of the student you wish to update? "))
        student_profile = {}
        
        for student in all_transcripts:
            current_student = int(student["transcript_id"])

            if id_num == current_student:
                student_profile = student
        
        if not student_profile:
            print("This is not a existing student, please try again.")
                
        while student_profile:
            print(student_profile)

            print("\n" \
                "1.First Name\n" \
                "2.Last Name\n" \
                "3.Course Mark\n"
                "4.Add Course\n"
                "5.Main Menu\n")

            change_student_request = int(input("What would you like to change? "))

            # Changing First Name
            if change_student_request == 1:
                print("Changing First Name")
                student_profile["firstname"] = input("What is the new name? ").capitalize()
                send_transcript(student_profile)
            
            # Changing Last Name
            elif change_student_request == 2:
                print("Changing Last Name")
                student_profile["lastname"] = input("What is the new name? ").capitalize()
                send_transcript(student_profile)
                
            # Changing a Course Mark
            elif change_student_request == 3:
                print("Changing Course Mark")
                
                selected_course = input("What Course Mark would you like changed? ")
                found_course = False
                grades_index_number = 0
                editing_course_mark = 0

                for i in range(len(student_profile["grades"])):
                    if student_profile["grades"][i]["course"] == selected_course:
                        found_course = True
                        grades_index_number = i

                if found_course:
                    editing_course_mark = int(input("What is the new course mark? "))
                    student_profile["grades"][grades_index_number]["mark"] = editing_course_mark
                    # Send the changes
                    send_transcript(student_profile)
                else:
                    print("Course not found")
            
            # Adding a Course
            elif change_student_request == 4:
                new_course_grade = {}
                # Ask for course name
                new_course_grade["course"] = input("Please enter a course name: ")
                # Ask for course mark
                new_course_grade["mark"] = int(input("What mark is being achieved? "))
                student_profile["grades"].append(new_course_grade)
                # Send the changes
                send_transcript(student_profile)
            
            elif change_student_request == 5:
                break

    elif menu_item == 5:
        sys.exit()

    else:
        print("This is an invalid option, please try again.")

