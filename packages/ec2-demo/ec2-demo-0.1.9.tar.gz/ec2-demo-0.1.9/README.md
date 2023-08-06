# EC2 Demo

[![Unstable package](https://img.shields.io/badge/_Unstable_package_-_This_code_is_for_demo_purposes_only_-red)](https://semver.org)


A small cli util to create, list and delete EC2 instances.


## Design

    ec2-demo create <env> <file.yaml>
    ec2-demo list <env>
    ec2-demo destroy <env> <id>


## Step 0

Set up environment.

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements.txt


## Step 1

Set up structure.

    - setup.py (note `ec2-demo` vs `ec2_demo`)
    - ec2_demo/cli.py
    - pip install -e .
    - config/
    - instances/

# Step 2

Add boto3 code.

    - instances.py
    - utils/tags.py

# Step 3

    - replace with logging.debug
    - add list command
    - add destroy command

# Step 4

    - Use env vars
    - Use yaml constructors for dynamic lookups
