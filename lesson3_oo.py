"""
Venture LLM - Python Lession 3, Object Orient Programming

Environment variables
- SERPER_API_KEY
- TOGETHER_API_KEY
"""
import os, json
import requests
from dotenv import load_dotenv
from together import Together

load_dotenv()

class NewsSummarizer:
    """
    News summarizers is a class which generate news summary based on different
    configurations
    """
    # Class Variables
    _serper_url: str = "https://google.serper.dev/news"

    def __init__(self, keyword: str) -> None: # initiate an instance of this class
        # private instance variables
        self._keyword: str = keyword
        self._newscount: int = 10
        self._llm: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self._SERPER_API_KEY: str = os.environ.get("SERPER_API_KEY")
        self._TOGETHER_API_KEY: str = os.environ.get("TOGETHER_API_KEY")
        self._serper_payload: dict = {
            "q": keyword,
            "location": "Hong Kong",
            "gl": "hk",
            "hl": "zh-tw",
            "num": self._newscount,
            "tbs": "qdr:d"
        }
        self._news: list = []
        self._prompt: str = ""
        # public instance variables
        self._summary: str = ""
    
    def set_keyword(self, keyword: str) -> None:
        self._keyword = keyword
        self._serper_payload['q'] = keyword

    def set_numofnews(self, count: int) -> None:
        self._newscount = count
        self._serper_payload['num'] = int(count)

    def set_llm(self, llm: str) -> None:
        self._llm = llm

    def summarize(self) -> str: #type hinting
        self._set_news()
        self._set_prompt()
        self._set_summary()
        return(self._summary)
    
    def __str__(self):
        return(f"NewsSummarizer(keyword={self._keyword}, newscount={self._newscount}, llm={self._llm})")
    
    def __repr__(self):
        return(f"NewsSummarizer(keyword={self._keyword}, newscount={self._newscount}, llm={self._llm})")

    def _set_news(self) -> None:
        """
        Create a function to get result from serper with a given keyword and
        number of results required
        """
        payload = json.dumps(self._serper_payload)
        headers = {
            'X-API-KEY': self._SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self._serper_url, headers=headers, data=payload)
        search_result = response.json()
        self._news = search_result['news']

    def _set_prompt(self) -> None:
        """
        Create a prompt based on the context, num_of_results and keyword
        """
        num_of_results = len(self._news)
        context = ''
        for n in self._news: # Control structure
            context += 'Headline: ' + n['title']
            context += '\nSnippet: ' + n['snippet']
            context += "\n\n"
        self._prompt = f"""
[INSTRUCTION]
You are a professional search result summarizer. You are good at summarizing search results which will be given in the CONTEXT section for a specific keyword.
The search result will include headline and snippet, please try to your best link the headline and snippet together and make it more readable to reader.
Disregarding the language being given in the question section, you should answer the question in traditional chinese only.

[CONTEXT]
{context}

[QUESTION]
Please summarize the {self._newscount} search result which was searched using the {self._keyword}. Please summarize all the news in one short paragraph. Do not miss any news.
"""

    def _set_summary(self) -> None:
        """
        Pass the prompt to Together AI for preset model to get response
        """
        client = Together(api_key=self._TOGETHER_API_KEY)
        response = client.chat.completions.create(
            model=self._llm,
            # temperature = 1.5,
            messages=[{"role": "user", "content": self._prompt}],
        )
        self._summary = response.choices[0].message.content

# Main flow
agent1: NewsSummarizer = NewsSummarizer("英超")
print(type(agent1))
"""
agent1 = NewsSummarizer("英超")
agent2 = NewsSummarizer("英超")
agent2.set_llm("google/gemma-2-27b-it")
print(agent1.summarize())
print("\n")
print(agent2.summarize())
agent2.summarize()
a = agent2.summarize()
"""
"""
print(s.summarize())
s.set_keyword("香港新聞")
print(s.summarize())
s.set_llm("Qwen/Qwen1.5-72B-Chat")
print(s.summarize())
"""