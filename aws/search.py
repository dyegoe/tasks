from invoke import Collection, task

from . import common

# EC2 tasks
@task(help={"ids": "List of EC2 instance IDs split by comma (,)"})
def ec2_ids(c, ids, profile="default", region=None, output="table"):
    """Get EC2 instances by IDs."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.ec2.get_ec2_instances_by_ids,
        instance_ids=ids.split(","),
    )


@task(help={"names": "List of EC2 instance names (tag:Name) split by comma (,)"})
def ec2_names(c, names, profile="default", region=None, output="table"):
    """Get EC2 instances by names."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.ec2.get_ec2_instances_by_tags,
        tag_key="Name",
        tag_values=names.split(","),
    )


@task(
    help={
        "tag": "List of EC2 instance tag=values split by comma (,). e.g. 'key1=value1,value2'"
    }
)
def ec2_tag(c, tag, profile="default", region=None, output="table"):
    """Get EC2 instances by tag=value1,value2.
    It works for a single tag only."""
    key, values = tag.split("=")
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.ec2.get_ec2_instances_by_tags,
        tag_key=key,
        tag_values=values.split(","),
    )


@task(help={"private_ips": "List of EC2 instance private IPs split by comma (,)"})
def ec2_private_ips(c, private_ips, profile="default", region=None, output="table"):
    """Get EC2 instances by private IPs."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.ec2.get_ec2_instances_by_private_ips,
        private_ips=private_ips.split(","),
    )


@task(help={"public_ips": "List of EC2 instance public IPs split by comma (,)"})
def ec2_public_ips(c, public_ips, profile="default", region=None, output="table"):
    """Get EC2 instances by public IPs."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.ec2.get_ec2_instances_by_public_ips,
        public_ips=public_ips.split(","),
    )


# @task
# def ec2_ami(c, ami, profile="default", region=None, output="table"):
#     """Get EC2 instances by AMI."""
#     common.aws_search(
#         profile,
#         common.get_region(c, region),
#         output,
#         common.ec2.get_ec2_instances_by_ami,
#         ami=ami,
#     )


# ENI tasks
@task
def eni_private_ips(c, private_ips, profile="default", region=None, output="table"):
    """Get ENIs by private IP."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.eni.get_enis_by_private_ips,
        private_ips=private_ips.split(","),
    )


@task
def eni_public_ips(c, public_ips, profile="default", region=None, output="table"):
    """Get ENIs by public IP."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.eni.get_enis_by_public_ips,
        public_ips=public_ips.split(","),
    )


# ELBs tasks
@task
def elb_arns(c, arns, profile="default", region=None, output="table"):
    """Get ELBs by ARN."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.elb.get_elbs_by_arns,
        arns=arns.split(","),
    )


@task
def elb_names(c, names, profile="default", region=None, output="table"):
    """Get ELBs by name."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.elb.get_elbs_by_names,
        names=names.split(","),
    )


@task
def elb_dns_names(c, dns_names, profile="default", region=None, output="table"):
    """Get ELBs by DNS name."""
    common.aws_search(
        profile,
        common.get_region(c, region),
        output,
        common.elb.get_elbs_by_dns_names,
        dns_names=dns_names.split(","),
    )


# Create Collection
ns = Collection("search")

ec2 = Collection("ec2")
ns.add_collection(ec2)
ec2.add_task(ec2_ids, "ids")
ec2.add_task(ec2_names, "names")
ec2.add_task(ec2_tag, "tag")
ec2.add_task(ec2_private_ips, "private-ips")
ec2.add_task(ec2_public_ips, "public-ips")

eni = Collection("eni")
ns.add_collection(eni)
eni.add_task(eni_private_ips, "private-ips")
eni.add_task(eni_public_ips, "public-ips")

elb = Collection("elb")
ns.add_collection(elb)
elb.add_task(elb_arns, "arns")
elb.add_task(elb_names, "names")
elb.add_task(elb_dns_names, "dns-names")
