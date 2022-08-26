# Jekii Capital Loan Management System

### API endpoints to a minimal loan management system.

#### NOTE : Please check these [Published API Docs](https://documenter.getpostman.com/view/9835426/Tzm5FwLV) to get examples and information of all test cases of the API endpoints.

### Major Technologies used:
1. Django
2. Django REST framework
3. PostgreSQL


### Introduction to codebase:
1. [backend](./backend) : The API endpoints folder with all settings and configuration.
2. [requirements.txt](./backend/requirements.txt) : Requirements file with all the necessary dependencies required to run the project.
3. [user](./backend/user) : App for user authentication and user roles and permissions.
4. [member](./backend/loan) : App for the member management of the borrower.
5. [loan](./backend/loan) : App for the loan management of the users.
6. User test cases present at [tests](./backend/user/tests)
7. Loan test cases present at [tests](./backend/loan/tests)

### Steps to run the projects:

**Pre-requites:**
1. python3.7 or greater

**Steps:**
1. Navigate to the project directory and create virtual enviroment by using this command ```python -m venv env
2. Activate your virtual enviroment with this command  for MacOS ```source env/bin/activate  for windows ```env/Scripts/activate
3. Install all projects dependencies by runnging this code ```pip3 install -r requirements.txt
4. Check your inside env/lib to see if all dependencies have been installed. 
3. Navigate to the folder with [manage.py](./docker-compose.yml).
4. To run migrations and set up the database, use commands:
```buildoutcfg
python manage.py makemigrations user
python manage.py makemigrations loan
python manage.py makemigrations member
python manage.py migrate
```
5. To start the development server, use command:
```buildoutcfg
python manage.py runserver
```
6. To shut the development serve, use 
```buildoutcfg
ctrl + c
```
**7. IMPORTANT: To test the backend with test cases, use command:**
```buildoutcfg
python manage.py test
```
8. Create the first admin user of the system using command:
```buildoutcfg
python manage.py createsuperuser
```

#### Key Points of the API:
1. There are 2 roles in the system -  Agent(credit officer) Admin(superuser).
2. Admins are the highest role available in the system and they can access the admin panel at http://127.0.0.1:8000/admin/ to view all data.
3. PBKDF2 algorithm with a SHA256 hash is used for hashing the password before storing it in the database.
4. [permissions.py](./backend/user/permissions.py) is used to set permissions of the user.
5. JWT is used to perform token authentication and the token is only valid for 2 hours after it's creation. This is to increase security of the system.
6. After 2 hours, a new token needs to be requested from the server.
7. Every API call is protected by permissions and authentication to ensure maximum safety.
8. History for "double safety" is being logged at every change made to a loan object. This can help us to rollback in extreme cases. Here is an example,
![History of Loan Object](./screenshots/history.png)
9. Filter by loan type is present.
10. East African Timezone is considered in the system and date handling is done accordingly.

#### Description of URL endpoints:

#### NOTE: Please check Postman Published Docs link given above to see examples of all URL endpoints.

