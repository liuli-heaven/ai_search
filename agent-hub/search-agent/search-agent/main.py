from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

API_URL = "https://api.bochaai.com/v1/web-search"
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
        return value_list
        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

@run_agent
def run(agent:MofaAgent):
    try:
        keyword = agent.receive_parameter('keywords')

        page_list = search_web_content(keyword)
        if len(page_list) == 0:
            agent.logger.error("search-agent调用失败， 返回文档数为0")
            agent.send_output(
            agent_output_name='error_result',
            agent_result=f"处理出错"
            )
        else:
            result = {
                'keyword': keyword,
                'page_list': page_list
            }
            agent_output_name = 'search_result'
            agent.send_output(agent_output_name=agent_output_name,
                          agent_result=result)
    except Exception as e:
        agent.logger.error(f"search-agent调用失败: {str(e)}")
        agent.send_output(
            agent_output_name='error_result',
            agent_result=f"处理出错： {str(e)}"
        )
def main():
    agent = MofaAgent(agent_name='search-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()
