#coding=utf-8
import datetime,time,re
from bs4 import BeautifulSoup
import sql_handle
from SeaSerpentFleet.get_base_html import *

COMPANY="sea serpent fleet"

def conv_time(st):
    now = st.split(".")
    return f"{now[2]}-{now[1]}-{now[0]}"

def get_today():
    today = datetime.date.today()
    return today

def get_now_data():
    # url = "https://www.seaserpentfleet.com/schedule"
    # res = requests.get(url)
    # soup = BeautifulSoup(res.text, 'lxml')
    res, soup = base_get_soup()
    it_content = soup.findAll("a", attrs={'href':re.compile('^#'), "class":re.compile('gradient-green-bg text-white$')})

    status = get_status(soup)
    places = get_places(res)
    prices = get_price(res)

    info = []
    for every in it_content:
        now = {}
        now["route_id"] = every["data-schedule-id"]
        now["start"] = conv_time(every["data-trip-start-date"])
        now["end"] = conv_time(every["data-trip-end-date"])
        now["boat"] = every["data-boat"]
        now["route"] = every["data-program"]
        now["departual"] = every["data-departual"]
        now["arrival"] = every["data-arrival"]
        now["status"] = next(status)
        now["places"] = next(places)
        now["price"] = next(prices)
        now["company"] = "sea serpent fleet"
        now["href"] = "https://www.seaserpentfleet.com/schedule"
        now["country"] = "Egypt"
        now["area"] = "Red Sea"
        info.append(now)
    print(info)
    print(info[0])
    return info





#获取船名
# def get_boats_list(soup):
#     boats = soup.findAll("a", attrs={"class": "dropdown-item", 'href': re.compile('^/boats')}, text=True)
#     print(boats)
#     # for boat in boats:
#     #     print(boat.text)
#     boats = [boat.text for boat in boats]
#     print(boats)
#     boats = list(set(boats))
#     print(boats)
#     return boats

#船的具体信息



#获取路线的状态
def get_status(soup):
    it_status = soup.findAll("td", attrs={'class':re.compile('^status')}, text=True)
    # print(it_status)
    print(len(it_status))
    # status_list = []
    status_list = [every.text.strip("\n") for every in it_status]
    print(status_list)
    status = iter(status_list)
    return status

#获取余位
def get_places(res):
    places = re.findall("\>(.*?)Free Places", res.text)
    places = iter(places)
    return places

#获取价格
def get_price(res):
    temp_prices = re.findall("Free Places \</td\>(.*?)\</td\>", res.text, re.DOTALL)
    print(temp_prices)
    prices = []
    for now in temp_prices:
        try:
            prices.append('€' + now.split('€')[1])
        except:
            prices.append("Request")
    print(prices)
    print(len(prices))
    prices = iter(prices)
    return prices



#main_route插入单条数据
def sea_sigle_insert(now, versionid=0):
    sql = f"insert into main_route(route_id, start, end, boat, route, departual, arrival, status, places, price, company, href, country, area, versionid) " \
        f"values(\"{now['route_id']}\",\"{now['start']}\",\"{now['end']}\",\"{now['boat']}\",\"{now['route']}\",\"{now['departual']}\"," \
        f"\"{now['arrival']}\",\"{now['status']}\",\"{now['places']}\",\"{now['price']}\"," \
        f"\"{now['company']}\",\"{now['href']}\",\"{now['country']}\",\"{now['area']}\", {versionid})"
    # print(sql)
    sql_handle.sql_excute(sql)


def excute_sql(sql):
    sql_handle.sql_excute(sql)

def sea_select(sql=f"SELECT * FROM main_route where company=\"{COMPANY}\""):
    return sql_handle.sql_search(sql)


#main_route更新数据
def main_route_update_data():
    new_info = get_now_data()
    new_ids = [data["route_id"] for data in new_info]
    now_db = sea_select()
    exist_ids = [data["route_id"] for data in now_db]
    print(exist_ids)

    # today = get_today()
    print("数据库数据为主...........................................")
    # print(new_ids)
    for data in now_db:
        if data["route_id"] not in new_ids:
            print(f"更新 公司【】 route_id【{data['route_id']}】为过期")
            # print(data)
            sql = f"update main_route set versionid=2 where id={data['id']} and company=\"{COMPANY}\""
            excute_sql(sql)

    print("网页数据为主...........................................")
    for data in new_info:
        #网页有的数据 数据库没有 直接insert 为正常状态
        if data["route_id"] not in exist_ids:
            print(f"插入route_id【{data['route_id']}】为完成")
            sea_sigle_insert(data)
        else:
            # 网页和数据库都存在的数据
            # insert一条状态为更新中的数据
            print(f"插入一条新数据 公司【{COMPANY}】 route_id【{data['route_id']}】状态为更新中")
            sea_sigle_insert(data, versionid=1)
            # update老数据为过期
            print(f"更新老数据 公司【{COMPANY}】 route_id【{data['route_id']}】为过期")
            sql = f"update main_route set versionid=2 where route_id=\"{data['route_id']}\" and versionid=0 and company=\"{COMPANY}\""
            excute_sql(sql)
            # update新数据为完成
            print(f"更新新数据 公司【{COMPANY}】 route_id【{data['route_id']}】为完成")
            sql = f"update main_route set versionid=0 where route_id=\"{data['route_id']}\" and versionid=1 and company=\"{COMPANY}\""
            excute_sql(sql)

    #删除过期数据
    print("清除过期数据...........................................................")
    sql = f"delete from main_route where versionid=2 and company=\"{COMPANY}\""
    excute_sql(sql)



t1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
main_route_update_data()
print(t1)
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))  )


