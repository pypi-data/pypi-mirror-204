import click

import requests

@click.command()
def hello():
    """Say hello"""
    click.echo('Hello, world!')

@click.group()
def figlu():
    """Figlu command line tool"""
    # 默认调用bash函数
    pass

def get_bash_scripts():
    url = 'http://39.101.69.111:4000/bash'
    r = requests.get(url)
    scripts = r.json()
    return scripts

def get_bash_script_dir(script):
    url = f'http://39.101.69.111:4000/bash/{script}'
    r = requests.get(url)
    scripts = r.json()
    return scripts

def get_bash_script(script, sub_script):
    url = f'http://39.101.69.111:4000/bash/{script}/{sub_script}'
    r = requests.get(url)
    script = r.text
    return script

def choose_script(scripts):
    script_index = 0
    while True:
        click.clear()
        click.echo('Select a script:')
        for i, script in enumerate(scripts):
            if i == script_index:
                click.echo(f'> {script}')
            else:
                click.echo(f'  {script}')
        key = click.getchar()
        if key == '\r':
            return scripts[script_index]
        elif key == '\x1b[A':
            script_index = (script_index - 1) % len(scripts)
        elif key == '\x1b[B':
            script_index = (script_index + 1) % len(scripts)

@figlu.command()
def bash():
    """Bash scripts"""
    import os
    scripts = get_bash_scripts()
    script = choose_script(scripts)
    sub_scripts = get_bash_script_dir(script)
    sub_script = choose_script(sub_scripts)
    bash_script = get_bash_script(script, sub_script)
    print("=" * 80)
    click.echo(bash_script)
    print("=" * 80)
    click.echo('Run this script?')
    if click.confirm('Continue?'):
        os.system(bash_script)
   
    


def main():
    print("Hello world!")

figlu.add_command(hello)
figlu.add_command(bash)

if __name__ == '__main__':
    figlu()
