# Code2Chill Platform Ownership & Maintenance Charter

This document formalizes project governance, operational maintenance boundaries, credential transfer protocols, and emergency escalation paths for Code2Chill (C2C).

---

## 1. Governance & Role Allocation

The platform divides administrative authority into clearly separated operational responsibilities:

| Domain | Responsible Roles | Core Responsibilities |
| :--- | :--- | :--- |
| **Executive Governance** | President (Lakshay Kalra)<br>Vice-President (Jiya Arora) | Strategic roadmap approval, faculty liaison communication, university policy compliance, final recruitment selection. |
| **Technical Operations** | Technical Heads (Samanyu Thakur, Bhupinder Singh) | Production server infrastructure, Docker orchestration, PostgreSQL backup automation, TLS certificates, repository maintenance, and security patches. |
| **Editorial & Content** | Content Heads (Tamanna Kakkar, Ayush Sharma) | Hackathon event publication, schedule management, participant project attribution, and university portal link verification. |
| **Brand & Media** | Social Media & Promotion (Jashan Bhalla, Muskan Dhanda) | Official photography, event posters, social sharing links, and public announcement alignment. |

---

## 2. Secure Credential Transfer Protocol

### Secret Classification
Production secrets are strictly separated from version control:

| Secret | Storage Location | Sensitivity | Rotation Policy |
| :--- | :--- | :--- | :--- |
| **Server Host SSH Keys** | Production host `~/.ssh/authorized_keys` | Critical | Ed25519 keys only. Rotate upon lead graduation. |
| **Database Password** (`POSTGRES_PASSWORD`) | `backend/.env.production` (permissions `0600`) | Critical | Rotate every 90 days or upon technician handover. |
| **Recruitment SMTP Credentials** | `backend/.env.production` (permissions `0600`) | High | App-specific passwords only. Rotate per semester. |
| **Staff Passwords** | PostgreSQL `admin_account` (Argon2id hash) | High | 15+ characters. Managed independently per user. |
| **GitHub Repository Admin** | GitHub Organization Settings | High | Multi-factor authentication (MFA) mandatory. |

### Secure Transfer Checklist
When transferring infrastructure access to incoming technical leads:
1. **Never transmit secrets via unencrypted channels**: Do not send passwords or SSH keys via plain email, Discord, or WhatsApp.
2. **Encrypted Vault Sharing**: Deliver credentials through an encrypted vault (e.g. Bitwarden, 1Password) or GPG-encrypted archive.
3. **Host Access Rotation**:
   - Add the new lead's public key (`ssh-ed25519 ...`) to the server.
   - Remove outgoing members' keys from `~/.ssh/authorized_keys`.
4. **Staff Account Provisioning**:
   - Generate a dedicated account for the new lead using `python -m app.create_admin`.
   - Deactivate former accounts in PostgreSQL (`UPDATE admin_account SET active = false WHERE email = '...'`).
5. **Database Credential Rotation**:
   - Generate a fresh password: `openssl rand -hex 24`.
   - Update `POSTGRES_PASSWORD` in `backend/.env.production` and restart the stack (`docker compose ... up -d`).

---

## 3. Routine Maintenance Calendar

| Frequency | Task | Responsible Lead | Command / Procedure |
| :--- | :--- | :--- | :--- |
| **Weekly** | Backup verification | Technical Head | Run `python backend/scripts/backup.py --list` to verify automated dump creation and SHA-256 integrity. |
| **Monthly** | Health & disk audit | Technical Head | Run `python backend/scripts/health_monitor.py --json`. Check Docker volume space (`docker system df`). |
| **Per Event** | Publish & archive | Content Head | Draft and publish hackathon dates. Update registration status to `ended` after competition closes. |
| **Per Cycle** | Recruitment drive | Executive Leads | Open recruitment cycle with approved university domain constraints; screen submissions; export final rosters. |
| **Per Semester** | Security dependencies | Technical Head | Run `uv lock --upgrade` and `npm update` in staging; run full test suites before production release. |

---

## 4. Emergency Escalation Matrix

```
[ Incident Detected ]
         │
         ├── Severity 1: Site Outage / Database Unavailable
         │   └── Escalate to: Technical Heads (Samanyu Thakur / Bhupinder Singh)
         │   └── Action: Check `docker compose logs`, restart services, or restore latest verified backup.
         │
         ├── Severity 2: Content Defacement / Inaccurate Information
         │   └── Escalate to: Content Heads (Tamanna Kakkar / Ayush Sharma)
         │   └── Action: Edit or unpublish record via `/admin` dashboard.
         │
         └── Severity 3: Suspected Credential Exposure / Account Compromise
             └── Escalate to: President & Technical Heads
             └── Action: Deactivate compromised accounts (`active=false`), rotate `POSTGRES_PASSWORD`, redeploy.
```

---

## 5. Formal Handover Acceptance

The Code2Chill platform repository, infrastructure configurations, living documentation suite, automated test suites, and operational scripts are officially completed and transferred to club leadership:

- **Repository**: `https://github.com/pranav-pushya/Code2Chill`
- **Documentation Master**: [Living Build Guide](BUILD_GUIDE.md)
- **Deployment Manual**: [Production Handover Guide](HANDOVER.md)
- **Technical Reference**: [Technical Architecture & Viva Guide](TECHNICAL_EXPLANATION.md)
- **Presentation Script**: [Demonstration Walkthrough Guide](DEMONSTRATION.md)
