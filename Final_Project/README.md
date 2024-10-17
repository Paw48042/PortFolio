# Kanban board

## Overview 
Refer to the requirement of the project 
>Your README.md file should be minimally multiple paragraphs in length, and should provide a comprehensive documentation of what you did and, if applicable, why you did it.

### What I did 

For the overview of the project, This final project is a Single page web application that focus on Task management for a small team. It’s use concept of a Kanban board. 
It's a single page application which have 3 columns, TODO, PROCESS and FINISHED. User can create task card on the TODO board which can assigned that task to other user. Whoever create the task can update or delete the task. 

### Why I did it? 

I'm work as a military. I create this to use as a task management web application to use in my unit, to track who responsible for the task, which task we have to do in the future, which task should be launched and which one we already finish. Since our organization can't afford to make everybody use Trello or microsoft team. I make one for my unit.

## Distinctiveness and complexity 
Refer to the requirement of the project 
>Your web application must be sufficiently distinct from the other projects in this course 

Here's why I believe that my project have distinctiveness and complex enough. 

- This project inspired by Task management web applications like trello and monday.com. Which I believe this doesn't match any of the previous project in the course. 
- The complexity of application is sure satisfied the requirements since it's using 3 models , User models, Task model, and Comment models.
- This project use Dajngo and Django rest framework for the backend, which I believe Django rest framework is not picked to be used in any of the prior projects
- For the front end complexity, This project used Django templates along with css, javascript. Also Bootstrap and animate.css for the animation. 
- This project is single page web application and there's only 1 project in the course, Mail. Since it's doesn't similar to the mail project. I believe it's Distinct from other project in the course. 


## Models 
Refer to the requirements, This  section will fall under 
> What’s contained in each file you created. 
and 
>Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.

There is 3 models using in the Kanban application. 
1. User model : This model is use to store user data. By extending AbstractUser class from Django. 
    1. I have also add role, to separates who is admin and who is just a member
    2. I've add company to group the user in the same company together, This will make the user can't assign task to another person from another  company 
    3. I've add profile picture.


2. Task model : This  model is use to  store task. the field will be 
    1. Task name : store the name of the task 
    2. Detail : store the detail of the task 
    3. Create Time: Store datetime right when the task is  create. 
    4. Create By : Store who is create the task
    5. Assigned : Store the data about who has been assigned to the task. 
    6. Status : Store task status, which will be, TODO, PROCESS, FINISH. 

3. Comment model : This model is use to  store comment made to the task. The field will be 
    1. author : Who write this comment 
    2. Task to Comment : which task the commenter commented 
    3. Comment : Comment details. 
    4. Create Time : The time comment is create 

## URLs (urls.py)

Refer to the requiremnet, This section will fall under 
>What’s contained in each file you created.

In urls.py there will be normal route, which render the page and API route, to get data from django rest framework 

- /register : This route will redirect user to the register page, user will have to input the company, Username, Email address, Password, Confirm Password, Firstname, Lastname and profile picture. 
- /login : This route will redirect user to the login page and ask user for username and password 
- /logout : This route will redirect user to the login page 
- / (index page) : This route will be render when user logged in to the system 
#### Task API
- api/get_task : This use to ```GET``` all the task that assigned to the user 
- api/get_one_task/< taskID > : this route will ```GET``` details of one specific task 
- api/get_user : this route will ```GET``` all the user in the same company 
- api/create_task : this route will create ```POST``` request to create a task 
- api/edit_tasks : this route will create ```PUT``` request to update the task 
- api/make_progress : this route will  create ```PUT``` request to update the status of the task (TODO, PROCESS, FINISH) 
- api/delete_task : this route will create ```DELETE``` request to delete the task 
#### User api
- api/update_role : this route will create ```PUT``` request to update user role 
- api/delete_user : this route will create ```DELETE``` request to delete user 

#### Comment API 
- api/get_comment/< taskID > : this route use to ```GET``` all comment that made to specific task 
- api/post_comment/< taskID > : This route use to make a ```POST``` request to post a comment to a specific task

## Front End (index.js)
Refer to the requirements, this topic will fall under  
>What’s contained in each file you created.
and 
>Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.

In index.js, all the features separates in functions. Each function do all the works such as 
- Fetch data 
- Add event listener 
- Load default page 


## Serializers (Serializers.py) 
Refer to the requirements, this topic will fall under  
>What’s contained in each file you created.

Unlike Django, Rest framework provide you a serializers class to work with. It works similarly like ```Forms``` and ```ModelForm```. All of the serializers create based on the need of use from ```api/views.py``` which use rest framework.

