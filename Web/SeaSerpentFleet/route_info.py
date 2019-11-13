#coding=utf-8
import re
import sql_handle
from SeaSerpentFleet.get_base_html import *
import logdebug
COMPANY="sea serpent fleet"

#获取路线名
def get_routes_menu():
    res, soup = base_get_soup()
    routs = soup.findAll("a", attrs={"class": "dropdown-item", 'href': re.compile('^/itineraries')}, text=True)
    # print(routs)
    print("-------------------------------")

    routes_href=[route["href"] for route in routs]
    routes_href = sorted(set(routes_href),key=routes_href.index)
    print(routes_href)

    routes = [rout.text for rout in routs]
    routes = sorted(set(routes),key=routes.index)
    print(routes)
    return routes, routes_href

# get_routes_menu()


#路线描述
def get_route_decription(soup):
    for elem in soup.find_all(["br"]):
        elem.replace_with(elem.text + "\n")
    desc = soup.findAll("p", attrs={"class": "text-nm grey-text text-medium line-h-sm"})
    return desc[0].text

#获取具体行程
def get_route_itinerary(soup):
    arrange = soup.findAll("p", attrs={"class": "text-half-nm"})
    arrange = [arg.text for arg in arrange]
    itinerary = ""
    for n in range(len(arrange)):
        itinerary += f"Day{str(n + 1)}{arrange[n]}"
    return itinerary


#获取潜点名称
def get_route_sites(soup):
    sites = soup.findAll("h3", attrs={"class": "text-lg text-bold grey-text"})
    sites = [site.text for site in sites]
    return sites


#获取潜点深度 难度
def get_sites_info(soup):
    infos = soup.findAll("span", attrs={"class": "text-nm"})
    times = int(len(infos)/2)
    now = iter(infos)
    depth = []
    difficulty = []
    for info in range(times):
        depth.append(next(now).text)
        difficulty.append(next(now).text)
    return depth, difficulty

#route_detail表的处理
def insert_route_detail(route, decription, itinerary, versionid=0, description_zh="", day_arrange_zh=""):
    sql = f"INSERT INTO route_detail(company, route, description, day_arrange, versionid, description_zh, day_arrange_zh) " \
        f"VALUES(\"{COMPANY}\", \"{route}\", \"{decription}\", \"{itinerary}\", '{versionid}', \"{description_zh}\", \"{day_arrange_zh}\")"
    print(sql)
    sql_handle.sql_excute(sql)


def update_route_detail(route, new=0, loc=None):
    sql = f"update route_detail set versionid={new} where route=\"{route}\"  and company=\"{COMPANY}\""
    if loc is not None:
        sql += f" and versionid={loc}"
    print(sql)
    sql_handle.sql_excute(sql)


#route_detail表的查询
def route_detail_select(route=None):
    sql=f"SELECT * FROM route_detail where company=\"{COMPANY}\""
    if route is not None:
        sql += f" and route=\"{route}\" "

    return sql_handle.sql_search(sql)

def clear_over_data():
    sql = f"delete from route_detail where versionid=2 and company=\"{COMPANY}\""
    sql_handle.sql_excute(sql)


#route_site_detail 表的新增
def insert_site_detail(route, site, depth, diffculty, rank, versionid=0):
    sql = f"INSERT INTO route_site_detail(company, route, site, depth, difficulty, rank, versionid)" \
        f" VALUES(\"{COMPANY}\",\"{route}\",'{site}','{depth}','{diffculty}',{rank},'{versionid}')"
    print(sql)
    sql_handle.sql_excute(sql)

#route_site_detail更新
def update_route_site_detail(route, new, loc=None, site=None):
    sql = f"update route_site_detail set versionid={new} where route=\"{route}\"  and company=\"{COMPANY}\" "
    if loc is not None:
        sql += f" and versionid={loc}"
    if site is not None:
        sql += f" and site=\"{site}\" "
    # print(sql)
    sql_handle.sql_excute(sql)


#route_site_detail表的查询
def site_detail_select(route=None):
    sql=f"SELECT * FROM route_site_detail where company=\"{COMPANY}\""
    if route is not None:
        sql += f" and route=\"{route}\" "
    return sql_handle.sql_search(sql)


def clear_sites_data():
    sql = f"delete from route_site_detail where versionid=2 and company=\"{COMPANY}\""
    sql_handle.sql_excute(sql)


