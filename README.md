SRE intern at IBM, ICT student at AGH University of Krakow. Writing a B.Sc. thesis on what mTLS and post-quantum key exchange cost a Kubernetes service mesh, building the backend of an IoT wood theft detector, and building [SOTP](https://github.com/Kacper-Slezak/SOTP), a network monitoring platform, in the open.

### Thesis ![now: write-up](https://img.shields.io/badge/now-write--up-9a6700?style=flat-square&labelColor=424a53)

[Istio PQC mTLS benchmark](https://github.com/Kacper-Slezak/Thesis_PQC): CPU, latency and memory cost of sidecar mTLS in Istio, classical X25519 vs hybrid post-quantum X25519MLKEM768, full and resumed TLS 1.3 handshakes, TLS 1.2 vs 1.3. Each configuration is forced with an EnvoyFilter and verified from Envoy statistics on every run; comparisons are paired inside blocks with a stability gate, 8 runs over 4 fresh-cluster sessions.

**Result:** the hybrid post-quantum key exchange adds ~3% sidecar CPU per request when every request opens a new connection, and nothing measurable with keep-alive. mTLS itself is the real cost: +112% CPU vs plaintext without connection reuse, ~7% with keep-alive.

![Kubernetes](https://img.shields.io/badge/Kubernetes-424a53?style=flat-square&logo=kubernetes&logoColor=white) ![Istio](https://img.shields.io/badge/Istio-424a53?style=flat-square&logo=istio&logoColor=white) ![Envoy](https://img.shields.io/badge/Envoy-424a53?style=flat-square&logo=envoyproxy&logoColor=white) ![k3d](https://img.shields.io/badge/k3d-424a53?style=flat-square&logo=k3s&logoColor=white) ![K6](https://img.shields.io/badge/K6-424a53?style=flat-square&logo=k6&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-424a53?style=flat-square&logo=prometheus&logoColor=white) ![Python](https://img.shields.io/badge/Python-424a53?style=flat-square&logo=python&logoColor=white)

### Wood theft detector

[Detektor kradzieży drewna](https://github.com/Kacper-Slezak/Detektor-kradziezy-drewna): 7-person IoT project at AGH. A sensor hidden by a roadside timber stack detects theft on the device and sends an alert to the forester over LoRa. I own the backend: FastAPI, async SQLAlchemy, TimescaleDB, ingest from The Things Network, and a frame simulator that replays theft, false-alarm and battery-drain scenarios. Images are built in GitHub Actions, pushed to GHCR and deployed behind Caddy on a 1 GB VPS with per-service memory limits.

![FastAPI](https://img.shields.io/badge/FastAPI-424a53?style=flat-square&logo=fastapi&logoColor=white) ![TimescaleDB](https://img.shields.io/badge/TimescaleDB-424a53?style=flat-square&logo=timescale&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-424a53?style=flat-square&logo=sqlalchemy&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-424a53?style=flat-square&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-424a53?style=flat-square&logo=githubactions&logoColor=white)

### SOTP <!-- sotp_badge starts -->![now: P0 Cleanup & Truth, 2 of 3](https://img.shields.io/badge/now-P0%20Cleanup%20%26%20Truth%2C%202%20of%203-9a6700?style=flat-square&labelColor=424a53)<!-- sotp_badge ends -->

[SOTP](https://github.com/Kacper-Slezak/SOTP): network monitoring platform. FastAPI with JWT and RBAC, Celery workers collecting ICMP and SNMPv3 metrics, PostgreSQL + TimescaleDB, HashiCorp Vault for device credentials, Prometheus and Grafana. Design decisions are recorded as [ADRs](https://github.com/Kacper-Slezak/SOTP/tree/main/docs/adr).

**Roadmap:** <!-- sotp_progress starts -->**[P0 Cleanup & Truth](https://github.com/Kacper-Slezak/SOTP/milestone/1) 2/3** → P1 Works End-to-End → P2 DevSecOps Pipeline → P3 Kubernetes → P4 GitOps, Secrets & Policy → P5 Observability & SRE → P6 Cloud IaC → P7 Product Features → P8 Advanced / Stretch<!-- sotp_progress ends -->

**Latest:** <!-- sotp_closed starts -->[#116 Architecture Decision Records (ADR) folder](https://github.com/Kacper-Slezak/SOTP/issues/116) · [#115 Repo cleanup: junk files, stale branches, honest roadmap](https://github.com/Kacper-Slezak/SOTP/issues/115) · [#103 CI breaking: remove test_icmp_all from core_backend](https://github.com/Kacper-Slezak/SOTP/issues/103)<!-- sotp_closed ends -->

![FastAPI](https://img.shields.io/badge/FastAPI-424a53?style=flat-square&logo=fastapi&logoColor=white) ![Celery](https://img.shields.io/badge/Celery-424a53?style=flat-square&logo=celery&logoColor=white) ![TimescaleDB](https://img.shields.io/badge/TimescaleDB-424a53?style=flat-square&logo=timescale&logoColor=white) ![Vault](https://img.shields.io/badge/Vault-424a53?style=flat-square&logo=vault&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-424a53?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-424a53?style=flat-square&logo=grafana&logoColor=white)

### Other projects

[ML-KEM from scratch](https://github.com/nix746/ml-kem): team implementation of NIST FIPS 203 (CRYSTALS-Kyber) in Python with only NumPy and the standard library: NTT, sampling, K-PKE and the Fujisaki-Okamoto transform. kyber-py is used only in tests, as a reference oracle.

[Entry System](https://github.com/Kacper-Slezak/Entry_System): two-factor access control with QR codes and face verification (DeepFace, Facenet512). FastAPI, PostgreSQL, Docker Compose; CI runs on mocked face embeddings.

[ThreatLens](https://github.com/Sullyvahnn/HackYeah): HackYeah 2025. Map of reported threats built in 24 hours; article classification and deduplication with the Groq and Gemini APIs.

[Packet classification](https://github.com/Martynka123-code/Online-machine-learning-based-packet-classification-project): team project. Real-time traffic classification on live captures, flow-based Random Forest vs byte-level CNN.

[LinkedIn](https://www.linkedin.com/in/kacper-%C5%9Bl%C4%99zak-739a20285/) · kacper.slezak.cv@gmail.com
