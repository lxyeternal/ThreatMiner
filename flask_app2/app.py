#coding:utf-8

from flask import Flask,render_template,url_for
# from all_hacker import *
# from main_hacker import *

#生成Flask实例
app = Flask(__name__)
@app.route('/')
def my_echart():

    # all_source = getcsv()                                           # 所有黑客的关系指向格式化数据
    # end_class, class_user,user_format_class = networkclass()        # end_class:所有黑客的分类格式化数据
    # class_one_network = onenetwork(all_source, class_user)
    #
    # class_forum_0x00sec_list = user_format_class[0]                 # forum_0x00sec论坛的黑客的格式化数据
    # class_forum_hackthissite_list = user_format_class[1]            # forum_hackthissite论坛的黑客的格式化数据
    # class_forum_antionline_list = user_format_class[2]              # forum_antionline论坛的黑客的格式化数据
    # class_forum_garage4hackers_list = user_format_class[3]          # forum_garage4hackers论坛的黑客的格式化数据
    # class_forum_hacktoday_list = user_format_class[4]               # forum_hacktoday论坛的黑客的格式化数据
    # class_forum_SafeSkyHacks_list = user_format_class[5]            # forum_SafeSkyHacks论坛的黑客的格式化数据
    #
    # source_forum_0x00sec_list = class_one_network[0]                # forum_0x00sec论坛中的黑客之间的关系的格式化数据
    # source_forum_hackthissite_list = class_one_network[1]           # forum_hackthissite论坛中的黑客之间的关系的格式化数据
    # source_forum_antionline_list = class_one_network[2]             # forum_antionline论坛中的黑客之间的关系的格式化数据
    # source_forum_garage4hackers_list = class_one_network[3]         # forum_garage4hackers论坛中的黑客之间的关系的格式化数据
    # source_forum_hacktoday_list = class_one_network[4]              # forum_hacktoday论坛中的黑客之间的关系的格式化数据
    # source_forum_SafeSkyHacks_list = class_one_network[5]           # forum_SafeSkyHacks论坛中的黑客之间的关系的格式化数据
    #
    # all_source_main = getcsv_mian()
    # end_class_main, user_list = networkclass_mian()                 # end_class_main:前1000个黑客分类的格式化数据
    # flask_source_main = source_main(all_source_main, user_list)     # flask_source_main：前1000个黑客之间的关系的格式化数据

    test_data = [5, 20, 36, 10, 10, 20]
    test_source = [{'source': 'shay', 'target': 'mahrsheelab', 'weight': 1}, {'source': 'shay', 'target': 'zorolord', 'weight': 3}, {'source': 'shay', 'target': 'bindu7', 'weight': 1}, {'source': 'shay', 'target': 'antogginly', 'weight': 1}]
    test_node = [{'category': 4, 'name': 'nishant', 'value': 4}, {'category': 4, 'name': 'hackethis29', 'value': 1}, {'category': 4, 'name': 'digitalyatri', 'value': 2}, {'category': 6, 'name': 'xxclickalotxx123', 'value': 2}]
#在浏览器上渲染my_templaces.html模板

    return render_template('my_template.html',node_source = str(test_node),link_source = str(test_source))
    # return render_template('my_template.html')


if __name__ == "__main__":
    #运行项目
    app.run(debug = True)
