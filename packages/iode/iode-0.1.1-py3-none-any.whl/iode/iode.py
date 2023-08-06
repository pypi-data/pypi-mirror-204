#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Gangdae Ju
# Created Date: Aug 10, 2021
# =============================================================================
import os
import shutil
import argparse
import configparser

version = '0.1.1'

iode_run_cmd = 'code' # 'code' or 'code-insider' 
iode_dir_path = os.path.join(os.path.expanduser('~'), '.iode')
iode_conf_path = os.path.join(os.path.expanduser('~'), '.iodeconfig')

def _list(args):
    global iode_dir_path
    for i in os.listdir(iode_dir_path):
        print(i)
    return 0

def _create(args):
    global iode_dir_path

    codeDir = os.path.join(iode_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    if os.path.exists(codeDir):
        print(f'ERROR: {args.env} is exist..')
        return -1

    try:
        os.makedirs(codeDir)
        os.makedirs(userdataDir)
        os.makedirs(extensionsDir)
        print('DONE : Successfully created..')
    except OSError:
        print('ERROR: Failed to create..')
        return -1
    
    return 0
    
def _delete(args):
    global iode_dir_path

    codeDir = os.path.join(iode_dir_path, args.env)

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} is not found..')
        return -1

    try:
        shutil.rmtree(codeDir)
        print('DONE : Successfully deleted..')
    except OSError:
        print('ERROR: Failed to delete..')
        return -1
    
    return 0

def _run(args):
    global iode_dir_path
    global iode_run_cmd
    
    codeDir = os.path.join(iode_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    cmd = iode_run_cmd

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} is not found..')
        return -1

    if os.path.exists(userdataDir):
        cmd =f'{cmd} --user-data-dir {userdataDir}'

    if os.path.exists(extensionsDir):
        cmd =f'{cmd} --extensions-dir {extensionsDir}'    
    
    try:
        cmd = f'{cmd} {args.path}'
        os.system(cmd)
    except OSError:
        print(f'ERROR: Faild to run {args.env}.')
        return -1

    return 0

def main():
    global iode_conf_path
    global iode_dir_path
    global iode_run_cmd
    
    if not os.path.exists(iode_conf_path):
        config_parser = configparser.ConfigParser()
        config_parser.add_section("setting")
        config_parser.set("setting", "iode_run", iode_run_cmd)
        config_parser.set("setting", "iode_dir", iode_dir_path)
        with open(iode_conf_path, "w") as fp:
            config_parser.write(fp)
    else:
        config_parser = configparser.ConfigParser()
        config_parser.read(iode_conf_path)
        iode_run_cmd = config_parser['setting']['iode_run']
        iode_dir_path = config_parser['setting']['iode_dir']
        # print(f'run_cmd = {iode_run_cmd}')
        # print(f'dir_path = {iode_dir_path}')
  
    if not os.path.exists(iode_dir_path):
        os.makedirs(iode_dir_path)
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--version', action='version', version=f'IODE v{version}')

    subparsers = arg_parser.add_subparsers()
    cmd_list = subparsers.add_parser('list', aliases=['l'], help='Show list of IODE environments.')
    cmd_list.set_defaults(func=_list)
    cmd_create = subparsers.add_parser('create', aliases=['c'], help='Create a new IODE environmtent.')
    cmd_create.add_argument('env')
    cmd_create.set_defaults(func=_create)
    cmd_delete = subparsers.add_parser('delete', aliases=['d'], help='Delete an IODE environmtent.')
    cmd_delete.add_argument('env')
    cmd_delete.set_defaults(func=_delete)
    cmd_run = subparsers.add_parser('run', aliases=['r'], help='Executes VSCODE using an IODE environment.')
    cmd_run.add_argument('env')
    cmd_run.add_argument('path')
    cmd_run.set_defaults(func=_run)
    
    args = arg_parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        arg_parser.parse_args(['-h'])

if __name__ == '__main__':
    main()
