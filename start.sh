#!/bin/bash

# ================================================
# 二手手机/平板验机 RAG 问答系统 - 启动脚本 (Linux/Mac)
# ================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  二手手机/平板验机 RAG 问答系统${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 进入 backend 目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/backend" || {
    echo -e "${RED}[错误] 无法进入 backend 目录${NC}"
    exit 1
}

# 检查 Python
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON=python
    else
        echo -e "${RED}[错误] 未检测到 Python，请确保已安装 Python 3.9+${NC}"
        echo "下载地址: https://www.python.org/downloads/"
        exit 1
    fi
else
    PYTHON=python3
fi

echo -e "${YELLOW}[检测] Python 版本:${NC}"
$PYTHON --version

# 检查依赖
echo ""
echo -e "${YELLOW}[检查] 检查依赖安装...${NC}"
$PYTHON -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[提示] 安装依赖中...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        # 尝试 pip3
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}[错误] 依赖安装失败，请手动执行: pip install -r requirements.txt${NC}"
            exit 1
        fi
    fi
fi
echo -e "${GREEN}[OK] 依赖检查完成${NC}"

# 检查向量库
echo ""
echo -e "${YELLOW}[检查] 检查向量库索引...${NC}"
$PYTHON -c "
import chromadb, sys
from pathlib import Path
try:
    c = chromadb.PersistentClient(path=str(Path('chroma_db')))
    c.get_collection('inspect_kb')
    print('ok')
except:
    sys.exit(1)
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[提示] 向量库未初始化，正在索引知识库...${NC}"
    $PYTHON scripts/index_kb.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 索引失败，请检查 api_clients.py 中的 API Key 配置${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[OK] 向量库就绪${NC}"

# 启动后端
echo ""
echo -e "${GREEN}[启动] 正在启动后端服务...${NC}"

# 清理旧进程
if [ -f server.pid ]; then
    kill $(cat server.pid) 2>/dev/null
    rm server.pid
fi

# 后台运行
nohup $PYTHON main.py > server.log 2>&1 &
PID=$!
echo $PID > server.pid

# 等待启动
echo -e "${YELLOW}[等待] 正在等待服务启动...${NC}"
sleep 3

# 检查是否启动成功
if kill -0 $PID 2>/dev/null; then
    URL="http://localhost:8000/static/index.html"
    echo -e "${GREEN}[成功] 后端服务已启动 (PID: $PID)${NC}"
    echo ""
    echo -e "${GREEN}[访问] 浏览器已自动打开:${NC}"
    echo "  $URL"
    echo ""

    # 自动打开浏览器
    if command -v xdg-open &> /dev/null; then
        xdg-open "$URL" 2>/dev/null
    elif command -v open &> /dev/null; then
        open "$URL" 2>/dev/null
    elif command -v gnome-open &> /dev/null; then
        gnome-open "$URL" 2>/dev/null
    else
        echo -e "${YELLOW}请手动在浏览器中打开: $URL${NC}"
    fi

    echo -e "${YELLOW}按 Ctrl+C 停止服务...${NC}"
    echo ""

    # 等待 Ctrl+C
    trap "echo ''; echo -e '${YELLOW}正在停止服务...${NC}'; kill $PID 2>/dev/null; rm -f server.pid; echo -e '${GREEN}服务已停止。${NC}'; exit 0" INT TERM
    while true; do
        sleep 1
    done
else
    echo -e "${RED}[错误] 服务启动失败，请查看 server.log 获取详细信息${NC}"
    cat server.log 2>/dev/null
    exit 1
fi
