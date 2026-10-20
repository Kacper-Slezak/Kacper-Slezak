# Kacper Ślęzak

ICT student at AGH University of Krakow · SRE Intern at IBM  
B.Sc. thesis on the cost of mTLS and post-quantum key exchange in a Kubernetes service mesh.

## Projects

**[Istio PQC mTLS benchmark](LINK)** — B.Sc. thesis  
Measures CPU and latency cost of mTLS in Istio: TLS 1.2 vs 1.3, classical X25519 vs hybrid post-quantum X25519MLKEM768. Configurations are forced with EnvoyFilters and verified from Envoy statistics on every run. Automated k3d + Istio setup, K6 load generation, Prometheus metrics, multi-session campaigns with paired statistical tests.

**[SOTP](https://github.com/Kacper-Slezak/SOTP)** — network monitoring platform, in **development**  
FastAPI API with JWT and RBAC, Celery workers collecting ICMP and SNMPv3 metrics, PostgreSQL + TimescaleDB, HashiCorp Vault for device credentials, Prometheus and Grafana, GitHub Actions CI. Design decisions recorded as ADRs.

**[Entry System](https://github.com/Kacper-Slezak/Entry_System)** — two-factor access control  
QR code + face verification (DeepFace, Facenet512), FastAPI, PostgreSQL, Docker Compose. CI runs on mocked face embeddings.

**[ThreatLens](https://github.com/Sullyvahnn/HackYeah)** — HackYeah 2025  
Map of reported threats built in 24h; article classification and deduplication with the Groq and Gemini APIs.

**[Packet classification](https://github.com/Martynka123-code/Online-machine-learning-based-packet-classification-project)** — team project  
Real-time traffic classification on live captures: flow-based Random Forest vs byte-level CNN.

## Tech
| | |
|---|---|
| Languages | Python · Bash |
| Containers & orchestration | Docker · Kubernetes · k3d |
| Service mesh | Istio · Envoy |
| Observability | Prometheus · Grafana · TimescaleDB |
| Backend & data | FastAPI · SQLAlchemy · Celery · PostgreSQL · Redis |
| CI/CD & security | GitHub Actions · HashiCorp Vault · Bandit |

[LinkedIn](…) · kacper.slezak.cv@gmail.com
