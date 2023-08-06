import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart


@click.command()
@click.option("-x", "--tart-executable", required=False, default="tart", type=str, help="Path to the tart executable.")
def cleanup(tart_executable):
    """Command to greet a user."""
    p = GitLabCustomCommandConfig()

    tart = Tart(exec_path=tart_executable)
    tart_vm_name = p.vm_name()

    tart_images = tart.list()
    tart_vm_map = dict()
    # create map from images
    for i in tart_images:
        tart_vm_map[i.name] = i

    if tart_vm_name in tart_vm_map:
        click.echo(f"[INFO] '{tart_vm_name}' found.")
        if tart_vm_map[tart_vm_name].running:
            click.echo(f"[INFO] stopping '{tart_vm_name}'")
            tart.stop(tart_vm_name)
        click.echo(f"[INFO] deleting '{tart_vm_name}'")
        tart.delete(tart_vm_name)
