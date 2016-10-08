# django-scaffold


ENDPOINTS

# User
- To add a user do the following
    - POST 'users/'
        - Include the following
        ```
            username, email, password, name
        ```
    - Expected Output
        ```
            {
              "email": "cheese@burdger.com",
              "id": 8,
              "username": "Cheeseburgerddd",
              "teaches": [],
              "courses": []
            }
        ```
 To get all users do the following
    - GET 'users/'

    - Expected Output
        ```
            {
  "Users": [
    {
      "username": "Cheeseburgers3",
      "id": 3,
      "email": "cheese@burgs2er.com",
      "courses": [],
      "teaches": []
    },
    {
      "username": "Cheeseburgers43",
      "id": 4,
      "email": "chez@bur.com",
      "courses": [],
      "teaches": []
    },
    {
      "username": "Cheesebur3gers",
      "id": 5,
      "email": "chez@bu2r.com",
      "courses": [],
      "teaches": []
    },
    {
      "username": "Chebur3gers",
      "id": 6,
      "email": "chez@bu2123r.com",
      "courses": [],
      "teaches": []
    },
    {
      "username": "teacher",
      "id": 7,
      "email": "tea@ch.com",
      "courses": [],
      "teaches": [
        4
      ]
    },
    {
      "username": "Cheeseburgerddd",
      "id": 8,
      "email": "cheese@burdger.com",
      "courses": [],
      "teaches": []
    }
  ]
}
        ```
- To delete a user do the following
    - DELETE 'users/'
        - Include the following
        ```
            id
        ```
    - Expected Output
        ```
            {
              "Message" : "User Deleted"
            }
        ```

- To get a user from an id 
    - POST 'user/'
        - Include the following
        ```
            id
        ```
    - Expected output
        ```
        {
          "email": "cheese@burdger.com",
          "id": 8,
          "username": "Cheeseburgerddd",
          "teaches": [],
          "courses": []
        }
        ```

- To Login a user do the following
    - POST 'login_user/'
        - Include the following
        ```
        username, password
        ```
        - Expected Response
        ```
        {
          "email": "cheese@burdger.com",
          "id": 8,
          "username": "Cheeseburgerddd",
          "teaches": [],
          "courses": []
        }
        ```

# Course
- To add a course do the following
    - POST 'course/'
        - Send the following data
            - 
            ```
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
          "Name": "Cs1500",
          'id' : 3
        }
        ```
- To get all courses do the following
    - GET 'course/'
        - Expected ouput 
        ```
        {
  "Courses": [
    {
      "Name": "CS1555",
      "Students": [],
      "id": 4,
      "Instructor": 7,
      "Description": "dontdie",
      "Chapters": [
        2
      ],
      "Class Identifier": "35fe9e4"
    }
  ]
}
        ```
- To delete a course
    - DELETE 'course/'
        - Send 
        ```
        course_id
        ```
        - Expected Output 
        ```
            {
              "Message": "Course Deleted"
            }
        ```
- To add a student to a course do the following
    - POST 'add_to_course/'
        - Send the following data
            - 
            ```
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
          "Name": "Cs1500",
          'id' : 3
        }
        ```
- To remove a student from a course do the following
    - POST 'remove_from_course/'
        - Send the following data
            - 
            ```
            'course_id, student_id'
            ```
        - Example ouput 
        ```
        {
          "Students": [
            2,
            5
          ],
          "Description": "depressing class",
          "Class Identifier": "d28dde2",
          "Instructor": 7,
          "Name": "Cs1500",
          'id' : 3
        }
        ```
- To get a course from id
    - POST 'course_from_id/'
        - Send the following data
        ```
            course_id
        ```
    - Expected Output 
    ```
        {
          "Students": [
            2,
            5
          ],
          "Description": "depressing class",
          "Class Identifier": "d28dde2",
          "Instructor": 7,
          "Name": "Cs1500",
          'id' : 3
        }
    ```
- To get a course from a user id
    - POST `courses_for_user/`
        - Send
        ```
            user_id
        ```
        - Expected response
        ```
{
  "Teaches": [
    {
      "Class Identifier": "6114824",
      "qrcode": "http://api.batterystapler.com/media/6114824.png",
      "Students": [],
      "Chapters": [],
      "Name": "Cs hates us",
      "Description": "LIke it realllly hates us",
      "id": 4,
      "Instructor": 6
    },
    {
      "Class Identifier": "5d72b32",
      "qrcode": "http://api.batterystapler.com/media/5d72b32.png",
      "Students": [],
      "Chapters": [],
      "Name": "Lets do it",
      "Description": "Horrible times",
      "id": 2,
      "Instructor": 6
    },
    {
      "Class Identifier": "c0b4f63",
      "qrcode": "http://api.batterystapler.com/media/c0b4f63.png",
      "Students": [],
      "Chapters": [],
      "Name": "This is where we panic a lot.",
      "Description": "Badtimes",
      "id": 1,
      "Instructor": 6
    }
  ],
  "Courses": []

        ```

# Chapter

- To add a Chapter 
    - POST 'chapter/'
        - Semd the following data
        ```
            course_id, description, name
        ```
    - Expect Response
    ```
{
  "Description": "real bad for you.",
  "Name": "Math is bad",
  "order": 1,
  "id": 2,
  "stapls": [],
  "course_id": 4
}

    ```
- To get all chapters
    - GET 'chapter/'
    -Expect Response
