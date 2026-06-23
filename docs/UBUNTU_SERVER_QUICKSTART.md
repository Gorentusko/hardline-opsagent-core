# Ubuntu Server Quickstart

This path is for testing OpsAgent Core on a remote Ubuntu server, lab box, or VPS.

## SSH into the server

```bash
ssh user@your-server
```

## Install Docker

Use your normal Docker install method for Ubuntu. The expected result is that these commands work:

```bash
docker --version
docker compose version
```

## Clone and run

```bash
git clone https://github.com/Gorentusko/hardline-opsagent-core.git
cd hardline-opsagent-core
cp .env.example .env
docker compose up -d --build
```

## Test

```bash
curl -s http://localhost:8088/health
curl -s http://localhost:8088/analyze
ls -lah data/reports
```

If testing from another machine, replace `localhost` with the server IP and make sure the firewall allows port `8088`.

## Stop

```bash
docker compose down
```

## Notes

- Default mock provider costs $0.
- No API key is needed.
- OpenRouter is optional and BYOK.
- No automatic remediation is performed.



