from db_handler import DbManager

task_data = """DROP TABLE IF EXISTS Persons;
CREATE TABLE Persons
(
    id      INT PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(20),
    height  INT,
    weight  INT,
    age     INT
);

INSERT INTO Persons (name, height, weight, age)
VALUES ('Вася', 165, 65, 20),
       ('Петя', 175, 85, 22),
       ('Вова', 185, 95, 25)
       ;"""
table_name = 'Persons'
table_description = """
-- DROP TABLE IF EXISTS Persons;
CREATE TABLE Persons
(
    id      INT PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(20),
    height  INT,
    weight  INT,
    age     INT
);"""

sql_request = "INSERT INTO Persons (name, height, weight, age) VALUES ('Маша', 175, 65, 18);"
# sql_request = "SHOW GRANTS FOR 'testuser'@'%';"

manager = DbManager()
# manager.create_table_from_task_data(task_data)
# manager.default_create_table(table_name, table_description)
# print(DbManager.parse_the_task(task_data))
# print(manager.data_query(sql_request))
# sql_request = "SELECT * FROM Persons;"
print(manager.data_query(sql_request))
