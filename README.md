# ⚡ ShadowBreach Agent
> An always-on autonomous cyber incident response simulator built for the AWS Builder Weekend Challenge (Level 200).

ShadowBreach automatically ingests security contexts, leverages **Amazon Bedrock (Nova Lite)** to craft realistic cloud incident response puzzles with mock CloudTrail/VPC logs, and publishes them daily to a serverless terminal dashboard without any human intervention.

---

## 🏗️ Architecture

```text
[ Amazon EventBridge (Cron Trigger) ]
                  │
                  ▼
[ AWS Lambda (Python Logic Engine) ]
                  │
                  ├──► [ Amazon Bedrock (Nova Lite Model) ]
                  │
                  ▼
[ GitHub Pages / S3 (Terminal Dashboard & JSON Feed) ]
                  │
                  ▼
[ End-User / Browser (Interactive Roleplay Drill) ]
```

1. **Amazon EventBridge:** Daily cron schedule triggers the orchestration function.
2. **AWS Lambda:** Serverless execution layer handling Bedrock prompt orchestration and output parsing.
3. **Amazon Bedrock (`amazon.nova-lite-v1:0`):** Synthesizes structured JSON cyber drills, including briefings, synthetic audit logs, tactical dilemmas, multi-choice mitigations, and architectural takeaways.
4. **Interactive Dashboard:** Lightweight, single-page terminal frontend hosted on GitHub Pages.

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
* Python 3.10+
* AWS Account with Bedrock model access (`amazon.nova-lite-v1:0` enabled in `us-east-1`)
* AWS CLI configured (`aws configure`)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/shadowbreach-agent.git](https://github.com/YOUR_GITHUB_USERNAME/shadowbreach-agent.git)
cd shadowbreach-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Generate a Daily Scenario via Amazon Bedrock
```bash
python test_agent.py
```

### 4. Run the Local Terminal UI
```bash
python -m http.server 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📦 Project Structure

```text
shadowbreach-agent/
├── index.html            # Hacker-terminal interactive web interface
├── daily_scenario.json   # Live dynamic JSON scenario feed
├── lambda_function.py    # Production AWS Lambda handler
├── test_agent.py         # Local Bedrock test execution script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusion rules
├── LICENSE               # MIT License
└── README.md             # Project documentation
```

---

## 🔒 Security & Best Practices
* **Zero Hardcoded Secrets:** AWS credentials rely entirely on IAM Roles or local AWS CLI profiles.
* **Strict JSON Schema Enforcement:** LLM outputs are programmatically validated before being published to the dashboard.
* **Cost Optimized:** Built natively within the AWS Free Tier using Bedrock Nova Lite and Serverless Lambda.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).