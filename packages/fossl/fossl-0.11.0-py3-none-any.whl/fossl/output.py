
'''
Console output functions
'''

from rich.console import Console
from rich.table import Table


console = Console()


def bold(text):
    '''A helper to let the argument appear bold.'''
    return pretty(f'[b]{text}[/]')


def pretty(text):
    '''A helper to let the argument appear bold.'''
    with console.capture() as capture:
        console.print(text, end='')
    return capture.get()


def print_license_list(licenses, brief=False):
    '''Prints a table of the known (to GitHub) FOSS licenses.'''
    spdx_ids = sorted([x['spdx_id'] for x in licenses])
    if brief:
        console.print(', '.join(spdx_ids))
        return
    table = Table(show_header=True, show_edge=True)
    table.add_column('SPDX ID')
    table.add_column('License Name')
    for val in spdx_ids:
        licinfo = [x for x in licenses if x['spdx_id'] == val][0]
        table.add_row(licinfo['spdx_id'], licinfo['name'])
    console.print(table)


def print_license_info(license_info, verbose=True):
    '''Prints detailed license information on the SPDX ID in the
       argument.'''
    if not verbose:
        console.print(f'[b]{license_info["name"]}[/], '
                      f'Permissions: {", ".join(license_info["permissions"])}')
        return
    table = Table(show_header=False, show_edge=False)
    table.add_column('left')
    table.add_column('right')
    if verbose:
        table.add_row('SPDX ID:', f'[b]{license_info["spdx_id"]}[/]')
        table.add_row('Name:', f'[b]{license_info["name"]}[/]')
        table.add_row('Description:', license_info['description'])
        table.add_row('Implementation:', license_info['implementation'])
        table.add_row('Permissions:', ', '.join(license_info['permissions']))
        table.add_row('Conditions', ', '.join(license_info['conditions']))
        table.add_row('Limitations:', ', '.join(license_info['limitations']))
    table.add_row('HTML URL:', f'[dodger_blue1]{license_info["html_url"]}[/]')
    table.add_row('GitHub API URL:', f'[dodger_blue1]{license_info["url"]}[/]')
    table.add_row('Featured on GitHub:',
                  'Yes' if license_info['featured'] else 'No')
    console.print(table)
