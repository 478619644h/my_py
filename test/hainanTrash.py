# /usr/bin/python
# -*- coding: utf-8 -*-
#author: hyj
#date: 2019/11/14


import requests,json
import psycopg2
import threading
import time

conn = psycopg2.connect(database="marscloud-parent-test", user="postgres", password="postgres", host="192.168.10.22",
                            port="5432")
g_id = 0

def getDeviceIds(start,pageSize):
    sql = '''
    SELECT
	equ.register_code,
	car.ID 
    FROM
        so_base_car car
        INNER JOIN so_base_car_equipment_detail detail ON car.ID = detail.so_vehicleinfo_id
        INNER JOIN so_base_equipment equ ON equ.ID = detail.so_equipment_id 
    WHERE
        car.project_id = '1061' 
        AND car.vehicle_type IN ( SELECT code FROM t_s_category WHERE code LIKE'A03A01%' ) 
        AND equ.asset_type = 'A06A02A01' 
    ORDER BY
        equ.register_code 
    ''' + 'LIMIT %d OFFSET %d' %(pageSize,start)
    with conn.cursor() as curs:
        curs.execute(sql)
        projectIds = curs.fetchall()

    return projectIds



def requestHbase(deviceId):
    hbaseUrl = 'http://192.168.1.65:37008/api/hbase/getData'
    #2020-06-08
    requestParam = {"deviceId":deviceId,"from":"1591545600000","to":"1591631999000"};
    result = requests.post(hbaseUrl,json.dumps(requestParam)).json()
    return result["data"]

def insertCarTrashRelation(trashId,vehicleId):
    sql = ''' 
        insert into so_trash_car_relation(id,trash_id,vehicle_id,create_time) values(
        replace(cast(uuid_generate_v4() as varchar),'-',''),
        '%s','%s',now()
        )
    '''%(trashId,vehicleId)
    with conn.cursor() as curs:
        curs.execute(sql)
        conn.commit()

def insertTrash(data):
    sql = '''
         INSERT into 
        so_base_garbage_container
        ("id",org_id,use_orgid,point_name,trashtype,address,longitude,latitude,project_id,collection_state,
        count,day,num,assetnumber,volume,province,city,area,town,village,district_code)
         VALUES ('%s','%s','%s','%s','trashtype001','%s',%s,%s,'%s',%s,%s,%s,%s,'%s','volume011','%s',%s,'%s','%s',%s,'%s')
    '''%(data["id"],
         data["orgId"],
         data["useOrgId"],
         data["trashName"],
         data["address"],
         data["longitude"],
         data["latitude"],
         data["projectId"],
         data["collectionState"],
         data["count"],
         data["day"],
         data["num"],
         data["assetNumber"],
         data["province"],
         data["city"],
         data["area"],
         data["town"],
         data["village"],
         data["districtCode"])
    with conn.cursor() as curs:
        curs.execute(sql)
        #conn.commit()


def converteLocationToName(bd_lon,bd_lat):
    url = 'https://restapi.amap.com/v3/geocode/regeo?key=7687200c4674525742e0012f8b617a7c&location=' + bd_lon + ","\
          + bd_lat + "&batch=false"
    result = requests.get(url)
    data = {}
    regeocode = result.json()["regeocode"]
    addressComponent = regeocode["addressComponent"]
    data["province"] = addressComponent["province"]
    data["city"] = "'省直辖县级行政区划'"
    if len(addressComponent["city"]) > 0:
        data["city"] = "'" + addressComponent["city"][0] + "'"
    data["area"] = addressComponent["district"]
    data["town"] = addressComponent["township"]
    data["village"] = 'null'
    if len(addressComponent["neighborhood"]['name']) > 0:
        data["village"] = "'" + addressComponent["neighborhood"]["name"][0] + "'"
    data["districtCode"] = addressComponent["adcode"]
    data["address"] = regeocode["formatted_address"]
    return data

def work(start,pageSize):
    convertedLongitude_ = None
    convertedLatitude_ = None
    deviceIds = getDeviceIds(start,pageSize)
    for item in deviceIds:
        deviceId = item[0]
        vehicleId = item[1]
        print("deviceId:  " + deviceId + " | vehicleId: " + vehicleId)
        hbaseData = requestHbase(deviceId)
        if hbaseData == None:
            continue
        if 'location' not in hbaseData:
            continue
        locations = hbaseData["location"]

        if len(locations) <= 0:
            continue
        print("本次查询的设备ID：" + item[0] + "车辆id:" + item[1])
        for location in locations:
            # mutex = threading.Lock()
            global g_id
            # if mutex.acquire(True):
            g_id += 1
            if "body" not in location:
                continue
            body = json.loads(location["body"])
            convertedLongitude = body["convertedLongitude"]
            convertedLatitude = body["convertedLatitude"]


            if(convertedLongitude_== convertedLongitude and convertedLatitude_ == convertedLatitude):

                #print("重复的经纬度  convertedLongitude: " + convertedLongitude + "| convertedLatitude: " + convertedLatitude)
                continue
            convertedLongitude_ = convertedLongitude
            convertedLatitude_ = convertedLatitude
            locNameInfo = converteLocationToName(convertedLongitude,convertedLatitude)
            locNameInfo["longitude"] = convertedLongitude
            locNameInfo["latitude"] = convertedLatitude
            locNameInfo["id"] = str(g_id)
            locNameInfo["orgId"] = "2124321166542345"
            locNameInfo["useOrgId"] = "2124321166542345"
            locNameInfo["trashName"] = locNameInfo["town"] + str(g_id)
            locNameInfo["projectId"] = "1061"
            locNameInfo["collectionState"] = 0
            locNameInfo["count"] = 1
            locNameInfo["day"] = 1
            locNameInfo["num"] = 1
            locNameInfo["assetNumber"] = "DFXM0000000" + str(g_id)
            insertTrash(locNameInfo)
            insertCarTrashRelation(g_id,vehicleId)
                # mutex.release()

if __name__ == '__main__':
    threading.Thread(target=work, args=(0, 60)).start()
    #threading.Thread(target=work, args=(10, 10)).start()
    # threading.Thread(target=work, args=(20, 10)).start()
    # threading.Thread(target=work, args=(30, 10)).start()
    # threading.Thread(target=work, args=(40, 20)).start()
