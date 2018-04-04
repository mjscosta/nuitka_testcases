#!/usr/bin/env python

#export PYTHONPATH=/usr/lib/python2.7/dist-packages/:/vagrant/test_nuitka_core/
import sys
import os
import os.path
import subprocess
import logging
import argparse
import shutil
import distutils.spawn

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Compile extension python modules with nuitka, recursively.')

parser.add_argument('--verbose', '-v', action='count', default=0,
                    help='print additional verbose information.')

parser.add_argument('--root-dir', default='.',
                    help='set root directory, from where to build nuitka modules.')
                  
parser.add_argument('--compile', nargs='?', const=True, default=False,
                    help='print additional verbose information.')
parser.add_argument('--clean', nargs='?', const=True, default=False,
                    help='clean nuitka build directories.')

parser.add_argument('--clean-modules', nargs='?', const=True, default=False,
                    help='clean nuitka compiled extension module files (.so or .pyd files).')

parser.add_argument('--clean-python', nargs='?', const=True, default=False,
                    help='clean python files that where compiled into extension modules.')

parser.add_argument('--patch-swig', nargs='?', const=True, default=False,
                    help='rewrite swig python modules for nuitka.')

parser.add_argument('--recurse-none', nargs='?', const=True, default=False,
                    help='do not recurse dependencies, see nuitka help.')

parser.add_argument('--recurse-to', type=str,
                    help='package to recurse to.')

parser.add_argument('--recurse-dir', type=str,
                    help='package to recurse to.')

parser.add_argument('--recurse-all', nargs='?', const=True, default=False,
                    help='recurse all.')

if distutils.spawn.find_executable('nuitka') is None:
    logger.error('please install nuitka, or make sure it is acessible in the path.')
    logger.error('use nuitka >= 0.5.28')
    exit(-1)


if len(sys.argv) == 0:
    parser.print_help()
    exit(-1)
    
arguments = parser.parse_args()

# logging configuration
log_levels = { 
    0 : logging.WARNING,
    1 : logging.INFO,
    2 : logging.DEBUG
}

logger.info('setting log level: {}'.format(log_levels.get(arguments.verbose, logging.NOTSET)))
#logging.basicConfig(level=logging.DEBUG) #log_levels.get(arguments.verbose, logging.NOTSET))
#logger.setLevel(logging.DEBUG)
logger.info('invoked with arguments: {}'.format(arguments))

#filter_directories = ['Python']
#filter_directories_with_cpp_sources = False

# swig targets use header files with name "<module_name>.i"
# swig files in order to be integrated with nuitka need to be changed,
# check http://www.tsheffler.com/blog/2015/01/05/nuitka-compiler-for-python/#Issues_with_Dynamically_Loaded_shared_objects_SWIG 
patch_swig_modules = True

# from https://stackoverflow.com/questions/5171502/c-vs-cc-vs-cpp-vs-hpp-vs-h-vs-cxx
cpp_sources = ['.c', '.C', '.cc', '.cxx', '.cpp', '.c++' ]
cpp_headers = ['.h', '.H', '.hh', '.hxx', '.hpp']


if arguments.patch_swig:
    logger.debug('about to patch swig modules.')
    for parent_dir, dirs, files in os.walk(arguments.root_dir):
        swig_header_modules = [os.path.splitext(f)[0] 
            for f in files if os.path.splitext(f)[1] in ['.i']]

        swig_lib_names = ["_" + f for f in swig_header_modules]

        swig_compiled_modules = [os.path.splitext(f)[0] for f in files 
            if os.path.splitext(f)[1] in ['.so', '.pyd'] 
            and os.path.splitext(f)[0] in swig_lib_names]

        swig_not_compiled_modules = [m for m in swig_lib_names if m not in swig_compiled_modules]
        if len(swig_not_compiled_modules) > 0:
            logger.warning("swig modules not compiled in {}!! : {}".format(parent_dir, swig_not_compiled_modules))

        if len(swig_compiled_modules) > 0:
            logger.info("swig compiled modules in {}: {}:".format(parent_dir, swig_compiled_modules))

        if len(swig_compiled_modules) > 0:
            for swig_compiled_module in swig_compiled_modules:
                swig_python_module = swig_compiled_module[1:] + ".py" # remove "_"
                swig_python_module_full_path = os.path.join(parent_dir, swig_python_module)
                logger.info("rewrite swig python module {}".format(swig_python_module_full_path))
                with open(swig_python_module_full_path, "w") as fh:
                    fh.write("import {}\n".format(swig_compiled_module))

