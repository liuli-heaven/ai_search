import requests
import json

# Define the OpenAPI server URL
API_URL = "https://api.bochaai.com/v1/web-search"
RERANK_URL = "https://api.bochaai.com/v1/rerank"
API_KEY = "sk-1983af62d2a74f969b034d8438c607c4"
headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

def search_web_content(keyword):
    # Prepare the request payload
    payload = json.dumps({
        "query": keyword,
        "summary": True,
        "count": 10,
        "page": 1
    })

    # Make the POST request to the WebPilot API
    response = requests.request("POST", API_URL, data=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        ret = response.json()  # Parse the JSON response
        data = ret.get('data')
        pages = data.get('webPages')
        value_list = pages.get('value')
        # Extract and display relevant information
        for value in value_list:
            print(f"page name is: {value.get('name')}")
            print(f"Page url is: {value.get('url')}")
            print(f"Page Summary is: {value.get('summary')}")
        return value_list
        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def rerank_content(keyword, page_list):
    # doc_list = [page.get('summary') for page in page_list]
    doc_list =  ["阿里巴巴集团发布《2024财年环境、社会和治理（ESG）报告》（下称“报告”），详细分享过去一年在 ESG各方面取得的进展。 报告显示，阿里巴巴扎实推进减碳举措，全集团自身运营净碳排放和价值链碳强度继续实现“双降”。 集团亦持续利用数字技术和平台能力，服务于无障碍、医疗、适老化和中小微企业等普惠发展。 阿里巴巴集团首席执行官吴泳铭在报告中表示：“ESG的核心是围绕如何成为一家更好的公司。 25年来，我们与ESG相关的行动所构成的公司底色，与创造商业价值的阿里巴巴一样重要。 在集团明确‘用户为先’和‘AI 驱动’的两大业务战略的同时，我们也明确ESG作为阿里巴巴基石战略之一的定位不变。 阿里巴巴在减少碳排放上取得扎实进展。",
      "ESG的核心是围绕如何成为一家更好的公司。 今年是阿里巴巴成立25年。 25年来，阿里巴巴秉持“让天下没有难做的生意”，协助国内电商繁荣发展；坚持开放生态，魔搭社区已开放了超3800个开源模型；助力乡村振兴，累计派出了29位乡村特派员深入27个县域；推动平台减碳，首创了范围3+减碳方案；坚持全员公益，用“人人3小时”带来小而美的改变……这些行动所构成的公司底色，与创造商业价值的阿里巴巴一样重要。 我希望这个过程中，每一个阿里人都能学会做难而正确的选择，保持前瞻、保持善意、保持务实。 一个更好的阿里巴巴，值得我们共同努力。 阿里巴巴二十多年来坚持不变的使命，是让天下没有难做的生意。 今天，这一使命被赋予了新的时代意义。"]
    payload = json.dumps({
        "model": "gte-rerank",
        "query": keyword,
        "top_n": 2,
        "return_documents": True,
        "documents": doc_list
    })
    response = requests.post(RERANK_URL, data=payload, headers=headers)
    if response.status_code == 200:
        ret = response.json()  # Parse the JSON response
        data = ret.get('data')
        result_list = data.get('results')
        # Extract and display relevant information
        for result in result_list:
            print(result)
    else:
        print(f"Error: {response.status_code} - {response.text}")



# Example usage
if __name__ == "__main__":
    keyword = "阿里巴巴2024年的ESG报告"
    # page_list = search_web_content(keyword)
    page_list = []
    rerank_content(keyword, page_list)
