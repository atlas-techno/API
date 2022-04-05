# Requirements(Make all of it as a root user)
1. run " sudo apt update && sudo apt upgrade -y "
2. run " useradd -m -d /home/cephalon/ -s /bin/bash cephalon && usermod -aG sudo cephalon "
3. run " sudo apt install python3 -y && sudo apt install python3-pip -y && sudo apt install git -y "
4. run " git config --global user.email "atlas.tech.senai@gmail.com" && git config --global user.username "atlas-techno" "
5. clone the repository "https://atlas-techno/API" on /
6. run " mkdir /app && cp -r API/ /app && rm -rf API " 
7. run " pip3 install virtualenv && cd /app && virtualenv venv && chmod a+x venv/bin/activate && source /app/venv/bin/activate"
8. run " pip3 install fastapi[all] "
9. run " curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - "
10. run " sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" "
11. run " sudo apt-get update && sudo apt-get install terraform "
12. Make the code corrections
13. run " uvicorn --host 0.0.0.0 app.main:app"
14. Configure the env for create packeages and modules
