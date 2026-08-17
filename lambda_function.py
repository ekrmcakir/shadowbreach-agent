import json
import os
import boto3
import urllib.request
from datetime import datetime

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-lite-v1:0')

def lambda_handler(event, context):
    prompt = f"""
    You are an autonomous Cyber Incident Roleplay Game Master.
    Generate a realistic 'Incident Response of the Day' scenario for cloud security engineers.
    
    The response MUST be valid JSON only, without markdown formatting or code fences, following this exact schema:
    {{
        "date": "{datetime.utcnow().strftime('%Y-%m-%d')}",
        "scenario_title": "Short catchy title",
        "threat_level": "CRITICAL / HIGH / MEDIUM",
        "briefing": "2-3 paragraphs describing the incident alert, affected AWS services, and initial attacker vectors.",
        "terminal_log": "Realistic mock CloudTrail or VPC Flow logs.",
        "dilemma": "What immediate tactical decision should the Lead SecOps engineer make?",
        "options": [
            {{
                "id": "A",
                "action": "Option A description",
                "is_optimal": false,
                "feedback": "Why this creates secondary issues."
            }},
            {{
                "id": "B",
                "action": "Option B description",
                "is_optimal": true,
                "feedback": "Correct mitigation strategy."
            }},
            {{
                "id": "C",
                "action": "Option C description",
                "is_optimal": false,
                "feedback": "Why this is ineffective."
            }}
        ],
        "key_takeaway": "1-2 sentences on best practices."
    }}
    """
    
    response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.7, "maxTokens": 1500}
    )
    
    response_text = response['output']['message']['content'][0]['text'].strip()
    if response_text.startswith("```json"): response_text = response_text[7:]
    if response_text.endswith("```"): response_text = response_text[:-3]
    
    return {
        "statusCode": 200,
        "body": json.dumps(json.loads(response_text.strip()))
    }