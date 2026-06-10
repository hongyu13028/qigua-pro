# -*- coding: utf-8 -*-
"""
Qigua Pro — Streamlit Web UI
传统决策手艺 · 让普通人也能用《易经》做决策辅助

启动：streamlit run app.py
浏览器打开：http://localhost:8501
"""

import streamlit as st
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

# ===页面配置 ===
st.set_page_config(
 page_title="Qigua Pro —传统决策手艺",
 page_icon="🪙",
 layout="wide",
 initial_sidebar_state="expanded",
)

# ===顶部 ===
st.title("🪙 Qigua Pro")
st.subheader("传统决策手艺 · 让普通人也能用《易经》做决策辅助")
st.markdown("---")

# ===侧边栏 ===
with st.sidebar:
 st.header("📖快速导航")
 st.markdown("""
 - [🪙 起卦](#起卦)
 - [📚6 层模型速查](#6 层模型速查)
 - [💼6 大场景案例](#6 大场景案例)
 - [⚙️ 关于](#关于)
 """)
 st.markdown("---")
 st.markdown("**当前版本**: v3.0")
 st.markdown("**作者**: 黄耀锋 (yaofeng-huang)")
 st.markdown("[GitHub](https://github.com/yaofeng-huang/qigua-pro) · [Gitee](https://gitee.com/yaofeng-huang/qigua-system)")

# === Tab1: 起卦 ===
st.header("🪙 起卦")
st.markdown("**一事一卦**——把模糊问题变成结构化输入，3 种起卦方式任选。")

question = st.text_input(
 "📝你的具体问题（一事一卦，必须能判吉凶）",
 placeholder="例：我下周要不要接那个5 万的订单？",
 help="好问法：我这单 XX业务能否在3个月内成交？坏问法：我今年能不能发财？"
)

col1, col2 = st.columns(2)
with col1:
 method = st.radio(
 "🎯 起卦方式",
 ["数字起卦", "时间起卦", "铜钱起卦"],
 horizontal=True,
 )

if method == "数字起卦":
 with col2:
 a = st.number_input("数字 a", min_value=1, value=88)
 b = st.number_input("数字 b", min_value=1, value=18)

