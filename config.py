# 山东省16个地市教育局网站配置
WEBSITES = {
    "济南市教育局": "http://jnedu.jinan.gov.cn/",
    "青岛市教育局": "http://edu.qingdao.gov.cn/",
    "淄博市教育局": "http://edu.zibo.gov.cn/",
    "枣庄市教育局": "http://edu.zaozhuang.gov.cn/",
    "东营市教育局": "http://dyjy.dongying.gov.cn/",
    "烟台市教育局": "http://jyj.yantai.gov.cn/",
    "潍坊市教育局": "http://jyj.weifang.gov.cn/",
    "济宁市教育局": "http://jnjy.jining.gov.cn/",
    "泰安市教育局": "http://jyj.taian.gov.cn/",
    "威海市教育局": "http://jyj.weihai.gov.cn/",
    "日照市教育局": "http://jyj.rizhao.gov.cn/",
    "临沂市教育局": "http://jyj.linyi.gov.cn/",
    "德州市教育局": "http://dzedu.dezhou.gov.cn/",
    "聊城市教育局": "http://jyty.liaocheng.gov.cn/",
    "滨州市教育局": "http://jy.binzhou.gov.cn/",
    "菏泽市教育局": "http://hzjy.heze.gov.cn/"
}

# 微信公众号配置（需要根据实际情况补充）
WECHAT_ACCOUNTS = {
    "济南教育": "jinan_edu",
    "青岛教育": "qingdao_edu",
    # ... 其他公众号配置
}

# 爬虫配置
CRAWLER_CONFIG = {
    "keyword": "思政",
    "date_range_days": 10,  # 每次爬取的天数
    "output_dir": "output",  # 输出目录
    "request_timeout": 10,  # 请求超时时间（秒）
    "retry_times": 3,  # 重试次数
} 