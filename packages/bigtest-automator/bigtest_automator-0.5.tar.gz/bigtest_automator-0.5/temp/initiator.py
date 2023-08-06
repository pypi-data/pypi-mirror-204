import db_ops as db

insert = "INSERT INTO SERVERS (NAME, SERVER_IP, USER_NAME, AUTH_METHOD, PASSWORD) VALUES ('Shantharam', '10.0.0.1','shantharamp','password','dummy');"
selectq = "SELECT * FROM SERVERS;"
delete_all = "DELETE FROM SERVERS;"

select = db.query_executor(selectq)

for item in select:
    print(item)

db.query_executor(delete_all)
#db.query_executor(insert)

sec_select = db.query_executor(selectq)

for item in sec_select:
    print(item)