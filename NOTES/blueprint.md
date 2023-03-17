Blueprint
-------------

- We use blueprints so, we can register multiple sub application to the main application
- Blueprint is an object which is similar to the flask class object. Both the classes have same set of attributes
- But we use blueprints only when we want creates a sub application
- By using Blueprint we can do separations of concerns
- We can logically separate each sub-application from each other
- Every sub application can have its own static files, template folders and view files



## Syntax for importing blueprint
```
from flask import Blueprint

app = Blueprint(<"app name">, "module name", urlprefix="/mysubapp")

```