if arguments.compile:
    # traverse root directory, and list directories as dirs and files as files
    for parent_dir, dirs, files in os.walk(arguments.root_dir):
        #print( root, dirs, files )
        
        current_directory_name = os.path.basename(parent_dir)
        logger.debug(current_directory_name)

        swig_header_modules = [os.path.splitext(f)[0]
            for f in files if os.path.splitext(f)[1] in ['.i']]

        python_files = [ f for f in files 
            if (not f == '__init__.py') # do not compile package python files
            and f.endswith('.py') 
            and not os.path.splitext(f)[0] == 'pyinstaller_specs' # do not compile pyinstaller specs
            and not os.path.splitext(f)[0] in swig_header_modules # do not compile swig modules.
            ]

        if len(python_files) > 0:
            logger.info('nuitka package to compile: {}'.format(parent_dir))
            logger.info('nuitka modules to compile: {}'.format(python_files))
            
        for _file in python_files:
            logger.debug('compiling {} with nuitka in {}'.format(_file, parent_dir))

            args = ['nuitka', '--module', _file, '--python-version=2.7']

            if arguments.recurse_to is not None:
                args.extend(['--recurse-to', arguments.recurse_to])

            if arguments.recurse_dir is not None:
                args.extend(['--recurse-directory', arguments.recurse_dir])

            if arguments.recurse_all is not None:
                args.extend(['--recurse-all'])

            if arguments.recurse_none is not None:
                args.extend(['--recurse-none'])

            logger.info('nuitka args: {}'.format(args))

            subprocess.call(args, cwd=parent_dir)
                
if arguments.clean:
    logger.debug('about to clean nuitka build directories.')
    for parent_dir, dirs, files in os.walk(arguments.root_dir):
        nuitka_build_dirs = [d for d in dirs if d.endswith('.build')]
        if len(nuitka_build_dirs) > 0:
            logger.debug('nuitka build dirs: {}.'.format(nuitka_build_dirs))
            for build_dir in nuitka_build_dirs:
                build_dir_full_path = os.path.join(parent_dir, build_dir)
                logger.info('Deleting nuitka build dir {}.'.format(build_dir_full_path))
                shutil.rmtree(build_dir_full_path)


if arguments.clean_modules:
    logger.debug('about to clean nuitka compiled extension modules.')
    for parent_dir, dirs, files in os.walk(arguments.root_dir):
        nuitka_compiled_modules = [f for f in files 
            if os.path.splitext(f)[1] in ['.so', '.pyd'] 
            and not f[:1] == '_'] # do not delete _<name>.so modules, swig
            
        if len(nuitka_compiled_modules) > 0:
            logger.debug('nuitka compiled extension modules: {}.'
                .format(nuitka_compiled_modules))
                
            for nuitka_compiled_module in nuitka_compiled_modules:
                nuitka_compiled_module_full_path = os.path.join(parent_dir, nuitka_compiled_module)
                logger.info('Deleting nuitka compiled extension module {}.'
                    .format(nuitka_compiled_module_full_path))
                os.remove(nuitka_compiled_module_full_path)

if arguments.clean_python:
    logger.debug('about to clean python files compiled to extension modules.')
    for parent_dir, dirs, files in os.walk(arguments.root_dir):
        nuitka_compiled_modules = [os.path.splitext(f)[0] for f in files if os.path.splitext(f)[1] in ['.so', '.pyd']]

        # do not delete python modules from swig external modules, file pattern "_<module_name>.(.pyd|.so)"
        python_modules = [os.path.splitext(f)[0] for f in files if os.path.splitext(f)[0] in nuitka_compiled_modules
                and (os.path.splitext(f)[1] in ['.py'])
                and not os.path.splitext(f)[0] == 'pyinstaller_specs' # do not delete spec files
                and not ('_' + os.path.splitext(f)[0]) in nuitka_compiled_modules # not swig modules
            ]

        if len(python_modules) > 0:
            logger.debug('nuitka delete python modules: {}.'
                .format(python_modules))

            for python_module in python_modules:
                python_module_full_path = os.path.join(parent_dir, python_module)
                logger.info('Deleting python module {}.'
                    .format(python_module_full_path))
                os.remove(python_module_full_path + '.py')
                try:
                    os.remove(python_module_full_path + '.pyc')
                except OSError:
                    pass                


