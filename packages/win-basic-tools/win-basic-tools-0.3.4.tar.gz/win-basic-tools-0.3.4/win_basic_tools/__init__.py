from io import StringIO
import os
import stat
import sys
import time

from colorama import Fore, Style, deinit, init

check_0 = (
    ('d', stat.FILE_ATTRIBUTE_DIRECTORY),
    ('l', stat.FILE_ATTRIBUTE_REPARSE_POINT),
)

check_1 = (
    ('a', stat.FILE_ATTRIBUTE_ARCHIVE),
    ('r', stat.FILE_ATTRIBUTE_READONLY),
    ('h', stat.FILE_ATTRIBUTE_HIDDEN),
    ('s', stat.FILE_ATTRIBUTE_SYSTEM)
)

icons_map = {
    'd': ' ',
    'l': ' ',
    'a': ' ',
    'else': ' '
}

colors_map = {
    'd': Fore.LIGHTBLUE_EX,
    'l': Fore.LIGHTCYAN_EX,
    'a': Fore.LIGHTGREEN_EX,
    'else': Fore.LIGHTYELLOW_EX
}


class DirEntryWrapper:
    # os.DirEntry is a final class, can't be subclassed
    __slots__ = 'entry', 'name', 'path'

    def __init__(self, entry: os.DirEntry):
        self.entry = entry
        self.name = entry.name
        self.path = entry.path

    def stat(self):
        try:
            return self.entry.stat()
        except PermissionError:
            return self.entry.stat(follow_symlinks=False)

    def is_dir(self):
        try:
            return self.entry.is_dir()
        except PermissionError:
            return self.entry.is_dir(follow_symlinks=False)

    def is_symlink(self):
        return self.entry.is_symlink()