* **Base URL : http:127.0.0.1:8000/** The base URL contains the dashboard. The dashboard data/info is different depending on the user token genrated. Admin user dashboard contains global statics while agent/credit officer contain individual performance data/info statistics.
* **User Endpoints:**
    1. **Signup: /user/signup/**
        1. This endpoint can be used to sign up a user(agent).
        2. Cannot signup if user already exists.
        3. Tokens have a validity of 2 hours only after which re-login is required.
        4. A user token is generated on successful registration.
        5. POST request has to be sent to this endpoint.
    2. **Create Admin: /user/create-admin/**
        1. This endpoint can be used by ADMINS ONLY to make more admin users.
        2. Authorization of admin level required to access this endpoint.
        3. POST request has to be sent to this endpoint.
    3. **Login : /user/login/**
        1. This endpoint can be used to log in by admin, agent.
        2. Cannot log in agent if it is not approved by the admin.
        3. Admin can login using correct credentials directly.
        4. A user token is generated on successful login.
        5. Tokens have a validity of 2 hours only after which re-login is required.
        6. POST request has to be sent to this endpoint.
    4. **Profile : /user/profile/**
        1. This endpoint can display the user information depending on the authorization token present in the header.
        2. Authorization is required to access this endpoint.
        3. GET request has to be sent to this endpoint.
    5. **List Users(Agent) : /user/list-agent/**
        1. This endpoint can be used by AGENTS OR ADMINS to list the members present in the system.
        2. Customer role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. GET request has to be sent to this endpoint.
    6. **List Users(Admin) : /user/list-approvals/**
        1. This endpoint can be used by ADMINS only to list the  agents present in the system.
        2. Agent role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. GET request has to be sent to this endpoint.
    7. **Approve or Delete and Agent/Credit officer : /user/approve-delete/<int:pk>/**
        1. This endpoint can be used by ADMINS only to list approve an agent to the system or delete one.
        2. Customer and Agent role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. PUT request with <int:pk> i.e. agent ID as a URL parameter with is_approved status can be used to approve or reject an agent.
        5. DELETE request with <int:pk> i.e. agent ID as a URL parameter can be used to delete an agent.
    8. **Delete Member/customer : /user/delete-member/<int:pk>/**
        1. This endpoint can be used by ADMINS only to delete a member.
        2. Agent/Credit officer role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        5. DELETE request with <int:pk> i.e. member ID as a URL parameter can be used to delete an agent.
* **Loan APIs:**
    1. **Request Loan by Agent for member : /loan/request-loan/**
        1. This endpoint is for the agent to request a loan to the admin on behalf of a customer/member.
        2. Only Agent role can access this endpoint.
        3. Authorization required to access this endpoint.
        4. POST request has to be sent to this endpoint.
    2. **Approve or Reject a loan by admin : /loan/approve-reject-loan/<int:pk>/**
        1. This endpoint is for the ADMIN users only to accept or reject a loan request.
        2. Agent/Credit officer role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. PUT request with <int:pk> i.e. loan ID as a URL parameter and status in the body can be used to approve or reject a loan.
    3. **Edit Loan by agent : /loan/edit-loan/<int:pk>/**
        1. This endpoint is for the AGENT/credit officer role only to edit loan details for a member.
        2. Authorization required to access this endpoint.
        3. PUT request with <int:pk> i.e. loan ID as a URL parameter and new loan details in the body can be used to edit a loan.
        4. If loan is already approved, then edit is not allowed.
    4. **List Loans of all customers to Admins and Agents : /loan/list-loans-admin-agents/**
        1. This endpoint can be used by agents and admin users to list all loans in the system.
        2. Authorization required to access this endpoint.
        3. GET request has to be sent to this endpoint.
        4. Filters available:
            1. status?=PENDING
            2. status?=APPROVED
            3. status?=CLEARED
        5. For example:
            1. For only one of the filters use: http://localhost:8000/loan/list-loans-admin-agent?status=APPROVED
            
    5. **Roll-over Loan by agent : /loan/roll-over-loan/<int:pk>/**
        1. This endpoint is for the AGENT/credit officer role only to rollover loan for a member.
        2. Authorization required to access this endpoint.
        3. PUT request with <int:pk> i.e. loan ID as a URL parameter and new loan details in the body can be used to edit a loan.
        
                   
    * **Member APIs:**
    1. **Add member by Agent : /loan/add-member/**
        1. This endpoint is for the agent to add a member.
        2. Only Agent role can access this endpoint.
        3. Authorization required to access this endpoint.
        4. POST request has to be sent to this endpoint.
    2. **Edit Member by agent : /loan/edit-member/<int:pk>/**
        1. This endpoint is for the AGENT/credit officer role only to edit member details.
        2. Authorization required to access this endpoint.
        3. PUT request with <int:pk> i.e. loan ID as a URL parameter and new loan details in the body can be used to edit a loan.
    4. **List all members in the system : /member/list-members-admin-agents/**
        1. This endpoint can be used by agents and admin users to list all members in the system.
        2. Authorization required to access this endpoint.
        3. GET request has to be sent to this endpoint.
        4. Filters available:
            1. status?=ACTIVE
            2. status?=INACTIVE
        5. For example:
            1. For only one of the filters use: http://localhost:8000/member/list-members-admin-agent?status=ACTIVE
    5. **List Loans of a particular Member : /member/list-loans/**
        1. This endpoint can be used by credit officer to list a member's loans in the system.
        2. Authorization required to access this endpoint.
        3. GET request has to be sent to this endpoint.
        4. Filters available:
            1. status?=PENDING
            2. status?=APPROVED
            3. status?=CLEARED
        5. For example:
            1. For only one of the filters use: http://localhost:8000/member/list-loans?status=APPROVED
