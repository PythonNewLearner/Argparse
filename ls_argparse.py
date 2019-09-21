import argparse
from pathlib import Path
import datetime
import pwd
import stat

def show_dir(p:Path,all=False,detail=True,human=False):
    def file_type(p:Path):
        if p.is_dir():
            return 'd'
        elif p.is_block_device():
            return 'b'
        elif p.is_char_device():
            return 'c'
        elif p.is_fifo():
            return 'p'
        elif p.is_socket():
            return 's'
        elif p.is_symlink():
            return 'l'
        else:
            return '-'

    def get_mode(mode:int,mode_str = ['r','w','x','r','w','x','r','w','x']):
        mode = mode & 0o777
        mstr= ''
        for i in range(8,-1,-1):
            m = mode >> i & 1
            if m:
                mstr += mode_str[8-i]
            else:
                mstr += '-'
        return mstr

    def get_size(size:int,units = ['','K','M','G','T','P']):
        index = 0
        while size >= 1000:
            size = size//1000
            index += 1
        return '{}{}'.format(size,units[index])

    def listdir(p:Path,all=False,detail=True,human=False):   #  drwxr-xr-x 5 baichen baichen  4096 Sep 20 16:27  venv
        path = Path(p)
        for x in path.iterdir():
            if not all and x.name.startswith('.'):
                continue

            if detail:
                st = x.stat()
                t = file_type(x)
                mode = get_mode(st.st_mode)
                atime = datetime.datetime.fromtimestamp(st.st_atime).strftime("%Y/%m/%d %H:%M:%S")

                size = get_size(st.st_size) if human else str(st.st_size)

                yield (t+mode, st.st_nlink, x.owner(), x.group(), size, atime, x.name)
            else:
                yield (x.name,)

    yield from sorted(listdir(p,all,detail,human),key=lambda x:x[-1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='ls', description='List information about the files', add_help=False)
    parser.add_argument('path', nargs='?', default='.', help='filepath')
    parser.add_argument('-l', dest='list', action='store_true', help='use a long listing format')
    parser.add_argument('-a', '--all', action='store_true', help='do not ignore entries starting with .')
    parser.add_argument('-h', '--human-readable', dest='human', action='store_true',help='with -l and/or -s, print human readable sizes (e.g., 1K 234M 2G)')
    args = parser.parse_args()

    for x in show_dir(args.path, args.all, args.list, args.human):
        print(x)
