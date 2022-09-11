def get_elbs_by_arns(session, arns):
    """Get all ELBs with a specific ARN.

    Args:
        session (botocore_session): AWS session.
        arns (list): List of ARNs.

    Returns:
        list: List of ELBs.
    """
    client = session.client("elbv2")
    try:
        response = client.describe_load_balancers(LoadBalancerArns=arns)
        print(response)
        return response
    except Exception:
        return None


def get_elbs_by_names(session, names):
    """Get all ELBs with a specific name.

    Args:
        session (botocore_session): AWS session.
        names (list): List of names.

    Returns:
        list: List of ELBs.
    """
    client = session.client("elbv2")
    try:
        response = client.describe_load_balancers(Names=names)
        return response
    except Exception:
        return None


def get_elbs_by_dns_names(session, dns_names):
    """Get all ELBs with a specific DNS name.

    Args:
        session (botocore_session): AWS session.
        dns_names (list): List of DNS names.

    Returns:
        list: List of ELBs.
    """
    client = session.client("elbv2")
    try:
        elbs = client.describe_load_balancers()
        response = {"LoadBalancers": []}
        for elb in elbs["LoadBalancers"]:
            if elb["DNSName"] in dns_names:
                response["LoadBalancers"].append(elb)
        return response
    except Exception:
        return None
