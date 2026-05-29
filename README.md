# Project Overview

Cloud bills can grow quickly without teams noticing.  
Developers often forget to shut down test servers, unused storage continues to accumulate, and idle databases keep running in the background. Even when these resources are not being used, they still generate charges.

Many companies only discover this waste when the monthly cloud bill becomes unexpectedly high.

This project demonstrates a three-phase cloud cost management solution built on AWS.  
The goal is to help organizations see where money is being spent, detect unnecessary costs, and automatically reduce waste.

The system was designed to:

- Monitor cloud spending in near real time
- Identify idle or unused resources that still generate charges
- Safely automate costs

# Phase 1: Cost Tracking & Alerts

# Objective
Track AWS costs in near real-time and notify when spending crosses defined thresholds.

# Services Used
- CloudWatch Billing Metrics
- AWS Lambda
- Amazon SNS
- Amazon S3

# What Was Implemented
- Enabled CloudWatch billing metrics
- Created a Lambda function to process billing data
- Configured SNS email alerts for cost thresholds
- Stored cost data in S3 for visualization
- Created a simple cost dashboard using S3-hosted assets

# Outcome
- Automated cost visibility
- Proactive alerts before costs grow unexpectedly
- Foundation for cost optimization decisions

# Phase 2: Cost Optimization

# Objective
Identify unused or underutilized AWS resources that increase cloud costs.

# Services Used
- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon CloudWatch

# What Was Implemented
- Detection of idle EC2 instances using CPU utilization metrics
- Identification of unattached EBS volumes
- Identification of unused EBS volumes
- Tag-based filtering to avoid stopping critical resources

# Outcome
- Clear visibility into wasteful resources
- Safer decision-making using tagging and metrics
- Preparation for automation in Phase 3


# Phase 3: Cost Automation (Auto-Stop)

# Objective
Automatically stop idle EC2 instances to reduce costs without manual intervention.

# Services Used
- AWS Lambda
- Amazon EC2
- Amazon EventBridge
- Amazon SNS

# What Was Implemented
- Dry-run mode to safely identify idle EC2 instances
- SNS notifications before any action was taken
- Automatic stopping of idle EC2 instances
- EventBridge scheduled execution (hourly/nightly)
- Safety checks using tags and CPU thresholds

# Outcome
- Fully automated EC2 cost control
- Reduced operational overhead
- Production-safe automation with notifications

# Security & Safety Measures
- IAM least-privilege permissions
- Tag-based resource protection
- Dry-run testing before real actions
- SNS notifications for transparency

# Lessons Learned
- Cost visibility is the foundation of cost optimization
- Automation must always include safety controls
- AWS tagging is critical for managing environments
- Event-driven architectures reduce manual work



