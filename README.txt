================================================================================
  二手手机/平板验机 RAG 问答系统 — 完整使用说明
================================================================================

一、项目简介
--------------------------------------------------------------------------------
本项目是一个基于 RAG（检索增强生成）技术的二手手机/平板验机智能问答系统。
用户可以通过左侧树形菜单浏览各品牌型号的验机知识，也可以通过自然语言向
AI 提问验机相关问题，系统会从知识库中检索相关片段，调用大模型生成回答。

技术栈：
  - 后端：Python + FastAPI + Uvicorn
  - 向量数据库：Chroma（本地持久化）
  - Embedding 模型：智谱 AI embedding-2（免费）
  - 大语言模型：DeepSeek Chat（注册送 500 万 tokens）
  - 前端：HTML/CSS/JS（原生实现，无框架依赖）


二、运行环境要求
--------------------------------------------------------------------------------
  - 操作系统：Windows 10/11 / macOS / Linux
  - Python 3.9 或更高版本
  - 网络：能够访问 api.deepseek.com 和 open.bigmodel.cn


三、前期准备 — 注册 API Key（必须）
--------------------------------------------------------------------------------
本系统需要两个免费的 API Key，请按以下步骤注册获取：

【1】智谱 AI API Key（用于文本向量化）
  - 访问 https://open.bigmodel.cn 注册账号
  - 登录后进入「API 密钥」页面
  - 点击「新建 API 密钥」，复制生成的 Key
  - 注册即赠送额度，本系统使用量极小，完全免费

【2】DeepSeek API Key（用于 AI 问答）
  - 访问 https://platform.deepseek.com 注册账号
  - 登录后进入「API Keys」页面
  - 点击「Create API Key」，复制生成的 Key
  - 注册即赠送 500 万 tokens，足够本作业使用

【3】填写 API Key
  - 用记事本或 VS Code 打开 backend/api_clients.py
  - 找到第 18 行：ZHIPU_API_KEY = "你的智谱API_KEY"
    将「你的智谱API_KEY」替换为刚才获取的智谱 Key
  - 找到第 22 行：DEEPSEEK_API_KEY = "你的DeepSeek_API_KEY"
    将「你的DeepSeek_API_KEY」替换为刚才获取的 DeepSeek Key
  - 保存文件


四、快速启动
--------------------------------------------------------------------------------

Windows 用户：
  1. 安装 Python 3.9+（从 python.org 下载，安装时勾选 Add to PATH）
  2. 在项目根目录双击 start.bat
  3. 脚本会自动安装依赖、索引知识库、启动服务并打开浏览器

macOS / Linux 用户：
  1. 确保已安装 Python 3.9+
  2. 打开终端，进入项目根目录
  3. 执行：chmod +x start.sh
  4. 执行：./start.sh

手动分步操作（如果一键启动失败）：
  1. 安装依赖
     pip install -r backend/requirements.txt

  2. 索引知识库（只执行一次）
     cd backend
     python scripts/index_kb.py

  3. 启动服务
     python main.py

  4. 打开浏览器访问
     http://localhost:8000/static/index.html


五、系统使用说明
--------------------------------------------------------------------------------

功能一：浏览验机知识
  - 左侧边栏展示「品牌 → 型号」树形菜单
  - 点击品牌名称展开/收起型号列表
  - 点击型号名称，右侧显示该型号的验机表格
  - 表格包含：验机项、正常/故障描述、特别注意、对比图

功能二：RAG 智能问答
  - 在底部输入框中输入问题（如 "iPhone 14 Pro Max 电池健康怎么看？"）
  - 点击「提问」按钮或按 Enter 键
  - 系统会：
    (1) 将你的问题转为向量
    (2) 从知识库中检索最相关的 3 条知识
    (3) 调用 DeepSeek AI 生成回答
    (4) 返回回答文本和相关参考图片

  - 推荐问题示例：
    · iPhone 14 Pro Max 屏幕绿屏怎么检查？
    · 小米14 Ultra 徕卡摄像头怎么验机？
    · iPhone 13 面容 ID 坏了能修吗？
    · Redmi Note 12 Turbo 性能怎么测试？
    · 二手手机电池健康低于多少不建议买？
    · 防水功能在二手手机上怎么验证？


六、项目文件结构
--------------------------------------------------------------------------------
project_root/
├── backend/
│   ├── data/
│   │   └── knowledge.json      # 验机知识库数据（可自定义扩充）
│   ├── scripts/
│   │   └── index_kb.py         # 知识库向量索引脚本
│   ├── static/
│   │   └── index.html          # 前端 Web 页面
│   ├── chroma_db/              # Chroma 向量数据库（自动生成）
│   ├── api_clients.py          # DeepSeek + 智谱 API 客户端封装
│   ├── main.py                 # FastAPI 后端主程序
│   └── requirements.txt        # Python 依赖清单
├── start.bat                   # Windows 启动脚本
├── start.sh                    # Linux/Mac 启动脚本
└── README.txt                  # 本说明文件


七、自定义扩充知识库
--------------------------------------------------------------------------------
如需添加更多品牌、型号或验机项，编辑 backend/data/knowledge.json 即可。
JSON 结构如下：

