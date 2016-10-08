# django-scaffold


ENDPOINTS

# Course
- To add a course do the following
    - POST 'course/'
        - Send the following data
            - ```
            'instructor_Id, description, name'
            ```
        - Expected ouput 
        ```
        {
          "Students": [
            1,
            2,
            5
          ],
          "Description": "depressing class",
          "Class Identifier": "d28dde2",
          "Instructor": 7,
          "Name": "Cs1500"
        }
        ```
- To add a student to a course do the following
    - POST 'add_to_course/'
        - Send the following data
            - ```
            'course_id, student_id'
            ```
        - Example ouput 
        ```
        {
          "Students": [
            1,
            2,
            5
          ],
          "Description": "depressing class",
          "Class Identifier": "d28dde2",
          "Instructor": 7,
          "Name": "Cs1500"
        }
        ```