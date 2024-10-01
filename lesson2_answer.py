"""
Venture LLM - Python Lession 2, Homework 2 sample answer

Environment variables
- SERPER_API_KEY
- TOGETHER_API_KEY
"""
import os, json
import requests
from dotenv import load_dotenv
from together import Together

load_dotenv()

def get_serper(keyword, num_of_result):
    """
    Create a function to get result from serper with a given keyword and
    number of results required
    """
    url = "https://google.serper.dev/news"

    payload = json.dumps({
        "q": keyword,
        "location": "Hong Kong",
        "gl": "hk",
        "hl": "zh-tw",
        "num": num_of_result,
        "tbs": "qdr:d"
    })
    headers = {
        'X-API-KEY': os.environ.get("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    search_result = response.json()
    return(search_result['news'])


def get_prompt(news, keyword):
    """
    Create a prompt based on the context, num_of_results and keyword
    """
    num_of_results = len(news)
    context = ''
    for n in news: # Control structure
        context += 'Headline: ' + n['title']
        context += '\nSnippet: ' + n['snippet']
        context += "\n\n"
    prompt_content = f"""
[INSTRUCTION]
You are a professional search result summarizer. You are good at summarizing search results which will be given in the CONTEXT section for a specific keyword.
The search result will include headline and snippet, please try to your best link the headline and snippet together and make it more readable to reader.
Disregarding the language being given in the question section, you should answer the question in traditional chinese only.

[CONTEXT]
{context}

[QUESTION]
Please summarize the {num_of_results} search result which was searched using the {keyword}. Please summarize all the news in one short paragraph. Do not miss any news.
  """
    return(prompt_content)


def get_summary(prompt):
    """
    Pass the prompt to Together AI for preset model to get response
    """
    client = Together()
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return(response.choices[0].message.content)

# Main flow
search_results = get_serper("英超", 10)
prompt = get_prompt(search_results, "英超")
summary = get_summary(prompt)
print(summary)