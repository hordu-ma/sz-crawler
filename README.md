# 山东省教育局思政新闻爬虫

这是一个用于爬取山东省 16 个地市教育局网站和公众号中关于"思政"相关新闻的爬虫程序。

## 功能特点

- 支持爬取山东省 16 个地市教育局网站
- 支持按日期范围爬取（默认 10 天）
- 自动生成 Markdown 格式的新闻汇总文件
- 支持自定义关键词搜索
- 包含错误重试机制
- 使用随机 User-Agent 避免被封禁

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 配置网站和公众号信息：

   - 编辑 `config.py` 文件，添加或修改网站 URL 和公众号信息

2. 运行爬虫：

   ```bash
   python crawler.py
   ```

3. 查看结果：
   - 爬取结果将保存在 `output` 目录下
   - 文件名格式：`思政新闻_开始日期_结束日期.md`

## 配置说明

在 `config.py` 中可以修改以下配置：

- `WEBSITES`: 教育局网站配置
- `WECHAT_ACCOUNTS`: 微信公众号配置
- `CRAWLER_CONFIG`: 爬虫基本配置
  - `keyword`: 搜索关键词
  - `date_range_days`: 爬取天数
  - `output_dir`: 输出目录
  - `request_timeout`: 请求超时时间
  - `retry_times`: 重试次数

## 注意事项

1. 请遵守网站的 robots.txt 规则
2. 建议适当设置爬取间隔，避免对目标网站造成压力
3. 部分网站可能需要特定的请求头或 Cookie，可能需要额外配置
4. 微信公众号爬取需要额外的认证信息，目前仅支持网站爬取
