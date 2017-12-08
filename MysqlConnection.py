####################################
# 设置mysql连接                     #
#                                  #
# online_connection:连接线上数据库   #
# local_connection:连接本地数据库    #
#                                  #
####################################
import pymysql.cursors


def online_connection():
    connection = pymysql.connect(host='192.168.100.253',
                                 port=3306,
                                 user='unireader',
                                 password='7LWFu(RMYHKb>dWvM6gEE(GKFWwhL',
                                 db='uniqueway_production',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def local_connection():
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 db='uniquway',
                                 password='Sun1327637497',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    return connection


def mysql_connection():
    # connection = local_connection()
    # connection = online_connection()
    connection = online_connection()
    return connection
