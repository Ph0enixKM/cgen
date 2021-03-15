import yaml
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filename', metavar='filename', help='alternative name of the config cgen.yaml file')
parser.add_argument('--dir', metavar='directory', help='where to create project (defaults to cwd)')

args = parser.parse_args()
filename = args.filename if args.filename else 'cgen.yaml'
src = '.c'
head = '.h'
compiler = 'clang'
flags = '-Wall -Wextra'
name = 'Program'
root = args.dir if args.dir else './'

lang = {
    'c': ['.c', '.h'],
    'cpp': ['.cpp', '.hpp'],
    'c++': ['.cpp', '.hpp']
}

class Reader:
    def __init__(self, filename):
        with open(filename) as file:
            self.filename = filename
            self.data = yaml.load(file, Loader=yaml.FullLoader)
    
    def settings(self):
        global src
        global head
        global compiler
        global flags
        global name
        if 'settings' in self.data:
            sett = self.data['settings']
            if 'lang' in sett:
                src = lang[sett['lang']][0]
                head = lang[sett['lang']][1]
            if 'compiler' in sett:
                compiler = sett['compiler']
            if 'flags' in sett:
                flags = sett['flags']
            if 'name' in sett:
                name = sett['name']


class Generator:
    def __init__(self, reader):
        self.data = reader.data

    def headerDefine(self, text):
        return text.upper().replace('-', '_')

    def libs(self):
        if 'libs' in self.data:
            os.mkdir(f'{root}/lib/')
            for key in self.data['libs']:
                os.mkdir(f'{root}/lib/{key}')
                with open(f'{root}/lib/{key}/{key}{head}', 'w') as lib_file:
                    lib_file.write(f'#ifndef {self.headerDefine(key)}\n')
                    lib_file.write(f'#define {self.headerDefine(key)}\n\n')
                    for module in self.data['libs'][key]:
                        lib_file.write(f'#include "{module}/{module}{head}"\n')
                        os.mkdir(f'{root}/lib/{key}/{module}')
                        with open(f'{root}/lib/{key}/{module}/{module}{src}', 'w') as file:
                            file.write(f'#include "{module}{head}"\n')
                        with open(f'{root}/lib/{key}/{module}/{module}{head}', 'w') as file:
                            file.write(f'#ifndef {self.headerDefine(module)}\n')
                            file.write(f'#define {self.headerDefine(module)}\n\n\n\n')
                            file.write(f'#endif\n')
                    lib_file.write(f'\n#endif\n')

    def modules(self):
        if 'modules' in self.data:
            for module in self.data['modules']:
                os.mkdir(f'{root}/src/{module}')
                with open(f'{root}/src/{module}/{module}{src}', 'w') as file:
                    file.write(f'#include "{module}{head}"\n')
                with open(f'{root}/src/{module}/{module}{head}', 'w') as file:
                    file.write(f'#ifndef {self.headerDefine(module)}\n')
                    file.write(f'#define {self.headerDefine(module)}\n\n\n\n')
                    file.write(f'#endif\n')

    def main(self):
        os.mkdir(f'{root}/src/')
        with open(f'{root}/src/main{src}', 'w') as file:
            file.write("/* Libraries */\n");
            if 'libs' in self.data:
                for key in self.data['libs']:
                    for module in self.data['libs']:
                        file.write(f'#include <{key}/{key}{head}>\n')
            file.write("\n/* Modules */\n");
            if 'modules' in self.data:
                for module in self.data['modules']:
                    file.write(f'#include "{module}/{module}{head}"\n')
            file.write('\n/* Temporary */\n#include <stdio.h>\n\n');
            file.write('\nint main() {\n\tprintf("Hello World!\\n");\n}\n');

    def makefile(self):
        with open(f'{root}/Makefile', 'w') as file:
            file.write(f'all:\n\t{compiler}')
            file.write(f' {flags} -o {name} -I lib ')
            file.write(f'src/main{src} ')
            for lib in self.data['libs']:
                for mod in self.data['libs'][lib]:
                    file.write(f'lib/{lib}/{mod}/{mod}{src} ')
            for mod in self.data['modules']:
                file.write(f'src/{mod}/{mod}{src} ')
            file.write(f'\n\nclean:\n\trm {name}\n\n')
            file.write(f'run:\n\t./{name}\n')
        
    def generate(self):
        self.main()
        self.libs()
        self.modules()
        self.makefile()


def main():
    if os.path.isfile('cgen.yaml'):
        reader = Reader(filename)
        reader.settings()
        gen = Generator(reader)
        gen.generate()


if __name__ == '__main__':
    main()
