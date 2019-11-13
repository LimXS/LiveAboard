#*-* coding:UTF-8 *-*

import tkinter as tk
import sql_handle


def company_select():
    sql=f"SELECT * FROM company_list "
    return sql_handle.sql_search(sql)


def all_route():
    sql = f"SELECT * FROM route_detail"
    return sql_handle.sql_search(sql)


def all_boat():
    sql = f"SELECT * FROM main_boat"
    return sql_handle.sql_search(sql)





def route_detail_select(need="description_zh", company=None):
    sql = f"SELECT * FROM route_detail where {need}=\"\""
    if company is not None:
        sql += f" and company=\"{company}\""
    return sql_handle.sql_search(sql)


def sigle_data_select(boat=None, route=None, company=None):
    if boat is not None:
        sql = f"SELECT * FROM main_boat where boat=\"{boat}\""
    if route is not None:
        sql = f"SELECT * FROM route_detail where route=\"{route}\""
    if company is not None:
        sql += f" and company=\"{company}\""
    print(sql)
    return sql_handle.sql_search(sql)

def main_data_select(need="description_zh", company=None, boat=None, table="main_boat", route=None):
    sql = f"SELECT * FROM {table} where {need}=\"\""
    if company is not None:
        sql += f" and company=\"{company}\""
    if boat is not None:
        sql += f" and boat=\"{boat}\""
    if route is not None:
        sql += f" and route=\"{route}\""
    print(sql)
    return sql_handle.sql_search(sql)


def sql_update_data(update_str, data, match=None, table="boat"):
    if table=="boat":
        sql = f"update main_boat set {update_str}=\"{data}\" where boat=\"{match}\""
    else:
        sql = f"update route_detail set {update_str}=\"{data}\" where route=\"{match}\""


    print(sql)
    sql_handle.sql_excute(sql)




def listbox_show():
    boats_need_des_update = main_data_select()
    boat1 = [dc_zh["boat"] + "-description_zh-boat" for dc_zh in boats_need_des_update]
    boats_need_acc_update = main_data_select("accommodation_zh")
    boat2 = [dc_zh["boat"] + "-accommodation_zh-boat" for dc_zh in boats_need_acc_update]
    boats_lists = boat1 + boat2

    route_need_des_update = main_data_select(table="route_detail")
    route1 = [dc_zh["route"] + "-description_zh-route" for dc_zh in route_need_des_update]
    route_need_day_update = main_data_select("day_arrange_zh", table="route_detail")
    route2 = [dc_zh["route"] + "-day_arrange_zh-route" for dc_zh in route_need_day_update]
    routes_lists = route1 + route2
    print(routes_lists)

    update_lists = boats_lists + routes_lists
    return update_lists



now_boat = all_boat()
now_route = all_route()
route1 = [dc_zh["route"]+"-description_zh-route" for dc_zh in now_route]
route2 = [dc_zh["route"]+"-day_arrange_zh-route" for dc_zh in now_route]

boat1 = [dc_zh["boat"]+"-description_zh-boat" for dc_zh in now_boat]
boat2 = [dc_zh["boat"]+"-accommodation_zh-boat" for dc_zh in now_boat]

# all_boats =
# all_routes =
all_list = boat1 +boat2 + route1 + route2


window = tk.Tk() # 第1步，实例化object，建立窗口window
window.title('My Window') # 第2步，给窗口的可视化起名字
window.geometry('600x350')  # 这里的乘是小x # 第3步，设定窗口的大小(长 * 宽)

# var1 = tk.StringVar()  # 创建变量，用var1用来接收鼠标点击具体选项的内容   # 第4步，在图形界面上创建一个标签label用以显示并放置
# l = tk.Label(window, bg='yellow',  font=('Arial', 10), width=25, height=17, textvariable=var1,
#              wraplength = 200,justify = tk.LEFT, takefocus=True).place(x=0, y=0)
scr2 = tk.Scrollbar()
l = tk.Text(window, width =27, height=20, font=("Arial", 10, "bold"), wrap=tk.WORD)
l.place(x=0, y=0)


# 第6步，创建一个方法用于按钮的点击事件
def print_selection():
    # value = lb.get(lb.curselection())  # 获取当前选中的文本
    which = text.get('1.0',tk.END)
    value = lb.get(lb.curselection())
    print(value)
    print(which)
    args = value.split("-")
    print(args)
    sql_update_data(args[1], which, args[0], args[2])





def show_data():
    value = lb.get(lb.curselection())  # 获取当前选中的文本
    values = value.split("-")
    print(values)
    if values[-1] == "boat":
        data = sigle_data_select(boat=values[0])[0]
    else:
        data = sigle_data_select(route=values[0])[0]
    l.delete('1.0', 'end')
    l.insert(tk.INSERT, data[values[1][:-3]])
    # var1.set(data[values[1][:-3]])  # 为label设置值
    text.delete('1.0', 'end')
    text.insert(tk.INSERT, data[values[1]])


def show_all():
    lb.delete(0,tk.END)
    for item in all_list:
        lb.insert('end', item)
    text.delete('1.0', 'end')

def show_changes():
    lb.delete(0,tk.END)
    for item in listbox_show():
        lb.insert('end', item)
    text.delete('1.0', 'end')






b2 = tk.Button(window, text='全部数据', width=10, height=1, command=show_all)
# 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
b2.pack(pady=1)
#

b3 = tk.Button(window, text='需更新的网页数据', width=15, height=1, command=show_changes) # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
b3.pack(pady=1)

# 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
b1 = tk.Button(window, text='更新翻译', width=10, height=1, command=print_selection)
b1.pack(pady=1)



# 第7步，创建Listbox并为其添加内容
# 创建Listbox
topF = tk.Frame(window)
topF.pack(fill=tk.Y, expand=tk.YES)

lb = tk.Listbox(topF, exportselection=False, width=25,  height=10)
lb.pack(side=tk.LEFT, fill=tk.Y, expand=tk.YES)


for item in listbox_show():
    lb.insert('end', item)  # 从最后一个位置开始加入值

scroll = tk.Scrollbar(topF, command=lb.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
# 设置self.lb的纵向滚动影响scroll滚动条
lb.configure(yscrollcommand=scroll.set)
lb.bind("<<ListboxSelect>>", lambda event, need="description":show_data())

text = tk.Text(window, width =27, height=20, font=("Arial", 10, "bold"), wrap=tk.WORD)
text.place(x=400, y=10)

window.mainloop()


# def rand_func(self, a, b, c):
#     print
#     "self:", self, "a:", a, "b:", b, "c:", c
#     print(a + b + c)
#
# self.frame.bind("<Return>",
#                         lambda event, a=10, b=20, c=30:
#                             self.rand_func(a, b, c))