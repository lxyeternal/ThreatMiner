#coding:utf-8

from flask import Flask,render_template
from all_hacker import *
from main_hacker import *

#生成Flask实例
app = Flask(__name__)
@app.route('/')
def my_echart():

    all_source = getcsv()                                           # 所有黑客的关系指向格式化数据
    end_class, class_user,user_format_class = networkclass()        # end_class:所有黑客的分类格式化数据
    class_one_network = onenetwork(all_source, class_user)

    class_forum_0x00sec_list = user_format_class[0]                 # forum_0x00sec论坛的黑客的格式化数据
    class_forum_hackthissite_list = user_format_class[1]            # forum_hackthissite论坛的黑客的格式化数据
    class_forum_antionline_list = user_format_class[2]              # forum_antionline论坛的黑客的格式化数据
    class_forum_garage4hackers_list = user_format_class[3]          # forum_garage4hackers论坛的黑客的格式化数据
    class_forum_hacktoday_list = user_format_class[4]               # forum_hacktoday论坛的黑客的格式化数据
    class_forum_SafeSkyHacks_list = user_format_class[5]            # forum_SafeSkyHacks论坛的黑客的格式化数据

    source_forum_0x00sec_list = class_one_network[0]                # forum_0x00sec论坛中的黑客之间的关系的格式化数据
    source_forum_hackthissite_list = class_one_network[1]           # forum_hackthissite论坛中的黑客之间的关系的格式化数据
    source_forum_antionline_list = class_one_network[2]             # forum_antionline论坛中的黑客之间的关系的格式化数据
    source_forum_garage4hackers_list = class_one_network[3]         # forum_garage4hackers论坛中的黑客之间的关系的格式化数据
    source_forum_hacktoday_list = class_one_network[4]              # forum_hacktoday论坛中的黑客之间的关系的格式化数据
    source_forum_SafeSkyHacks_list = class_one_network[5]           # forum_SafeSkyHacks论坛中的黑客之间的关系的格式化数据

    all_source_main = getcsv_mian()
    end_class_main, user_list = networkclass_mian()                 # end_class_main:前1000个黑客分类的格式化数据
    flask_source_main = source_main(all_source_main, user_list)     # flask_source_main：前1000个黑客之间的关系的格式化数据

#在浏览器上渲染my_templaces.html模板

    return render_template('my_template.html',node_source = end_class,link_source = all_source,node_source0 = end_class_main,link_source0 = flask_source_main,node_source1 = class_forum_0x00sec_list,link_source1 = source_forum_0x00sec_list,node_source2 = class_forum_hackthissite_list,link_source2 = source_forum_hackthissite_list,node_source3 = class_forum_antionline_list,link_source3 = source_forum_antionline_list,node_source4 = class_forum_garage4hackers_list,link_source4 = source_forum_garage4hackers_list,node_source5 = class_forum_hacktoday_list,link_source5 = source_forum_hacktoday_list,node_source6 = class_forum_SafeSkyHacks_list,link_source6 = source_forum_SafeSkyHacks_list)

if __name__ == "__main__":
    #运行项目
    app.run(debug = True)
