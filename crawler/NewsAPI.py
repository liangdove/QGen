from newsapi import NewsApiClient
import json
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import Dic2JSON

# /v2/top-headlines
def NewsAPI_headlines(q:str, category:str, language:str, country:str):
    newsapi = NewsApiClient(api_key='31b1d37be40a414890c526231ec10b70')
    top_headlines = newsapi.get_top_headlines(q=q,
                                              category=category,
                                              language=language,
                                              country=country)
    titles = [article["title"] for article in top_headlines["articles"]]
    # print(titles)
    return titles


# /v2/everything
def NewsAPI_everything(q:str, from_date:str = '2025-02-01', to_date:str = '2025-03-01', language:str = 'zh', sort_by:str = 'relevancy'):
    newsapi = NewsApiClient(api_key='31b1d37be40a414890c526231ec10b70')
    all_articles = newsapi.get_everything(q=q,
                                        #   sources='bbc-news,the-verge',
                                        #   domains='bbc.co.uk,techcrunch.com',
                                          from_param=from_date,
                                          to=to_date,
                                          language=language,
                                          sort_by=sort_by,
                                          )
    # print(Dic2JSON(all_articles))
    
    # 提取所有文章的标题
    titles = [article["title"] for article in all_articles["articles"]]
    # print(titles)
    
    return titles

# NewsAPI_everything("天命人")


