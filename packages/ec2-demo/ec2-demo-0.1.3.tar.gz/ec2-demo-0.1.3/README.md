# EC2 Demo

A small cli util to create, list and delete EC2 instances.


## Design

    ec2-demo create <env> <file.yaml>
    ec2-demo list <env>
    ec2-demo delete <env> <id>


## Implementation

We will use:

- `click` for the cli interface, not `argparse` and related
- `boto3` for the API calls (SDK)
