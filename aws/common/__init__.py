import boto3
import json
from tabulate import tabulate

from . import deserialize, ec2, eni, elb


def get_aws_session(profile_name, region_name):
    """Get an AWS session using the profile and region names.

    Args:
        profile_name (string): AWS profile name. You can use 'all' to search across all profiles.
        region_name (string): AWS region name. You can use 'all' to search across all regions.

    Yields:
        botocore_session: It will retrieve a session for each profile and region.
    """
    if profile_name == "all":
        profiles = boto3.Session().available_profiles
        for profile in profiles:
            yield from get_aws_session(profile, region_name)
    elif region_name == "all":
        try:
            session = boto3.Session(profile_name=profile_name, region_name="us-east-1")
            client = session.client("ec2")
            regions = client.describe_regions(
                Filters=[
                    {
                        "Name": "opt-in-status",
                        "Values": ["opt-in-not-required", "opted-in"],
                    }
                ]
            )["Regions"]
            for region in regions:
                yield from get_aws_session(profile_name, region["RegionName"])
        except Exception:
            yield None
    else:
        try:
            session = boto3.Session(profile_name=profile_name, region_name=region_name)
            yield session
        except Exception:
            yield None


def aws_search(profile_name, region_name, output, func, **kwargs):
    """Iterate over all AWS sessions and call the function with the provided arguments.

    Args:
        profile_name (string): AWS profile name.
        region_name (string): AWS region name.
        output (string): output format. You can choose between table, json.
        func (function): function to call.
    """
    for session in get_aws_session(profile_name, region_name):
        if session is not None:
            response = func(session, **kwargs)
            if response is not None:
                data = deserialize.deserialize(response)
                print_data(
                    profile=session.profile_name,
                    region=session.region_name,
                    data=data,
                    output=output,
                )
        else:
            continue


def print_data(profile, region, data, output):
    """Print the data in a table.

    Args:
        profile (string): AWS profile name.
        region (string): AWS region name.
        data (dict): dict of AWS resources.
        output (string): output format. You can choose between table, json.
    """
    if output == "table":
        print(
            "[+] Session created for profile '{}' and region '{}'".format(
                profile, region
            )
        )
        print(
            tabulate(
                data,
                headers="keys",
                tablefmt="pretty",
            )
        )
    elif output == "json":
        print(
            json.dumps(
                {
                    "profile": profile,
                    "region": region,
                    "data": data,
                },
                indent=2,
            )
        )


def get_region(c, region):
    """Get the region from the context or the default value.

    Args:
        c (context): fabric context.
        region (string): AWS region name.

    Returns:
        string: AWS region name.
    """
    return c.get("AWS_REGION", "eu-central-1") if region is None else region
