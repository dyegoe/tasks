from invoke import Collection, Config, task

from . import ansible, aws, docker

from os import environ, path, getcwd
from configparser import ConfigParser

# Set initial Global Variables
HOME = path.expanduser("~")
CURRENT_DIR = getcwd()

# Load invoke configuration if it exists
c = Config()
invoke_config = f"{CURRENT_DIR}/invoke.yaml"
if path.isfile(invoke_config):
    c.set_runtime_path(invoke_config)
    c.load_runtime()

# Set the SSH key to use
SSH_PRIVATE_KEY_EXPAND = path.expanduser(c.get("SSH_PRIVATE_KEY", "~/.ssh/id_rsa"))

# Load AWS credentials
aws_credentials = ConfigParser()
aws_credentials.read(f"{HOME}/.aws/credentials")
AWS_ACCESS_KEY_ID = environ.get(
    "AWS_ACCESS_KEY_ID",
    aws_credentials.get("default", "aws_access_key_id", fallback="not-found"),
)
AWS_SECRET_ACCESS_KEY = environ.get(
    "AWS_SECRET_ACCESS_KEY",
    aws_credentials.get("default", "aws_secret_access_key", fallback="not-found"),
)

# Load registry password from file if it exists
registry_password_file = f"{CURRENT_DIR}/.registry_password.secrets"
if path.isfile(registry_password_file):
    with open(registry_password_file, "r") as f:
        REGISTRY_PASSWORD = f.read().strip()
else:
    REGISTRY_PASSWORD = ""

# Get try to get config from 'invoke.yml' file
try:
    DOCKER_CONTAINER_NAME = c["DOCKER_CONTAINER_NAME"]
    DOCKER_IMAGE_NAME = c["DOCKER_IMAGE_NAME"]
    DOCKER_IMAGE_TAG = c["DOCKER_IMAGE_TAG"]
    DOCKER_CONTAINER_WORKDIR = c["DOCKER_CONTAINER_WORKDIR"]
    SSH_PRIVATE_KEY = c["SSH_PRIVATE_KEY"]
    ANSIBLE_INVENTORY_FILE = c["ANSIBLE_INVENTORY_FILE"]
except KeyError as k:
    raise SystemExit(f"You must set {k} in the 'invoke.yml' file")

# Create main Collection, configure and add sub-collections
ns = Collection("main")
ns.configure(
    {
        "HOME": HOME,
        "CURRENT_DIR": CURRENT_DIR,
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        "REGISTRY_PASSWORD": REGISTRY_PASSWORD,
        "SSH_PRIVATE_KEY_EXPAND": SSH_PRIVATE_KEY_EXPAND,
        "DOCKER_CONTAINER_NAME": DOCKER_CONTAINER_NAME,
        "DOCKER_IMAGE_NAME": DOCKER_IMAGE_NAME,
        "DOCKER_IMAGE_TAG": DOCKER_IMAGE_TAG,
        "DOCKER_CONTAINER_WORKDIR": DOCKER_CONTAINER_WORKDIR,
        "SSH_PRIVATE_KEY": SSH_PRIVATE_KEY,
        # "ANSIBLE_INVENTORY_FILE": ANSIBLE_INVENTORY_FILE,
    }
)
ns.add_collection(ansible)
ns.add_collection(aws)
ns.add_collection(docker)


# Add tasks to main Collection
@task(iterable=["names"])
def hello(c, names):
    for key in c:
        print(key)

    for name in names:
        print(f"Hello {name}!")


ns.add_task(hello)
