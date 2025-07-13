# Copilot Instructions for sz-crawler

## 项目架构与核心流程

- 本项目为山东省教育局思政新闻爬虫，核心入口为 `crawler.py`，主要爬取 16 个地市教育局网站，按日期和关键词筛选，生成 Markdown 汇总。
- 配置文件 `config.py` 定义爬取目标（网站/公众号）、关键词、日期范围、输出目录等参数。
- 运行主流程：
  1. 编辑 `config.py` 配置目标和参数。
  2. 执行 `python crawler.py` 启动爬虫。
  3. 结果输出至 `output/`，文件名格式为 `思政新闻_开始日期_结束日期.md`。
- 日志输出到 `crawler.log`，便于调试和错误追踪。

## 关键开发模式与约定

- 所有网络请求均使用 `requests.Session`，并禁用 SSL 校验（`verify=False`），如需安全访问请调整。
- User-Agent 随机化（`fake_useragent`），部分网站需特殊 Referer 头（见 `_get_headers` 方法）。
- 错误重试机制由 `CRAWLER_CONFIG['retry_times']` 控制。
- 仅支持网站爬取，公众号爬取为预留，需补充认证信息。
- Markdown 汇总由 pandas 处理，内容格式化在主类 `SZCrawler` 内实现。

## 构建与打包

- 使用 `build.py` 通过 PyInstaller 打包为单文件可执行程序，输出至 `dist/`，并自动复制 `config.py`。
- 打包命令：`python build.py`，如有 `icon.ico` 会自动加入。
- 依赖管理见 `requirements.txt`，需先 `pip install -r requirements.txt`。

## 重要文件与目录

- `crawler.py`：主爬虫逻辑，包含所有核心方法和数据流。
- `config.py`：所有目标和参数配置，务必同步更新。
- `output/`：爬取结果输出目录。
- `crawler.log`：运行日志。
- `build.py`：打包脚本。
- `requirements.txt`：依赖列表。

## 其他约定

- 遵守目标网站 robots.txt，合理设置爬取间隔。
- 若需扩展公众号或 GUI 功能，参考 `crawler_gui.py` 预留接口。
- 代码风格以简洁、可维护为主，异常处理和日志记录优先。

---

如需补充特殊约定或遇到不明确的开发流程，请在此文档补充说明。
