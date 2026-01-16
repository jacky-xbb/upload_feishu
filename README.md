# 飞书文件上传工具

这个工具可以扫描指定目录下所有子文件夹中的 `00_Publish` 目录，并将其中的文件上传到飞书云文档。

## 环境要求

- Python 3.7+
- 支持 Windows、macOS、Linux

## 安装依赖

```bash
pip install lark-oapi python-dotenv
```

## 配置

在项目根目录创建 `.env` 文件，填入以下配置：

```env
FEISHU_APP_ID=你的应用ID
FEISHU_APP_SECRET=你的应用密钥
FEISHU_PARENT_NODE=目标文件夹Token
```

### 获取配置信息

1. **应用 ID 和密钥**：

   - 访问 [飞书开放平台](https://open.feishu.cn/app)
   - 创建或选择一个应用
   - 在「凭证与基础信息」中获取 `App ID` 和 `App Secret`

2. **文件夹 Token**：

   - 在飞书云文档中打开目标文件夹
   - 从 URL 中复制文件夹 Token（URL 最后一段字符串）
   - 例如：`https://example.feishu.cn/drive/folder/fldcnxxxxxx` 中的 `fldcnxxxxxx`

3. **权限设置**：
   - 在应用管理后台，确保应用已开通「云文档」权限
   - 需要 `drive:drive:readonly` 和 `drive:drive:write` 权限

## 使用方法

### 1. 演练模式 (推荐)

查看将要上传的文件清单，但不执行实际上传：

```bash
python feishu_uploader.py <目录路径> --dry-run
```

### 2. 标准上传 (串行)

适合文件数量较少或对稳定性要求极高的场景：

```bash
python feishu_uploader.py <目录路径>
```

### 3. 高速并发上传 (推荐 ⚡)

启用 5 线程并发上传，相比标准模式可提升 **70-80%** 的上传性能。程序内置速率限制器，严格遵守飞书 API 的 5 QPS 限制。

```bash
python feishu_uploader.py <目录路径> --concurrent
```

### 4. 专项重试模式

如果运行过程中有少量文件因网络波动上传失败，工具会自动保存失败清单至 `failed_uploads.json`。使用该参数可**仅重试**这些失败任务：

```bash
python feishu_uploader.py <目录路径> --retry
# 也可以配合并发模式
python feishu_uploader.py <目录路径> --concurrent --retry
```

---

## 核心特性

### 增量上传

工具会自动记录已成功文件的哈希值（SHA256），存储在 `.upload_history.json` 中。

- **默认行为**：仅上传内容发生变更或新增的文件。
- **强制模式**：使用 `--force` 参数忽略历史记录，重新上传所有文件。

### 失败自动记录

任务结束时，如果有上传失败的文件，工具会将详细路径和元数据保存到 `failed_uploads.json`。处理成功后该文件会自动删除。

### 目录结构保留

工具会完美还原本地 `00_Publish` 及其子目录的层级。

- 本地路径示例：`项目A/00_Publish/子目录/文件.pdf`
- 飞书路径示例：`项目A/00_Publish/子目录/文件.pdf`

---

## 工作原理 (两阶段执行)

1. **阶段 1：扫描与目录准备 (串行)**

   - 扫描所有 `00_Publish` 目录并计算文件哈希。
   - 串行创建飞书端目录结构（飞书 API 不支持并发创建目录）。
   - 缓存所有文件夹 Token。

2. **阶段 2：文件上传 (并发/串行)**
   - 基于缓存的 Token 进行文件上传。
   - 并发模式下使用 `ThreadPoolExecutor` (5 并发)。
   - 使用速率限制器确保请求频率 ≤ 5 QPS。

## 示例

```bash
# 最常用的高效上传方式：扫描目录、增量上传、并发执行
python feishu_uploader.py /Users/bxb/Projects --concurrent

# 如果发现上传失败了，进行重试：
python feishu_uploader.py /Users/bxb/Projects --concurrent --retry

# 即使文件没变，也强制全部覆盖一次：
python feishu_uploader.py /Users/bxb/Projects --concurrent --force
```

---

## 构建可执行程序 (macOS)

如果你需要将工具打包成独立的 Mac 应用程序 (.app)，请按照以下步骤操作：

### 1. 安装 PyInstaller

在你的 Python 环境中安装打包工具：

```bash
pip install pyinstaller
```

### 2. 执行构建

使用项目中已有的配置文件进行构建：

```bash
pyinstaller 飞书上传工具.spec --noconfirm
```

### 3. 获取结果

构建完成后，在项目根目录的 **`dist/`** 文件夹中可以找到 **`飞书上传工具.app`**。

### 4. 首次运行说明

由于未经过开发者签名，首次打开时：

1. **请勿** 直接双击（会提示身份不明的开发者）。
2. **右键点击** `飞书上传工具.app`，选择 **“打开”**。
3. 在弹出的对话框中再次点击 **“打开”**。
4. 之后即可正常双击使用。

---

## 目录结构示例

```
项目根目录/
├── 项目A/
│   └── 00_Publish/
│       ├── 文件1.pdf
│       └── 文件2.docx
├── 项目B/
│   └── 00_Publish/
│       └── 报告.xlsx
└── 项目C/
    └── 其他文件/
```

运行后，将上传：

- `项目A/文件1.pdf`
- `项目A/文件2.docx`
- `项目B/报告.xlsx`

## 注意事项

- **API 频率限制**：飞书 API 每秒限制 5 次请求（5 QPS），工具已内置限制器，请勿在此基础上由于外部脚本或其他方式额外增加调用压力。
- **权限不足**：如遇 `forbidden` 错误，请确保飞书应用已获得相应文件夹的**“可编辑”**权限。
- **文件大小**：当前接口支持单个文件最高 20MB。
- **历史文件**：`.upload_history.json` 是增量上传的核心，请勿随意删除，除非你想重传所有内容。
