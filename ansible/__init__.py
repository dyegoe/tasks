from invoke import Collection, task

ns = Collection("ansible")


@task
def playbook(c, playbook, inventory=None, *args):
    """Run an Ansible playbook.
    This task expects the following 'invoke.yaml' variables to be set:
    - ANSIBLE_PLAYBOOKS_DIR
    - ANSIBLE_INVENTORY_FILE
    - SSH_PRIVATE_KEY"""
    try:
        inventory_file = (
            inventory if inventory is not None else c["ANSIBLE_INVENTORY_FILE"]
        )
    except KeyError as k:
        raise SystemExit(f"You must specify '--inventory' or set {k} in invoke.yaml")

    print(
        f"ansible-playbook -i {inventory_file} -e ansible_ssh_private_key_file={c['SSH_PRIVATE_KEY_EXPAND']} {playbook} {' '.join(args)}"
    )


@task
def play_deploy_stag(c):  ## Runs playbook/deploy_apps.yml -e env=stag
    """Run playbook/deploy_apps.yml -e env=stag"""
    print("Running playbook/deploy_apps.yml -e env=stag")
    playbook(
        c,
        "playbooks/deploy_apps.yml",
        "-e @examples/deploy.yml",
        "-e env=stag",
        f"-e registry_password={c['REGISTRY_PASSWORD']}",
    )


@task
def play_deploy_prod(c):  ## Runs playbook/deploy_apps.yml -e env=prod
    """Run playbook/deploy_apps.yml -e env=prod"""
    print("Running playbook/deploy_apps.yml -e env=prod")
    playbook(
        c,
        "playbooks/deploy_apps.yml",
        "-e @examples/deploy.yml",
        "-e env=prod",
        f"-e registry_password={c['REGISTRY_PASSWORD']}",
    )


deploy = Collection("deploy")
deploy.add_task(play_deploy_stag, "stag")
deploy.add_task(play_deploy_prod, "prod")

ns.add_task(playbook, "play")
ns.add_collection(deploy)
