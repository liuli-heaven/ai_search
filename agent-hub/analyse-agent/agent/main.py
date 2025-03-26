from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import json
import openai

system_prompt = """
用户会输入他想要搜索的内容，根据其输入的信息，要解析出关键词，并以json格式返回，其中关键词为一个字符串列表
同时进行判断该用户此次搜索是否需要进行联网查找，若不需要，则将返回结果中need_search字段设置为false，同时在content字段做出回应
若需要查找则为true，将content字段置为空

EXAMPLE INPUT: 
我认为ai的出现极大的提高了生产效率

EXAMPLE JSON OUTPUT:
{
    "keywords": ["AI"、"出现"、"极大提高"、"生产效率"],
    "need_search": false,
    "content": "我同意你的观点..."
}
"""
base_url = 'https://api.deepseek.com'
api_key = 'sk-5f131943356d4c588356edabd9920db8'
class SearchEngine:
    def __init__(self, api_key, base_url):
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def extract_keywords(self, text):
        messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": text}]
        response = self.client.chat.completions.create(
            model='deepseek-chat',
            messages=messages,
            response_format={
                'type' : 'json_object'
            }
        )
        return json.loads(response.choices[0].message.content)

@run_agent
def run(agent:MofaAgent):
    try:
        user_input = agent.receive_parameter('query')

        searchEngine = SearchEngine(api_key=api_key, base_url=base_url)
        value = searchEngine.extract_keywords(user_input)
        keywords = value["keywords"]
        need_search = value["need_search"]
        print("now is ok")
        print("need_search is: ", need_search)
        if need_search == False :
            result = value['content']
            agent_output_name = 'analyse_result'
            agent.send_output(agent_output_name=agent_output_name,
                              agent_result=result)
        else :
            result = ""
            for keyword in keywords:
                result = result + keyword + " "
            agent_output_name = 'error_result'
            agent.send_output(agent_output_name=agent_output_name,
                              agent_result=result)
    except Exception as e:
        agent.logger.error(f"deepseek调用失败: {str(e)}")
        agent.send_output(
            agent_output_name='error_result',
            agent_result=f"处理出错： {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='analyse-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()
