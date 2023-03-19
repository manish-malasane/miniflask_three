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