# Install Matrix

| Environment | Works in v0.1.1? | Notes |
|---|---:|---|
| Windows 11 + Docker Desktop | Yes | Recommended reviewer path |
| Mac + Docker Desktop | Expected | Same Docker Compose flow |
| Ubuntu Server + Docker Engine | Yes | Best server-style path |
| Existing Docker host | Yes | Clone/copy and run Compose |
| Proxmox host without Docker | No | Do not install Docker on production Proxmox just to test |
| Kubernetes | Not yet | Future packaging option |
| Local GPU/Ollama | Not yet | Planned future lane |

## Key design decision

OpsAgent Core should be easy to test without a paid AI key. The default mock provider is part of the product, not a fallback hack.

