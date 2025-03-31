import os
import time
import sys
from urllib.parse import urlparse
from datetime import datetime
from github import Github, GithubException
from functools import lru_cache
import requests
from tqdm import tqdm

class GitHubDocDownloader:
    def __init__(self):
        self.g = self.create_github_instance()
        self.repo = None
        self.local_dir = ""
        self.downloaded_count = 0

    def create_github_instance(self):
        """创建GitHub实例（带认证）"""
        token = os.getenv('GITHUB_TOKEN')
        if token:
            return Github(token)

        print("\n提示：使用GitHub Token可获得更高API限额（5000次/小时 vs 60次/小时）")
        print("创建Token指南：https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
        token = input("请输入GitHub Token（直接回车使用匿名访问）: ").strip()
        return Github(token) if token else Github()

    def show_rate_limit(self):
        """显示当前API配额状态（修复时间计算问题）"""
        rate_limit = self.g.get_rate_limit()
        core = rate_limit.core
        reset_timestamp = core.reset.timestamp()  # 直接获取时间戳
        current_timestamp = datetime.now().timestamp()
        remaining_seconds = max(0, reset_timestamp - current_timestamp)

        mins, secs = divmod(int(remaining_seconds), 60)
        print(f"\n[API状态] 剩余请求: {core.remaining}/{core.limit}")
        print(f"[API状态] 重置时间: {mins}分{secs}秒后")

    def parse_url(self, url):
        """解析GitHub仓库URL"""
        parsed = urlparse(url)
        if parsed.netloc != 'github.com':
            raise ValueError("必须是GitHub仓库URL")

        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("URL格式不正确")

        owner, repo_name = path_parts[0], path_parts[1]
        repo_name = repo_name.replace('.git', '')
        return owner, repo_name

    def safe_api_call(self, func):
        """带错误重试的API调用"""
        for attempt in range(3):
            try:
                return func()
            except requests.exceptions.RequestException as e:
                print(f"网络错误: {e} (尝试 {attempt+1}/3)")
                time.sleep(2 ** attempt)
            except GithubException as e:
                if e.status == 403 and "rate limit" in str(e).lower():
                    self.handle_rate_limit_exceeded()
                else:
                    raise
        raise GithubException(504, "请求失败，超过最大重试次数")

    def handle_rate_limit_exceeded(self):
        """处理速率限制超限"""
        reset_timestamp = self.g.rate_limiting_resettime
        wait_time = max(reset_timestamp - time.time() + 5, 0)
        mins, secs = divmod(int(wait_time), 60)
        print(f"\n⚠️ API限额已用尽，等待 {mins}分{secs}秒...")
        time.sleep(wait_time)

    def find_docs_folder(self):
        """查找文档目录"""
        for folder in ['doc', 'docs']:
            try:
                self.safe_api_call(lambda: self.repo.get_contents(folder))
                return folder
            except GithubException as e:
                if e.status != 404:
                    raise
        raise FileNotFoundError("未找到doc/docs目录")

    def download_markdown(self):
        """主下载方法"""
        base_folder = self.find_docs_folder()
        self.local_dir = os.path.join(os.getcwd(), self.repo.name, base_folder)
        os.makedirs(self.local_dir, exist_ok=True)

        print(f"\n开始下载文档：{self.repo.full_name}/{base_folder}")
        self.recursive_download(base_folder)
        print(f"\n✅ 下载完成！共下载 {self.downloaded_count} 个Markdown文件")
        print(f"文件保存至：{os.path.abspath(self.local_dir)}")

    def recursive_download(self, path):
        """递归下载目录内容"""
        try:
            contents = self.safe_api_call(lambda: self.repo.get_contents(path))
        except GithubException as e:
            print(f"无法访问路径 {path}: {e}")
            return

        for content in contents:
            if content.type == "dir":
                self.recursive_download(content.path)
            elif content.name.endswith('.md'):
                self.save_markdown_file(content)
                self.downloaded_count += 1

    def save_markdown_file(self, content):
        """保存单个Markdown文件"""
        file_path = os.path.join(self.local_dir, content.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            file_content = content.decoded_content.decode('utf-8')
        except UnicodeDecodeError:
            file_content = content.decoded_content.decode('utf-8', errors='replace')
            print(f"注意：{content.path} 包含非UTF-8字符，已替换处理")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f"已下载: {content.path}")

    def run(self):
        """主运行流程"""
        try:
            url = input("请输入GitHub仓库URL: ").strip()
            owner, repo_name = self.parse_url(url)
            
            self.show_rate_limit()
            self.repo = self.safe_api_call(lambda: self.g.get_repo(f"{owner}/{repo_name}"))
            
            self.download_markdown()
        except Exception as e:
            print(f"\n❌ 错误发生: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    downloader = GitHubDocDownloader()
    downloader.run()