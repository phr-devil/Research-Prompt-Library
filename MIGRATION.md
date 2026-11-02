# Migration / 从原仓库导出到独立 GitHub 仓库

这是过渡导出分支的说明，不是新仓库的运行依赖。目标仓库建议 `phr-devil/Problem-Data-Research-Workflow`。

在 GitHub 上新建**空白**仓库（不要勾选自动添加 README / .gitignore），之后在 PowerShell 执行：

```powershell
git clone --branch export/pd-rw-v1.3-standalone --single-branch https://github.com/phr-devil/Research-Prompt-Library.git Problem-Data-Research-Workflow
cd Problem-Data-Research-Workflow
Remove-Item -Recurse -Force .git
git init -b main
git add .
git commit -m "Initial standalone PD-RW v1.3"
git remote add origin https://github.com/phr-devil/Problem-Data-Research-Workflow.git
git push -u origin main
```

重新 init 是为避免把旧库其他章节的 Git 历史带入新项目。部署后运行 `python -m unittest discover -s tests -v`，检查根目录 README/AGENTS/START 链接。最后再在原仓库单独提出移除第十章及旧测试/索引引用的 PR；**新仓库内容核实之前不要从旧仓库删除**。
