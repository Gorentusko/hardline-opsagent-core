# Windows 11 Quickstart

This path is for reviewers or users testing OpsAgent Core from a normal Windows 11 laptop.

## What you need

Install:

1. Docker Desktop for Windows
2. Git for Windows, or download the repo as a ZIP
3. PowerShell, already included with Windows

Docker Desktop may ask to enable WSL 2. Accept that. WSL 2 is the normal Windows path for Linux containers.

## Option A: Clone with Git

Open PowerShell:

```powershell
git clone https://github.com/hardlineitgroup/hardline-opsagent-core.git
cd hardline-opsagent-core
copy .env.example .env
docker compose up --build
```

## Option B: Download ZIP from GitHub

1. Go to the GitHub repo.
2. Click **Code**.
3. Click **Download ZIP**.
4. Right-click the ZIP in Downloads.
5. Click **Extract All**.
6. Open PowerShell in the extracted folder.

Then run:

```powershell
copy .env.example .env
docker compose up --build
```

## Test the app

Open another PowerShell window:

```powershell
curl.exe http://localhost:8088/health
curl.exe http://localhost:8088/analyze
dir .\data\reports
```

Open in a browser:

```text
http://localhost:8088
```

## Optional: use OpenRouter

Default mode is free/mock/offline. To use your own OpenRouter key, edit `.env`:

```env
OPSAGENT_LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
```

Then restart:

```powershell
docker compose down
docker compose up --build
```

## Stop the app

In the terminal running Compose:

```powershell
Ctrl+C
```

Or from another terminal:

```powershell
docker compose down
```

## Common Windows issues

### `docker` is not recognized

Docker Desktop is not installed, not running, or PowerShell was opened before Docker finished installing. Start Docker Desktop and reopen PowerShell.

### Port 8088 already in use

Edit `docker-compose.yml` and change:

```yaml
"8088:8088"
```

to something like:

```yaml
"8090:8088"
```

Then open:

```text
http://localhost:8090
```

### Docker Desktop asks about WSL 2

Enable WSL 2. That is expected for Windows Linux containers.


## Note about PowerShell curl

Older Windows PowerShell aliases `curl` to `Invoke-WebRequest`, which can show a script parsing warning.

Use this instead:

```powershell
curl.exe http://localhost:8088/health
curl.exe http://localhost:8088/analyze
```
