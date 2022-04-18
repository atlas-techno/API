import os
def plan_and_apply(user,workspace):
    os.chdir(f'/atlas/{user}/{workspace}/')
    os.system("terraform init && terraform fmt && terraform validate && terraform apply --auto-approve")

def destroy_():
    os.system("terraform destroy --auto-approve")
