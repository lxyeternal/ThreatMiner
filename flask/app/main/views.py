# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/apple/Downloads/flask")
from all_hacker import *
from main_hacker import *
from figure_hack import *
from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user 
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main

logger = get_logger(__name__)
cfg = get_config()

#  数据准备
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

new_sec_list = figure_users(sql_new, sql_0x00sec)
new_hackthissite_list = figure_users(sql_new, sql_hackthissite)
new_antionline_list = figure_users(sql_new, sql_antionline)
new_garage4hackers_list = figure_users(sql_new, sql_garage4hackers)
new_hacktoday_list = figure_users(sql_new, sql_hacktoday)
new_SafeSkyHacks_list = figure_users(sql_new, sql_SafeSkyHacks)

alive_sec_list = figure_users(sql_alive, sql_0x00sec)
alive_hackthissite_list = figure_users(sql_alive, sql_hackthissite)
alive_antionline_list = figure_users(sql_alive, sql_antionline)
alive_garage4hackers_list = figure_users(sql_alive, sql_garage4hackers)
alive_hacktoday_list = figure_users(sql_alive, sql_hacktoday)
alive_SafeSkyHacks_list = figure_users(sql_alive, sql_SafeSkyHacks)

all_sec_list = all_user(sql_all, sql_0x00sec)
all_hackthissite_list = all_user(sql_all, sql_hackthissite)
all_antionline_list = all_user(sql_all, sql_antionline)
all_garage4hackers_list = all_user(sql_all, sql_garage4hackers)
all_hacktoday_list = all_user(sql_all, sql_hacktoday)
all_SafeSkyHacks_list = all_user(sql_all, sql_SafeSkyHacks)

# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user)


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')

# 总体社交网络图
@main.route('/all_network', methods=['GET', 'POST'])
@login_required
def all_network():

    # return common_list(CfgNotify, 'all_network.html')
    return render_template('all_network.html',node_source = end_class,link_source = all_source,node_source0 = end_class_main,link_source0 = flask_source_main,node_source1 = class_forum_0x00sec_list,link_source1 = source_forum_0x00sec_list,node_source2 = class_forum_hackthissite_list,link_source2 = source_forum_hackthissite_list,node_source3 = class_forum_antionline_list,link_source3 = source_forum_antionline_list,node_source4 = class_forum_garage4hackers_list,link_source4 = source_forum_garage4hackers_list,node_source5 = class_forum_hacktoday_list,link_source5 = source_forum_hacktoday_list,node_source6 = class_forum_SafeSkyHacks_list,link_source6 = source_forum_SafeSkyHacks_list)

# top1000社交网络图
@main.route('/top1000', methods=['GET', 'POST'])
@login_required
def top1000():

    return render_template('top1000.html',node_source0 = end_class_main,link_source0 = flask_source_main)

# 0x00sec论坛社交网络图
@main.route('/0x00sec', methods=['GET', 'POST'])
@login_required
def _0x00sec():

    return render_template('0x00sec.html',node_source1 = class_forum_0x00sec_list,link_source1 = source_forum_0x00sec_list)

# hackthissite论坛社交网络图
@main.route('/hackthissite', methods=['GET', 'POST'])
@login_required
def hackthissite():

    return render_template('hackthissite.html',node_source2 = class_forum_hackthissite_list,link_source2 = source_forum_hackthissite_list)

# antionline论坛社交网络图
@main.route('/antionline', methods=['GET', 'POST'])
@login_required
def antionline():

    return render_template('antionline.html',node_source3 = class_forum_antionline_list,link_source3 = source_forum_antionline_list)

# garage4hackers论坛社交网络图
@main.route('/garage4hackers', methods=['GET', 'POST'])
@login_required
def garage4hackers():

    return render_template('garage4hackers.html',node_source4 = class_forum_garage4hackers_list,link_source4 = source_forum_garage4hackers_list)

# hacktoday论坛社交网络图
@main.route('/hacktoday', methods=['GET', 'POST'])
@login_required
def hacktoday():

    return render_template('hacktoday.html',node_source5 = class_forum_hacktoday_list,link_source5 = source_forum_hacktoday_list)

# safeSkyHacks论坛社交网络图
@main.route('/safeSkyHacks', methods=['GET', 'POST'])
@login_required
def safeSkyHacks():

    return render_template('safeSkyHacks.html',node_source6 = class_forum_SafeSkyHacks_list,link_source6 = source_forum_SafeSkyHacks_list)

# 黑客用户画像查询
@main.route('/echats', methods=['GET', 'POST'])
@login_required
def echats():
    return render_template('echats.html')

# 0x00sec论坛用户画像查询
@main.route('/table_0x00sec', methods=['GET', 'POST'])
@login_required
def table_0x00sec():
    return render_template('table_0x00sec.html',new_sec_list = new_sec_list,alive_sec_list = alive_sec_list,all_sec_list = all_sec_list)

# hackthissite论坛用户画像查询
@main.route('/table_hackthissite', methods=['GET', 'POST'])
@login_required
def table_hackthissite():
    return render_template('table_hackthissite.html',new_hackthissite_list = new_hackthissite_list,alive_hackthissite_list = alive_hackthissite_list,all_hackthissite_list = all_hackthissite_list)

# antionline论坛用户画像查询
@main.route('/table_antionline', methods=['GET', 'POST'])
@login_required
def table_antionline():
    return render_template('table_antionline.html',new_antionline_list = new_antionline_list,alive_antionline_list = alive_antionline_list,all_antionline_list = all_antionline_list)

# garage4hackers论坛用户画像查询
@main.route('/table_garage4hackers', methods=['GET', 'POST'])
@login_required
def table_garage4hackers():
    return render_template('table_garage4hackers.html',new_garage4hackers_list = new_garage4hackers_list,alive_garage4hackers_list = alive_garage4hackers_list,all_garage4hackers_list = all_garage4hackers_list)

# hacktoday论坛用户画像查询
@main.route('/table_hacktoday', methods=['GET', 'POST'])
@login_required
def table_hacktoday():
    return render_template('table_hacktoday.html',new_hacktoday_list = new_hacktoday_list,alive_hacktoday_list = alive_hacktoday_list,all_hacktoday_list = all_hacktoday_list)

# safeSkyHacks论坛用户画像查询
@main.route('/table_safeSkyHacks', methods=['GET', 'POST'])
@login_required
def table_safeSkyHacks():
    return render_template('table_safeSkyHacks.html',new_SafeSkyHacks_list = new_sec_list,alive_SafeSkyHacks_list = alive_SafeSkyHacks_list,all_SafeSkyHacks_list = all_SafeSkyHacks_list)

# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')
