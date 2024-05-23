from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v2.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = os.getenv('SPARKAI_APP_ID', '')
SPARKAI_API_SECRET = os.getenv('SPARKAI_API_SECRET', '')
SPARKAI_API_KEY = os.getenv('SPARKAI_API_KEY', '')
#星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv2'

def conversation(context):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
     # 通过循环将 context 转换为 ChatMessage 实例列表
    messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in context]
    handler = ChunkPrintHandler()
    return spark.generate([messages], callbacks=[handler])

# s = conversation([{"role":"system","content":"你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"},{"role": "user", "content": "你是李白吗"}])
# print(s)
