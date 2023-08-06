from pathlib import Path
import subprocess
import click


def run(args):
    command = [f'{Path(__file__).parent.parent}/bin/docker-compose'] + list(args)
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode().strip()


@click.command('docker-compose')
@click.argument('args', nargs=-1)
def docker_compose(args):
    output = run(args)
    click.echo(output)

if __name__ == '__main__':
    docker_compose()
