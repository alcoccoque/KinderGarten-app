#Python app about kindergarten accounting 
Based on kivy and sqlite
## Database consist of 5 tables:
###Parents
|    Name    | Type    | Keywords                  |
|:----------:|---------|---------------------------|
| ID_PARENTS | INTEGER | PRIMARY KEY AUTOINCREMENT |
| NAME       | TEXT    | NOT_NULL                  |
|            |         |                           |
###KinderGarten
|  Name  | Type    | Keywords                  |
|:------:|---------|---------------------------|
| ID_KDG | INTEGER | PRIMARY KEY AUTOINCREMENT |
| NAME   | TEXT    | NOT_NULL                  |
| STREET | TEXT    | NOT NULL                  |
###PersonalAccount
|    Name    | Type    | Keywords                  |
|:----------:|---------|---------------------------|
| ID         | INTEGER | PRIMARY KEY AUTOINCREMENT |
| ID_KDG     | INTEGER | NOT_NULL                  |
| ID_PARENTS | INTEGER | NOT_NULL                  |
| FULL_NAME  | TEXT    | NOT NULL                  |
|FOREIGN KEY(ID_PARENTS) REFERENCES Parents(ID_PARENTS) ON DELETE CASCADE ON UPDATE CASCADE|
###BooKeeping
|         Name         | Type    | Keywords                                                |
|:--------------------:|---------|---------------------------------------------------------|
| ID_BK                | INTEGER | PRIMARY KEY AUTOINCREMENT                               |
| ID_M                 | INTEGER | NOT_NULL                                                |
| numOfVisitDays       | INTEGER | NOT_NULL                                                |
| monthlyPaymentResult | REAL    | GENERETED always as (1000 / 22 * numOfVisitDays) stored |
| ID                   | INTEGER | NOT_NULL                                                |
|FOREIGN KEY(ID) REFERENCES  personalAccount(ID) ON DELETE CASCADE ON UPDATE CASCADE|
###Admin
|   Name   | Type | Keywords |
|:--------:|------|----------|
| name     | TEXT | TEXT     |
| password | TEXT | NOT_NULL |
##Enter
login:admin
password: password