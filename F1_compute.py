# python F1_compute.py
import json
from pathlib import Path

# 按文件评测预测结果，计算严格匹配的 Precision、Recall 和 F1
def main():
    for name in ["results/few_shot_deepseek.json", "results/few_shot_qwen.json","results/few_shot_gpt.json",
                 "results/one_shot_deepseek.json", "results/one_shot_qwen.json","results/one_shot_gpt.json",
                 "results/zero_shot_deepseek.json","results/zero_shot_qwen.json","results/zero_shot_gpt.json"]:
        path = Path(name)
        if path.exists():
            eval_file(path)
        else:
            print(f"未找到文件: {name}")

# 评测单个预测结果文件
def eval_file(pred_file: Path):
    with pred_file.open(encoding="utf-8") as f:
        data = json.load(f)
    # 取出完整的结果列表
    results = data["results"]
    ps, rs, fs = [], [], []
    # 取出结果列表中每个句子的 真实实体和预测实体
    for item in results:
        gold = item["gold_entities"]
        pred = item["pred_entities"]
        # 计算严格匹配的 P、R、F1
        p, r, f1 = strict_match(gold, pred)
        ps.append(p)
        rs.append(r)
        fs.append(f1)
    #一个文件内每个句子的 P、R、F1 求平均，作为整体的评测结果
    avg_p = sum(ps) / len(ps)
    avg_r = sum(rs) / len(rs)
    avg_f = sum(fs) / len(fs)
    print("-" * 40)
    print(f"文件{pred_file}的指标评估:")
    print(f"  Precision = {avg_p:.4f}")
    print(f"  Recall    = {avg_r:.4f}")
    print(f"  F1        = {avg_f:.4f}")
    print("-" * 40)

# 计算每个句子严格匹配的 Precision、Recall 和 F1
def strict_match(gold, pred):
    gold_set = {(e["entity"], e["type"]) for e in gold}
    pred_set = {(e["entity"], e["type"]) for e in pred}
    TP = len(gold_set & pred_set)# 计算预测出的正例数量
    FP = len(pred_set - gold_set)# 计算预测出的负例数量
    FN = len(gold_set - pred_set)# 计算没有预测出的正例数量
    precision = TP / (TP + FP + 1e-8)
    recall = TP / (TP + FN + 1e-8)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)
    return precision, recall, f1

if __name__ == "__main__":
    main()
