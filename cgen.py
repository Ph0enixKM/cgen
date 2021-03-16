import yaml
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filename', metavar='filename', help='alternative name of the config cgen.yaml file')

args = parser.parse_args()
filename = args.filename if args.filename else 'cgen.yaml'
filename = 'cgen.yml' if os.path.exists('cgen.yml') and filename == 'cgen.yaml' else filename
src = '.c'
head = '.h'
compiler = 'clang'
flags = '-Wall -Wextra'
name = 'Program'
root = '.'

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
        global root
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
            if 'dir' in sett:
                root = sett['dir']


class Generator:
    def __init__(self, reader):
        self.data = reader.data
        self.generated = []

    def headerDefine(self, text):
        return text.upper().replace('-', '_')

    def libs(self):
        if 'libs' in self.data:
            librootpath = f'{root}/lib'
            if not os.path.exists(librootpath):
                os.mkdir(librootpath)

            for key in self.data['libs']:
                libpath = f'{librootpath}/{key}'

                if not os.path.exists(libpath):
                    os.mkdir(libpath)
                    with open(f'{libpath}/{key}{head}', 'w') as lib_file:
                        lib_file.write(f'#ifndef {self.headerDefine(key)}\n')
                        lib_file.write(f'#define {self.headerDefine(key)}\n\n')

                        for module in self.data['libs'][key]:
                            source_file = f'{libpath}/{module}/{module}{src}'
                            header_file = f'{libpath}/{module}/{module}{head}'
                            lib_file.write(f'#include "{module}/{module}{head}"\n')
                            os.mkdir(f'{libpath}/{module}')
                            with open(source_file, 'w') as file:
                                file.write(f'#include "{module}{head}"\n')
                                self.generated.append(source_file)
                            with open(header_file, 'w') as file:
                                file.write(f'#ifndef {self.headerDefine(module)}\n')
                                file.write(f'#define {self.headerDefine(module)}\n\n\n\n')
                                file.write(f'#endif\n')
                                self.generated.append(header_file)
                        lib_file.write(f'\n#endif\n')

    def modules(self):
        if 'modules' in self.data:
            for module in self.data['modules']:
                modpath = f'{root}/src/{module}'
                if not os.path.exists(modpath):
                    os.mkdir(modpath)
                    source_file = f'{modpath}/{module}{src}'
                    header_file = f'{modpath}/{module}{head}'
                    with open(source_file, 'w') as file:
                        file.write(f'#include "{module}{head}"\n')
                        self.generated.append(source_file)
                    with open(header_file, 'w') as file:
                        file.write(f'#ifndef {self.headerDefine(module)}\n')
                        file.write(f'#define {self.headerDefine(module)}\n\n\n\n')
                        file.write(f'#endif\n')
                        self.generated.append(header_file)

    def main(self):
        srcpath = f'{root}/src/'
        if not os.path.exists(srcpath):
            os.mkdir(srcpath)
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
                file.write('\n/* Temporary */\n#include <stdio.h>\n\n')
                file.write('\nint main() {\n\tprintf("Hello World!\\n");\n}\n')
                self.generated.append(f'{root}/src/main{src}')

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
            self.generated.append(f'{root}/Makefile')
        
    def generate(self):
        if not os.path.exists(root):
            os.makedirs(root)
        self.main()
        self.libs()
        self.modules()
        self.makefile()

    def info(self):
        title = '\033[42m\033[30m'
        color = '\033[32m'
        light = '\033[32m\033[2m'
        clear = '\033[0m'
        print(f'\n{title} DONE {clear}')
        print(f'{color}Generated {len(self.generated)} file(s) 🎉{clear}')
        for file in self.generated:
            print(f'{light}{file}{clear}')


def main():
    if os.path.isfile(filename):
        reader = Reader(filename)
        reader.settings()
        gen = Generator(reader)
        gen.generate()
        gen.info()
    else:
        title = '\033[43m\033[30m'
        color = '\033[33m'
        clear = '\033[0m'
        print(f'\n{title} WARNING {clear}')
        print(f'{color}Could not find "cgen.yaml" file in current directory{clear}')


if __name__ == '__main__':
    main()
