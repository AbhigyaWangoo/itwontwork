from server import Issue

cx_issues = [
    Issue(
        id=1,
        subject="Service Outage in EC2",
        body="Hi Team,\nI am currently unable to access my EC2 instances in the us-east-1 region. The console shows them as 'stopped,' and I cannot start them. Could you please investigate this issue as soon as possible?\nThank you!",
        url="https://example.com/ticket/1",
        updated_at="2024-10-06T12:00:00Z",
        raw="Service Outage in EC2: Hi Team, I am currently unable to access my EC2 instances..."
    ),
    Issue(
        id=2,
        subject="Performance Issues with RDS",
        body="Hello,\nWe are experiencing significant latency with our RDS instance, especially during peak hours. Queries that usually take a few milliseconds are now taking several seconds. Can you help us identify the cause and suggest any optimizations?\nRegards,\n[Customer Name]",
        url="https://example.com/ticket/2",
        updated_at="2024-10-06T12:00:00Z",
        raw="Performance Issues with RDS: Hello, We are experiencing significant latency..."
    ),
    Issue(
        id=3,
        subject="Unexpected Charges",
        body="Hi AWS Support,\nI noticed a charge of $300 on my last bill that I wasn’t expecting. I’m not sure what service caused this increase. Can you provide a breakdown of charges related to my account, specifically for the last month?\nThank you!",
        url="https://example.com/ticket/3",
        updated_at="2024-10-06T12:00:00Z",
        raw="Unexpected Charges: Hi AWS Support, I noticed a charge of $300..."
    ),
    Issue(
        id=4,
        subject="Unauthorized Access Detected",
        body="Dear Support Team,\nI received a notification about unusual login attempts to my AWS account from an unrecognized IP address. Please assist me in investigating this potential security breach and securing my account.\nThanks!",
        url="https://example.com/ticket/4",
        updated_at="2024-10-06T12:00:00Z",
        raw="Unauthorized Access Detected: Dear Support Team, I received a notification..."
    ),
    Issue(
        id=5,
        subject="Issues with IAM Role Permissions",
        body="Hello,\nI’ve been trying to access certain S3 buckets using my IAM role, but I keep receiving an 'Access Denied' error. Could you please check if the permissions are configured correctly for my role?\nBest,\n[Customer Name]",
        url="https://example.com/ticket/5",
        updated_at="2024-10-06T12:00:00Z",
        raw="Issues with IAM Role Permissions: Hello, I’ve been trying to access..."
    ),
    Issue(
        id=6,
        subject="CloudFormation Stack Deployment Failed",
        body="Hi Team,\nI attempted to deploy a new CloudFormation stack, but it failed with an error message about missing parameters. Can you help me understand why it failed and how to resolve the issue?\nAppreciate your help!",
        url="https://example.com/ticket/6",
        updated_at="2024-10-06T12:00:00Z",
        raw="CloudFormation Stack Deployment Failed: Hi Team, I attempted to deploy..."
    ),
    Issue(
        id=7,
        subject="Auto-Scaling Not Functioning Properly",
        body="Hello,\nMy auto-scaling group is not scaling up during peak traffic hours as expected. I’ve configured the scaling policies, but they don’t seem to trigger. Can you help me troubleshoot this?\nThank you!",
        url="https://example.com/ticket/7",
        updated_at="2024-10-06T12:00:00Z",
        raw="Auto-Scaling Not Functioning Properly: Hello, My auto-scaling group..."
    ),
    Issue(
        id=8,
        subject="VPN Connection Issues",
        body="Hi AWS Support,\nWe’re having trouble maintaining a stable connection with our VPN. It frequently drops, and we cannot access our resources in the VPC. Can you assist us in diagnosing this issue?\nRegards,\n[Customer Name]",
        url="https://example.com/ticket/8",
        updated_at="2024-10-06T12:00:00Z",
        raw="VPN Connection Issues: Hi AWS Support, We’re having trouble maintaining..."
    ),
    Issue(
        id=9,
        subject="Issues Integrating Lambda with S3",
        body="Hello,\nI’m trying to trigger a Lambda function when a new object is uploaded to an S3 bucket, but it doesn’t seem to be working. Could you guide me through the necessary permissions and settings to ensure this integration works?\nThank you!",
        url="https://example.com/ticket/9",
        updated_at="2024-10-06T12:00:00Z",
        raw="Issues Integrating Lambda with S3: Hello, I’m trying to trigger a Lambda..."
    ),
    Issue(
        id=10,
        subject="Difficulty Restoring from Backup",
        body="Hi Team,\nI attempted to restore an RDS instance from a snapshot, but the process failed with an error message. Can you provide assistance on how to troubleshoot this and successfully restore the instance?\nBest regards,\n[Customer Name]",
        url="https://example.com/ticket/10",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    ),
        Issue(
        id=11,
        subject="Can't restore from Backup",
        body="""I tried to restore a DynamoDB instance from a snapshot, but the process failed and displayed an error message. Could you please assist me with troubleshooting this issue so that I can successfully restore the instance?
Best regards,
[Customer Name]""",
        url="https://example.com/ticket/10",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    ),
        Issue(
        id=12,
        subject="Restore from Backup not working",
        body="""When I attempted to restore an RDS instance using a snapshot, the process failed with no error message. I would appreciate your guidance on troubleshooting this issue to ensure a successful restoration. Thank you""",
        url="https://example.com/ticket/10",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    )
]

all_comments = {
    10: [{"plain_body": "Hey! Can you describe your issue for me, what is the error message?", "author_id": 34135425366419}, {"plain_body": "sure, I'm seeing a 404: you are not a cool user. So You have been rejected.", "author_id": 34135451130771}, {"plain_body": "Please tell it you are a cool person, and retry!", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
    11: [{"plain_body": "Hey! Can you describe your issue for me, what is the error message?", "author_id": 34135425366419}, {"plain_body": "sure, I'm seeing a 500: table not found", "author_id": 34135451130771}, {"plain_body": "Most likely, you don't have a table setup. Thus, please set it up then try again", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
    12: [{"plain_body": "Hey! Can you describe your issue for me, what query did you run", "author_id": 34135425366419}, {"plain_body": "sure, I ran the query 'backup table users;'", "author_id": 34135451130771}, {"plain_body": "please try it again with the following statement: 'backup table users --no-cache;'", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
}