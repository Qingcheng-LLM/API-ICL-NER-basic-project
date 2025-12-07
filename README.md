
## 🚀项目简介:
本实验旨在通过调用大语言模型的 API，实现基于上下文学习（In-Context Learning, ICL）的命名实体识别（NER）任务。通过本项目可以熟悉 Prompt 模板的设计与上下文示例构造；基于少样本学习的 NER 任务的实现；不同提示策略下大模型 NER 性能的评估与分析。项目大致包含以下内容：<br>  
 1.数据格式转换<br>
 2.API接口配置<br>
 3.ICL与NER任务的实现<br>
 4.指标评估<br>  
  
项目数据集取自 BC5CDR 数据集，使用 prepare_data.py 脚本选取前 500 条样本进行实验。<br>  
项目提供GPT、Qwen、Deepseek三种模型的API调用逻辑，具体调用脚本见 api_wrapper.py 脚本。<br>  
项目提供zero-shot、one-shot、few-shot三种 prompts 模板，分别对三种模型进行指标测试<br>  
项目运行入口为 run.py 脚本，运行指令已在文件开头给出，运行结果保存在results文件夹下。<br>  
项目提供准确率、召回率、F1值 三种评估指标，运行结果已经给出，仅供参考。<br>  

    
## 📊 模型API来源： 

 1.项目所用模型根目录来自base_url = "https://api.openai.com/v1"<br>  
 2.如需复现，可选择https://openrouter.ai/settings/credits网页购买API-KEY，在项目 api_wrapper.py 脚本的api_key处填入密钥，即可运行此项目<br>  

## 📊 各模型各样本性能参数指标：
本实验对一种模型对应的一个样本类型选取500条样本进行推理，计算各种组合的参数指标，共合计推理4500条样本，用时约7小时，性能参数指标如下：<br>  
```
    模型         样本       准确率     召回率        F1 <br>
gpt-4o-mini      zero       0.6411     0.5599     0.5808<br>
gpt-4o-mini      one        0.6466     0.6020     0.6077<br>
gpt-4o-mini      few        0.6295     0.6118     0.6046<br>
deepseek-v3.2    zero       0.6567     0.6738     0.6528<br>
deepseek-v3.2    one        0.6577     0.6900     0.6618<br>
deepseek-v3.2    few        0.6870     0.7141     0.6875<br>
qwen-2.5-72b     zero       0.6040     0.6291     0.6036<br>
qwen-2.5-72b     one        0.6205     0.6605     0.6272<br>
qwen-2.5-72b     few        0.6376     0.6875     0.6448<br>
```
## 🗓项目目录: 
```
ICL-NER-PROJECT/  
├─ prompts/                 # 提示词模型，包含零、单、少样本  
├─ results/                 # 存放模型推理结果  
├─ old_bc5cdr.tsv           # 未经处理的数据集  
├─ prepare_data.py          # 处理数据的脚本  
├─ bc5cdr_500.json          # 处理后的500条数据  
├─ api_wrapper.py           # API调用逻辑  
├─ run.py                   # 推理脚本  
├─ repair.py                # 修复json文件  
└─ F1_compute.py            # 指标计算  
```