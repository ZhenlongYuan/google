import os
import json
import requests
from bs4 import BeautifulSoup
import re

def get_scholar_stats(scholar_id):
    """从 Google Scholar 获取引用数据"""
    # 使用你的实际 Google Scholar 链接
    url = f"https://scholar.google.com/citations?user={scholar_id}&hl=zh-CN"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"正在获取 Google Scholar 数据: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 方法1: 尝试通过 id 查找引用数
        citations_element = soup.find('div', id='gsc_rsb_st')
        if citations_element:
            tds = citations_element.find_all('td', class_='gsc_rsb_std')
            if len(tds) > 0:
                citations = tds[0].text.strip()
                print(f"通过方法1找到引用数: {citations}")
                return citations
        
        # 方法2: 尝试通过表格类查找
        table = soup.find('table', id='gsc_rsb_st')
        if table:
            tds = table.find_all('td', class_='gsc_rsb_std')
            if len(tds) > 0:
                citations = tds[0].text.strip()
                print(f"通过方法2找到引用数: {citations}")
                return citations
        
        # 方法3: 使用正则表达式在页面中搜索
        citation_pattern = r'"citedby":(\d+)'
        match = re.search(citation_pattern, response.text)
        if match:
            citations = match.group(1)
            print(f"通过方法3找到引用数: {citations}")
            return citations
            
        print("未找到引用数，使用默认值 0")
        return "0"
        
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return "error"

def main():
    scholar_id = os.getenv('SCHOLAR_ID')
    if not scholar_id:
        print("错误: 未设置 SCHOLAR_ID 环境变量")
        return
    
    print(f"开始处理 Google Scholar ID: {scholar_id}")
    citations = get_scholar_stats(scholar_id)
    
    # 构建 shields.io 兼容的 JSON 格式
    stats_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(citations),
        "color": "blue",
        "cacheSeconds": 86400,
        "logoSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"#4285F4\"><path d=\"M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-3L9 8l3-5 3 5-3 13z\"/></svg>"
    }
    
    # 保存到 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2, ensure_ascii=False)
    
    print(f"统计数据已更新: {stats_data}")

if __name__ == "__main__":
    main()