elif method == "时间起卦":
 st.info(f"⏰ 用当前时间起卦：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

else: #铜钱起卦
 coins_input = st.text_input(
 "🪙6 个爻位（从下到上，每爻0/1）",
 placeholder="例：110010",
 help="奇数=阳爻，偶数=阴爻"
 )
 change_yao = st.number_input("变爻位置（1-6）", min_value=1, max_value=6, value=4)

# 起卦按钮
if st.button("🔮 起卦", type="primary", use_container_width=True):
 if not question:
 st.error("❌ 请先填写你的问题")
 elif len(question) <5:
 st.warning("⚠️ 问题太模糊，请具体到「人 / 事 / 时间窗口」")
 else:
 #跑 qigua.py
 with st.spinner("🔮 起卦中..."):
 try:
 cmd = ["python", "qigua.py"]
 if method == "数字起卦":
 cmd.extend(["--number", str(int(a)), str(int(b))])
 elif method == "时间起卦":
 cmd.extend(["--time"])
 else: #铜钱
 coins = coins_input.strip().split()
 if len(coins) !=6:
 st.error("❌铜钱起卦需要6 个爻位")
 st.stop()
 cmd.extend(["--coins"] + coins + ["--change", str(change_yao)])
 cmd.extend(["--question", question])

 result = subprocess.run(
 cmd,
 capture_output=True,
 text=True,
 cwd=os.path.dirname(os.path.abspath(__file__)),
 timeout=30,
 )

 if result.returncode ==0:
 st.success("✅ 起卦成功！")
 st.markdown("### 📜卦象报告")
 st.code(result.stdout, language="text")

 #提示下一步
 st.info("💡 **下一步**：把上面的输出贴给 ChatGPT / Claude / 通义 / Mavis，"
 "配上 `qigua_prompt.md` 作为 System Prompt，立刻得到完整决策建议书。")
 with st.expander("📋 查看 qigua_prompt.md (v2.0)全文"):
 try:
 prompt_path = Path(__file__).parent / "qigua_prompt.md"
 prompt_text = prompt_path.read_text(encoding="utf-8")
 st.markdown(prompt_text)
 except Exception as e:
 st.error(f"读取失败：{e}")
 else:
 st.error("❌ 起卦失败")
 st.code(result.stderr, language="text")

 except subprocess.TimeoutExpired:
 st.error("❌ 起卦超时（30秒）")
 except FileNotFoundError:
 st.error("❌找不到 qigua.py，请确认在 qigua-pro目录下运行")
 except Exception as e:
 st.error(f"❌ 出错了：{e}")

st.markdown("---")

# === Tab2:6 层模型速查 ===
st.header("📚6 层模型速查")
st.markdown("决策系统的核心——6 层模型帮你看「时机 + 主客 +抓手 +机遇」。")

layer_tabs = st.tabs([
 "1️⃣阴阳遁",
 "2️⃣ 月令旺衰",
 "3️⃣爻位六神",
 "4️⃣ 用神",
 "5️⃣ 八门九星",
 "6️⃣ 三奇",
])

with layer_tabs[0]:
 st.subheader("1️⃣阴阳遁")
 st.markdown("""
**核心**：大节奏判断。冬至→夏至 =阳遁（攻），夏至→冬至 =阴遁（守）。

**2026节奏**：
 -2025-12-21 ~2026-06-21：**阳遁**（上半年主推）
 -2026-06-21 ~2026-12-22：**阴遁**（下半年修炼）

**实战判断**：
 -距夏至/冬至 >12 天：节奏平稳
 -距夏至/冬至 <12 天：**攻/守的尾巴**——关键窗口
 - 当天：极高风险/极高机遇
""")

with layer_tabs[1]:
 st.subheader("2️⃣ 月令旺衰")
 st.markdown("""
**核心**：环境顺逆。事情属于哪个五行 vs 当月这个五行的状态。

**5 个状态**：
 - **旺**：当令，大胆做
 - **相**：我生的，顺势
 - **休**：生我的，维持
 - **囚**：克我的，别强求
 - **死**：我克的，借力 /退守

**口诀**：当令的旺，我生的相，生我的休，克我的囚，我克的死。

**火行业（1688/电商）节奏**：
 -5-7 月（旺）：重点投入、主推新品
 -4-8 月（相/旺）：加大运营
 -9-10 月（休）：维持、准备秋冬
 -11-1 月（囚）：收缩、修内功
 -2-3 月（死）：最小化、准备春季
""")

with layer_tabs[2]:
 st.subheader("3️⃣爻位六神")
 st.markdown("""
**核心**：主客关系。动爻位置决定谁是主、谁是客。

**主客4原则**：
 -动静：动者为客，静者为主
 -先后：先动为客，后动为主
 -态度：主动为客，被动为主
 - 地盘：流动为客，稳定为主

**5 种关系**：
 - **客生主**：外部助力上门（最舒服）
 - **主生客**：自己过度付出（最累）
 - **比和**：双方契合（最理想）
 - **客克主**：主动出击受挫（别硬推）
 - **主克客**：看似占优实则空（白费功夫）
""")

with layer_tabs[3]:
 st.subheader("4️⃣ 用神")
 st.markdown("""
**核心**：关键抓手。6爻中"最旺"或"最相关"的那一爻 = 用神。

**4 种神**：
 - **用神**：关键抓手
 - **忌神**：千万别碰
 - **仇神**：用神的敌人（间接忌）
 - **原神**：用神的助力

**实战**：
 -5爻（领导/主角位）动 → 用神在决策人
 - 初爻（基础位）动 → 用神在基础
 - 二爻（现状位）动 → 用神在当前阶段
""")

with layer_tabs[4]:
 st.subheader("5️⃣ 八门九星")
 col1, col2 = st.columns(2)
 with col1:
 st.markdown("""
**八门**（做事状态）：

**3 个宜主动**：
 - **开门**：格局舒展（开工、面试、签约）
 - **休门**：安稳平和（拜访、求人、调解）
 - **生门**：生机绵长（求财、长期规划）

**5 个需谨慎**：
 -伤门：多有波折（仅维权）
 -杜门：气场闭塞（仅学习）
 -景门：文书信息（考试、文案）
 -死门：状态停滞（仅断舍离）
 -惊门：突发变故
""")
 with col2:
 st.markdown("""
**九星**（环境气场）：

 - **天辅星**：文运、贵人缘（人际）
 - **天任星**：稳重、包容（深耕）
 - **天心星**：理智、决断（重要决策）
 - **天芮星**：隐患、疏漏（修内功）
 - **天蓬星**：魄力、突破（小额试错）
 - **天柱星**：沟通、口舌（慎用）
""")

with layer_tabs[5]:
 st.subheader("6️⃣ 三奇")
 st.markdown("""
**核心**：机遇识别。6爻中出现天干 → 看是否有乙 /丙 / 丁 三奇。

 - **乙奇**（乙木）：**隐性助力**——老客户/暗中扶持
 - **丙奇**（丙火）：**显性机会**——新流量入口/明面机会
 - **丁奇**（丁火）：**细微转机**——微调纠错/补救失误

**判断**：
 -出现1 个奇：有局部机遇
 -出现2 个奇：机遇叠加
 - **三奇都齐**：大有可为，但需耐心 +主动识别
""")

st.markdown("---")

# === Tab3:6 大场景案例 ===
st.header("💼6 大场景案例")
st.markdown("**理论 +实践**——6 大生活场景的真实问卦案例。")

# 用 expander展示每个场景
scenarios = {
 "💼事业决策": {
 "icon": "💼",
 "question": "我该不该接那个8 万的兼职项目？",
 "qigua_method": "数字起卦（a=42, b=17）",
 "result": {
 "ben": "地天泰（11/64）",
 "zhi": "雷天大壮",
 "hu": "雷地豫",
 "cuo": "天地否",
 "zong": "天地泰（本卦）",
 },
 "interpretation": """
**卦象核心**：泰 = 通泰、平安。下卦乾（天/刚）上卦坤（地/柔）——刚柔并济，外柔内刚。

**6 层模型判断**：
 -阴阳遁：阳遁中（4 月），节奏平稳
 - 月令旺衰：4 月木旺，兼职属火，**相**——可做但要控成本
 - 主客分析：动爻在5爻，你是**客**（主动接）→兼职方**主**
 - 用神：5爻 +丙奇（显性机会）——这是明面上的机遇
 - 八门：休门（安稳）——合作起来不会太累
 - 三奇：丙奇到位（1/3）——机会真实但需努力

**行动建议**：
1. **可以接**——卦象显示这是一个真实机会
2. **但控制在月利润30% 以内**——客生主但火相不旺，别压太多
3. **签合同前确认3件事**：交付标准 /付款节奏 / 修改次数
4. **应期**：30 天后看效果
""",
 },
 "👨‍👩‍👧家庭关系": {
 "icon": "👨‍👩‍👧",
 "question": "我下周跟老婆吵架了，要不要主动道歉？",
 "qigua_method": "时间起卦",
 "result": {
 "ben": "泽水困（47/64）",
 "zhi": "泽地萃",
 "hu": "水风井",
 "cuo": "山火贲",
 "zong": "水泽节",
 },
 "interpretation": """
**卦象核心**：困 =困顿、艰难。上卦兑（泽/悦）下卦坎（水/险）——表面平和但内心有险。

**6 层模型判断**：
 -阴阳遁：阴遁中（9 月），内敛期——适合复盘、修复
 - 月令旺衰：9 月金旺，关系属火，**囚**——克制状态，需主动
 - 主客分析：动爻在2爻，你**主**（主动方）→老婆**客**（被动等待）
 - 用神：2爻（现状位）+乙奇（隐性助力）——身边有人会帮你
 - 八门：杜门（闭塞）——目前沟通不畅，需要打破
 - 三奇：乙奇到位——有人会暗中帮你修复

**行动建议**：
1. **必须主动**——你主客客，主动权在你
2. **不要硬扛**——杜门配囚，不沟通只会更糟
3. **借乙奇助力**——可以是孩子、岳父母、或共同朋友
4. **不要带礼物**——带礼物是主客克的信号，会让对方觉得"买赎"
5. **真诚道歉 +倾听**——困卦的关键是"先承认困，再找解法"
""",
 },
 "🎓子女教育": {
 "icon": "🎓",
 "question": "我家孩子要不要报这个2 万的补习班？",
 "qigua_method": "铜钱起卦（110100，第4爻变）",
 "result": {
 "ben": "风火家人（37/64）",
 "zhi": "风天小畜",
 "hu": "天火同人",
 "cuo": "水泽节",
 "zong": "火风鼎",
 },
 "interpretation": """
**卦象核心**：家人 =家庭和睦之道。上卦巽（风/顺）下卦离（火/明）——外顺内明。

**6 层模型判断**：
 -阴阳遁：阳遁末（6 月），攻的尾巴——决策要快
 - 月令旺衰：6 月火旺，教育属火，**旺**——适合投入
 - 主客分析：动爻在4爻，孩子**主**（被推动）→ 你**客**（决策方）
 - 用神：4爻（转折点）+丙奇（显性机会）——这是明面上的机遇
 - 八门：开门（顺）——适合开始新事
 - 三奇：丙奇到位——机会真实

**行动建议**：
1. **可以报**——卦象强烈支持
2. **但要看孩子意愿**——孩子主客关系，决定了学习效果
3. **设3 个月检验期**——旺月投入，9 月金旺时复盘效果
4. **配套：每天陪读30 分钟**——家人卦的核心是"家庭和睦"，不只是花钱
""",
 },
 "🏥 健康养生": {
 "icon": "🏥",
 "question": "我该不该做这个1 万的体检套餐？",
 "qigua_method": "数字起卦（a=88, b=18）",
 "result": {
 "ben": "山泽损（41/64）",
 "zhi": "地泽临",
 "hu": "地山谦",
 "cuo": "风雷益",
 "zong": "泽山咸",
 },
 "interpretation": """
**卦象核心**：损 =减损的平衡艺术。上卦艮（山/止）下卦兑（泽/悦）——止于外而悦于内。

**6 层模型判断**：
 -阴阳遁：阳遁中（5 月），节奏平稳
 - 月令旺衰：5 月火旺，健康属水，**囚**——克制状态，需主动养
 - 主客分析：动爻在1爻（初爻），你**主**（主动决定）→体检方**客**
 - 用神：1爻 +乙奇（隐性助力）——有人会推荐具体项目
 - 八门：休门（安稳）——检查过程不会太难受
 - 三奇：乙奇到位（隐性）——可能发现小问题但能提前处理

**行动建议**：
1. **应该做**——损卦配隐性问题，趁早发现
2. **选基础套餐**——不需要过度检查（主克客易白费）
3. **重点查：血压/血糖/甲状腺**——这是30+ 男性重点
4. **体检后调作息**——体检只是发现，关键是日常管理
""",
 },
 "💰财务投资": {
 "icon": "💰",
 "question": "我这10 万闲钱要不要投那个年化8% 的产品？",
 "qigua_method": "数字起卦（a=66, b=22）",
 "result": {
 "ben": "雷火丰（55/64）",
 "zhi": "雷地豫",
 "hu": "地火明夷",
 "cuo": "风水涣",
 "zong": "火雷噬嗑",
 },
 "interpretation": """
**卦象核心**：丰 =盛大、丰收。上卦震（雷/动）下卦离（火/明）——动而明。

**6 层模型判断**：
 -阴阳遁：阳遁末（6 月），攻的尾巴——决策要快
 - 月令旺衰：6 月火旺，投资属水，**囚**——克制状态，需谨慎
 - 主客分析：动爻在5爻（你**主**）→投资方**客**
 - 用神：5爻 + 白虎（速度）——快速决策
 - 八门：开门（顺）——产品流程合规
 - 三奇：缺（无奇）——没有明显机遇，需要自己判断

**行动建议**：
1. **谨慎**——6 层模型给的是"囚 +缺奇"，机会不显著
2. **先小额试水（1 万）**——白虎配开门，先试再放大
3. **明确4件事**：本金保障 /流动性 /退出机制 /风险等级
4. **不高于闲钱50%**——火克金，金融产品风险高
5. **30 天后复盘**——看实际收益 vs预期
""",
 },
 "🤝 人际社交": {
 "icon": "🤝",
 "question": "那个朋友约我合伙，我要不要答应？",
 "qigua_method": "时间起卦",
 "result": {
 "ben": "天火同人（13/64）",
 "zhi": "天水讼",
 "hu": "火水未济",
 "cuo": "地水师",
 "zong": "火天大有",
 },
 },
 "interpretation": """
**卦象核心**：同人 = 同心、志同道合。上卦乾（天/刚）下卦离（火/明）——刚健而光明。

**6 层模型判断**：
 -阴阳遁：阳遁中（4 月），节奏平稳
 - 月令旺衰：4 月木旺，合作属火，**相**——顺势可做
 - 主客分析：动爻在5爻（朋友**主**）→ 你**客**（被邀）
 - 用神：5爻 +丙奇（显性机会）——明面上的机会
 - 八门：开门（顺）——开始新事的好时机
 - 三奇：丙奇到位——机会真实

**行动建议**：
1. **可以答应**——同人卦是"志同道合"的吉卦
2. **但要明确分工**——丙奇配开门，先定清楚谁做什么
3. **签书面协议**——火配天，光明正大
4. **设3 个月磨合期**——合作需要时间
5. **保持独立性**——同人不是合二为一，是各有所长
""",
 }

# 选择场景
scenario_names = list(scenarios.keys())
selected = st.selectbox("选择场景查看案例", scenario_names)

scenario = scenarios[selected]
with st.expander(f"{scenario['icon']} {selected}完整案例", expanded=True):
 st.markdown(f"### 📝 问题")
 st.info(scenario["question"])
 st.markdown(f"### 🎯 起卦方式")
 st.code(scenario["qigua_method"])
 st.markdown("### 🔮卦象结果")
 col1, col2, col3, col4, col5 = st.columns(5)
 cols_data = [
 ("本卦", scenario["result"]["ben"]),
 ("之卦", scenario["result"]["zhi"]),
 ("互卦", scenario["result"]["hu"]),
 ("错卦", scenario["result"]["cuo"]),
 ("综卦", scenario["result"]["zong"]),
 ]
 for col, (label, value) in zip([col1, col2, col3, col4, col5], cols_data):
 with col:
 st.metric(label, value)
 st.markdown("### 📖完整解读")
 st.markdown(scenario["interpretation"])

 # 一键起卦按钮
 if st.button(f"🔮 用这个问题跑一卦", key=f"btn_{selected}"):
 with st.spinner("起卦中..."):
 try:
 cmd = ["python", "qigua.py", "--time", "--question", scenario["question"]]
 result = subprocess.run(
 cmd,
 capture_output=True,
 text=True,
 cwd=os.path.dirname(os.path.abspath(__file__)),
 timeout=30,
 )
 st.code(result.stdout, language="text")
 except Exception as e:
 st.error(f"出错了：{e}")

st.markdown("---")

# === Tab4: 关于 ===
st.header("⚙️ 关于 Qigua Pro")
st.markdown("""
**版本**: v3.0
**作者**: 黄耀锋 (yaofeng-huang)
**License**: MIT
**仓库**: 
 - GitHub: https://github.com/yaofeng-huang/qigua-pro
 - Gitee: https://gitee.com/yaofeng-huang/qigua-system

**核心定位**：
 - 不是算命
 - 不是预测
 - 是**结构化思考工具**

**命理边界**：
 -命理当民俗看
 - 方法论当工具用
 - 最终拍板的是人

**6 大不适用场景**：
 - ❌ 具体数字预测（中不中奖）
 - ❌情感安慰（他爱不爱我）
 - ❌宿命论（我命里有没有 X）
 - ❌ 求神问卦型问题
 - ❌模糊问题（边界不清）
 - ❌ 多问题合问

**适用场景**：事业/家庭/教育/健康/财务/社交6 大生活场景 +1688运营。
""")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
 🪙 Qigua Pro v3.0 · 让传统决策智慧成为现代人的工具
</div>
""", unsafe_allow_html=True)
