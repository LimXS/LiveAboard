#coding=utf-8
import re
import sql_handle
from SeaSerpentFleet.get_base_html import *
import logdebug

COMPANY="sea serpent fleet"

#获取船名
def get_boats_menu():
    res, soup = base_get_soup()
    boats_info = soup.findAll("a", attrs={"class": "dropdown-item", 'href': re.compile('^/boats')}, text=True)
    boats = [boat.text for boat in boats_info]
    boats = sorted(set(boats), key=boats.index)
    print(boats)

    boats_href=[boat["href"] for boat in boats_info]
    boats_href = sorted(set(boats_href),key=boats_href.index)
    print(boats_href)

    return boats, boats_href



def get_boat_description(soup):
    desc = soup.findAll("p", attrs={"class": "text-nm grey-text text-medium line-h-sm"})
    return desc[0].text

def get_boat_accommodation(soup):
    desc = soup.findAll("p", attrs={"class": "text-nm white-text text-medium line-h-sm"})
    return desc[0].text


def get_boat_main_infos(soup):
    infos = soup.findAll("span", attrs={"class": "text-sm text-medium white-text"})
    info = [info.text for info in infos]
    return info



def select_main_boats(boat=None):
    sql = f"SELECT * FROM main_boat where company=\"{COMPANY}\""
    if boat is not None:
        sql += f" and boat=\"{boat}\" "
    return sql_handle.sql_search(sql)

def update_main_boats(boat, new, loc=None):
    sql = f"update main_boat set versionid={new} where boat=\"{boat}\"  and company=\"{COMPANY}\" "
    if loc is not None:
        sql += f" and versionid={loc}"
    sql_handle.sql_excute(sql)

def insert_main_boat(boat, guest, length, width, speed, wifi, nitrox, description, accommodation,
                     description_zh="", accommodation_zh="", versionid=0):
    sql = f"INSERT INTO main_boat (company, boat, guest, length, width, speed, wifi, nitrox, description, accommodation,description_zh, accommodation_zh, versionid) " \
        f"VALUES(\"{COMPANY}\", \"{boat}\", \"{guest}\", \"{length}\", '{width}', \"{speed}\", \"{wifi}\", \"{nitrox}\", \"{description}\"," \
        f" \"{accommodation}\", \"{description_zh}\", \"{accommodation_zh}\", {versionid})"
    # print(sql)
    sql_handle.sql_excute(sql)

def clear_main_boat_data():
    sql = f"delete from main_boat where versionid=2 and company=\"{COMPANY}\""
    sql_handle.sql_excute(sql)



def change_zh(sql_data, data_en, sql_str_en="description", sql_str_zh="description_zh"):
    if sql_data[sql_str_en] != data_en:
        description_zh = ""
        logdebug.addlogmes("INFO", "数据源变动 decription 请修改中文翻译", f"公司【{COMPANY}】船【{sql_data['boat']}】")
    else:
        description_zh = sql_data[sql_str_zh]
    return description_zh


def main_boat_update_data():
    new_boats, boats_href = get_boats_menu()
    use = iter(new_boats)

    now_boats = select_main_boats()
    exist_boats = [boat["boat"] for boat in now_boats]

    for boat in exist_boats:
        if boat not in new_boats:
            print(f"数据库中【{COMPANY}】该船【{boat}】网页返回值中不在 更新状态为过期.......................")
            update_main_boats(boat, 2, 0)


    for href in boats_href:
        boat = next(use)
        res, soup = base_get_detail(href.strip())

        description = get_boat_description(soup)
        accommodation = get_boat_accommodation(soup)
        infos = iter(get_boat_main_infos(soup))
        # print(infos)

        if boat not in exist_boats:
            print(f"数据库中【{COMPANY}】没有该船【{boat}】网页返回值有 是新船 直接新增")
            insert_main_boat(boat, next(infos), next(infos), next(infos), next(infos), next(infos), next(infos), description, accommodation)

        else:
            sql_data = select_main_boats(boat)[0]
            description_zh = change_zh(sql_data, description, "description", "description_zh")
            accommodation_zh = change_zh(sql_data, accommodation, "accommodation", "accommodation_zh")

            # if description_zh or accommodation_zh =="":
            print(f"插入一条新数据 公司【{COMPANY}】 boat【{boat}】 状态为更新中")
            insert_main_boat(boat, next(infos), next(infos), next(infos), next(infos), next(infos), next(infos),
                             description, accommodation, description_zh, accommodation_zh, versionid=1)

            # update老数据为过期
            print(f"更新老数据 公司【{COMPANY}】 boat【{boat}】 状态为过期")
            update_main_boats(boat, 2, 0)

            # update新数据为完成
            print(f"更新新数据 公司【{COMPANY}】 boat【{boat}】 状态为完成")
            update_main_boats(boat, 0, 1)

    print("清除过期数据...........................................................")
    clear_main_boat_data()




main_boat_update_data()



# get_boats_menu()

main_boat_update_data()


def room_type_update_data():
    pass


def accommodations_update_data():
    pass


def food_beverage_update_data():
    pass