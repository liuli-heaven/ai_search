from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

# Define the OpenAPI server URL
RERANK_URL = "https://api.bochaai.com/v1/rerank"
API_KEY = "sk-1983af62d2a74f969b034d8438c607c4"
headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

def rerank_content(keyword, page_list):
    doc_list = [page.get('summary') for page in page_list]

    payload = json.dumps({
        "model": "gte-rerank",
        "query": keyword,
        "return_documents": True,
        "documents": doc_list
    })
    response = requests.post(RERANK_URL, data=payload, headers=headers)
    if response.status_code == 200:
        ret = response.json()  # Parse the JSON response
        data = ret.get('data')
        result_list = data.get('results')
        # Extract and display relevant information
        return result_list
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


@run_agent
def run(agent:MofaAgent):
    input = agent.receive_parameter('input')
    page_list = input['page_list']
    doc_list = rerank_content(input['keyword'], page_list)
    if len(doc_list) == 0:
        agent.logger.error("rerank agent error")
        agent.send_output(
            agent_output_name='error_result',
            agent_result=f"rerank agent 处理出错"
        )
    else:
        result = []
        for doc in doc_list:
            idx = doc.get('index')
            result.append(page_list[idx])
        agent_output_name = 'rerank_result'
        agent.send_output(agent_output_name=agent_output_name,
                          agent_result=result)

def main():
    agent = MofaAgent(agent_name='rerank-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()
