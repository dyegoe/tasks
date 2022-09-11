def get_enis_by_private_ips(session, private_ips):
    """Get all ENIs with a specific private IP.

    Args:
        session (botocore_session): AWS session.
        private_ips (list): List of private IPs.

    Returns:
        list: List of ENIs.
    """
    client = session.client("ec2")
    try:
        response = client.describe_network_interfaces(
            Filters=[{"Name": "addresses.private-ip-address", "Values": private_ips}]
        )
        return response
    except Exception:
        return None


def get_enis_by_public_ips(session, public_ips):
    """Get all ENIs with a specific public IP.

    Args:
        session (botocore_session): AWS session.
        public_ips (list): List of public IPs.

    Returns:
        list: List of ENIs.
    """
    client = session.client("ec2")
    try:
        response = client.describe_network_interfaces(
            Filters=[{"Name": "addresses.association.public-ip", "Values": public_ips}]
        )
        return response
    except Exception:
        return None