class Ls:
    '''
    Lists the content of a directory.
    '''

    __slots__ = 'opt', 'path', 'out', 'files', 'dirs', 'size'

    def __init__(self, opt='', path='.', to_cache=False) -> None:

        init()

        if not opt or opt.startswith('-'):
            self.opt, self.path = opt, path
        else:
            self.opt, self.path = '', opt

        self.out = StringIO() if to_cache else sys.stdout
        self.files = 0
        self.dirs = 0
        self.size = 0

    def __del__(self):
        deinit()

    def echo(self, signal=0) -> None:
        try:
            scandir = os.scandir(self.path)

        except NotADirectoryError:
            print(f'{self.path} is not a directory.', file=self.out)
            return
        except PermissionError as err:
            if signal:  # not going recursively on echo()
                print(f'{str(err)[:12]} {err.strerror}: {err.filename}',
                      file=self.out)
                return

            aux = os.path.realpath(self.path)
            if aux != self.path:
                self.path = aux
                self.echo(signal=1)
            else:
                print(f'{str(err)[:12]} {err.strerror}: {err.filename}',
                      file=self.out)

            return
        except OSError:
            print(f'{self.path} is not a valid path.', file=self.out)
            return

        scandir = [DirEntryWrapper(i) for i in scandir]

        # just add to the list if it will be ever displayed
        # first we remove hidden ones if user hasn't asked for it
        dir = [
            i for i in scandir
            if ('a' in self.opt or not (
                i.name.startswith('.') or
                i.stat().st_file_attributes &
                stat.FILE_ATTRIBUTE_HIDDEN)
                )
        ]

        if 'l' not in self.opt:
            # if in, i would want the oposite order
            dir.sort(key=lambda x: (x.stat().st_mode, x.name), reverse=True)

            print(
                *[self._type_color(i) for i in dir],
                sep='   ', file=self.out
            )
            return

        dir.sort(key=lambda x: (x.stat().st_mode, x.name))

        for i in dir:
            filemode_str = self._windows_filemode(
                i.stat().st_file_attributes
            )

            # print() by 'column item' for better performance
            print(end=' ', file=self.out)
            print(filemode_str, end='   ', file=self.out)
            print(time.strftime(
                '%d %b %y %H:%M', time.localtime(
                    i.stat().st_ctime)), end='   ', file=self.out)
            print(
                self._humanize_size(i).rjust(7),
                end='   ', file=self.out
            )
            print(self._type_color(i), file=self.out)

        if not any((self.files, self.dirs)):
            return

        total_size = self._humanize_size2(self.size).rjust(7)
        print(
            str(self.files).rjust(3) + ' Files',
            str(self.dirs).rjust(2) + ' Dirs',
            'Total: ', total_size,
            sep='  ', file=self.out
        )

    def _type_color(self, i: DirEntryWrapper) -> str:
        is_syml = i.is_symlink()
        is_dir = i.is_dir()

        if is_dir:
            self.dirs += 1
        if is_syml:
            self.files += 1

        if 'c' not in self.opt:
            return i.name

        if is_dir or is_syml:
            joined = os.path.join(os.path.realpath(self.path), i.name)
            if os.path.realpath(i.path) != joined:
                return (Fore.CYAN
                        + i.name
                        + Fore.LIGHTBLACK_EX
                        + ' --> '
                        + os.path.realpath(i.path)
                        + Style.RESET_ALL)

            return Fore.LIGHTBLUE_EX + i.name + Style.RESET_ALL

        self.files += 1
        if i.name.endswith(('.zip', '.exe', '.msi', '.dll',
                            '.bat', '.sys', '.log', '.ini')):
            return Fore.YELLOW + i.name + Style.RESET_ALL
        if i.name.endswith(('.py', '.pyx', '.pyd', '.pyw')):
            return Fore.GREEN + i.name + Style.RESET_ALL
        if i.name.endswith(('.tmp')):
            return Fore.LIGHTBLACK_EX + i.name + Style.RESET_ALL
        if i.name.endswith(('.pdf')):
            return Fore.LIGHTRED_EX + i.name + Style.RESET_ALL
        return i.name

    def _humanize_size2(self, entry: int) -> str:
        units = ('k', 'M', 'G')
        final = ''

        for unit in units:
            if entry < 1024:
                break
            entry /= 1024
            final = unit

        if final:
            data = f'{entry:.1f}{final}'
        else:
            data = str(entry)

        if 'c' in self.opt:
            if 'G' in data:
                data = Fore.RED + data + Style.RESET_ALL
                data = data.rjust(16)
            elif 'M' in data:
                data = Fore.LIGHTRED_EX + data + Style.RESET_ALL
                data = data.rjust(16)
            elif 'k' in data:
                data = Fore.YELLOW + data + Style.RESET_ALL
                data = data.rjust(16)

        return data

    def _humanize_size(self, i: DirEntryWrapper):
        if i.is_dir():
            return '-'

        entry = i.stat().st_size

        self.size += entry

        return self._humanize_size2(entry)

    def _windows_filemode(self, data: int):
        if data == 0x80:
            res = list('-a---')
        else:
            res = list('-----')
            for check in check_0:
                if data & check[1]:
                    res[0] = check[0]

            for ind, check in zip(range(1, 5), check_1):
                if data & check[1]:
                    res[ind] = check[0]

        icon = ''
        if 'i' in self.opt:
            for ind in range(5):
                if res[ind] in icons_map:
                    icon = icons_map[res[ind]]
                    break
            else:
                icon = icons_map['else']

        done = False  # flags coloring icon
        if 'c' in self.opt:
            for ind in range(5):
                if res[ind] == '-':
                    continue
                if icon and res[ind] in icons_map and not done:
                    icon = colors_map[res[ind]] + icon + Style.RESET_ALL
                    done = True
                res[ind] = (Fore.BLUE + res[ind] + Style.RESET_ALL)

            if icon == icons_map['else']:
                icon = colors_map['else'] + icon + Style.RESET_ALL

        if not icon:
            icon = '  '

        return icon + ''.join(res)
