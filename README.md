# Paper-screening-use-LLM （密钥还有余额可用，先到先得
# Excel 文献分类脚本

## 项目简介
批量读取 Excel 的 **Title/Abstract** 字段，请求 `api.chatanywhere.tech`（`gpt-3.5-turbo`（默认，可选）），解析返回格式生成三类标签：**Damage / Type / Automation**，并写回新的 Excel 文件。

## 工作流程
1. 读取输入 Excel（默认示例：`updated.xlsx`）。  
2. 逐行向接口发送请求（带重试/异常处理）。  
3. 解析形如：`Damage is n, Type is n, Automation is n !!!` 的文本并提取数值。  
4. 结果写入 `分类后.xlsx`，控制台打印进度与提取结果。

## 快速开始
```bash
# 1) Python 环境
python --version     # 建议 3.8+

# 2) 安装依赖（按实际代码为准）
pip install pandas openpyxl requests

# 3) 运行脚本（按你的脚本文件名为准）
python ×××.py
```

## 配置说明
- **输入文件**：在脚本中修改 `excel_file_path` 指向你的 Excel（需包含列 `Title`，可选 `Abstract`）。  
- **输出文件**：默认写为 `分类后.xlsx`（与输入同目录或脚本中指定的位置）。  
- **接口与密钥**：脚本里若写死了 `Authorization`，**强烈建议**改为用环境变量读取，例如：
  - Windows (PowerShell)：`setx CHATANYWHERE_API_KEY "sk-xxxx"`  
  - Linux/macOS：`export CHATANYWHERE_API_KEY="sk-xxxx"`

  随后在代码中使用 `os.environ.get("CHATANYWHERE_API_KEY")` 读取，避免密钥泄露。

## 输出字段
- **Damage**：0=破坏性；1=非破坏性  
- **Type**：0=定性；1=定量  
- **Automation**：0=全手动；1=手动+设备；3=少人参与（以提示词/代码中的定义为准）

## 注意事项
- **返回格式依赖**：若模型未返回固定短语（如没有 `Damage is ...`），解析会失败或得到空值。  
- **速率限制**：批量调用建议加上重试与节流，避免触发限频。  
- **路径/平台**：当前多为 Windows 路径示例，跨平台可能需调整。  
- **隐私安全**：不要提交带有真实 API Key 的代码到仓库。

## 可选增强
- 将输入/输出路径改为命令行参数（`argparse`）。  
- 增加 `timeout/重试/速率限制` 与结构化日志。  
- 对异常与空值做更健壮的校验与提示。
