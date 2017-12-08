import pandas as pd
import os
from MysqlConnection import mysql_connection

def GetRegions(id) -> list:
    """
    :id: 一个国家的country_id
    :return: 获得该id对应国家的所有Region名字的列表
    """
    connection = mysql_connection()
    sql = "select distinct name from regions where country_id = +" + str(id) + " and is_forbid = 0;"
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    region_list = []
    for ele in result:
        region_list.append(ele["name"])
    cur.close()
    connection.close()
    return region_list


def GetRegions_ID(id) -> pd.DataFrame:
    """
    :param id: 一个country_id
    :return: 返回这个country_id对应国家的region_name和region_id
    """
    connection = mysql_connection()
    sql = "select distinct name,id from regions where country_id = 28 and is_forbid = 0;"
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    connection.close()
    return pd.DataFrame(result)


def GetRoutes(id) -> list:
    """
    :return: 返回一个线路列表，每个元素是一个列表([起点，终点])
    且这个列表不包括已经完成的线路。
    """
    Routes = []
    region_list = GetRegions(id)
    for i in range(len(region_list)):
        for j in range(len(region_list)):
            if (i != j) & (region_list[i] != "Toyota") & \
                    (region_list[j] != "Toyota") & (region_list[i] != "Shima") \
                    & (region_list[j] != "Shima") & (region_list[i] != "Nagomi") & (region_list[j] != "Nagomi"):
                Routes.append([region_list[i], region_list[j]])
    if os.path.exists("result") is False:
        os.makedirs("result")
    files = os.listdir("result")
    for file in files:
        try:
            region1 = file.split("-")[0]
            region2 = file.split("10")[0].split("-")[1]
            for route in Routes:
                if (route[0] == region1) & (route[1] == region2):
                    Routes.remove(route)
        except:
            pass
    return Routes


