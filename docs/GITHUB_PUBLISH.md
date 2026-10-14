# 发布与邀请协作

本目录已整理为独立 Git 仓库。只发布此目录，不上传上一层的 outputs、work、个人 Vault、备份或其他历史交付包。当前没有配置 GitHub remote，也没有推送。

下载的 ZIP 不包含 .git 历史或配置；若从 ZIP 解压开始，在下面的提交命令前先运行 `git init --initial-branch=main`。已初始化的本地发布目录无需重复执行。

## 发布前

先运行本地测试、阅读 README 与 LICENSE、查看 `git status --short`，确认提交目录中没有个人笔记或运行文件。示例复制为 my-vault 后使用，该目录已忽略。

## 通过 Git 发布

在 GitHub 创建一个空仓库，例如 `ai-knowledge-graph-assistant`，不要同时初始化另一份 README 或许可证。在本目录终端执行下面命令；将最后的地址替换成你实际创建的仓库地址：

```bash
git add .
git commit -m "Prepare Phase 2 Knowledge Bridge MVP"
git remote add origin https://github.com/YOUR_ACCOUNT/ai-knowledge-graph-assistant.git
git push -u origin main
```

YOUR_ACCOUNT 是明确的待替换参数，不是已经存在的远端。Git 使用你本机已配置的提交身份；本项目不替你设置用户名或邮箱。若系统提示没有身份，按你的账户信息配置后再提交。

也可用 GitHub Desktop 添加此本地仓库、查看文件差异、提交，再选择 Publish repository。仓库公开或私有由你决定。

## 发布后

检查 README、文档链接和 Actions 运行结果。以 docs/ROADMAP.md 的小任务创建 Issues；邀请协作者使用分支与 PR。不要要求他们把个人 Vault 提交到源码仓库。

仓库提供 bug_report.md、feature_request.md 与 PR 模板；模板仅在发布后生效。自动化配置已提交，远端是否通过需实际运行确认。
