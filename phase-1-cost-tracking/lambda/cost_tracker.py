import boto3
import json
import os
from datetime import datetime, timezone

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
sns = boto3.client("sns", region_name="us-east-1")
s3 = boto3.client("s3")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
S3_BUCKET = os.environ["S3_BUCKET"]
ALERT_THRESHOLD = float(os.environ.get("ALERT_THRESHOLD", "50.0"))


def get_current_month_cost():
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Billing",
        MetricName="EstimatedCharges",
        Dimensions=[{"Name": "Currency", "Value": "USD"}],
        StartTime=datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        EndTime=datetime.now(timezone.utc),
        Period=86400,
        Statistics=["Maximum"],
    )

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return 0.0

    latest = max(datapoints, key=lambda x: x["Timestamp"])
    return round(latest["Maximum"], 2)


def save_to_s3(cost):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "estimated_cost_usd": cost,
        "threshold_usd": ALERT_THRESHOLD,
        "alert_triggered": cost >= ALERT_THRESHOLD,
    }

    key = f"cost-data/{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/cost.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(record, indent=2),
        ContentType="application/json",
    )
    return key


def send_alert(cost):
    message = (
        f"AWS Cost Alert\n\n"
        f"Your estimated AWS charges have reached ${cost:.2f} USD this month.\n"
        f"Configured threshold: ${ALERT_THRESHOLD:.2f} USD\n\n"
        f"Log in to the AWS Billing Console to review your usage.\n"
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}"
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"AWS Cost Alert: ${cost:.2f} exceeds threshold of ${ALERT_THRESHOLD:.2f}",
        Message=message,
    )


def lambda_handler(event, context):
    cost = get_current_month_cost()
    s3_key = save_to_s3(cost)

    alert_sent = False
    if cost >= ALERT_THRESHOLD:
        send_alert(cost)
        alert_sent = True

    result = {
        "estimated_cost_usd": cost,
        "threshold_usd": ALERT_THRESHOLD,
        "alert_sent": alert_sent,
        "s3_key": s3_key,
    }

    print(json.dumps(result))
    return result