{
  "brands": [
    {
      "name": "品牌名",
      "models": [
        {
          "name": "型号名",
          "check_points": [
            {
              "category": "验机项名称（如 屏幕显示）",
              "description": "正常/故障描述",
              "special_note": "特别注意事项",
              "compare_img": "对比图片URL"
            }
          ]
        }
      ]
    }
  ]
}

编辑后重新运行索引脚本即可更新向量库：
  cd backend
  python scripts/index_kb.py

图片 URL 可以使用 picsum.photos 占位图，或替换为真实图片 URL。
如果要使用本地图片，请将图片放入 backend/static/images/ 目录，
然后在 knowledge.json 中填写相对路径（如 /static/images/xxx.jpg），
但由于 Chrome 安全策略，建议使用在线图片 URL。


八、课程作业补充说明
--------------------------------------------------------------------------------

【UML 图绘制指导】（需用户自行绘制）

本系统涉及以下 UML 图，建议使用 Draw.io（免费在线工具）绘制：

1. 用例图 (Use Case Diagram)
   - 角色：用户
   - 用例：
     · 浏览品牌/型号树
     · 查看验机表格
     · 提问验机问题
     · 查看 AI 回答
   - 建议：将「提问验机问题」include 关系指向「检索知识库」和「调用 AI 生成答案」

2. 类图 (Class Diagram)
   - 主要类：
     · FastAPI 应用 (MainApp)
     · 知识库管理 (KnowledgeManager)
     · 向量检索器 (VectorRetriever)
     · DeepSeekClient（封装 DeepSeek API）
     · ZhipuEmbeddingClient（封装智谱 Embedding API）
     · 前端页面 (Frontend)
   - 需要标注类的属性、方法及类间关系（关联、依赖）

3. 顺序图 (Sequence Diagram)
   - 场景 A：用户浏览型号验机表
     · 用户 → 前端 → 后端 /api/brands → 读取 knowledge.json → 返回数据 → 渲染表格
   - 场景 B：用户提问 RAG 问答
     · 用户 → 前端 → 后端 /api/ask → 智谱 Embedding API → Chroma 检索
       → DeepSeek API → 返回答案和图片 → 前端展示


【演示视频必备回答要点】

在演示视频中，请务必回答以下问题：

Q1: 本系统解决了什么痛点？
A1:
  - 信息不对称：二手交易中买家缺乏专业知识，卖家可能隐瞒问题
  - 验机知识碎片化：网上验机教程分散在不同平台，查找费时
  - 缺乏图像对比：纯文字描述难以判断故障程度
  - 本系统将结构化验机知识 + 图片对比 + AI 问答结合，一站式解决问题

Q2: 创新性体现在哪里？
A2:
  - RAG 技术的应用：传统问答只能检索固定的 FAQ，本系统通过 RAG
    让 AI 理解问题并从知识库中检索相关信息后生成答案，准确且灵活
  - 图片与文本联合返回：不只有文字回答，还关联相关对比图
  - 完全免费：利用两家国内 AI 平台免费额度，零成本部署
  - 结构化 + 非结构化融合：既有表格化验机清单，又有自然语言问答

Q3: 系统局限性及改进方向？
A3:
  - 当前知识库手动构建，可开发自动爬取验机文章的工具
  - 可增加用户上传验机图片、AI 自动检测故障的功能（接入多模态模型）
  - 可添加用户评价、验机报告导出功能


九、故障排除
--------------------------------------------------------------------------------

问题 1：pip install 报错
  → 尝试：pip install --upgrade pip
  → 或使用：python -m pip install -r backend/requirements.txt

问题 2：Chroma 相关错误
  → 确保 Python 版本 ≥ 3.9
  → 可尝试更新 chromadb：pip install --upgrade chromadb

问题 3：智谱 API 调用失败
  → 确认 ZHIPU_API_KEY 已正确替换
  → 检查网络是否能访问 open.bigmodel.cn

问题 4：DeepSeek API 调用失败
  → 确认 DEEPSEEK_API_KEY 已正确替换
  → 检查 DeepSeek 账户是否有余额（新注册有 500 万免费额度）
  → 从 platform.deepseek.com 查看 API 使用情况

问题 5：端口 8000 被占用
  → 修改 backend/main.py 最后一行 port=8000 为其他端口（如 8001）
  → 同时修改 start.bat / start.sh 中的访问地址

问题 6：前端页面打开但空白或报错
  → 按 F12 打开浏览器开发者工具，查看 Console（控制台）中的错误信息
  → 确认后端服务是否正在运行（重新运行启动脚本）
  → 确认浏览器未阻止 localhost 的跨域请求


十、API 接口文档（供扩展开发参考）
--------------------------------------------------------------------------------

启动服务后，访问以下地址可查看自动生成的 OpenAPI 文档：
  http://localhost:8000/docs

主要接口：
  GET  /api/brands     → 获取品牌树 JSON
  POST /api/ask        → RAG 问答 {"question": "..."}
  GET  /api/health     → 健康检查


================================================================================
  祝您顺利完成课程作业！📱✨
================================================================================