This file contains 
- ```TaskSerializers()```
- ```CreateTaskSerializer()```
- ```UserSerializer()```
- ```CommentSerializer()```
- ```GetCommentSerializer()```
- ```UpdateTaskSerializer()```
- ```EditTaskSerializer()```
- ```UpdateRoleSerializer()```

## File structure

This topic will falls under 
>What’s contained in each file you created.

The files created will describe into front end and backend part
- For the front end, the files create will be at the static, which will contains ```index.js```. This file will handle all the front end such as Fetching data, show page and hide page. these operation will be display on index.html files, for the authentication part will be on ```login.html``` and ```register.html``` 

- For the backend, authentications such as login, logout, register will be in ```Kanban/views.py ``` . This project separates the api part in the folder ```api/``` which will have another views.py that handle all the api such as ```get_task``` ```create_task``` and many more.
 
- ```Final_Project```
    - ```Kanban``` contains all the web application content
        - ```api``` contains all the api view using django rest framework
            - ```__init__.py``` empty file use to make django run this file when run ```python3 manage.py runserver```
            - ```views.py``` contains api views create using django rest framework.
        - ```static``` contains all static files
            - ```Kanban``` 
                - ```index.js``` contains all the front end functionality
                - ```styles.css``` contains all the customs style that not using bootstrap and animate.css
        - ```templates``` 
            - ```index.html``` contains all the prefill content for the single page application. this will be complete when using with javascript.
            - ```layout.html``` layout for reuse.
            - ```login.html``` login template
            - ```register.html``` register template
        - ```admin.py``` contains all the model that superuser want to see and manage in the admin page
        - ```apps.py``` auto create by django
        - ```forms.py``` Contains register form and login form.
        - ```models.py``` contains all the models in the project application.
        - ```serializers.py``` Django rest framework require to create serializers.py to serailize all the data and control, validate data whether input or output, this file will contains all the serializer that use with the api views create using django rest framework.
        - ```tests.py``` auto create by django
        - ```urls.py``` contains all the routing in an app level
        - ```views.py``` contains views using Django framework
    - ```media``` Contains all the media (Profile picture for each user) in this example. it will have 6 user Dororo, Giroro, Keroro, Kururu, Tamama, id1234, also contains default image in the case user doesn't upload the profile picture
    - ```Final_Project``` create when run ```django-admin startproject Final_Project```
        - ```__init__.py``` auto create by django
        - ```asgi.py``` auto create by django
        - ```settings.py``` contains all the setting and package install for the project
        - ```urls.py``` manage routing in an app level.
        - ```wsgi.py``` auto create by django
    - ```db.sqlite3``` auto generate when run migrate
    - ```manage.py``` auto create by django
    - ```README.md``` It is this file. 
    - ```requirements.txt``` contains all the package needed to runthe application

## How to run your application (Installation and running)
Refer to the requirement, this will fall under 
>How to run your application. 


for the first step, refer to the requirement. This will fall under 
>If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!

#### Install all the package use
```
pip3 install -r requirements.txt
```

#### Run migrations

```
python3 manage.py makemigrations
python3 manage.py migrate
```

#### Run the server 
```
python3 manage.py runserver
``` 

you can register the new account or decide to use an existing account, here's the ID and password 
```
1. ID : Keroro Password : keroro 
2. ID : Tamama Password : tamama
3. ID : Giroro Password : giroro
4. ID : Dororo Password : dororo
5. ID : Kururu Password : kururu 
```


## Features (Any other additional information the staff should know about your project.)

This topics will fall under 
>Any other additional information the staff should know about your project.

#### User and company
- This app group user in a company, where the first who create this group(first one who register with each company name) will have the rights of Admin, where you can see all post of all user in that company, edit post and be able to move task from todo to process or finish 

- The other user who register after the company was created, will have the role of member, which can only create task and manage thier own task 

#### Board

- Board is a way to organize task, on homepage, there will be 3 boards 
    1. Todo board : which will be the board for the task that newly create. 
    2. Process board : Process board is the board for processing task, to let other member that have been assigned to that task know that it's on the working process and everyone that have been assigned should be help to get this task done.
    3. Finish board : Finish board is the board to let each member that have been assigned task to, know that the task is finished.

#### Task 

- Each task will represents as a card, and will have 3 status Todo, process, finish. As it's will fall into each board. 
- Member who've been assigned to a task can click at the task card to view, But will not be able to move task or edit. That privilleges will be for Admin or the owner of the task(Who create the task).
- Task that appear on the user's board can be click to see the detail of the task, such as full description for the task, other member who've assigned to this task and the comment made on this task.

#### Comment 

- Each task can be comment by a user 
    





