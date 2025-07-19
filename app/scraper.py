import requests
from lxml import html
from urllib.parse import urljoin
from datetime import datetime
import hashlib

def getAllNewsUrls(homeUrl, urls_path):
    print('home URL -->', homeUrl)
    response = requests.get(homeUrl, timeout=10)
    if response.status_code != 200:
        print("Failed to fetch home URL:", homeUrl)
        print("response.status_code ",response.status_code)
        return []
    else:
        tree = html.fromstring(response.content)
        urls = tree.xpath(urls_path)
        full_urls = [url if url.startswith("http") else urljoin(homeUrl, url) for url in urls]
        return full_urls

def generate_article_id_from_url(url):
    # Hash the URL to create a unique fallback ID
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def parse_timestamp(ts_str):
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))  # Handle ISO 8601 format
    except Exception:
        return None

def getEachNewInfo(url, html_paths_for_data):
    print('Each News URL -->', url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("Failed to fetch article:", url)
        return {}
    else:
        tree = html.fromstring(response.content)
        result = {
            'url': url,
            'article_id': generate_article_id_from_url(url)  # fallback ID from URL
        }
        
        for key, path in html_paths_for_data.items():
            data = tree.xpath(path)
            if key == 'publication_timestamp':
                result[key] = parse_timestamp(data[0]) if data else None
            elif key == 'article_id':
                result[key] = data[0] if data else result['article_id']  # Keep URL-based fallback
            else:
                result[key] = data[0] if data else None

        return result

def getAllNewsInfo(websites):
    all_data = []
    for name, site_info in websites.items():
        print(f"\n--- Scraping {name} ---")
        homeUrl = site_info['homeUrl']
        urls_path = site_info['urls_path']
        html_paths_for_data = site_info['html_paths_for_data']

        urls = getAllNewsUrls(homeUrl, urls_path)
        print(f"Found {len(urls)} article URLs")

        for url in urls:
            data = getEachNewInfo(url, html_paths_for_data)
            data['source'] = name
            all_data.append(data)

    return all_data

