import os
def plan_and_apply(user,workspace):
    os.chdir(f'/atlas/{user}/{workspace}/')
    os.system("terraform init && terraform fmt && terraform validate && terraform apply --auto-approve")

def destroy_(user,workspace):
    os.system(f'/atlas/{user}/{workspace}/terraform destroy --auto-approve')
