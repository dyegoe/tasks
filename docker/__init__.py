from invoke import Collection, task

ns = Collection("docker")


@task
def build(c):
    """Build the Docker image.
    This function expects the following 'invoke.yaml' variables to be set:
    - DOCKER_IMAGE_NAME
    - DOCKER_IMAGE_TAG"""
    print(f"Building docker image {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']}")
    c.run(f"docker build -t {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']} .")


@task
def run(c, local=False, aws=True, ssh=True):
    """Run the Docker image.
    This function expects the following 'invoke' variables to be set:
    - DOCKER_IMAGE_NAME
    - DOCKER_IMAGE_TAG
    - DOCKER_CONTAINER_NAME
    - DOCKER_CONTAINER_WORKDIR"""
    print(f"Running {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']}")
    mount_local = "" if not local else f"-v {c['CURRENT_DIR']}:/ansible"
    aws_access_key_id = (
        "" if not aws else f"-e AWS_ACCESS_KEY_ID={c['AWS_ACCESS_KEY_ID']}"
    )
    aws_secret_access_key = (
        "" if not aws else f"-e AWS_SECRET_ACCESS_KEY={c['AWS_SECRET_ACCESS_KEY']}"
    )
    ssh_private_key = (
        "" if not ssh else f"-v {c['SSH_PRIVATE_KEY_EXPAND']}:/root/.ssh/id_rsa"
    )
    workdir = c.get("DOCKER_CONTAINER_WORKDIR", "/root")
    c.run(
        " ".join(
            [
                f"docker run --rm",
                f"{aws_access_key_id}",
                f"{aws_secret_access_key}",
                f"{mount_local}",
                f"{ssh_private_key}",
                f"{workdir}",
                f"--name {c['DOCKER_CONTAINER_NAME']}",
                f"-it {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']} sh",
            ]
        ),
        pty=True,
    )


@task
def stop(c):
    """Stop the Docker container
    This function expacts the following 'invoke' variables to be set:
    - DOCKER_CONTAINER_NAME"""
    print(f"Stoping docker container {c['DOCKER_CONTAINER_NAME']}")
    c.run(f"docker stop {c['DOCKER_CONTAINER_NAME']}")


@task
def rm(c):
    """Remove the Docker container
    This function expacts the following 'invoke' variables to be set:
    - DOCKER_CONTAINER_NAME"""
    print(f"Removing docker container {c['DOCKER_CONTAINER_NAME']}")
    c.run(f"docker rm -f {c['DOCKER_CONTAINER_NAME']}")


@task
def rmi(c):
    """Remove the Docker image
    This function expacts the following 'invoke' variables to be set:
    - DOCKER_IMAGE_NAME
    - DOCKER_IMAGE_TAG"""
    print(f"Removing docker image {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']}")
    c.run(f"docker rmi -f {c['DOCKER_IMAGE_NAME']}:{c['DOCKER_IMAGE_TAG']}")


ns.add_task(build)
ns.add_task(run)
ns.add_task(stop)
ns.add_task(rm)
ns.add_task(rmi)
