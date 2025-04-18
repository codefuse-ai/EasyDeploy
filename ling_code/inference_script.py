# -*- coding: utf-8 -*-
import os
from vllm import LLM
from vllm.sampling_params import SamplingParams

# os.environ['LD_LIBRARY_PATH'] = '/root/miniconda3/lib/python3.10/site-packages/nvidia/cublas/lib'
# model_path = '/mnt/modelops/models/Bailing_Code_MoE_Lite_4K_Chat_20250304_dpsk_gptq_int4'
model_path = '{your model path}'

enforce_eager = False

# GPU运行
trust_remote_code = True
tensor_parallel_size = 1
gpu_memory_utilization = 0.80
max_model_len = 4096
max_tokens = 4096
model = LLM(model_path, trust_remote_code=trust_remote_code, tensor_parallel_size=tensor_parallel_size, enforce_eager=enforce_eager, gpu_memory_utilization=gpu_memory_utilization, max_model_len=max_model_len)
prompt = "<role>SYSTEM<\\/role>假设你是一个医疗助理，请回答问题，回答时需要遵循下列要求。\n要求：\n1. 首先总起概括，然后在回答中使用数字1、2、3等进行分条目阐述解释，并在最后总结。\n2. 对参考内容当中与问题相关且正确的部分进行整合，可以结合医学知识进行适当推理。\n3. 回答内容专业详实、逻辑清晰，不能出现医学错误。严谨礼貌，符合医疗及政策规范。\n4. 对于不合规或者高风险的医疗项目，要提示中国大陆不允许展开。\n5. 对于上门进行医疗服务的相关问题，要提示需要在有相应资质的诊疗机构由专业医疗人员进行。\n6. 对于高风险处方药，需要向用户表明风险。\n7. 对于违规引产，需要说明不建议，若需要引产，则要在符合医疗政策和规范的情况下去有资质的医院进行。\n8. 对于有偿献血，需要说明中国大陆不存在有偿献血，献血都是无偿的。\n9. 请不要忘记你是一个医疗助理，针对问题给出积极正向的建议和科普，而不能像医生一样给出确定性的诊疗意见。\n<role>HUMAN<\\/role>艾滋病患者如何正确服用抗病毒药？<role>ASSISTANT<\\/role>"

sample_params = SamplingParams(max_tokens=max_tokens, ignore_eos=False)
result = model.generate(prompt, sampling_params=sample_params, prompt_token_ids=None)
print('result: {}'.format(result))
