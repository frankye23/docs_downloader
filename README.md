# GitHub 文档下载器 📂⬇️

一个优雅的Python工具，用于下载GitHub仓库中的文档目录（`/docs` 或 `/doc`）及其所有Markdown文件。

![GitHub stars](https://img.shields.io/github/stars/frank23/docs_downloader?style=social)
![Python version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ 功能特性

- **智能识别文档目录** - 自动检测 `docs` 或 `doc` 文件夹
- **递归下载** - 下载目录结构中的所有Markdown文件
- **API友好** - 显示剩余API请求次数和重置时间
- **断点续传** - 支持网络错误自动重试（最多3次）
- **多环境支持** - 支持带Token认证或匿名访问
- **进度显示** - 清晰的下载进度和文件计数

## 📦 安装

```bash
git clone https://github.com/frankye23/docs_downloader
cd docs_downloader
pip install -r requirements.txt
```

或直接安装依赖：

```bash
pip install pygithub tqdm requests
```

## 🚀 使用方法

### 基本使用

```bash
python github_docs_downloader.py
```

按提示输入：
1. GitHub仓库URL（例如：`https://github.com/ollama/ollama`）
2. （可选）GitHub个人访问令牌

### 使用GitHub Token（推荐）

```bash
export GITHUB_TOKEN="your_personal_access_token"
python github_docs_downloader.py
```

> 获取Token指南：[创建个人访问令牌](https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 🌟 示例输出

```text
[API状态] 剩余请求: 58/60
[API状态] 重置时间: 42分15秒后

开始下载文档：ollama/ollama/docs
已下载: docs/README.md
已下载: docs/api.md
已下载: docs/benchmark.md
已下载: docs/development.md
已下载: docs/docker.md
已下载: docs/examples.md
已下载: docs/faq.md


✅ 下载完成！共下载15 个Markdown文件
文件保存至：/Users/you/ollama/docs
```

## 🛠 技术细节

- 使用[PyGithub](https://pygithub.readthedocs.io/)库处理GitHub API交互
- 采用LRU缓存优化API调用
- 自动处理UTF-8编码问题
- 完善的错误处理和重试机制

## 🤝 贡献指南

1. Fork项目
2. 创建分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建Pull Request

## 📜 许可证

MIT License © 2025 frankye23

---

<p align="center">
❤️ 用Python构建 | 🚀 高效下载文档 | 📚 知识无边界
</p>