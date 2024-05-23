import json
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

    
def get_scores_from_spark_api(conversations):
    # 定义提示，要求严格输出格式
    prompt = (
        "请根据以下五个维度对对话进行评分，并给出每个维度的评分(1到10分):\n"
        "1. 词汇难度: 使用复杂和多样词汇的程度\n"
        "2. 句法复杂度: 综合使用T-单位(T-unit)计数从句密度，文本长度，依赖关系长度等\n"
        "3. 可读性公式: 通过SMOG指数、Flesch-kincaid等级等方式评估文本的可读性\n"
        "4. 文本结构: 文本组织的逻辑性和清晰度\n"
        "5. 读者背景知识: 读者的背景知识对文本理解的影响\n\n"
        "请严格按照以下JSON格式输出，不要包含其他信息:\n"
        "{\n"
        "  \"lexical_difficulty_score\": <1到10的评分>,\n"
        "  \"syntactic_complexity_score\": <1到10的评分>,\n"
        "  \"readability_formula_score\": <1到10的评分>,\n"
        "  \"text_structure_score\": <1到10的评分>,\n"
        "  \"reader_background_knowledge_score\": <1到10的评分>\n"
        "}"
    )
    
    # 将多个对话内容添加到上下文中
    context = [{"role": "system", "content": prompt}]
    for convo in conversations:
        context.append({"role": convo['role'], "content": convo['content']})

    response = conversation(context)
    # 假设 response 返回的格式严格是一个 JSON 字符串
    scores_text = response.generations[0][0].text.strip()
    
    # 解析评分结果，假设返回结果是一个 JSON 字符串
    scores = json.loads(scores_text)
    
    return {
        'lexical_difficulty_score': scores.get('lexical_difficulty_score'),
        'syntactic_complexity_score': scores.get('syntactic_complexity_score'),
        'readability_formula_score': scores.get('readability_formula_score'),
        'text_structure_score': scores.get('text_structure_score'),
        'reader_background_knowledge_score': scores.get('reader_background_knowledge_score')
    }