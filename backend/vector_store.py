"""
轻量级向量存储

用 numpy 实现余弦相似度检索，替代 chromadb。
纯 Python 实现，无需 C++ 编译，适合 Windows 环境。

数据持久化到 JSON 文件，无需额外数据库服务。
"""

import json
import numpy as np
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """轻量向量存储，基于 numpy 余弦相似度检索"""

    def __init__(self, persist_dir: str = "vector_store"):
        """
        初始化向量存储

        Args:
            persist_dir: 数据持久化目录
        """
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.persist_dir / "data.json"

        # 内存数据
        self.ids: list[str] = []
        self.documents: list[str] = []
        self.metadatas: list[dict] = []
        self.embeddings: list[list[float]] = []

        # 尝试从文件加载
        self._load()

    def _load(self):
        """从文件加载数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.ids = data.get("ids", [])
                self.documents = data.get("documents", [])
                self.metadatas = data.get("metadatas", [])
                self.embeddings = data.get("embeddings", [])
                logger.info(f"已加载向量存储: {len(self.ids)} 条记录")
            except Exception as e:
                logger.warning(f"加载向量存储失败，将重新创建: {e}")

    def save(self):
        """保存数据到文件"""
        data = {
            "ids": self.ids,
            "documents": self.documents,
            "metadatas": self.metadatas,
            "embeddings": self.embeddings,
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"向量存储已保存: {len(self.ids)} 条记录")

    def add(self, ids: list[str], documents: list[str],
            metadatas: list[dict], embeddings: list[list[float]]):
        """
        添加向量数据

        Args:
            ids: 唯一标识列表
            documents: 文本内容列表
            metadatas: 元数据列表
            embeddings: 向量列表
        """
        self.ids.extend(ids)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self.embeddings.extend(embeddings)
        self.save()

    def count(self) -> int:
        """返回记录总数"""
        return len(self.ids)

    def clear(self):
        """清空所有数据"""
        self.ids = []
        self.documents = []
        self.metadatas = []
        self.embeddings = []
        if self.data_file.exists():
            self.data_file.unlink()
        logger.info("向量存储已清空")

    def query(self, query_embedding: list[float], n_results: int = 3) -> dict:
        """
        查询最相似的文档

        使用余弦相似度计算向量距离。

        Args:
            query_embedding: 查询向量
            n_results: 返回结果数

        Returns:
            dict: 包含 ids, documents, metadatas, distances 的字典
                  (格式与 chromadb 兼容，便于替换)
        """
        if not self.embeddings:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

        # 转为 numpy 数组
        query_vec = np.array(query_embedding, dtype=np.float32)
        all_vecs = np.array(self.embeddings, dtype=np.float32)

        # 计算余弦相似度 → 距离 (1 - cos_sim)
        # 先归一化
        query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
        all_norms = all_vecs / (np.linalg.norm(all_vecs, axis=1, keepdims=True) + 1e-10)

        cos_sims = np.dot(all_norms, query_norm)
        distances = 1.0 - cos_sims  # 越小越相似

        # 取 top-k
        n = min(n_results, len(distances))
        top_indices = np.argsort(distances)[:n]

        result_ids = [self.ids[i] for i in top_indices]
        result_docs = [self.documents[i] for i in top_indices]
        result_metas = [self.metadatas[i] for i in top_indices]
        result_dists = [float(distances[i]) for i in top_indices]

        logger.info(f"向量检索: {len(self.embeddings)} 条中返回 top-{n}")

        return {
            "ids": [result_ids],
            "documents": [result_docs],
            "metadatas": [result_metas],
            "distances": [result_dists]
        }
