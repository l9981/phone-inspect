"""
知识库向量索引脚本

将 knowledge.json 中的验机知识逐条向量化并存入向量数据库。
在运行主程序之前，必须执行此脚本建立索引。

用法：
    cd backend
    python scripts/index_kb.py
"""

import json
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api_clients import ZhipuEmbeddingClient
from vector_store import VectorStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DIR = BASE_DIR / "vector_store"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"


def load_knowledge() -> dict:
    """加载知识库 JSON 文件"""
    if not KNOWLEDGE_FILE.exists():
        logger.error(f"知识库文件不存在: {KNOWLEDGE_FILE}")
        sys.exit(1)
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_documents(data: dict) -> list:
    """
    将知识库数据转换为文档块列表

    每个验机点生成一个文档块，包含品牌、型号、验机项、
    描述和特别注意事项等信息。
    """
    documents = []
    doc_id = 0

    for brand in data.get("brands", []):
        brand_name = brand["name"]
        for model in brand.get("models", []):
            model_name = model["name"]
            for point in model.get("check_points", []):
                category = point["category"]
                description = point["description"]
                special_note = point.get("special_note", "")
                img_url = point.get("compare_img", "")

                doc_text = (
                    f"品牌: {brand_name}\n"
                    f"型号: {model_name}\n"
                    f"验机项: {category}\n"
                    f"正常/故障描述: {description}\n"
                )
                if special_note:
                    doc_text += f"特别注意事项: {special_note}"

                metadata = {
                    "brand": brand_name,
                    "model": model_name,
                    "category": category,
                    "img_url": img_url,
                    "doc_id": str(doc_id)
                }

                documents.append({
                    "id": f"doc_{doc_id}",
                    "text": doc_text,
                    "metadata": metadata
                })
                doc_id += 1

    return documents


def index_knowledge():
    """主索引流程"""
    logger.info("=" * 50)
    logger.info("知识库向量索引工具")
    logger.info("=" * 50)

    # 1. 加载知识库
    logger.info(f"正在加载知识库: {KNOWLEDGE_FILE}")
    data = load_knowledge()
    documents = build_documents(data)
    logger.info(f"共生成 {len(documents)} 个文档块")

    # 2. 初始化 Embedding 客户端
    client = ZhipuEmbeddingClient()
    try:
        test_vec = client.get_embedding("测试连接")
        logger.info(f"智谱 Embedding API 连接成功，向量维度: {len(test_vec)}")
    except ValueError as e:
        logger.error(str(e))
        logger.error("请先在 api_clients.py 中替换 ZHIPU_API_KEY")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"智谱 API 连接失败: {e}")
        sys.exit(1)

    # 3. 初始化向量存储（清空重建）
    logger.info(f"初始化向量存储: {VECTOR_DIR}")
    store = VectorStore(persist_dir=str(VECTOR_DIR))
    store.clear()

    # 4. 逐条生成向量并添加
    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for i, doc in enumerate(documents):
        logger.info(f"[{i+1}/{len(documents)}] 处理: "
                     f"{doc['metadata']['brand']} {doc['metadata']['model']} "
                     f"- {doc['metadata']['category']}")
        try:
            embedding = client.get_embedding(doc["text"])
            ids.append(doc["id"])
            texts.append(doc["text"])
            metadatas.append(doc["metadata"])
            embeddings.append(embedding)
        except RuntimeError as e:
            logger.warning(f"  跳过: {e}")
            continue

    # 5. 写入向量存储
    if ids:
        store.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
        logger.info(f"✅ 索引成功！共存入 {store.count()} 条知识记录")
        logger.info(f"存储位置: {VECTOR_DIR}")
    else:
        logger.error("没有有效文档可索引")
        sys.exit(1)

    # 6. 汇总
    logger.info("")
    logger.info("=" * 50)
    logger.info("索引完成！")
    logger.info(f"品牌数: {len(data.get('brands', []))}")
    model_count = sum(len(b.get("models", [])) for b in data.get("brands", []))
    logger.info(f"型号数: {model_count}")
    check_count = sum(
        len(m.get("check_points", []))
        for b in data.get("brands", [])
        for m in b.get("models", [])
    )
    logger.info(f"验机点数: {check_count}")
    logger.info(f"已索引: {len(ids)} 条")
    logger.info("现在可以启动主程序了: python main.py")
    logger.info("=" * 50)


if __name__ == "__main__":
    index_knowledge()
