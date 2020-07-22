# import pymysql
# # 连接->创建指针->操作->关闭
# # 连接
# db = pymysql.connect('localhost', 'root', 'mysql123','fhjx')
# # 创建指针
# cursor = db.cursor()
# # 执行命令
# cursor.execute("SELECT VERSION()")
# # 获取单条数据
# data = cursor.fetchone()
# print(data)
# print(type(data))
# # 如果表shenzhen存在则删除，重新创建
# # cursor.execute("DROP TABLE IF EXISTS shenzhen")
# # print("结果：{}".format(cursor.fetchone()))
# # 使用预处理语句创建表
# # sql = """CREATE TABLE shenzhen (
# #     rownum_	int PRIMARY KEY,
# #     houses_floor_space int,
# #     rent_price float,
# #     ho_orien char(10),
# #     houses_floor_no int,
# #     houses_rm_no int,
# #     houses_type	char(20),
# #     proj_region	char(20),
# #     proj_name char(50),
# #     deco_type char(20),
# #     ho_id char(20) UNIQUE
# #     )"""
# # 插入值
# sql = """INSERT INTO shenzhen (
#     houses_floor_space, rent_price, ho_orien, 
#     houses_floor_no, houses_rm_no, houses_type,
#      proj_region, proj_name, deco_type,ho_id) 
#      VALUES 
#      (40.95,4669,'北',31,3102,'一房','南山区','塘朗城广场','毛坯房','100001011671')
#      """
# try:
#     cursor.execute(sql)
#    # 数据改动后需要提交到数据库执行
#     db.commit()
#     print(cursor.fetchall())
# except Exception as err:
#     # 如果发生错误则回滚
#     db.rollback()
#     print(err)
# db.close()
"""
用变量向SQL语句中传递参数:
user_id = "test123"
password = "password"

con.execute('insert into Login values( %s,  %s)' % \
             (user_id, password))
"""
import pymysql

class DB():
    def __init__(self, host='my.syao.fun', port=3306, db='', user='root', passwd='mysql123', charset='utf8'):
        # 建立连接 
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型        
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标        
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行        
        self.conn.commit()
        # 关闭游标        
        self.cur.close()
        # 关闭数据库连接        
        self.conn.close()


if __name__ == '__main__':
    with DB(db='fhjx') as db:
        db.execute('select * from shenzhen')
        print(dir(db))
        for i in db:
            print(i)
