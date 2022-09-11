from invoke import Collection, task


@task
def update(c):
    """Update the submodules."""
    c.run("git submodule update --init --recursive")
