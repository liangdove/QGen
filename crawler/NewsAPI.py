from newsapi import NewsApiClient
import json
# Init
newsapi = NewsApiClient(api_key='31b1d37be40a414890c526231ec10b70')

# # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='deepseek',
#                                           category='business',
#                                           language='en',
#                                           country='us')
# formatted_response = json.dumps(top_headlines, indent=4, ensure_ascii=False) # JSON格式化字典
# print(formatted_response)


# /v2/everything
all_articles = newsapi.get_everything(q='印尼主权基金启动',
                                    #   sources='bbc-news,the-verge',
                                    #   domains='bbc.co.uk,techcrunch.com',
                                      from_param='2025-02-01',
                                      to='2025-03-01',
                                      language='zh',
                                      sort_by='relevancy',
                                      )
formatted_response = json.dumps(all_articles, indent=4, ensure_ascii=False) # JSON格式化字典
with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(formatted_response)


# # /v2/top-headlines/sources
# sources = newsapi.get_sources(
#   language='zh',
  
# )
# formatted_response = json.dumps(sources, indent=4, ensure_ascii=False) # JSON格式化字典
# # print(formatted_response)
# with open('result.txt', 'w', encoding='utf-8') as file:
#     file.write(formatted_response)