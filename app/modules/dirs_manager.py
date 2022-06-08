import os   
def create_workspace(user,workspace):
    if not os.path.isdir(f'/atlas/{user}'):
        os.mkdir(f'/atlas/{user}')
    os.chdir(f'/atlas/{user}')
    if not os.path.isdir(f'/atlas/{user}/{workspace}'):
        os.mkdir(f'{workspace}')
    os.chdir(f'/atlas/{user}/{workspace}')
    if not os.path.isdir(f'/atlas/{user}/keys'):
        os.mkdir(f'/atlas/{user}/keys')

def delete_dir(user,workspace):
    os.chdir(f'/atlas/{user}')
    os.system(f'rm -rf {workspace}')

def rename_dir(user,workspace,rename):
    os.rename(f'/atlas/{user}/{workspace}', f'/atlas/{user}/{rename}')

def goto(user,workspace):
    os.chdir(f'/atlas/{user}/{workspace}')