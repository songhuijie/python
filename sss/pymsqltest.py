#! -*- coding:utf-8 -*-
import pymysql


def test():
    conn2db = pymysql.connect("127.0.0.1", "root", "instagram@web.", "instagram")

    cur = conn2db.cursor()

    sql = "INSERT INTO `test` ( `test`) VALUES (\
                '%s')" % (
        'jiedage' )
    cur.execute(sql)
    conn2db.commit()
    cur.close()
    conn2db.close()

    return True


if __name__ == '__main__':
    test()
    print(1)
    exit()