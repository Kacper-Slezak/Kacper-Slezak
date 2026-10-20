SRE intern at IBM, ICT student at AGH University of Krakow. Writing a B.Sc. thesis on what mTLS and post-quantum key exchange cost a Kubernetes service mesh, and building [SOTP](https://github.com/Kacper-Slezak/SOTP), a network monitoring platform, in the open.

### Thesis ![now: analysis](https://img.shields.io/badge/now-analysis-9a6700?style=flat-square&labelColor=424a53)

[Istio PQC mTLS benchmark](https://github.com/Kacper-Slezak/Thesis_PQC): CPU and latency cost of mTLS in Istio, TLS 1.2 vs 1.3 and classical X25519 vs hybrid post-quantum X25519MLKEM768. Each configuration is forced with an EnvoyFilter and verified from Envoy statistics on every run. Paired statistical tests across measurement sessions.

![Kubernetes](https://img.shields.io/badge/Kubernetes-424a53?style=flat-square&logo=kubernetes&logoColor=white) ![Istio](https://img.shields.io/badge/Istio-424a53?style=flat-square&logo=istio&logoColor=white) ![Envoy](https://img.shields.io/badge/Envoy-424a53?style=flat-square&logo=envoyproxy&logoColor=white) ![k3d](https://img.shields.io/badge/k3d-424a53?style=flat-square&logo=k3s&logoColor=white) ![K6](https://img.shields.io/badge/K6-424a53?style=flat-square&logo=k6&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-424a53?style=flat-square&logo=prometheus&logoColor=white) ![Python](https://img.shields.io/badge/Python-424a53?style=flat-square&logo=python&logoColor=white)

### SOTP <!-- sotp_badge starts -->![now: P0 Cleanup & Truth, 2 of 3](https://img.shields.io/badge/now-P0%20Cleanup%20%26%20Truth%2C%202%20of%203-9a6700?style=flat-square&labelColor=424a53)<!-- sotp_badge ends -->

[SOTP](https://github.com/Kacper-Slezak/SOTP): network monitoring platform. FastAPI with JWT and RBAC, Celery workers collecting ICMP and SNMPv3 metrics, PostgreSQL + TimescaleDB, HashiCorp Vault for device credentials, Prometheus and Grafana. Design decisions are recorded as [ADRs](https://github.com/Kacper-Slezak/SOTP/tree/main/docs/adr).

![FastAPI](https://img.shields.io/badge/FastAPI-424a53?style=flat-square&logo=fastapi&logoColor=white) ![Celery](https://img.shields.io/badge/Celery-424a53?style=flat-square&logo=celery&logoColor=white) ![TimescaleDB](https://img.shields.io/badge/TimescaleDB-424a53?style=flat-square&logo=timescale&logoColor=white) ![Vault](https://img.shields.io/badge/Vault-424a53?style=flat-square&logo=vault&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-424a53?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-424a53?style=flat-square&logo=grafana&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-424a53?style=flat-square&logo=githubactions&logoColor=white)

<table><tr><td valign="top" width="50%">

#### Roadmap
<!-- sotp_progress starts -->
**[P0 Cleanup & Truth](https://github.com/Kacper-Slezak/SOTP/milestone/1): 2/3** (current)

[P1 Works End-to-End](https://github.com/Kacper-Slezak/SOTP/milestone/2): 0/8

[P2 DevSecOps Pipeline](https://github.com/Kacper-Slezak/SOTP/milestone/3): 0/13

[P3 Kubernetes (K3d + Helm)](https://github.com/Kacper-Slezak/SOTP/milestone/4): 0/7

[P4 GitOps, Secrets & Policy](https://github.com/Kacper-Slezak/SOTP/milestone/5): 0/4

[P5 Observability & SRE](https://github.com/Kacper-Slezak/SOTP/milestone/6): 1/8

[P6 Cloud IaC (AWS, plan-only)](https://github.com/Kacper-Slezak/SOTP/milestone/7): 0/4

[P7 Product Features](https://github.com/Kacper-Slezak/SOTP/milestone/8): 0/12

[P8 Advanced / Stretch](https://github.com/Kacper-Slezak/SOTP/milestone/9): 0/6
<!-- sotp_progress ends -->

</td><td valign="top" width="50%">

#### Recently closed
<!-- sotp_closed starts -->
[#116 Architecture Decision Records (ADR) folder](https://github.com/Kacper-Slezak/SOTP/issues/116) - 2026-10-12

[#115 Repo cleanup: junk files, stale branches, honest roadmap](https://github.com/Kacper-Slezak/SOTP/issues/115) - 2026-10-07

[#103 CI breaking: remove test_icmp_all from core_backend](https://github.com/Kacper-Slezak/SOTP/issues/103) - 2026-10-07

[#108 prometheus.yml scrapes localhost:9090 instead of backend:8000](https://github.com/Kacper-Slezak/SOTP/issues/108) - 2026-10-07

[#44 Implement Pagination, Sorting, and Filtering for Device List](https://github.com/Kacper-Slezak/SOTP/issues/44) - 2026-10-07

[#63 Monitoring Implementation: Prometheus + FastAPI Instrumentator](https://github.com/Kacper-Slezak/SOTP/issues/63) - 2026-10-07
<!-- sotp_closed ends -->

</td></tr></table>

### Other projects

[Entry System](https://github.com/Kacper-Slezak/Entry_System): two-factor access control with QR codes and face verification (DeepFace, Facenet512). FastAPI, PostgreSQL, Docker Compose; CI runs on mocked face embeddings.

[ThreatLens](https://github.com/Sullyvahnn/HackYeah): HackYeah 2025. Map of reported threats built in 24 hours; article classification and deduplication with the Groq and Gemini APIs.

[Packet classification](https://github.com/Martynka123-code/Online-machine-learning-based-packet-classification-project): team project. Real-time traffic classification on live captures, flow-based Random Forest vs byte-level CNN.

### Tools I use

Python, Bash. Docker, Kubernetes, k3d, Istio, Envoy. Prometheus, Grafana, TimescaleDB. FastAPI, SQLAlchemy, Celery, PostgreSQL, Redis. GitHub Actions, HashiCorp Vault.

[LinkedIn](https://www.linkedin.com/in/kacper-%C5%9Bl%C4%99zak-739a20285/) · kacper.slezak.cv@gmail.com
