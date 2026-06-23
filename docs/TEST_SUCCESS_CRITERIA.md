# Test Success Criteria

A local demo is successful when:

```text
/health returns HTTP 200
/health returns {"status":"ok","llm_provider":"mock"}
/analyze returns HTTP 200
/analyze returns status ok, health, score, findings, report_paths
data/reports contains a Markdown report
```

For Windows PowerShell, use:

```powershell
curl.exe http://localhost:8088/health
curl.exe http://localhost:8088/analyze
dir .\data\reports
```

## Known acceptable warning

If Docker socket access is unavailable, the app still runs and generates a report. Docker inspection is marked as limited.

## v0.1.2 improvement

The Docker collector now tries the Docker Engine Unix socket API before falling back to a Docker CLI call.



