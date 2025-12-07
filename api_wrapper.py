
from openai import OpenAI

def call_model(prompt, model):#给大模型输入提示，返回回复内容 

    # GPT调用逻辑
    if model.lower().startswith("gpt-") :
        client = OpenAI(api_key="sk-xxx",
                        base_url = "https://openrouter.ai/api/v1")# 请替换为自己的 OpenAI API Key
        response = client.chat.completions.create( #发起一次“聊天补全”请求
            model="openai/gpt-4o-mini",#这里可以替换为你想调用的模型名称
            messages=[{"role": "user", "content": prompt}],#【这是"user发给模型的prompt】
            temperature=0,
        )
        return response.choices[0].message.content#选取第一个候选答案，候选答案的消息对象，消息对象里的生成内容
    # DeepSeek调用逻辑
    if model.lower().startswith("deepseek-") :
        client = OpenAI(api_key="sk-xxx",
                        base_url = "https://openrouter.ai/api/v1")# 请替换为自己的 OpenAI API Key
        response = client.chat.completions.create( #发起一次“聊天补全”请求
            model="deepseek/deepseek-v3.2-exp",
            messages=[{"role": "user", "content": prompt}],#【这是"user发给模型的prompt】
            temperature=0,
        )
        return response.choices[0].message.content#选取第一个候选答案，候选答案的消息对象，消息对象里的生成内容
    # Qwen调用逻辑--用DashScope官方 Python SDK 的写法
    if model.lower().startswith("qwen-") :
        client = OpenAI(api_key= "sk-xxx",
                        base_url="https://openrouter.ai/api/v1")# 请替换为自己的 OpenRouter API Key
        completion = client.chat.completions.create(
            model="qwen/qwen2.5-vl-72b-instruct",
            messages=[{"role": "user","content": prompt}],#【这是"user发给模型的prompt】
            temperature=0,
        )
        return completion.choices[0].message.content#选取第一个候选答案，候选答案的消息对象，消息对象里的生成内容
    raise ValueError(f"暂不支持的此模型: {model}，可以添加此模型的调用逻辑")