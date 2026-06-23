# GitHub Push Later

Use this when you are logged into GitHub and ready to push.

## From the repo folder

```powershell
git status
git branch -M main
git remote add origin https://github.com/Gorentusko/hardline-opsagent-core.git
git push -u origin main
```

If the remote already exists:

```powershell
git remote set-url origin https://github.com/Gorentusko/hardline-opsagent-core.git
git push -u origin main
```

## GitHub repo setup

Do not initialize the GitHub repo with a README, license, or `.gitignore`, because this local repo already has those files.

