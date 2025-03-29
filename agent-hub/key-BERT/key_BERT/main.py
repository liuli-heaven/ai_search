from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import os
from dotenv import load_dotenv
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer

# 加载中文分词方法
import hanlp
tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
pos = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)

@run_agent
def run(agent: MofaAgent):
    try:
        # 加载环境变量
        load_dotenv('.env.secret')
        
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=os.getenv('LLM_API_KEY'),
            base_url=os.getenv('LLM_API_BASE')
        )
        
        # 接收用户输入
        doc = agent.receive_parameter('query')
        
        # 加载中文编码模型
        kw_model = KeyBERT(model='BAAI/bge-small-zh-v1.5')
        vectorizer = CountVectorizer(tokenizer=tok)
        key_words = kw_model.extract_keywords(doc, vectorizer=vectorizer, top_n=20)
        key_words = key_words[:10]

        
        # 调用 LLM
        response = client.chat.completions.create(
            model=os.getenv('LLM_MODEL'),
            messages=[
                {"role": "system", "content": "你需要根据这一组（关键词，权重）对，去除中间重复的部分.然后将剩余部分按照权重从高到低排序，输出成一个json对象，格式如下:{'key1':0.9,'key2':0.8}"},
                {"role": "user", "content": str(key_words)}
            ],
            response_format={
                'type': 'json_object'},
            stream=False
        )

        # 发送输出
        agent.send_output(
            agent_output_name='llm_result',
            agent_result=response.choices[0].message.content
        )
        
    except Exception as e:
        agent.send_output(
            agent_output_name='llm_result',
            agent_result=f"Error: {str(e)}"
        )
    
def main():
    agent = MofaAgent(agent_name='key-BERT')
    run(agent=agent)
if __name__ == "__main__":
    main()
