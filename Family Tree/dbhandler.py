
from matplotlib.pyplot import table
import mysql.connector


def connection():
  # mydb = mysql.connector.connect(
  #   host="localhost",
  #   user="root",
  #   password="prem11267",
  #   database="familytree"
  # )
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="psk112678",
    database="familytree"
  )
  mycursor = mydb.cursor(buffered=True)
  return mycursor, mydb

def create_user_table(tablename):
  mycursor,conn = connection()
  mycursor.execute("SHOW TABLES")
  tables = [each[0] for each in list(mycursor)]
  if tablename in tables :
    print (f"Table {tablename} already exist !")
    return None
  else:
    try:
      mycursor.execute("CREATE TABLE users (uid INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), "
                       "password VARCHAR(255), email VARCHAR(255));")
    except Exception as e:
      print(f"Error while creating db table {e}")
      return None
    else:
      print(f"table {tablename} created successfully!")

def create_persons_table(tablename):
  mycursor,conn = connection()
  mycursor.execute("SHOW TABLES")
  tables = [each[0] for each in list(mycursor)]
  if tablename in tables :
    print (f"Table {tablename} already exist !")
    return None
  else:
    try:
      mycursor.execute("CREATE TABLE Persons (personID INT AUTO_INCREMENT PRIMARY KEY,"
                       "personname VARCHAR(255), middlename VARCHAR(255),gender VARCHAR(255), birth DATE, death DATE, "
                       "image LONGBLOB,"
                       "fatherID INT,motherID INT,userID INT,"
                       "partnerID INT,imgPath VARCHAR(255),"
                       "FOREIGN KEY (userID) REFERENCES users(uid));")

    except Exception as e:
      print(f"Error while creating db table {e}")
      return None
    else:
      print(f"table {tablename} created successfully!")

def create_persons_table(tablename):
  mycursor,conn = connection()
  mycursor.execute("SHOW TABLES")
  tables = [each[0] for each in list(mycursor)]
  if tablename in tables :
    print (f"Table {tablename} already exist !")
    return None
  else:
    try:
      mycursor.execute("CREATE TABLE Persons (personID INT AUTO_INCREMENT PRIMARY KEY,"
                       "firstname VARCHAR(255), lastname VARCHAR(255),gender VARCHAR(255), birth DATE, death DATE, "
                       "image LONGBLOB,"
                       "fatherID INT,motherID INT,userID INT,"
                       "partnerID INT,imgPath VARCHAR(255),"
                       "birthcountry VARCHAR(255),birthcity VARCHAR(255), birthaddress VARCHAR(255),marital_status VARCHAR(255),"
                       "FOREIGN KEY (userID) REFERENCES users(uid));")

    except Exception as e:
      print(f"Error while creating db table {e}")
      return None
    else:
      print(f"table {tablename} created successfully!")


def create_tree_access_table(treeaccess):
  mycursor,conn = connection()
  mycursor.execute("SHOW TABLES")
  tables = [each[0] for each in list(mycursor)]
  if treeaccess in tables :
    print (f"Table {treeaccess} already exist !")
    return None
  else:
    try:
      mycursor.execute("CREATE TABLE Persons (id INT AUTO_INCREMENT PRIMARY KEY,"
                       "firstname VARCHAR(255), lastname VARCHAR(255),gender VARCHAR(255), birth DATE, death DATE, "
                       "image LONGBLOB,"
                       "fatherID INT,motherID INT,userID INT,"
                       "partnerID INT,imgPath VARCHAR(255),"
                       "FOREIGN KEY (userID) REFERENCES users(uid)) ;")

    except Exception as e:
      print(f"Error while creating db table {e}")
      return None
    else:
      print(f"table {treeaccess} created successfully!")



if __name__ == '__main__':
  create_user_table('users')
  create_persons_table('persons')


'''

CREATE TABLE Persons (personID INT(11) AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255), gender VARCHAR(255), birth DATE, death DATE, image LONGBLOB,
FOREIGN KEY (personID) REFERENCES Persons(fatherID), 
FOREIGN KEY (personID) REFERENCES Persons(motherID),
FOREIGN KEY (uid) REFERENCES users(userID));

'''



