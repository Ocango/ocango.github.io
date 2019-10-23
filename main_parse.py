from pytz import timezone
from datetime import datetime
from func_tool.beautifulofmd import BeautifulOfMD,modify_image_tag
from models.projects import ProjectModel

#时区控制
cst_tz = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')

#时间处理
##时间判断
zone_to_text = {
    0:'深夜了，一盏孤灯下是否风景独好！',
    1:'早上好，Move along，nothing to see here。',
    2:'上午好，Work Work，Ready to work！',
    3:'中午好，大口吃饭，大碗喝酒！',
    4:'下午好，清茶奶酥，摇椅蒲扇！',
    5:'晚上好，More work？'
}
hour_to_zone = ((24,0,1,2,3,4),(5,6,7),(8,9,10,11),(12,),(13,14,15,16,17,18),(19,20,21,22,23))
##返回欢迎致辞
def welcome_home():
    utc_time = datetime.utcnow().replace(tzinfo=utc_tz)
    now_time = utc_time.astimezone(cst_tz)
    for i in range(len(hour_to_zone)):
        if now_time.hour in hour_to_zone[i]:
            welcome_text = zone_to_text.get(i,'Welcome！')
    welcome_text += '' +'今天是' + now_time.strftime('%m') + '月' + now_time.strftime('%d') + '日。'
    return welcome_text

#API功能库
##MarkDown转化HTML,
def exe_mdToHTML(my_content):
    '''传入content对象'''
    html = BeautifulOfMD()
    my_content.content_HTML = html.convert_to_HTML(my_content.content_md,modify_image_tag(my_content.id))

#articles接口功能库
def querystr(whereitem,wherestr):
    '''
    转置查询条件为可读，目前有：
    case whereitem:
    when link_project:主题：project_name
    when link_date:时间：xx年xx月
    otherwise:内容包含：xxxxx
    '''
    if whereitem == 'link_project':
        return "主题：" + ProjectModel.find_by_id(wherestr).name
    elif whereitem == 'link_date':
        return "时间：" + wherestr[2:4] + "年" + wherestr[5:7] + "月"
    else:
        return "内容包含：" + wherestr