#潜点表更新
def update_site_table():
    new_routes, routes_href = get_routes_menu()
    use = iter(new_routes)

    now_sites = site_detail_select()
    exist_site_routes = [site["route"] for site in now_sites]


    for route in exist_site_routes:
        if route not in new_routes:
            print(f"数据库中[【{COMPANY}】该路线【{route}】网页返回值中不在 更新状态为过期.......................")
            update_route_site_detail(route, 2, 0)


    for href in routes_href:
        route = next(use)
        res, soup = base_get_detail(href.strip())
        print(route)
        sites = get_route_sites(soup)
        depth, difficulty = get_sites_info(soup)

        print(sites)
        print(depth)
        print(difficulty)


        if route in exist_site_routes:
            exist_sites = [site["site"] for site in site_detail_select(route)]

            for site in exist_sites:
                if site not in sites:
                    print(f"数据库里面的这个公司【{COMPANY}】路线【{route}】潜点【{site}】网页返回值里面 不在 更新状态为过期")
                    update_route_site_detail(route, 2, 0, site)



        #网页存在数据库不存在
        print("网页为主.......................")
        if route not in exist_site_routes:
            # 如果整条路线不存在 直接新增
            for n in range(len(sites)):
                print(f"该公司【{COMPANY}】路线【{route}】是新路线 直接新增新潜点【{sites[n]}】")
                insert_site_detail(route, sites[n], depth[n], difficulty[n], n+1)
        else:
            #如果路线存在 则检查潜点是否存在
            route_sites = site_detail_select(route)
            exist_sites = [site["site"] for site in route_sites]
            for n in range(len(sites)):
                if sites[n] not in exist_sites:
                    #如果不存在 直接新增
                    print(f"该公司【{COMPANY}】路线【{route}】路线是新潜点【{sites[n]}】 直接新增")
                    insert_site_detail(route, sites[n], depth[n], difficulty[n], n + 1)
                else:
                    #如果存在在则进行更新
                    # insert一条状态为更新中的数据
                    print(f"插入一条新数据 公司【{COMPANY}】 route【{route}】 site【{sites[n]}】状态为更新中")
                    insert_site_detail(route, sites[n], depth[n], difficulty[n], n + 1, versionid=1)
                    # update老数据为过期
                    print(f"更新老数据 公司【{COMPANY}】 route【{route}】 site【{sites[n]}】 状态为过期")
                    update_route_site_detail(route, 2, 0, sites[n])
                    # update新数据为完成
                    print(f"更新新数据 公司【{COMPANY}】 route【{route}】 site【{sites[n]}】 状态为完成")
                    update_route_site_detail(route, 0, 1, sites[n])

    print("清除过期数据...........................................................")
    clear_sites_data()




def update_route_table():
    new_routes, routes_href = get_routes_menu()
    use = iter(new_routes)

    now_routes = route_detail_select()
    exist_route = [data["route"] for data in now_routes]


    print("数据库数据为主...........................................")
    # print(new_ids)
    for data in now_routes:
        if data["route"] not in new_routes:
            print(f"更新 路线 route【{data['route']}】为过期")
            update_route_detail(data["route"], 2)


    print("网页新数据为主...........................................")
    for href in routes_href:
        route = next(use)
        res, soup = base_get_detail(href.strip())
        print(route)
        description = get_route_decription(soup)
        itinerary = get_route_itinerary(soup)

        # 网页有的数据 数据库没有 直接insert 为正常状态
        if route not in exist_route:
            print(f"插入route【{route}】为完成")
            insert_route_detail(route, description, itinerary)
        else:
            # 网页和数据库都存在的数据
            # insert一条状态为更新中的数据
            sql_data = route_detail_select(route)
            # print(sql_data)
            if sql_data[0]["description"] != description:
                description_zh = ""
                logdebug.addlogmes("INFO", "数据源变动 description 请修改中文翻译", f"公司【{COMPANY}】路线【{route}】")
            else:
                description_zh = sql_data[0]["description_zh"]

            if sql_data[0]["day_arrange"] != itinerary:
                day_arrange_zh = ""
                logdebug.addlogmes("INFO", "数据源变动 day_arrange 请修改中文翻译", f"公司【{COMPANY}】路线【{route}】")
            else:
                day_arrange_zh = sql_data[0]["day_arrange_zh"]

            if day_arrange_zh or description_zh =="":
                print(f"插入一条新数据 公司【{COMPANY}】 route【{route}】 状态为更新中")
                insert_route_detail(route, description, itinerary, versionid=1, description_zh=description_zh, day_arrange_zh=day_arrange_zh)
                # update老数据为过期
                print(f"更新老数据 公司【{COMPANY}】 route【{route}】 状态为过期")
                update_route_detail(route, 2, 0)

                # update新数据为完成
                print(f"更新新数据 公司【{COMPANY}】 route【{route}】 状态为完成")
                update_route_detail(route, 0, 1)


    # 删除过期数据
    print("清除过期数据...........................................................")
    clear_over_data()

update_route_table()
# update_site_table()

