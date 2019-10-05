#!/usr/bin/env python3

import os
from sys import argv
from collections import defaultdict


# type to extensions
VALID_NAMES = {
    'apaga': ('sql',),
    'consulta': ('sql',),
    'controle': ('sql',),
    'fisico': ('sql',),
    'popula': ('sql',),
    'conceitual': ('brM3',),
    'logico': ('brM3',),
    'doc': ('pdf', 'doc', 'docx'),
}


_exts = set(ext for exts in VALID_NAMES.values() for ext in exts)


# Renamed exercise is like: class_type_name_registrationnumber.ext
def is_renamed_exercise(filee):
    return (any((filee.endswith(ext)) for ext in _exts)
            and filee.startswith('aula'))


# Shortname exercise is like: consulta.sql
def is_shortname_exercise(filee):
    # Just some iterations
    short_names = (f'{n}.{ext}' for n, _exts in
                   VALID_NAMES.items() for ext in _exts)

    return filee in short_names


def type_to_presentation_type(typee):
    if typee.lower() != 'doc':
        return typee[0].upper() + typee[1:]
    return 'DOC'


def alert_ignored_files(ignored_files):
    print('=============================\n'
          '\tIgnored Files\n'
          '=============================')
    ignored_files = '\n'.join(
        f'  {i+1}. {f}' for i, f in enumerate(ignored_files)
    )
    print("The following files will be ignored because they don't"
          f" look like exercises:\n{ignored_files}")


def alert_renamings_to_be_applied(renamings):
    print('======================================\n'
          '\tRenamings to be applied:\n'
          '======================================')
    total_renamings = 0
    for old_name, new_name in renamings.items():
        if old_name != new_name:
            total_renamings += 1
            print(f'{total_renamings}. {old_name} ----> {new_name}')
        else:
            print(f'  X. {old_name} is already renamed!')
    print(f'\nTotal of renamings: {total_renamings}')

    if not total_renamings:
        print('No renamings to be applied!')
        exit(0)


def confirm_operations(renamings, ignored_files):
    alert_ignored_files(ignored_files)
    print()
    alert_renamings_to_be_applied(renamings)

    try:
        input('\nLooks good? ENTER to confirm or CTRL-C to cancel')
    except KeyboardInterrupt:
        print('\n\nRenaming cancelled! No files were touched!')
        exit(0)


def rename_files(renamings):
    for old_name, new_name in renamings.items():
        os.rename(old_name, new_name)

    print(f'\nFinished! Renamings applied!')


if __name__ == '__main__':

    if len(argv) <= 3:
        print("Usage example: vandor-rename"
              " [class_name] [your_name] [your_registration_number]")
        exit(0)

    _, class_name, name, registration_number, *_ = argv

    def get_new_name(typee, ext=None):
        new_name = '_'.join((class_name, typee, name, registration_number))
        ext = ext or VALID_NAMES[typee.lower()][0]

        return f'{new_name}.{ext}'

    def parse_files(all_files):
        renamings = defaultdict(lambda: '')
        renamings_reversed = defaultdict(lambda: '')
        ignored_files = []

        for f in all_files:
            if not renamings[f]:  # Sanity check
                new_name = ''
                if is_renamed_exercise(f):
                    typee = type_to_presentation_type(f.split('_')[1])
                    new_name = get_new_name(typee)
                elif is_shortname_exercise(f):
                    typee, ext = f.split('.')
                    typee = type_to_presentation_type(typee)
                    new_name = get_new_name(typee, ext)
                else:
                    ignored_files.append(f)
                    continue

                renamings[f] = new_name
                renamings_reversed[new_name] = f
            else:
                raise ValueError(f"'{new_name}' can be generated by '{f}'"
                                 f" and '{renamings_reversed[f]}'!"
                                 " No files will be renamed!")

        renamings = {k: v for k, v in renamings.items() if v}
        return renamings, ignored_files

    def beg():
        print('Cool application? Please give a star on Github:'
              ' https://github.com/icaropires/vandor-rename !')

    all_files = os.listdir()
    renamings, ignored_files = parse_files(all_files)

    confirm_operations(renamings, ignored_files)
    rename_files(renamings)

    beg()
