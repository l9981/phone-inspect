"""
API 客户端封装

提供 DeepSeek 大语言模型和智谱 AI Embedding 的调用接口。
用户需要自行替换两个 API Key 才能正常使用。
"""

import requests
import json
import logging

logger = logging.getLogger(__name__)

# ============================================================
# ⚠️ 请在下方替换为你的真实 API Key
# ============================================================

# 智谱 AI API Key (从 https://open.bigmodel.cn 注册获取)
# 注册后进入控制台 → API密钥 → 新建API key（赠送额度足够本作业使用）
ZHIPU_API_KEY = "c7ae8c21fa8d4db3a5c83c7796b0b20e.rNV3RK9EDj955N3c"

# DeepSeek API Key (从 https://platform.deepseek.com 注册获取)
# 注册即送 500 万 tokens，进入 API Keys 页面创建
DEEPSEEK_API_KEY = "sk-b321c40349d24a688e9a1946cf95ef9f"

# ============================================================


class ZhipuEmbeddingClient:
    """智谱 AI Embedding API 客户端

    使用智谱 AI 的 embedding-2 模型将文本转换为向量表示。
    该模型免费使用，适用于中小规模知识库的向量化。

    官方文档：https://open.bigmodel.cn/dev/api/text-embedding
    """

    def __init__(self, api_key: str = None):
        """
        初始化 Embedding 客户端

        Args:
            api_key: 智谱 AI API Key，不传则使用默认占位符
        """
        self.api_key = api_key or ZHIPU_API_KEY
        if self.api_key == "你的智谱API_KEY":
            logger.warning("⚠️ 智谱 API Key 未替换！请在 api_clients.py 中填入你的 Key。")
        self.url = "https://open.bigmodel.cn/api/paas/v4/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_embedding(self, text: str) -> list:
        """
        将文本转换为向量

        Args:
            text: 需要向量化的文本内容

        Returns:
            list: 768 维的浮点数向量

        Raises:
            ValueError: API Key 未替换时抛出
            RuntimeError: API 调用失败时抛出
        """
        if self.api_key == "你的智谱API_KEY":
            raise ValueError("请先在 api_clients.py 中替换 ZHIPU_API_KEY 为你的真实 Key")

        payload = {
            "model": "embedding-2",
            "input": text
        }

        try:
            logger.info(f"调用智谱 Embedding API，文本长度: {len(text)} 字符")
            resp = requests.post(
                self.url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            embedding = result["data"][0]["embedding"]
            logger.info(f"向量生成成功，维度: {len(embedding)}")
            return embedding
        except requests.exceptions.Timeout:
            raise RuntimeError("智谱 Embedding API 请求超时(30s)，请检查网络连接")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            detail = e.response.text[:200] if e.response.text else "无详细信息"
            if status == 401:
                raise RuntimeError("智谱 API Key 无效或已过期，请检查 ZHIPU_API_KEY")
            elif status == 429:
                raise RuntimeError("智谱 API 请求过于频繁，请稍后重试（限流）")
            elif status == 500:
                raise RuntimeError("智谱服务器内部错误，请稍后重试")
            else:
                raise RuntimeError(f"智谱 API HTTP {status}: {detail}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("无法连接到智谱 API，请检查网络连接或代理设置")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise RuntimeError(f"解析智谱 API 响应失败: {str(e)}")


class DeepSeekClient:
    """DeepSeek 大语言模型 API 客户端

    使用 DeepSeek Chat 模型进行对话生成，适用于 RAG 问答。
    推荐参数：temperature=0.3 以保证答案的准确性。

    官方文档：https://platform.deepseek.com/api-docs
    """

    def __init__(self, api_key: str = None):
        """
        初始化 DeepSeek 客户端

        Args:
            api_key: DeepSeek API Key，不传则使用默认占位符
        """
        self.api_key = api_key or DEEPSEEK_API_KEY
        if self.api_key == "你的DeepSeek_API_KEY":
            logger.warning("⚠️ DeepSeek API Key 未替换！请在 api_clients.py 中填入你的 Key。")
        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """
        发送对话消息并获取模型回复

        Args:
            messages: 对话消息列表，格式为 [{"role": "user"/"system", "content": "..."}]
            temperature: 生成温度(0-2)，越低越确定，建议0.3
            max_tokens: 最大生成 token 数

        Returns:
            str: 模型生成的回答文本

        Raises:
            ValueError: API Key 未替换时抛出
            RuntimeError: API 调用失败时抛出
        """
        if self.api_key == "你的DeepSeek_API_KEY":
            raise ValueError("请先在 api_clients.py 中替换 DEEPSEEK_API_KEY 为你的真实 Key")

        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            logger.info(f"调用 DeepSeek Chat API，消息数: {len(messages)}")
            resp = requests.post(
                self.url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            answer = result["choices"][0]["message"]["content"]
            logger.info(f"DeepSeek 回答生成成功，长度: {len(answer)} 字符")
            return answer
        except requests.exceptions.Timeout:
            raise RuntimeError("DeepSeek API 请求超时(30s)，请检查网络连接")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            detail = e.response.text[:200] if e.response.text else "无详细信息"
            if status == 401:
                raise RuntimeError("DeepSeek API Key 无效或已过期，请检查 DEEPSEEK_API_KEY")
            elif status == 402:
                raise RuntimeError("DeepSeek 账户余额不足，请充值")
            elif status == 429:
                raise RuntimeError("DeepSeek API 请求频率过高，请稍后重试")
            elif status == 500:
                raise RuntimeError("DeepSeek 服务器内部错误，请稍后重试")
            else:
                raise RuntimeError(f"DeepSeek API HTTP {status}: {detail}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("无法连接到 DeepSeek API，请检查网络连接或代理设置")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise RuntimeError(f"解析 DeepSeek API 响应失败: {str(e)}")


if __name__ == "__main__":
    """测试 API 连接"""
    logging.basicConfig(level=logging.INFO)

    # 测试 Embedding
    client = ZhipuEmbeddingClient()
    try:
        vec = client.get_embedding("测试文本")
        print(f"✅ Embedding 测试成功，向量维度: {len(vec)}")
    except (ValueError, RuntimeError) as e:
        print(f"❌ Embedding 测试失败: {e}")

    # 测试 Chat
    deepseek = DeepSeekClient()
    try:
        answer = deepseek.chat([
            {"role": "system", "content": "你是验机助手，请简短回答。"},
            {"role": "user", "content": "你好"}
        ])
        print(f"✅ DeepSeek Chat 测试成功: {answer[:50]}...")
    except (ValueError, RuntimeError) as e:
        print(f"❌ DeepSeek Chat 测试失败: {e}")
