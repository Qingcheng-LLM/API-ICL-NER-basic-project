import json
from pathlib import Path

# 构建一个句子的字典表示，包含文本和实体列表
def build_example(tokens, tags):# 【tokens】:词列表，【tags】:对应的 IOB 标签列表
    text = " ".join(tokens)#把tokens列表拼成一句话
    entities = []# 准备列表用来存这句话中的实体
    i = 0
    while i < len(tokens):
        tag = tags[i]# 遍历这句话所有的 token 对应的标签 
        if tag.startswith("B-"):# 遇到 B- 开头的标签，说明是一个实体的开始
            ent_type = tag[2:]  # B-Chemical → Chemical
            start = i
            j = i + 1
            # 连续的 I-同类型 也并到这个实体里
            while j < len(tokens) and tags[j].startswith("I-") and tags[j][2:] == ent_type:#继续往后找，直到标签不再是 I-同类型
                j += 1
            ent_text = " ".join(tokens[start:j])#把这个实体的所有 token 拼成实体文本
            entities.append({"entity": ent_text, "type": ent_type})#把这个实体记录下来
            i = j
        else:
            i += 1
    return {"text": text, "entities": entities}


# 从 BC5CDR IOB 格式的文件中加载数据集，返回句子和实体的列表
def load_bc5cdr_iob(files, max_samples=None):
    data = []
    path=Path(files)
    # 读取 IOB 文件
    with path.open(encoding="utf-8") as f:
        tokens, tags = [], []
        for line in f:
            line = line.strip() 
            # 【按句子划分】遇到空行，说明一个句子结束
            if not line:
                if tokens:# 句子结束，且存在token，构建一个句子的字典表示
                    example = build_example(tokens, tags)
                    data.append(example)
                    tokens, tags = [], []
                    if max_samples is not None and len(data) >= max_samples:# 如果达到样本数上限，停止读取
                        return data
                continue
            # 读取非空行，解析 token 和 BIO标签
            parts = line.split()
            token = parts[0]
            tag = parts[-1]
            tokens.append(token)
            tags.append(tag)
        # 处理文件结尾的最后一个句子
        if tokens and (max_samples is None or len(data) < max_samples):
            example = build_example(tokens, tags)
            data.append(example)
            tokens, tags = [], []
    return data


if __name__ == "__main__":
    dataset = load_bc5cdr_iob("old_bc5cdr.tsv", max_samples=500)
    out_path = Path("bc5cdr_500.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("转换完成，保存到 bc5cdr_500.json")