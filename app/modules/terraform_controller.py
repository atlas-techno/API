import os
def plan_and_apply(workspace):
    os.chdir(f'/atlas/{workspace}/')
    os.system("terraform init && terraform fmt && terraform validate && terraform plan && terraform apply --auto-approve")

def destroy_():
    os.system("terraform destroy --auto-approve")

#def var_insert(args*):
 #   pass
