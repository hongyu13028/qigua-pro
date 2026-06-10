# -*- coding: utf-8 -*-
"""
Qigua Pro - Streamlit Web UI
"""

import streamlit as st
import subprocess
import os
from pathlib import Path
from datetime import datetime

st.set_page_config(
 page_title="Qigua Pro",
 page_icon="🪙",
 layout="wide",
)

st.title("🪙 Qigua Pro")
st.subheader("传统决策手艺")
st.markdown("---")

with st.sidebar:
 st.header("📖快速导航")
 st.markdown("[🪙 起卦](#起卦)")
 st.markdown("---")
 st.markdown("**版本**: v3.0")

st.header("🪙 起卦")

question = st.text_input(
 "📝你的具体问题",
 placeholder="例: 下周该不该接5万订单?",
)

col1, col2 = st.columns(2)
with col1:
 method = st.radio("起卦方式", ["数字", "时间", "铜钱"], horizontal=True)

if method == "数字":
 with col2:
 a = st.number_input("数字 a", value=88)
 b = st.number_input("数字 b", value=18)

if st.button("🔮 起卦", type="primary"):
 if not question:
 st.error("请先填写问题")
 else:
 with st.spinner("起卦中..."):
 try:
 cmd = ["python", "qigua.py"]
 if method == "数字":
 cmd.extend(["--number", str(int(a)), str(int(b))])
 else:
 cmd.extend(["--time"])
 cmd.extend(["--question", question])

 result = subprocess.run(
 cmd,
 capture_output=True,
 text=True,
 cwd=os.path.dirname(os.path.abspath(__file__)),
 timeout=30,
 )

 if result.returncode ==0:
 st.success("✅ 起卦成功")
 st.code(result.stdout)
 else:
 st.error("起卦失败")
 st.code(result.stderr)
 except Exception as e:
 st.error(f"出错: {e}")

st.markdown("---")
st.markdown("**MIT License** · **黄耀锋** · v3.0")
