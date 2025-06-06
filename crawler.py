import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse
from fake_useragent import UserAgent
import pandas as pd
from config import WEBSITES, WECHAT_ACCOUNTS, CRAWLER_CONFIG
import logging
import time
import urllib3
from urllib.parse import urljoin, urlparse
import re
import sys

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SZCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.output_dir = CRAWLER_CONFIG['output_dir']
        self._create_output_dir()
        self.session = requests.Session()
        self.session.verify = False
        self.stop_flag = False

    def _create_output_dir(self):
        """创建输出目录"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_headers(self, url):
        """获取随机User-Agent和特定网站的请求头"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # 针对特定网站添加额外的请求头
        domain = urlparse(url).netloc
        if 'jinan.gov.cn' in domain:
            headers['Referer'] = 'http://jnedu.jinan.gov.cn/'
        elif 'qingdao.gov.cn' in domain:
            headers['Referer'] = 'http://edu.qingdao.gov.cn/'

        return headers

    def _is_valid_url(self, url):
        """检查URL是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _normalize_url(self, url, base_url):
        """标准化URL"""
        if not url:
            return None
        
        # 处理JavaScript链接
        if url.startswith('javascript:'):
            return None
            
        # 处理相对路径
        if not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)
            
        # 移除URL中的锚点
        url = url.split('#')[0]
        
        return url if self._is_valid_url(url) else None

    def _fetch_page(self, url):
        """获取页面内容"""
        for attempt in range(CRAWLER_CONFIG['retry_times']):
            if self.stop_flag:
                return None
                
            try:
                logger.info(f"正在请求页面: {url} (尝试 {attempt + 1}/{CRAWLER_CONFIG['retry_times']})")
                
                # 设置请求头
                headers = self._get_headers(url)
                
                # 发送请求
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=CRAWLER_CONFIG['request_timeout']
                )
                response.raise_for_status()
                
                # 检测并设置正确的编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = response.apparent_encoding
                
                logger.info(f"成功获取页面: {url}")
                return response.text
                
            except requests.exceptions.SSLError as e:
                logger.error(f"SSL错误: {url}, 错误: {str(e)}")
            except requests.exceptions.ConnectionError as e:
                logger.error(f"连接错误: {url}, 错误: {str(e)}")
            except requests.exceptions.Timeout as e:
                logger.error(f"请求超时: {url}, 错误: {str(e)}")
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {url}, 错误: {str(e)}")
            except Exception as e:
                logger.error(f"未知错误: {url}, 错误: {str(e)}")
            
            if attempt < CRAWLER_CONFIG['retry_times'] - 1:
                wait_time = (attempt + 1) * 2
                logger.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        return None

    def _parse_news_links(self, html, source_name, base_url):
        """解析新闻链接，仅在标题中搜索关键词"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        news_links = []
        
        # 针对不同网站使用不同的解析策略
        domain = urlparse(base_url).netloc
        
        # 查找所有可能的新闻链接容器
        news_containers = []
        if 'jinan.gov.cn' in domain:
            news_containers = soup.find_all(['div', 'ul'], class_=re.compile(r'news|list|content'))
        elif 'qingdao.gov.cn' in domain:
            news_containers = soup.find_all(['div', 'ul'], class_=re.compile(r'news|list|content'))
        else:
            # 默认查找所有链接
            news_containers = [soup]
        
        for container in news_containers:
            for link in container.find_all('a'):
                if self.stop_flag:
                    return news_links
                    
                href = link.get('href')
                text = link.get_text(strip=True)
                
                # 检查标题中是否包含关键词
                if href and text and CRAWLER_CONFIG['keyword'] in text:
                    # 标准化URL
                    full_url = self._normalize_url(href, base_url)
                    if full_url:
                        news_links.append({
                            'source': source_name,
                            'title': text,
                            'url': full_url,
                            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        logger.info(f"找到相关新闻: {text}")
        
        return news_links

    def crawl_website(self, name, url):
        """爬取指定网站"""
        if self.stop_flag:
            return []
            
        logger.info(f"开始爬取: {name} ({url})")
        html = self._fetch_page(url)
        if html:
            news_links = self._parse_news_links(html, name, url)
            logger.info(f"在 {name} 中找到 {len(news_links)} 条相关新闻")
            return news_links
        return []

    def save_to_markdown(self, news_links, start_date, end_date):
        """保存为Markdown文件"""
        if not news_links:
            logger.warning("没有找到相关新闻")
            return

        filename = f"{self.output_dir}/思政新闻_{start_date}_{end_date}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 思政新闻汇总 ({start_date} 至 {end_date})\n\n")
            f.write(f"## 统计信息\n\n")
            f.write(f"- 总新闻数: {len(news_links)}\n")
            f.write(f"- 爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 按来源分组
            sources = {}
            for link in news_links:
                if link['source'] not in sources:
                    sources[link['source']] = []
                sources[link['source']].append(link)
            
            # 写入每个来源的新闻
            for source, links in sources.items():
                f.write(f"## {source} ({len(links)}条)\n\n")
                for link in links:
                    f.write(f"- [{link['title']}]({link['url']})\n")
                    f.write(f"  - 爬取时间: {link['crawl_time']}\n\n")

        logger.info(f"结果已保存到: {filename}")

    def run(self, start_date=None, end_date=None):
        """运行爬虫"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=CRAWLER_CONFIG['date_range_days'])).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"开始爬取 {start_date} 至 {end_date} 的新闻")
        all_news_links = []
        
        # 爬取网站
        total_sites = len(WEBSITES)
        for i, (name, url) in enumerate(WEBSITES.items(), 1):
            if self.stop_flag:
                break
                
            try:
                news_links = self.crawl_website(name, url)
                all_news_links.extend(news_links)
                time.sleep(2)  # 增加爬取间隔，避免请求过于频繁
            except Exception as e:
                logger.error(f"爬取 {name} 时发生错误: {str(e)}", exc_info=True)
                continue

        # 保存结果
        if not self.stop_flag:
            self.save_to_markdown(all_news_links, start_date, end_date)
            logger.info(f"爬取完成，共找到 {len(all_news_links)} 条新闻")

def main():
    try:
        # 检查是否使用命令行模式
        if len(sys.argv) > 1 and sys.argv[1] == '--cli':
            crawler = SZCrawler()
            start_date = None
            end_date = None
            
            # 解析命令行参数
            if len(sys.argv) > 2:
                start_date = sys.argv[2]
            if len(sys.argv) > 3:
                end_date = sys.argv[3]
                
            crawler.run(start_date, end_date)
        else:
            # 尝试导入GUI相关模块
            try:
                import tkinter as tk
                from tkinter import ttk, messagebox, scrolledtext
                import threading
                import queue
                
                # 如果成功导入，启动GUI模式
                root = tk.Tk()
                from crawler_gui import SZCrawlerGUI
                app = SZCrawlerGUI(root)
                root.mainloop()
            except ImportError:
                print("无法启动图形界面，请使用命令行模式：")
                print("python crawler.py --cli [开始日期] [结束日期]")
                print("日期格式：YYYY-MM-DD")
                sys.exit(1)
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 