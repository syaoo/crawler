# 读取文本文件写入sql
import pymysql

def readfile(dpath,delimiter,skiprows=0):
    """
    读取文本数据到列表
    dpath: 文本地址
    delimiter: 列分割符号
    skiprows: 要跳过的行数, 默认0
    返回数据列表
    """
    with open(dpath, 'r') as f:
        dat=f.readlines()
    i=skiprows
    for line in dat[1:]:
        line = line.split(delimiter)
        line = [i.lstrip().rstrip() for i in line]
        line[-1] = line[-1].rstrip('\n')
        dat[i] = line
        i+=1
    return dat[skiprows:]

if __name__ == "__main__":
    dpath = './spdider/szfdc/data/202003061747.txt'
    delimiter = '\t'
    data = readfile(dpath, delimiter,skiprows=1)
    sqlserver = 'my.syao.fun'
    sqlserver = 'localhost'
    sqlport = 3306
    sqluser = 'root'
    sqlpassword = 'mysql123'
    sqldatabase = 'fhjx'
    table = 'shenzhen'
    db = pymysql.connect(host = sqlserver, port=sqlport, user=sqluser, passwd=sqlpassword,db=sqldatabase,charset='utf8')
    cursor = db.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS %s (
        `rownum_` int(10) primary key,
        `houses_floor_space` float,
        `rent_price` float,
        `ho_orien` char(20),
        `houses_floor_no` int(10),
        `houses_rm_no` int(10),
        `houses_type` char(20), 
        `proj_region` varchar(25),
        `proj_name` varchar(25),
        `deco_type` char(10),
        `ho_id` char(20) unique
    )'''%(table)
    try:
        cursor.execute(sql)
        for line in data[1:]:
            sql = "INSERT INTO %s \
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
                    VALUES\
                    (%s,%s,%s,'%s',%s,%s,'%s','%s','%s','%s','%s')"%\
                    (table,\
                    data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6],data[0][7],data[0][8],data[0][9],data[0][10],\
                        line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10])
            cursor.execute(sql)
    except Exception as e:
            db.rollback()
            print(e)
    db.commit()
    db.close()