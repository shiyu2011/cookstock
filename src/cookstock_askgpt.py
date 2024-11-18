import os
import re
import json as js
import datetime as dt
import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI



import random

#define some constants
class algoParas:   
    RETREIVE_DAYS = 1

def find_path():
    home_dir = os.path.expanduser("~")
    for root, dirs, files in os.walk(home_dir):
        if 'cookstock' in dirs:
            return os.path.join(root, 'cookstock')
    return None

def get_random_proxy():
    proxiesPath = os.path.join(find_path(), "proxy.txt")
    with open(proxiesPath, 'r') as f:
        proxies = [line.strip() for line in f.readlines()]  # Remove trailing whitespace or newlines
    
    proxy = random.choice(proxies)
    proxy_parts = proxy.split(':')
    return {
        "http": f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}",
        "https": f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"
    }


def fetch_with_proxy(url, headers):
    try:
        proxy = get_random_proxy()
        # print(f"Using proxy: {proxy}")
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10, verify=False)
        # Check if the response was successful
        if response.status_code == 200:
            print("Request successful!")
            return BeautifulSoup(response.text, "lxml")
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Proxy error: {e}")
        return None

class CookStockAskGPT:
    def __init__(self, base_path=None):
        self.client = OpenAI()
        self.cost_per_token_prompt = 0.15 / 1000000
        self.cost_per_token_answer = 0.60 / 1000000
        self.text_cost = 0
        self.base_path = base_path or find_path()
        self.soup = None
        self.headers_list = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'}
        ]


    def _ask_gpt(self, ticker, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an insightful and knowledgeable stock analytics."},
                    {
                        "role": "user",
                        "content": f"Write a summary for the news within 30 words and clearly write a note within 20 words which tells me if this news is related to the stock ticker {ticker} and if it is so positive that it could drive this stock soar. {prompt}",
                    },
                ]
            )
            if response.choices[0].message:
                answer = response.choices[0].message.content
                usage = response.usage
                self.text_cost += (
                    self.cost_per_token_prompt * usage.prompt_tokens +
                    self.cost_per_token_answer * usage.completion_tokens
                )
                return answer
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def _get_website(self, url, use_proxy=False):
        """Fetch website content with optional proxy."""
        header = random.choice(self.headers_list)
        try:
            if use_proxy == 1:
                #get api from env
                api_key = os.getenv('SCRAPER_API_KEY')
                if not api_key:
                    raise ValueError("SCRAPER_API_KEY not set in environment variables.")
                payload = {'api_key': api_key, 'url': url}
                response = requests.get('https://api.scraperapi.com/', params=payload)
            elif use_proxy == 2:
                self.soup = fetch_with_proxy(url, header)
                return
            else:
                response = requests.get(url, headers=header)
            self.soup = BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching website: {e}")
            self.soup = None


    def _get_business_summary(self, ticker):
        if self.soup is None:
            url = f'https://finance.yahoo.com/quote/{ticker}'
            self._get_website(url, use_proxy=2)
        soup = self.soup
        if not soup:
            return None
        summary = soup.find('section', attrs={'data-testid': 'company-overview-card'})
        if not summary:
            return None
        description = summary.find('div', attrs={'class': 'description'})
        if not description:
            return None
        return description.find('p').get_text()

    def _extract_news(self, ticker):
        if self.soup is None:
            url = f'https://finance.yahoo.com/quote/{ticker}'
            self._get_website(url, use_proxy=2)
        soup = self.soup
        if not soup:
            return None
        news_section = soup.find('section', attrs={'data-testid': 'recent-news'})
        if not news_section:
            return []

        news_items = news_section.find_all('div', attrs={'class': 'stream-item'})
        news_list = []

        for item in news_items:
            content = item.find('a', href=True, title=True)
            if not content:
                continue

            url_news = content['href']
            title_news = content['title']
            publishing_div = item.find("div", attrs={'class': 'publishing'})
            if not publishing_div:
                continue

            time_ago_text = publishing_div.text.strip()
            days_match = re.search(r"(\d+) days ago", time_ago_text)
            today_match = re.search(r"(\d+) hours ago", time_ago_text) or \
                          re.search(r"(\d+) minutes ago", time_ago_text) or \
                          re.search(r"(\d+) seconds ago", time_ago_text)
            
            today = dt.date.today()
            if days_match:
                days_ago = int(days_match.group(1))
            else:
                days_ago = 0 ##for all situation, go into the page for check

            
            past_date = today - dt.timedelta(days=days_ago)
            if past_date < dt.date.today() - dt.timedelta(days=algoParas.RETREIVE_DAYS):
                break

            # Fetch news article content
            self._get_website(url_news, use_proxy=2)
            #check the time again, sometimes the news above fool you
            if not self.soup:
                continue
            date_text = self.soup.find('div', attrs={'class': 'byline-attr-time-style'}).text.strip()
            if not date_text:
                continue
            #'Tue, Nov 12, 2024, 9:40 AM 2 min read'
            clean_date_text = re.sub(r'\s\d+\s(?:seconds?|mins?|minutes?|hours?)\sread$', '', date_text, flags=re.IGNORECASE)  
            struct_time = time.strptime(clean_date_text, "%a, %b %d, %Y, %I:%M %p")
            formatted_date = dt.datetime(*struct_time[:6])
            if formatted_date.date() < dt.date.today() - dt.timedelta(days=algoParas.RETREIVE_DAYS):
                break
            article_div = self.soup.find('div', attrs={'class': 'article-wrap'})
            if not article_div:
                continue

            paragraphs = article_div.find_all('p')
            combined_content = " ".join(p.get_text(strip=True) for p in paragraphs)
            review = self._ask_gpt(ticker, combined_content)

            news_list.append({
                "title": title_news,
                "url": url_news,
                "date": str(formatted_date.date()),
                "review": review
            })

        return news_list

    def analyze_single_ticker(self, ticker):
        print(f"Analyzing {ticker}...")
        business_summary = self._get_business_summary(ticker)
        news = self._extract_news(ticker)
        return {
            "ticker": ticker,
            "business_summary": business_summary,
            "news": news
        }


