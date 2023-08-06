# Mongeasy

Mongeasy is a easy to use library to be used for simple access to a MongoDB database, without any need for schemas or validation. Just store the data as it is used in your application.

### Connection
Connection to the database is handled automtically for you if you have the conenction information in a configfile or set as environment variables.

#### Connection using configfile
Create a file called `mongeasy.conf` and place it in your project root folder.

The contents of the file should be:

```bash
[mongoeasy]
connection_string = mongodb://localhost:27017/
database_name = mydatabase
```

#### Connection using environment variables
You can, as an alternative method, define your connection information using environment variables. Just set these two:

```bash
MONGOEASY_CONNECTION_STRING=mongodb://localhost:27017/
MONGOEASY_DATABASE_NAME=mydatabase
```

### Create a document class
To use Mongeasy you will create a document class that can be used with the collection of choice. To do this you will use the `create_document_class` factory function like this:

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

```

The first argument is the name the class will get and the second argument is the name of the collection to use. If the collection does not exist it will be created when you use the class to store documents.

You will not need to assign the returned value to a class variable as in the example above, as the generated class is injected into the current namespace:

```python
from mongeasy import create_document_class


create_document_class('User', 'users')

# The class User exist from this point in the code

```

### Create a store a document
You can create a documnet by using the generated class. You can either use keyword arguments or pass a dict.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Create a document using keyword arguments
user1 = User(name='Alice', age=25)
user1.save()

# Create a document using a dict
user2 = User({'name': 'Bob', 'age': 30})
user2.save()

```

### Find documents
You can find documents using the `find` method on the generated class. This method will return a list of documents.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find all documents
users = User.all()

# Find all documents with age 25
users = User.find({'age': 25})

```
#### Find one document
You can find one document using the `find` method on the generated class.

Find will return a ResultList object that can be used to get the first, or last, document in the list. If no document is found None is returned.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')

```

### Update a document
You can update a document just by changing the attributes and then calling the `save` method.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
else:
    # Update the age of the user
    user.age = 26
    user.save()
```

### Delete a document
You can delete a document by calling the `delete` method on the document.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
else:
    # Delete the user
    user.delete()
```

You can also delete all documents in a collection by calling the `delete` method on the generated class.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')


# Delete using a filter
User.delete({'age': 25})

# Delete all documents in the collection
User.delete()
```

### Indexes
You can create indexes on the collection by using the `create_index` method on the generated class.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Create a unique index on the name field
User.create_index('name', unique=True)
```

### Other uses
When you create the document class you have an option to pass additional bases classes. You can use this feature to add functionality to the generated class.

This can also be useful if you want to use Mongeasy with for example flask-login.

```python
from flask import Flask
from flask_login import UserMixin, LoginManager
from mongeasy import create_document_class
from bson import ObjectId

login_manager = LoginManager()
# Create User class with mongeasy and UserMixin from flask_login as a base class
User = create_document_class('User', 'users', base_classes=(UserMixin,))
def get_id(self):
    return str(self._id)
# Add get_id method to User class
User.get_id = get_id


def create_app():
    app = Flask(__name__)
   # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Load the user object from the database using the user_id
        user_id = ObjectId(user_id)
        user = User.find(_id=user_id).first()
        return user

    return app

```
### Query objects
To simplify queries to the database you can use the mongeasy query object. You construct it and make your query using normal python syntax.

Instead of using a mongodb query like this
```python
query = {'$or': [{'$or': [{'name': {'$eq': 'John'}}, {'age': {'$lt': 40}}]}, {'$and': [{'name': {'$eq': 'Jane'}}, {'age': {'$gt': 20}}]}]}
```

you can accomplish the same thing by using the Query object

```python
query = Query('(name == "John" or age < 40) or (name == "Jane" and age > 20)')
```

The query can then be used in your queries like this:

```python
result = User.find(query)
```


### ResultList
All queries that can return more than one document will return a `ResultList` object. This object can be used to get the first or last document in the list, or None if no document is found.


```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
```

There are also other methods on the `ResultList` object that can be used. These are:

* `first` - Get the first document in the list or None if no document is found
* `last` - Get the last document in the list or None if no document is found
* `first_or_none` - Get the first document in the list or None if no document is found, same as first
* `last_or_none` - Get the last document in the list or None if no document is found, same as last
* `map` - Apply a given function to each element in the list and return a new ResultList containing the results
* `filter` - Filter the list using a given function and return a new ResultList containing the results
* `reduce` - Apply a given function to each element in the list and return a single value
* `group_by` - Group the list by a given key and return a dict with the results grouped by the key
* `random` - Get a random document from the list or None if no document is found


### Contributing
Contributions are welcome. Please create a pull request with your changes.

### Issues
If you find any issues please create an issue on the github page.

### License
This project is licensed under the MIT License - see the LICENSE file for details