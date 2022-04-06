import os
def plan_and_apply():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform init && terraform fmt && terraform validate && terraform plan && terraform apply --auto-approve")
def destroy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform destroy --auto-approve")
