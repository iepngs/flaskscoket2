from model.BaseModel import getDbCursor

class UserModel(object):
    __dbCursor = None

    def __init__(self):
        self.__dbCursor = getDbCursor()

    def User(self, startIndex = 0):
        fields = 'id uid,cellphone,nickname,sex,age,sign,user_type,init_time'
        sql = 'select %s from qy_user limit %d, 3' % (fields, startIndex)
        self.__dbCursor.execute(sql)
        # executemany()方法可以一次插入多条值，执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数。
        return self.__dbCursor.fetchall()