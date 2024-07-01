#pip install mysql-connector-python

from getpass import getpass
from mysql.connector import connect, Error
from .Settings import settings

def run_query(hosts, port, db_query, user, pwd):
    try:
        result_all = []
        for host in hosts:     
            print(f'Host:{host}')                   
            # user=input("Enter username: "), password=getpass("Enter password: ")
            with connect(host=host,port=port, user=user,
                    password=pwd) as connection:  
                with connection.cursor() as cursor:                      
                    res = cursor.execute(db_query, multi=True)                                    
                    for result in res:                                      
                        if result.with_rows:
                            print("Rows produced by statement '{}':".format(result.statement))
                            res_list = result.fetchall()
                            for row in res_list:
                                print(row)
                            result_all.append(res_list)
                        else:
                            print("Number of rows affected by statement '{}': {}".format(
                            result.statement, result.rowcount))
                connection.commit() 
        return result_all        
    except Error as e:
        print(e)
    
    
    
#if __name__ == '__main__':   
def sql_request():
    #hosts = ['localhost']
    port = 3306
    db_query = f"use game;select hi_score from score where nome = '{settings.name}';"
    res_list = run_query(settings.hosts, port, db_query, 'user_game', '123')
    #print("RESULT ALL")
    res = ''
    for row in res_list:
        #print(row)
        res = row
    
    res = list(res)
    #print(res[0][0])
    return res[0][0]
    
def sql_update(hiscore):
    #hosts = ['localhost']
    port = 3306
    db_query = f"use game;update score set hi_score = {hiscore} where nome = '{settings.name}';"
    res_list = run_query(settings.hosts, port, db_query, 'user_game', '123')
    
def sql_name():
    #hosts = ['localhost']
    port = 3306
    db_query = f"use game;select nome from score where nome = '{settings.name}';"
    res_list = run_query(settings.hosts, port, db_query, 'user_game', '123')
    
    res = ''
    for row in res_list:        
        res = row
    
    res = list(res)    
    return res[0][0]

def sql_login():
    #hosts = ['localhost']
    port = 3306    
    db_query = f"use game;select nome from score where nome = '{settings.name}' and pass = '{settings.pwd}';"
    res_list = run_query(settings.hosts, port, db_query, 'user_game', '123')
    
    res = ''
    for row in res_list:        
        res = row
    
    res = list(res)   
    #print(res, settings.name, settings.pwd) 
    if len(res)>0: return 1
    else: return 0
    
def sql_register():
    #hosts = ['localhost']
    port = 3306
    db_query = f"use game;INSERT INTO score VALUES ('0', '{settings.name}', '{settings.pwd}');"
    res_list = run_query(settings.hosts, port, db_query, 'user_game', '123')