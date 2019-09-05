# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/apple/Downloads/flask")
from app import get_logger, get_config
from figure import *
from overview import *
from enents_list import *
from detail import *
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user 
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main

logger = get_logger(__name__)
cfg = get_config()


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
    entity_list = entity()
    ten_list = tablechart()
    line_chart = linechart()
    end_class_main, flask_source_main = main_hacker()
    return render_template('index.html',current_user=current_user,node_source0 = end_class_main,link_source0 = flask_source_main,entity_list = entity_list,line_chart = line_chart,ten_list = ten_list)

# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')

# 黑客用户画像查询
@main.route('/echats/<username>', methods=['GET', 'POST'])
def echats(username):
    temp_name = username
    try:
        user_infro,user_forums,field = user_information(username)
        user_rank_list, user_rank_value = rank_hacker(username,user_forums)
        user_posts = user_post(username)
        user_radar = one_user_radar(username)
        event_list = hacker_events(username)
    except:
        temp_name = username
        list_name = ['dannykld','diasporateam','b0nd','keenankholman','freeresources999','michaelcady','cyberdrain','msbachman','fust3rcluck']
        username = list_name[random.randint(0,8)]
        user_infro, user_forums, field = user_information(username)
        user_rank_list, user_rank_value = rank_hacker(username, user_forums)
        user_posts = user_post(username)
        user_radar = one_user_radar(username)
        event_list = hacker_events(username)
    return render_template('figure.html',username = temp_name,user_infro = user_infro,user_posts = user_posts,user_rank_list = user_rank_list,user_rank_value = user_rank_value,field = field,user_radar = user_radar,event_list = event_list)


# 黑客画像展示
@main.route('/figure', methods=['GET', 'POST'])
def figure():
    return render_template('echats.html')


# 最新事件列表展示
@main.route('/threats_list/<list_type>', methods=['GET', 'POST'])
def threats_list(list_type):
    if list_type == "new_threats":
        combine_list = new_list()
        topic = ["最新事件","全部事件"]
        new_alink  = "all_threats"
    else:
        combine_list = all_news_list()
        topic = ["全部事件", "最新事件"]
        new_alink = "new_threats"
    return render_template('newslist.html',combine_list = combine_list,topic = topic,alink = new_alink)


# 事件详情展示
@main.route('/event_detail', methods=['GET', 'POST'])
def event_detail():
    title = request.args.get('title')
    theme1 = request.args.get('theme1')
    theme2 = request.args.get('theme2')
    head_info = get_abstract(title)
    all_events_list,all_tigger,all_user = timeline_detail(title)
    domain_list, ip_list, cve_list, hash_list, email_list = get_allentity(title)
    all_relation_event = get_relative_event(title)
    return render_template('event_detail.html',theme1 = theme1,theme2 = theme2,head_info = head_info,all_events_list = all_events_list,domain_list = domain_list, ip_list = ip_list, cve_list = cve_list, hash_list = hash_list, email_list =  email_list,all_relation_event = all_relation_event)


# 事件细节展示
@main.route('/weibu1', methods=['GET', 'POST'])
def weibu1():
    return render_template('event_detail_1.html')

# 事件细节展示
@main.route('/weibu2', methods=['GET', 'POST'])
def weibu2():
    return render_template('event_detail_2.html')

# 事件细节展示
@main.route('/weibu3', methods=['GET', 'POST'])
def weibu3():
    return render_template('event_detail_3.html')

# 事件细节展示
@main.route('/weibu4', methods=['GET', 'POST'])
def weibu4():
    return render_template('event_detail_4.html')

# 事件细节展示
@main.route('/echarts', methods=['GET', 'POST'])
def echarts():
    return render_template('echats.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')
