"""
二手手机/平板验机 RAG 问答系统 - 后端服务

基于 FastAPI 构建，提供：
1. GET /api/brands - 获取品牌/型号树及验机知识
2. POST /api/ask - 基于 RAG 的自然语言问答

运行方式：python main.py
"""

import json
import os
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from api_clients import ZhipuEmbeddingClient, DeepSeekClient
from vector_store import VectorStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
VECTOR_DIR = BASE_DIR / "vector_store"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"

zhipu_client = ZhipuEmbeddingClient()
deepseek_client = DeepSeekClient()

app = FastAPI(
    title="二手手机/平板验机 RAG 问答系统",
    description="基于检索增强生成(RAG)的二手验机智能问答系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    logger.warning(f"静态文件目录不存在: {STATIC_DIR}")


def load_knowledge() -> dict:
    """加载知识库 JSON 文件"""
    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(f"知识库文件不存在: {KNOWLEDGE_FILE}")
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_vector_store() -> VectorStore | None:
    """获取向量存储实例，检查是否有数据"""
    store = VectorStore(persist_dir=str(VECTOR_DIR))
    if store.count() == 0:
        logger.warning("向量库为空，请先运行 index_kb.py")
        return None
    return store


@app.get("/api/brands")
def get_brands():
    """获取品牌/型号树及验机知识"""
    try:
        data = load_knowledge()
        logger.info("知识库数据加载成功")
        return data
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"知识库 JSON 解析错误: {e}")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    images: list[str]


@app.post("/api/ask", response_model=AskResponse)
def ask_question(req: AskRequest):
    """
    RAG 问答接口

    流程：
    1. 用户问题 → 智谱 Embedding API 向量化
    2. 向量库中检索 top-3 最相似知识片段
    3. 拼接上下文 → 调用 DeepSeek API 生成答案
    4. 返回答案文本 + 相关图片 URL 列表
    """
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    question = req.question.strip()
    logger.info(f"收到问题: {question}")

    # 1. 向量化
    try:
        query_embedding = zhipu_client.get_embedding(question)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"向量化失败: {e}")
    except Exception as e:
        logger.error(f"向量化异常: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"向量化服务异常: {str(e)}")

    # 2. 检索
    store = get_vector_store()
    if store is None:
        raise HTTPException(
            status_code=500,
            detail="向量库未初始化，请先运行 index_kb.py 建立索引"
        )

    try:
        results = store.query(query_embedding, n_results=3)
    except Exception as e:
        logger.error(f"检索失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"知识检索失败: {e}")

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        answer = "抱歉，知识库中没有找到与您问题相关的验机信息。请尝试换个问法。"
        return AskResponse(answer=answer, images=[])

    # 拼接上下文
    context_parts = []
    images = []
    seen_images = set()

    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        brand = meta.get("brand", "未知品牌")
        model = meta.get("model", "未知型号")
        category = meta.get("category", "未知项")
        img_url = meta.get("img_url", "")

        context_parts.append(
            f"【参考{i+1}】品牌: {brand} | 型号: {model} | 验机项: {category}\n内容: {doc}"
        )
        if img_url:
            # 支持JSON数组格式的多张图
            urls = []
            if img_url.startswith('['):
                try: urls = json.loads(img_url)
                except: urls = [img_url]
            else:
                urls = [img_url]
            for u in urls:
                if u and u not in seen_images:
                    images.append(u)
                    seen_images.add(u)

    context = "\n\n".join(context_parts)
    similarity_info = (
        f"\n(检索相似度范围: {min(distances):.4f} ~ {max(distances):.4f})"
        if distances else ""
    )

    logger.info(f"检索到 {len(documents)} 条相关知识，{len(images)} 张相关图片")

    # 3. 调用 DeepSeek
    system_prompt = (
        "你是专业的二手手机/平板验机顾问。请基于提供的验机知识库内容，"
        "回答用户的验机相关问题。\n\n回答要求：\n"
        "1. 如果知识库中有相关信息，请基于知识库内容给出详细准确的回答\n"
        "2. 如果知识库中没有完全匹配的信息，请根据相近内容给出参考建议\n"
        "3. 建议实际的验机操作步骤，让用户能够动手测试\n"
        "4. 如果用户问题与验机无关，礼貌地告知本系统仅回答二手验机相关问题\n"
        "5. 回答使用中文，清晰有条理"
    )

    user_prompt = (
        f"【知识库参考信息】\n{context}\n{similarity_info}\n\n"
        f"【用户问题】\n{question}\n\n"
        f"请根据以上参考信息回答用户的问题。"
    )

    try:
        answer = deepseek_client.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"AI 回答生成失败: {e}")
    except Exception as e:
        logger.error(f"DeepSeek 调用异常: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AI 服务异常: {str(e)}")

    logger.info(f"回答生成完成，长度: {len(answer)} 字符，关联图片: {len(images)} 张")
    return AskResponse(answer=answer, images=images)


@app.get("/api/health")
def health_check():
    """健康检查接口"""
    store = get_vector_store()
    kb_ready = store is not None
    count = store.count() if kb_ready else 0
    return {
        "status": "ok",
        "vector_store_ready": kb_ready,
        "vector_store_count": count,
        "knowledge_file_exists": KNOWLEDGE_FILE.exists()
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 50)
    logger.info("二手手机/平板验机 RAG 问答系统")
    logger.info("=" * 50)
    logger.info(f"启动服务: http://localhost:8000/static/index.html")
    logger.info("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
