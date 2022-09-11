from collections import OrderedDict
import pandas as pd


def find_tag_name(instance):
    """Get the name of an instance.

    Args:
        instance (dict): dict of an instance.

    Returns:
        string: name of the instance.
    """
    if "Tags" in instance:
        for tag in instance["Tags"]:
            if tag["Key"] == "Name":
                return tag["Value"]
    return None


def sort_data(data, order, ascending):
    """Sort the data by the provided column.

    Args:
        data (dict): dict of AWS resources.
        order (list): list of columns to sort by.
        ascending (list): list of booleans to sort by.

    Returns:
        dict: sorted dict of AWS resources.
    """
    if len(data) < 1:
        return data
    df = pd.DataFrame(data)
    df.sort_values(by=order, ascending=ascending, inplace=True)
    return df.to_dict(orient="records")


def deserialize_ec2_instances(response):
    """Deserialize the EC2 instances response.

    Args:
        response (dict): dict of EC2 instances.

    Returns:
        dict: dict of EC2 instances.
    """
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(
                OrderedDict(
                    [
                        ("InstanceState", instance.get("State", None).get("Name")),
                        ("InstanceName", find_tag_name(instance)),
                        ("InstanceId", instance.get("InstanceId", None)),
                        ("InstanceType", instance.get("InstanceType", None)),
                        (
                            "AvailabilityZone",
                            instance.get("Placement", None).get(
                                "AvailabilityZone", None
                            ),
                        ),
                        ("PrivateIpAddress", instance.get("PrivateIpAddress", None)),
                        ("PublicIpAddress", instance.get("PublicIpAddress", None)),
                    ]
                )
            )
    return sort_data(instances, ["InstanceState", "InstanceName"], [True, True])


def deserialize_enis(response):
    """Deserialize the ENIs response.

    Args:
        response (dict): dict of ENIs.

    Returns:
        dict: dict of ENIs.
    """
    enis = []
    for eni in response["NetworkInterfaces"]:
        enis.append(
            OrderedDict(
                [
                    ("PrivateIp", eni.get("PrivateIpAddress", None)),
                    ("PublicIp", eni.get("Association", None).get("PublicIp", None)),
                    ("NetworkInterfaceId", eni.get("NetworkInterfaceId", None)),
                    ("InterfaceType", eni.get("InterfaceType", None)),
                    ("InstanceId", eni.get("Attachment", None).get("InstanceId", None)),
                    ("AvailabilityZone", eni.get("AvailabilityZone", None)),
                    ("Status", eni.get("Status", None)),
                ]
            )
        )
    return sort_data(
        enis, ["Status", "InterfaceType", "InstanceId"], [True, True, True]
    )


def deserialize_elbs(response):
    """Deserialize the ELBs response.

    Args:
        response (dict): dict of ELBs.

    Returns:
        dict: dict of ELBs.
    """
    elbs = []
    for elb in response["LoadBalancers"]:
        elbs.append(
            OrderedDict(
                [
                    ("LoadBalancerName", elb.get("LoadBalancerName", None)),
                    ("DNSName", elb.get("DNSName", None)),
                    ("Type", elb.get("Type", None)),
                    ("Scheme", elb.get("Scheme", None)),
                    ("LoadBalancerArn", elb.get("LoadBalancerArn", None)),
                ]
            )
        )
    return sort_data(elbs, ["LoadBalancerName"], [True])


def deserialize_images(response):
    """Deserialize the images response.

    Args:
        response (dict): dict of images.

    Returns:
        dict: dict of images.
    """
    images = []
    for image in response["Images"]:
        images.append(
            OrderedDict(
                [
                    ("ImageId", image.get("ImageId", None)),
                    ("Name", image.get("Name", None)),
                    ("CreationDate", image.get("CreationDate", None)),
                ]
            )
        )
    return sort_data(images, ["CreationDate"], [False])


def deserialize(response):
    """Deserialize the response.

    Args:
        response (dict): dict of AWS resources.

    Returns:
        dict: dict of AWS resources.
    """
    if "Reservations" in response:
        return deserialize_ec2_instances(response)
    elif "NetworkInterfaces" in response:
        return deserialize_enis(response)
    elif "LoadBalancers" in response:
        return deserialize_elbs(response)
    elif "Images" in response:
        return deserialize_images(response)
    else:
        print(response)
        return None
