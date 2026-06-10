# -*- coding: utf-8 -*-
"""
Qigua Pro —演示录屏脚本
真实录制 CLI跑起来的画面，转成 GIF放到 README

录制方法：
1. 安装 ffmpeg：winget install Gyan.FFmpeg
2.准备 PowerShell终端窗口（建议黑底绿字字体）
3. 运行本脚本，自动录屏30 秒
4. 输出 demo.gif

手动录制方法（如果不想用脚本）：
 - 用 OBS Studio 或 Windows 自带录屏
 -跑 python qigua.py --time --question "..."
 -截取30 秒录屏
 - 转成 GIF（用 https://ezgif.com/video-to-gif 或 ffmpeg）
"""

import subprocess
import time
from pathlib import Path

def record_with_ffmpeg(duration=30, output="demo.gif"):
 """用 ffmpeg录屏"""
 print("🎬 开始录屏...")
 print(f"⏱️录制时长：{duration}秒")
 print(f"💾 输出文件：{output}")
 print()
 print("请在 PowerShell 里手动跑：")
 print(' python qigua.py --time --question "下周该不该接5万订单?"')
 print()
 print("⚠️ 请现在切换到 PowerShell窗口，30 秒后录屏结束")
 print()

 cmd = [
 "ffmpeg",
 "-f", "gdigrab",
 "-framerate", "15",
 "-i", "desktop",
 "-t", str(duration),
 "-vf", "fps=15,scale=800:-1:flags=lanczos",
 "-y",
 output,
 ]
 try:
 subprocess.run(cmd, check=True)
 print(f"✅录屏完成：{output}")
 except FileNotFoundError:
 print("❌ 没找到 ffmpeg，请先安装：winget install Gyan.FFmpeg")
 except subprocess.CalledProcessError as e:
 print(f"❌录屏失败：{e}")

if __name__ == "__main__":
 import sys
 duration = int(sys.argv[1]) if len(sys.argv) >1 else30
 output = sys.argv[2] if len(sys.argv) >2 else"demo.gif"
 record_with_ffmpeg(duration, output)
