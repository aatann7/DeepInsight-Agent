import akshare as ak
from openai import OpenAI
import sys
import os

# ================= 配置区 =================
# 🔴 请在这里填入你的 DeepSeek API Key
API_KEY = "xxxxxxxxxxxxxxx" 
# =========================================

# 初始化 AI 客户端
client = OpenAI(
    api_key=API_KEY, 
    base_url="https://api.deepseek.com"
)

def call_ai_model(prompt):
    """
    真·AI调用函数
    """
    print(f"\n🧠 DeepInsight 正在连接大脑，深度分析中... (请稍等10-20秒)")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的商业分析师，擅长将复杂金融数据翻译成大白话。"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 调用失败: {e}\n请检查你的 API Key 是否正确，或网络是否通畅。"

def get_stock_name_safe(symbol):
    """
    安全版数据获取：如果 akshare 联网失败，自动切换为手动输入
    """
    print(f"🔍 正在核对代码 {symbol} ...")
    
    # 尝试 1：自动联网获取
    try:
        # 临时尝试移除代理环境变量，防止代理干扰国内请求
        # (这只影响当前脚本运行时的环境，不会改你电脑的设置)
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        
        df = ak.stock_zh_a_spot_em()
        stock_row = df[df['代码'] == symbol]
        if not stock_row.empty:
            real_name = stock_row.iloc[0]['名称']
            print(f"✅ 锁定标的：【{real_name}】")
            return real_name
        else:
            print(f"❌ 代码 {symbol} 无效，请检查。")
            return None

    # 尝试 2：如果报错（比如代理冲突），切换手动模式
    except Exception as e:
        print(f"\n⚠️ 网络数据源连接受阻 (原因: 代理冲突/网络波动)")
        print(f"💡 别担心，这不会影响 AI 分析。")
        print(f"👉 既然自动核对失败，请手动告诉我这家公司叫什么？")
        manual_name = input(f"请输入 {symbol} 的公司名称 (例如 锦浪科技): ")
        if manual_name.strip():
            return manual_name
        return None

def generate_analysis(symbol, stock_name):
    """
    核心逻辑层：你的【新八大板块】Prompt
    """
    system_prompt = f"""
    【角色】专业商业分析师 (非娱乐化，非生活化，非荐股)。
    【目标】为用户提供 {stock_name} ({symbol}) 的深度商业认知报告。
    
    请严格按照以下【八大板块】输出，不要遗漏：
    
    1. **🆔 人话身份证 (专业版)**
       - 给出标准的行业定义。
       - 解释其核心业务解决什么商业痛点。
    
    2. **🌳 产品知识树 & 黑话翻译**
       - 产品分类 (A/B/C) 及功能简介。
       - 解释 3 个核心行业术语 (解释需通俗但专业)。
    
    3. **🔗 产业链地位**
       - 上游依赖谁？下游卖给谁？
       - 评估其在链条中的话语权 (强/弱)。
    
    4. **🏆 江湖排位 (必须含数据)**
       - 全球/国内排名 (如：Top 3)。
       - 市场份额 (Market Share) 估算。
       - 列出 2-3 个主要竞争对手名字。
    
    5. **💰 搞钱能力**
       - 拆解营收来源占比 (Business Mix)。
    
    6. **⚙️ 商业底层逻辑**
       - 它是靠什么驱动增长的？(技术领先？成本优势？渠道垄断？)
    
    7. **💣 排雷指南 (风险)**
       - 重点提示：原材料涨价、政策变动、技术迭代等实体经营风险。
       - ❌ 禁止提示股价波动风险。
    
    8. **📝 一句话总结**
       - 客观概括其行业地位及核心逻辑。
    """
    
    return call_ai_model(system_prompt)

# --- 运行入口 ---
if __name__ == "__main__":
    print("="*50)
    print("🚀 DeepInsight-Agent V3.0 (网络安全版)")
    print("="*50)
    
    # 简单的 Key 检查
    if "sk-" not in API_KEY:
        print("❌ 错误提醒：你还没有在代码第 8 行填入 DeepSeek API Key！")
        print("请打开 core_agent.py 文件，填入 Key 之后再运行。")
        sys.exit()

    while True:
        user_input = input("\n请输入股票代码 (输入 q 退出): ")
        if user_input.lower() == 'q':
            break
        
        # 使用安全版获取函数
        real_name = get_stock_name_safe(user_input)
        
        if real_name:
            report = generate_analysis(user_input, real_name)
            print("\n" + "-" * 30 + f" {real_name} 分析报告 " + "-" * 30)
            print(report)
            print("-" * 70)