class CookStockAskGPTBatch:
    def __init__(self, input_json, output_json, base_path=None):
        self.input_json = input_json
        self.output_json = output_json
        self.client = OpenAI()
        self.cost_per_token_prompt = 0.15 / 1000000
        self.cost_per_token_answer = 0.60 / 1000000
        self.text_cost = 0
        if base_path:
            self.base_path = base_path
        self.base_path = find_path()
        self.output_json = setup_result_file(output_json)
    
    def analyze_batch(self):
        with open(self.input_json, 'r') as f:
            tickers_data = js.load(f)
        results = tickers_data.copy()
        for entry in results['data']:
            for ticker, details in entry.items():
                try:
                    x = CookStockAskGPT()
                    analysis = x.analyze_single_ticker(ticker)
                    self.text_cost += x.text_cost
                    print(f"Total text cost so far: {self.text_cost}")
                    if analysis:
                        details['åbusiness_summary'] = analysis['business_summary']
                        details['news'] = analysis['news']
                        results['data'].append({ticker: details})
                        append_to_json(self.output_json, {ticker: details})
                except Exception as e:
                    print(f"Error: {e}")
                    continue
            
def load_json(filepath):
    with open(filepath, "r") as f:
        return js.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        js.dump(data, f, indent=4)

def append_to_json(filepath, ticker_data):
    data = load_json(filepath)
    data['data'].append(ticker_data)
    save_json(filepath, data)

def setup_result_file(filePath):
    save_json(filePath, {"data": []})
    return filePath


# Example usage:
if __name__ == "__main__":
    analyzer = CookStockAskGPT()

    # Single ticker analysis
    # single_result = analyzer.analyze_single_ticker("CCRD")
    # print(single_result)

    # # Batch analysis
    input_json = os.path.join(analyzer.base_path, "results/2024-11-17", "Technology_HealthCare_Finance_Energy.json")
    output_json = os.path.join(analyzer.base_path, "results", "combinedData_gpt.json")
    analyzerBatch = CookStockAskGPTBatch(input_json, output_json)
    analyzerBatch.analyze_batch()
