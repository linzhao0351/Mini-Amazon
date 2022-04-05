#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 23:21:09 2022

@author: root
"""

from flask import current_app as app

class dal_api():
    
    def __init__(self):
        pass 
    
    @staticmethod
    def select(table_name, *, fields=None, cond=None):      
        if fields is None:
            field_arg = "*"
        else:
            field_arg = ", ".join(fields)
        
        if cond is None:
            cond_arg = ""
        else:
            cond_arg = "WHERE %s" % cond
        
        sqlstr = '''SELECT %s FROM %s %s''' % (field_arg, table_name, cond_arg) 
        print(sqlstr)
        result = app.db.execute(sqlstr)
        return result

    @staticmethod
    def insert(table_name, records):
        if type(records) == list:
            value_arg = ""
            for k in range(0, len(records)):
                if type(records[k]) == str:
                    value_arg += '''"%s", ''' % records[k]
                else:
                    value_arg += '''%s, ''' % records[k]
            value_arg = value_arg[:-2]
            sqlstr = '''INSERT INTO %s VALUES (%s)''' % (table_name, value_arg)
        elif type(records) == dict:
            column_arg = ""
            value_arg = ""
            for k in records.keys():
                column_arg += "%s, " % k
                if type(records[k]) == str:
                    value_arg += '''"%s", ''' % records[k]
                else:
                    value_arg += '''%s, ''' % records[k]
            column_arg = column_arg[:-2]
            value_arg = value_arg[:-2]
            sqlstr = '''INSERT INTO %s COLUMN (%s) VALUES (%s)''' % (table_name, column_arg, value_arg)
            
        # print(sqlstr)
        result = app.db.execute(sqlstr)
        return result
    
    @staticmethod
    def delete(table_name, cond):
        sqlstr = "DELETE FROM %s WHERE %s" % (table_name, cond)
        # print(sqlstr)
        result = app.db.execute(sqlstr)
        return result
    
    @staticmethod
    def update(table_name, update_info, cond=None):
        set_arg = ""
        for k in update_info.keys():
            if type(update_info[k]) == str:
                set_arg += '''%s="%s", ''' % (k, update_info[k])
            else:
                set_arg += '''%s=%s, ''' % (k, update_info[k])
        set_arg = set_arg[:-2]
        
        if cond is None:
            cond_arg = ""
        else:
            cond_arg = "WHERE %s" % cond
            
        sqlstr = '''UPDATE %s SET %s %s''' % (table_name, set_arg, cond_arg)
        # print(sqlstr)
        result = app.db.execute(sqlstr)
        return result
    
    @staticmethod
    def naturalJoin(t1, t2):
        sqlstr = '''SELECT * FROM %s NATURAL JOIN %s''' % (t1, t2)
         # print(sqlstr)
        result = app.db.execute(sqlstr)
        return result
    
    @staticmethod
    def outerJoin(t1, t2, match_fields, cond=None):
        match_arg = ""
        for k in match_fields.keys():
            match_arg += "%s.%s = %s.%s " % (t1, k, t2, match_fields[k])
        
        if cond is None:
            cond_arg = ""
        else:
            cond_arg = "WHERE %s" % cond
        
        sqlstr = '''SELECT * FROM %s LEFT OUTER JOIN %s ON %s %s''' % (t1, t2, match_arg, cond_arg)
        # print(sqlstr)
        result = app.db.execute(sqlstr)
        return result
        

# if __name__ == '__main__':
#     app = dal_api()
    
    # examples
    # app.select("User_info")
    # app.select("User_info", fields = ["name"])
    # app.select("User_info", fields = ["name"], cond = "age>5")
    
    # app.insert("User_info", ["Bob", 15])
    # app.insert("User_info", {"name":"Bob", "age":15})    
    
    # app.delete("User_info", "age>5")
    
    # app.update("User_info", {"age": 8}, '''name = "Bob"''')
    
    # app.naturalJoin("User_info", "User_browsing_history")
    
    # app.outerJoin("User_info", "order_info_detail", {"user_id": "buyer_id"})
    
    
    
    
    