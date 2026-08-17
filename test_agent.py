import json
import boto3
from datetime import datetime

# Initialize AWS Bedrock Runtime Client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = 'amazon.nova-lite-v1:0'

print("🤖 ShadowBreach Agent: Connecting to Amazon Bedrock to synthesize a new incident scenario...")

prompt = f"""
You are an autonomous Cyber Incident Roleplay Game Master.
Generate a realistic 'Incident Response of the Day' scenario for cloud security engineers regarding AWS S3 bucket public leak, IAM privilege escalation, or unauthorized STS credential usage.

The response MUST be valid JSON only, without markdown formatting or code fences, following this exact schema:
{{
    "date": "{datetime.utcnow().strftime('%Y-%m-%d')}",
    "scenario_title": "Short catchy title (e.g., Operation Ghost Token)",
    "threat_level": "CRITICAL",
    "briefing": "Description of the simulated alert and affected AWS services.",
    "terminal_log": "Realistic mock CloudTrail or VPC Flow logs showing the breach.",
    "dilemma": "What immediate tactical decision should the Lead SecOps engineer make?",
    "options": [
        {{
            "id": "A",
            "action": "Option A description",
            "is_optimal": false,
            "feedback": "Why this creates secondary issues or fails."
        }},
        {{
            "id": "B",
            "action": "Option B description",
            "is_optimal": true,
            "feedback": "Correct least-privilege mitigation and containment strategy."
        }},
        {{
            "id": "C",
            "action": "Option C description",
            "is_optimal": false,
            "feedback": "Why this is ineffective or escalates blast radius."
        }}
    ],
    "key_takeaway": "Key best practice rule (e.g., IAM condition keys, IMDSv2, GuardDuty rules)."
}}
"""

try:
    response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.7, "maxTokens": 1500}
    )
    
    raw_text = response['output']['message']['content'][0]['text'].strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    
    scenario = json.loads(raw_text.strip())
    
    # Save the generated scenario to daily_scenario.json
    with open("daily_scenario.json", "w") as f:
        json.dump(scenario, f, indent=2)
        
    print("✅ Success! Amazon Bedrock generated a new scenario and updated 'daily_scenario.json':")
    print(f"Scenario Title: {scenario.get('scenario_title')}")
    print(f"Threat Level:   {scenario.get('threat_level')}")
except Exception as e:
    print(f"❌ Execution failed: {e}")