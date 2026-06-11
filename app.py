import streamlit as st
import subprocess
import os
st.set_page_config(page_title="Qigua Pro", page_icon="🪙", layout="wide")
st.title("🪙 Qigua Pro")
st.subheader("传统决策手艺")
st.markdown("---")
st.header("起卦")
question = st.text_input("问题", placeholder="下周该不该接5万订单")
method = st.radio("方式", ["数字", "时间", "铜钱"])
a =0
b =0
if method == "数字":
 a = st.number_input("数字 a", value=88)
 b = st.number_input("数字 b", value=18)
run = st.button("起卦")
if not run:
 st.stop()
if question == "":
 st.error("请先填写问题")
 st.stop()
with st.spinner("起卦中"):
 cmd = ["python", "qigua.py", "--question", question]
 if method == "数字":
  cmd = ["python", "qigua.py", "--number", str(int(a)), str(int(b)), "--question", question]
 elif method == "时间":
  cmd = ["python", "qigua.py", "--time", "--question", question]
 result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)), timeout=30)
if result.returncode ==0:
 st.success("✅ 起卦成功")
 st.code(result.stdout)
else:
 st.error("起卦失败")
 st.code(result.stderr)
st.markdown("---")
with st.expander("6层模型速查"):
 st.markdown("1.阴阳遁2.月令旺衰3.爻位六神4.用神5.八门九星6.三奇")
with st.expander("6大场景案例"):
 st.markdown("-事业 -家庭 - 教育 - 健康 -财务 -社交")
st.markdown("MIT · 黄耀锋 · v3.0")
