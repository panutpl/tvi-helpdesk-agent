# TechCorp IT Security Policy

> Version 2.3 | Effective: January 1, 2025
> Last updated: February 28, 2025
> Owner: IT Security Team (security@techcorp.co.th)

---

## 1. Password Policy

### 1.1 Password Requirements

All TechCorp accounts must meet the following password criteria:

- Minimum length: **12 characters**
- Must contain at least:
  - 1 uppercase letter (A-Z)
  - 1 lowercase letter (a-z)
  - 1 number (0-9)
  - 1 special character (!@#$%^&*)
- Must NOT contain:
  - Your name, username, or email address
  - Dictionary words (without modification)
  - Sequential characters (e.g., "abc123", "qwerty")
  - Previously used passwords (last 10 passwords are remembered)

### 1.2 Password Rotation

| Account Type | Rotation Period | Grace Period |
|-------------|----------------|--------------|
| Standard employee | Every 90 days | 7 days after expiry |
| Admin/Privileged | Every 60 days | 3 days after expiry |
| Service accounts | Every 180 days | No grace period |

After the grace period, the account will be **automatically locked**. Contact IT Helpdesk to unlock.

### 1.3 Multi-Factor Authentication (MFA)

MFA is **mandatory** for all employees. Supported methods:

1. **Authenticator App** (preferred): Google Authenticator or Microsoft Authenticator
2. **Hardware key**: YubiKey (issued by IT upon request)
3. **SMS OTP**: Available but discouraged (less secure)

MFA is required for:
- All logins to corporate systems (SSO)
- VPN connections
- Admin panel access
- Any access from a new device or location

---

## 2. VPN Policy

### 2.1 When VPN is Required

You **must** connect to VPN when:
- Working from home or any location outside the office
- Accessing internal systems (HRMS, internal dashboards, staging environments)
- Connecting to production databases or servers

You do **not** need VPN for:
- Email (via Outlook web or mobile app)
- Slack
- Google Workspace (Docs, Sheets, Drive)
- Public-facing websites

### 2.2 VPN Setup

| Platform | Client | Config File |
|----------|--------|-------------|
| macOS | WireGuard | Download from IT Portal |
| Windows | WireGuard | Download from IT Portal |
| iOS/Android | WireGuard mobile | Scan QR from IT Portal |
| Linux | wg-quick | Config available on IT Portal |

**Setup steps:**
1. Go to https://it-portal.techcorp.co.th/vpn
2. Login with your SSO credentials
3. Download the configuration file for your platform
4. Import into WireGuard client
5. Connect and verify by visiting https://internal.techcorp.co.th

**Troubleshooting:**
- If connection fails, ensure you are not on a restricted network (some hotels/airports block WireGuard)
- Try switching between WiFi and mobile data
- If VPN was working but suddenly disconnected, your config may have expired (configs rotate every 30 days)
- Contact IT Helpdesk if issues persist: it-helpdesk@techcorp.co.th or Slack #it-support

### 2.3 VPN Restrictions

- VPN sessions are limited to **12 hours** before requiring re-authentication
- Maximum **2 concurrent VPN sessions** per user (e.g., laptop + phone)
- VPN access is logged and monitored for security audits
- Do NOT share your VPN configuration with anyone

---

## 3. Device Policy

### 3.1 Company-Issued Devices

All company-issued devices (laptops, phones) must:
- Have full-disk encryption enabled (FileVault for Mac, BitLocker for Windows)
- Have the latest OS security patches installed (auto-update must be ON)
- Have endpoint protection software installed (CrowdStrike Falcon)
- Be registered in the MDM (Mobile Device Management) system

**Loss or theft:** Report immediately to IT Security team via:
- Email: security@techcorp.co.th
- Emergency hotline: 02-XXX-XXXX ext. 911
- Slack: #security-incident

We will remotely wipe the device within 1 hour of report.

### 3.2 Personal Devices (BYOD)

Personal devices may be used to access company resources **only if**:
- Device is registered in the MDM system
- Device has screen lock enabled (PIN, biometric, or password)
- Device OS is up-to-date (no more than 2 major versions behind)
- Separation between work and personal data is maintained (work profile)

**Prohibited on personal devices:**
- Storing company documents locally (use Google Drive/cloud only)
- Accessing production systems
- Taking screenshots of sensitive data

### 3.3 Software Installation

| Category | Policy |
|----------|--------|
| Approved software list | Install freely (see IT Portal for list) |
| Development tools (IDE, CLI) | Install freely, no approval needed |
| Browser extensions | Only from approved list |
| Communication tools | Only company-approved (Slack, Zoom, Google Meet) |
| AI tools (ChatGPT, Copilot, etc.) | Allowed for **non-sensitive work** only (see Section 5) |
| Cracked/pirated software | **Strictly prohibited** — disciplinary action |

---

## 4. Data Classification & Handling

### 4.1 Data Classification Levels

| Level | Description | Examples | Handling |
|-------|------------|----------|----------|
| **Public** | Information intended for public | Marketing materials, blog posts | No restrictions |
| **Internal** | General internal information | Meeting notes, internal wikis | Keep within company systems |
| **Confidential** | Sensitive business data | Financial reports, HR data, customer PII | Encrypted storage, restricted access |
| **Restricted** | Highly sensitive | Credentials, encryption keys, trade secrets | Need-to-know basis, audit logged |

### 4.2 Data Handling Rules

- **Never** send Confidential or Restricted data via personal email
- **Never** upload Confidential or Restricted data to personal cloud storage
- **Never** share credentials via Slack, email, or any messaging platform (use 1Password shared vaults)
- **Always** use company-approved file sharing (Google Drive with proper permissions)
- **Always** encrypt files before sending externally (use company PGP key or password-protected ZIP)

---

## 5. AI Tools Usage Policy

### 5.1 Approved AI Tools

| Tool | Status | Conditions |
|------|--------|-----------|
| GitHub Copilot (Business) | ✅ Approved | Company-managed subscription only |
| ChatGPT Team/Enterprise | ✅ Approved | Company workspace only |
| Google Gemini (Workspace) | ✅ Approved | Via company Google account |
| Personal ChatGPT (free/plus) | ⚠️ Restricted | Non-sensitive queries only |
| Claude | ⚠️ Restricted | Non-sensitive queries only |
| Open-source models (local) | ✅ Approved | Run locally, no data leaves device |

### 5.2 Rules for AI Tool Usage

**Allowed:**
- Writing/debugging code (non-proprietary logic)
- Drafting emails and documents (non-confidential)
- Research and learning
- Generating test data

**Prohibited:**
- Inputting customer data, PII, or financial data
- Sharing proprietary algorithms or business logic
- Uploading internal documents or code repositories
- Using AI to generate security credentials or keys

Violation of AI usage policy will result in disciplinary action up to and including termination.

---

## 6. Incident Reporting

### 6.1 What to Report

Report immediately if you:
- Receive a suspicious email (phishing)
- Notice unauthorized access to your accounts
- Lose a device with company data
- Accidentally share sensitive data with wrong recipients
- Notice unusual system behavior (potential malware)
- Find a security vulnerability in company systems

### 6.2 How to Report

| Urgency | Channel | Response Time |
|---------|---------|---------------|
| Critical (data breach, active attack) | Hotline: 02-XXX-XXXX ext. 911 | 15 minutes |
| High (suspicious access, lost device) | Slack: #security-incident | 1 hour |
| Medium (phishing email, policy question) | Email: security@techcorp.co.th | 4 hours |
| Low (general security question) | Slack: #it-support | 1 business day |

### 6.3 Phishing Response

If you receive a suspicious email:
1. **Do NOT click** any links or download attachments
2. **Do NOT reply** to the sender
3. Forward the email to security@techcorp.co.th
4. Report in Slack #security-incident with subject line
5. Delete the email from your inbox

---

## 7. Network Security

### 7.1 WiFi Networks

| Network | Purpose | Access |
|---------|---------|--------|
| TechCorp-Corp | Employee devices (managed) | Auto-connect via MDM certificate |
| TechCorp-Guest | Visitors and personal devices | Password rotates weekly (ask reception) |
| TechCorp-IoT | Office IoT devices | IT-managed only |

**Rules:**
- Never connect company devices to unknown/public WiFi without VPN
- Never create personal hotspots/access points in the office
- Report any unfamiliar WiFi networks that appear to be TechCorp-related

### 7.2 Port & Protocol Restrictions

Outbound traffic is filtered. If you need access to a blocked port/service for development:
1. Submit a request via IT Portal → "Firewall Exception"
2. Specify: source, destination, port, protocol, business justification
3. Exceptions are reviewed within 2 business days
4. All exceptions expire after 90 days (renewable)

---

## 8. Compliance & Training

- All employees must complete **Security Awareness Training** annually (via LMS)
- Deadline: Within 30 days of joining, then annually in Q1
- Failure to complete training will result in restricted system access
- Simulated phishing tests are conducted quarterly — failing 2 consecutive tests triggers mandatory additional training

---

## 9. Contact Information

| Team | Contact | Hours |
|------|---------|-------|
| IT Helpdesk | it-helpdesk@techcorp.co.th / Slack #it-support | Mon-Fri 8:00-19:00 |
| IT Security | security@techcorp.co.th / Slack #security-incident | Mon-Fri 9:00-18:00 |
| Emergency | 02-XXX-XXXX ext. 911 | 24/7 |
| IT Portal | https://it-portal.techcorp.co.th | Self-service 24/7 |
