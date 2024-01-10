import psycopg2

# 检查Python版本
from sys import version_info
if version_info.major != 3:
    raise Exception('请使用Python 3 来完成此项目')


sql_data = '''

SELECT all_date.create_date, project.group_name,project.project_name,car.cars,use_eq_car.cars as use_cars,智能手环 as 智能手环,老年机 as 老年机,卡片机 as 卡片机,对讲机 as 对讲机,
桑德盒子 as 桑德盒子,GPS定位仪 as GPS定位仪,超声波油感探测器 as 超声波油感探测器,RFID读卡器 as RFID读卡器,RFID发卡器 as RFID发卡器,
渗沥液传感器 as 渗沥液传感器,智能水表 as 智能水表,智能电表 as 智能电表,人流量监控设备 as 人流量监控设备,满溢传感器 as 满溢传感器,
地埋桶传感器 as 地埋桶传感器,柠檬科技 as 柠檬科技,中导GPS as 中导GPS FROM (
select to_char(create_date,'yyyy-MM-dd') create_date,project_id,count(id) as cars from
so_base_car WHERE project_id  = \'{0}\' GROUP BY project_id,to_char(create_date,'yyyy-MM-dd') 
) car
RIGHT JOIN (
SELECT to_char(create_date,'yyyy-MM-dd') create_date FROM (
SELECT create_date FROM so_base_car WHERE project_id = \'{0}\' UNION SELECT create_date from so_base_equipment WHERE project_id = \'{0}\'
) t GROUP BY to_char(create_date,'yyyy-MM-dd') ORDER BY create_date 
) all_date on car.create_date = all_date.create_date
left join (
SELECT to_char(car.create_date,'yyyy-MM-dd') create_date,car.project_id,count(car.id) cars FROM so_base_car car 
inner join so_base_car_equipment_detail detail on car.id = detail.so_vehicleinfo_id 
inner join so_base_equipment equipment on detail.so_equipment_id = equipment.id
WHERE car.project_id = \'{0}\'
GROUP BY car.project_id,to_char(car.create_date,'yyyy-MM-dd')
)
use_eq_car on use_eq_car.create_date = all_date.create_date
left join (
SELECT  create_date,sum(智能手环) as 智能手环,sum(老年机) as 老年机,sum(卡片机) as 卡片机,sum(对讲机) as 对讲机,
sum(桑德盒子) as 桑德盒子,sum(GPS定位仪) as GPS定位仪,sum(超声波油感探测器) as 超声波油感探测器,sum(RFID读卡器) as RFID读卡器,sum(RFID发卡器) as RFID发卡器,
sum(渗沥液传感器) as 渗沥液传感器,sum(智能水表) as 智能水表,sum(智能电表) as 智能电表,sum(人流量监控设备) as 人流量监控设备,sum(满溢传感器) as 满溢传感器,
sum(地埋桶传感器) as 地埋桶传感器,sum(柠檬科技) as 柠檬科技,sum(中导GPS) as 中导GPS
FROM crosstab(
'SELECT
e.create_date,
	e.project_id,
	ts.NAME,
	e.num 
FROM
	t_s_category ts
	RIGHT JOIN ( 
		SELECT 
		to_char( create_date, ''yyyy-MM-dd'' ) create_date,
		project_id, asset_type,
		COUNT ( ID ) AS num
		FROM so_base_equipment WHERE project_id = '\'{0}\''
		GROUP BY asset_type, project_id, to_char( create_date, ''yyyy-MM-dd'' ) ) e
	ON ts.code = e.asset_type',$$values('老年机'), ('卡片机'), ('对讲机'),('智能手环'),('桑德盒子'),('GPS定位仪'),
('超声波油感探测器'),('RFID读卡器'),('RFID发卡器'),('渗沥液传感器'),('智能水表'),('智能电表'),('人流量监控设备'),('满溢传感器'),
('地埋桶传感器'),('柠檬科技'),('中导GPS')$$)
as score(create_date VARCHAR,project_id VARCHAR, 老年机 int, 卡片机 int, 对讲机 int,智能手环 int,
桑德盒子 int, GPS定位仪 int,超声波油感探测器 int, RFID读卡器 int, RFID发卡器 int,
渗沥液传感器 int, 智能水表 int, 智能电表 int,人流量监控设备 int, 满溢传感器 int,
地埋桶传感器 int, 柠檬科技 int, 中导GPS int) GROUP BY project_id,create_date ORDER BY create_date
) eachEqu on eachEqu.create_date = all_date.create_date
,
(
SELECT gp.group_name,pro.id,pro.project_name FROM so_project_info pro left join so_project_group_relation relation on pro.id = relation.project_id
LEFT JOIN so_project_group gp on relation.group_id = gp.id WHERE pro.id = \'{0}\'
) project 


'''


sql_all_project_id = '''
SELECT id from so_project_info
'''
conn=psycopg2.connect(database="marscloud-parent",user="postgres",password="marscloud",host="192.168.1.48",port="5432")
curs=conn.cursor()


curs.execute(sql_all_project_id)
projectIds = curs.fetchall()

for projectId in projectIds:
    curs.execute(sql_data.format(projectId[0]))
    alldate = curs.fetchall()
    for date in alldate:
        print(date)



