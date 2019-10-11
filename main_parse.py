from pytz import timezone
from datetime import datetime

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

#index功能库