```
{
  "Chapters": [
    {
      "course_id": 4,
      "Description": "real bad for you.",
      "Name": "Math is bad",
      "stapls": [],
      "id": 2,
      "order": 1
    }
  ]
}

- To get Chapter from Id
    - POST 'chapter_from_id/'
        - Send
        ```
        chapter_id
        ```
    - Expected response
    ```
    {
  "course_id": 4,
  "order": 1,
  "stapls": [],
  "Description": "real bad for you.",
  "id": 2,
  "Name": "Math is bad"
}
```
- To delete a Chapter   
    - DELETE 'chapter/'
    - Send 
        ```
        chapter_id
        ```
        - Expected Output 
        ```
            {
              "Message": "chapter Deleted"
            }
        ```

- Get all chapters for course
    - Send 'chapter_from_course/'
        - POST
        ```
        'course_id'
        ```
    - Expected result
```
{
  "Chapters": [
    {
      "course_id": 4,
      "Description": "real bad for you.",
      "Name": "Math is bad",
      "stapls": [],
      "id": 2,
      "order": 1
    }
  ]
}
```

- To get Chapter from course
    - POST 'chapter_from_course/'
        - Send
        ```
        course_id
        ```
    - Expected response
    ```
{
  "Chapters": [
    {
      "course_id": 4,
      "Description": "real bad for you.",
      "Name": "Math is bad",
      "stapls": [],
      "id": 2,
      "order": 1
    }
  ]
}
```

# Stapls
- To get all Stapls
    - GET 'stapls/'
    - Expected Response
    ```
    {
  "Stapls": [
    {
      "options": [],
      "comments": [],
      "stapl_id": 2,
      "date_created": "2016-10-08T12:12:25.138161Z",
      "Chapter_id": 2,
      "Responses": [],
      "user_id": 7
    }
  ]
}
    ```
- To delete a Stapl
    - DELETE 'stapls/'
    - Send
    ```
        stapl_id
    ```
    - Expected Response 
    ```
    {
    "Message": "Stapl Deleted"
    }
    ```
To add a poll
    - POST 'poll_from_chapter/'
        - Send
        ```
        chapter_id, options, user_id
        ```
        - You can send multiple options by sending "options": "item", "options": "item"
        - Expected Response
        ```
{
  "date_created": "2016-10-08T12:28:30.156131Z",
  "stapl_id": 8,
  "Chapter_id": 2,
  "Responses": [],
  "comments": [],
  "user_id": 7,
  "options": [
    [
      43,
      "Yellow , Blue,  Jay"
    ],
    [
      44,
      "Red green"
    ]
  ]
}
        ```
To set a poll to inactive
    - POST 'poll_inactive/'
        - Send
        ```
        stapl_id
        ```
        - Expected Response
        ```
        {
        "Message" : "Sucessfully set poll to inactive"
        }
        ```
To get percentages of a poll
    - POST 'poll_results/'
        - Send
        ```
            stapl_id
        ```
        - Expected Results
        ```
{
  "results": [
    [
      43,
      "Yellow , Blue,  Jay",
      100
    ],
    [
      44,
      "Red green",
      0
    ]
  ]
}
        ```

To answer a poll.
    - POST 'answer_poll/'
        - Send
        ```
        user_id, option_id, stapl_id
        ```
        - Expected results
        ```
            {
              "user_id": 7,
              "poll_id": 8,
              "option_id": 43
            }
        ```


To add a note
    - POST 'note_from_chapter/'
        - Send
        ```
        chapter_id, request.files['upload'] (NAME IT WITH UPLOAD FOR SENDING), user_id
        ```
        - You can send multiple options by sending "options": "item", "options": "item"
        - Expected Response
        ```
{
  "date_created": "2016-10-08T12:55:34.186586Z",
  "comments": [],
  "user_id": 7,
  "filepath": "media/cheesebuger/sep21.pdf",
  "Chapter_id": 2,
  "stapl_id": 9
}
        ```


To add a deck
    - POST 'deck_from_chapter/'
        - Send
        ```
        chapter_id, user_id
        ```
        - You can send multiple options by sending "options": "item", "options": "item"
        - Expected Response
        ```
{
  "date_created": "2016-10-08T12:55:34.186586Z",
  "comments": [],
  "user_id": 7,
  "text": "Yellow , Blue,  Jay, please dont hurt me im in absolute agony.",
  "Chapter_id": 2,
  "stapl_id": 9
}
        ```

To add a flashcard
    - Post 'flashcard_from_deck'
        - Send
        ```
            front, back, deck_id, user_id
        ```
        - Expected Response
        ```
{
  "id": 2,
  "user_id": 6,
  "back": "correct",
  "front": "I DONT LIKE LIVING"
}
        ```
To remove a FlashCard
    - DELETE 'remove_flashcard/'
        - Send
        ```
        flashcard_id
        ```
        - Expected Response
        ```
        {"Message": "FlashCard was removed"}
        ```

To add a comment
    - POST 'create_comment/'
        - Send 
        ```
            comment, user_id, stapl_id
        ```
        - Expected Response
        ```
        {
  "text": "I really hate you so much at this moment.",
  "date_created": "2016-10-08T13:21:52.466934Z",
  "user_id": 7,
  "stapl_id": 11
}
```

To get all comments for a stapl
    - POST 'comments_for_stapl/'
        - Send
        ```
        stapl_id
        ```
        - Expected Response
        ```
        {
  "Comments": [
    {
      "text": "I really hate you so much at this moment.",
      "user_id": 7,
      "date_created": "2016-10-08T13:21:52.466934Z",
      "stapl_id": 11
    }
  ]
}

```


# QRCODE AND CLASS IDENTIFIER
- To get Course ID from QRCode Image
    - POST 'decode_qr/'
        - Send
        ```
            request.files['upload']
        ```
        - Expected Response
        ```
        {"Message": 1}
        ```

- To get Course ID from class_identifier
    - POST 'decode_qr/'
        - Send
        ```
            class_identifier
        ```
        - Expected Response
        ```
        {"Message": 1}
        ```
