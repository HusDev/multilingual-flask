## Get Started: 

### 1- cmd: 
```
>pip install -r requirements.txt 
>createdb mydb
>psql mydb
```
### 2- put your datanbase url here:'
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'Your Database URL'
```
### 3- python:
```
>>>from app import db
>>>db.create_all()
```
### 4- postgresql:
```
#insert into lang values('en','English');
#insert into lang values('ar','Arabic');
```
