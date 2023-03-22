### project structure


miniflask_v3   (main-project-root)
├── NOTES
├── README.md
├── blueprint.md
├── main.py    (entrypoint)
├── requirements.txt
├── resources  (sub-application 1)
│   ├── __init__.py
│   └── starwars.py
├── tasks      (sub-application 2)
│   ├── __init__.py
│   └── api.py

shoppingpal.com (Project) - product_catalogue_api (present) - product_info_crawling_api (source) - user authentication & authorization - payment-paytm_api - payment-cod_api


user_auth_api (project root)
    - user_profile  (package / sub-application)
    - user_choices  (sub-application)

MicroFinanceLoanPortal (project root)
    - IDAM 
        - 127.0.0.1:5000/idam/user/signup
        - 127.0.0.1:5000/idam/user/login
        - 127.0.0.1:5000/idam/user/email_verification
        - 127.0.0.1:5000/idam/user/mobile_verification
        - 127.0.0.1:5000/idam/user/pan_upload
        
    - LoanProcessing
        - 127.0.0.1:5000/loan/cibil
        - 127.0.0.1:5000/loan/credit_history
        - 127.0.0.1:5000/loan/types
        - 127.0.0.1:5000/loan/document_verification
        - 127.0.0.1:5000/loan/application_submittion
    



miniflask_v3  (project-root)
    - IDAM (sub-application1)
    - saving_account (sub-application2)


NOTE -
    IDAM - Indentity and Access Management

CRUD
create
Retrieve (Read)
Update
Delete


#### Project Structure
- flask_three  (project root dir)
    - api_1    (sub app)
      - __init__.py (this file tells python that this folder is a python package)
      - http_requests (http end-points)
        - __init__.py  (this file tells python that this folder is a python package)
        - characters_.py   |
        - films_.py        |
        - planets_.py      | ----  (all the http end points GET, POST, ..)
        - species_py       |
        - starships_.py    |
        - vehicles_.py     |
    - starwars_app.py   (all the registered blueprints of app_1)
    - dal     (data access layer package)
      - __init__.py 
      - settings (package related to db configs)
        - __init__.py
        - secrets.toml
      - dml.py (data-manipulation code)
      - db_conn_helper.py (helps to connect with db)
    - models (pydantic models)
      - __init__.py
      - basemodel.py    (some common fields)
      - datamodels      (pydantic models)
        - __init__.py
        - characters.py
        - films.py
        - planets.py
        - species.py
        - starships.py
        - vehicles.py
    - response validation
      - __init__.py
      - response.py (response data validation)
    - .gitignore  (files to ignore)
    - README.md (Project Documentation)
    - requirements.txt  (keep dependencies)
    - requirements.dev.txt (to keep development dependencies)
    - venv (virtual env [isolation])
