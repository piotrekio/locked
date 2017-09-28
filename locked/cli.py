import functools
import getpass
import time

import click

from . import clipboard
from . import password_manager


DEFAULT_STORAGE_PATH = './storage.locked'
MIN_PASSWORD_LENGTH = 8


def is_password_valid(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    return True


def get_password_with_confirmation():
    password1 = password2 = ''
    while not is_password_valid(password1) or password1 != password2:
        password1 = getpass.getpass('Enter password: ')
        password2 = getpass.getpass('Confirm password: ')
    return password1


def get_password(*args, confirm=False, prompt='Enter password'):
    if confirm:
        return get_password_with_confirmation()
    return getpass.getpass(f'{prompt}: ')


def handle_invalid_password(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except password_manager.InvalidPassword:
            click.secho('Invalid password', fg='red')
    return wrapper


option_storage_path = functools.partial(
    click.option,
    '--storage-path',
    default=DEFAULT_STORAGE_PATH,
    type=click.Path(exists=True)
)


@click.group()
def main(): pass


@main.command()
@click.argument('storage_path',
    default=DEFAULT_STORAGE_PATH,
    type=click.Path()
)
def init(storage_path):
    password = get_password(confirm=True)
    password_manager.initialize(storage_path, password)


@main.command()
@click.argument('key')
@click.argument('subkey')
@click.argument('value', default='')
@option_storage_path()
@handle_invalid_password
def set(storage_path, key, subkey, value):
    password = get_password()
    if not value:
        value = get_password(prompt='Enter value')
    password_manager.set(storage_path, password, key, subkey, value)


@main.command()
@click.argument('key', default='')
@click.argument('subkey', default='')
@click.option('--clear', default=30, type=click.INT)
@option_storage_path()
@handle_invalid_password
def get(storage_path, key, subkey, clear):
    password = get_password()

    if not key:
        for key in password_manager.get_keys(storage_path, password):
            click.echo(key)
        return

    value = password_manager.get(storage_path, password, key, subkey)

    if not value:
        return

    if subkey:
        clipboard.set(value.encode())
        if clear:
            click.echo(f'Value copied to clipboard. '
                       f'I will be removed in {clear} seconds...')
            time.sleep(clear)
            clipboard.clear()
        return

    for sk, v in value.items():
        click.echo(f'{sk}: {v}')


@main.command()
@click.argument('key')
@click.argument('subkey', default='')
@option_storage_path()
@handle_invalid_password
def remove(storage_path, key, subkey):
    password = get_password()
    password_manager.remove(storage_path, password, key, subkey)


if __name__ == '__main__':
    main()

