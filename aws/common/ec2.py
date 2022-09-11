AMI_NAMES = {
    "amzn2-x86_64": {
        "owner": "amazon",
        "filters": [{"Name": "name", "Values": ["amzn2-ami-hvm-*-x86_64-gp2"]}],
    },
    "amzn2-arm64": {
        "owner": "amazon",
        "filters": [{"Name": "name", "Values": ["amzn2-ami-hvm-*-arm64-gp2"]}],
    },
    "amzn2-kernel-5-x86_64": {
        "owner": "amazon",
        "filters": [
            {"Name": "name", "Values": ["amzn2-ami-kernel-5.10-hvm-*-x86_64-gp2"]}
        ],
    },
    "amzn2-kernel-5-arm64": {
        "owner": "amazon",
        "filters": [
            {"Name": "name", "Values": ["amzn2-ami-kernel-5.10-hvm-*-arm64-gp2"]}
        ],
    },
}


def get_ec2_instances_by_ids(session, instance_ids):
    """Get all EC2 instances with a specific instance ID.

    Args:
        session (botocore_session): AWS session.
        instance_ids (list): List of instance IDs.

    Returns:
        list: List of EC2 instances.
    """
    client = session.client("ec2")
    try:
        response = client.describe_instances(InstanceIds=instance_ids)
        return response
    except client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            return {"Reservations": []}
        else:
            return None
    except Exception as e:
        return None


def get_ec2_instances_by_tags(session, tag_key, tag_values):
    """Get all EC2 instances with a specific tag.

    Args:
        session (botocore_session): AWS session.
        tag_key (string): Tag key.
        tag_values (list): List of tag values.

    Returns:
        list: List of EC2 instances.
    """
    client = session.client("ec2")
    try:
        response = client.describe_instances(
            Filters=[{"Name": "tag:{}".format(tag_key), "Values": tag_values}]
        )
        return response
    except Exception:
        return None


def get_ec2_instances_by_private_ips(session, private_ips):
    """Get all EC2 instances with a specific private IP.

    Args:
        session (botocore_session): AWS session.
        private_ips (list): List of private IPs.

    Returns:
        list: List of EC2 instances.
    """
    client = session.client("ec2")
    try:
        response = client.describe_instances(
            Filters=[{"Name": "private-ip-address", "Values": private_ips}]
        )
        return response
    except Exception:
        return None


def get_ec2_instances_by_public_ips(session, public_ips):
    """Get all EC2 instances with a specific public IP.

    Args:
        session (botocore_session): AWS session.
        public_ips (list): List of public IPs.

    Returns:
        list: List of EC2 instances.
    """
    client = session.client("ec2")
    try:
        response = client.describe_instances(
            Filters=[{"Name": "ip-address", "Values": public_ips}]
        )
        return response
    except Exception:
        return None


def get_amis(session, owner_ids, filters):
    """Get all AMIs with a specific owner ID.

    Args:
        session (botocore_session): AWS session.
        owner_ids (list): List of owner IDs.

    Returns:
        list: List of AMIs.
    """
    client = session.client("ec2")
    try:
        response = client.describe_images(Owners=owner_ids, Filters=filters)
        return response
    except Exception:
        return None
