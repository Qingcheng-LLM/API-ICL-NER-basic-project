
import argparse
import json
import time
from repair import repair_and_load
from pathlib import Path
from api_wrapper import call_model

# python run.py --prompt_file prompts/few_shot.txt --model_name deepseek-v3.2-exp --output_file results/few_shot_deepseek.json
# python run.py --prompt_file prompts/few_shot.txt --model_name qwen-2.5-72b-instruct --output_file results/few_shot_qwen.json
# python run.py --prompt_file prompts/few_shot.txt --model_name gpt-4o-mini --output_file results/few_shot_gpt.json

# python run.py --prompt_file prompts/one_shot.txt --model_name deepseek-v3.2-exp --output_file results/one_shot_deepseek.json
# python run.py --prompt_file prompts/one_shot.txt --model_name qwen-2.5-72b-instruct --output_file results/one_shot_qwen.json
# python run.py --prompt_file prompts/one_shot.txt --model_name gpt-4o-mini --output_file results/one_shot_gpt.json

# python run.py --prompt_file prompts/zero_shot.txt --model_name deepseek-v3.2-exp --output_file results/zero_shot_deepseek.json
# python run.py --prompt_file prompts/zero_shot.txt --model_name qwen-2.5-72b-instruct --output_file results/zero_shot_qwen.json
# python run.py --prompt_file prompts/zero_shot.txt --model_name gpt-4o-mini --output_file results/zero_shot_gpt.json

def main():
    args = parse_args()
    run(
        data_file=args.data_file,
        prompt_file=args.prompt_file,
        output_file=args.output_file,
        model_name=args.model_name,
        sleep_sec=args.sleep_sec,
        max_samples=args.max_samples,
    )
# 解析命令行参数
def parse_args(): 
    parser = argparse.ArgumentParser(description="BC5CDR NER few-shot 推理脚本") 
    parser.add_argument( "--data_file", type=Path, default=Path("bc5cdr_500.json"), help="数据集 JSON 文件路径", ) 
    parser.add_argument( "--prompt_file", type=Path, default=Path("prompts/few_shot.txt"), help="few-shot Prompt 模板文件", ) 
    parser.add_argument( "--output_file", type=Path, default=Path("results/pred_few_shot.json"), help="预测结果输出路径", ) 
    parser.add_argument( "--model_name", type=str, default="gpt-4o", help="调用的大模型名称（例如 gpt-4o, qwen, deepseek-chat 等）", ) 
    parser.add_argument( "--sleep_sec", type=float, default=0.5, help="两次请求之间的间隔，防止 QPS 过高", ) 
    parser.add_argument( "--max_samples", type=int, default=None, help="仅在调试时使用，限制前 N 条样本", ) 
    return parser.parse_args()

# 运行推理脚本
def run(data_file ,prompt_file ,output_file ,model_name: str = "gpt-4o",sleep_sec: float = 0.5,max_samples: int | None = None):
    # 读数据集 和 prompt 模板
    with data_file.open(encoding="utf-8") as f:
        dataset = json.load(f)
    if max_samples is not None:
        dataset = dataset[:max_samples]
    with prompt_file.open(encoding="utf-8") as f:
        template = f.read()
    results = []
    for i, sample in enumerate(dataset):
        # 构造完整的 prompt
        text = sample["text"]
        gold_entities = sample.get("entities", [])
        prompt = template.replace("{text}", text) #把输入文本填进模板
        # 调用大模型API
        try:
            raw_output = call_model(prompt, model=model_name)#使用自定义函数call_model调用大模型API，把 Prompt 发给大模型（比如 GPT-4o / DeepSeek / Qwen），拿到字符串形式的回复
        except Exception as e:#如果调用失败，则记录错误信息
            raw_output = f"ERROR: {e}"
        # 拿到的回复应该是json形式，不然进行JSON 修复 和 解析
        parsed = repair_and_load(raw_output)  # 解析后的回复
        pred_entities = parsed.get("entities", [])#从解析结果中提取预测的实体列表
        # 记录结果
        results.append(
            {
                "id": i,
                "text": text,
                "gold_entities": gold_entities, #真实的实体列表
                "raw_output": raw_output,       #大模型的原始回复
                "parsed_output": parsed,        #解析后的回复
                "pred_entities": pred_entities, #预测的实体列表
            }
        )
        if (i + 1) % 20 == 0:#每处理20条样本，打印一次进度
            print(f"已完成 {i+1} 条样本")
        time.sleep(sleep_sec)#防止请求过快，进行短暂休眠
    # 保存结果更多信息到文件
    output = {
        "mode": str(output_file).split("_")[1],  # 从文件名中提取模式名称
        "model": model_name,
        "num_samples": len(dataset),
        "results": results,}#完整的结果列表
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"完成，共 {len(dataset)} 条样本，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
