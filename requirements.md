# Requirements(Make all of it as a root user)
1. run " sudo apt update && sudo apt upgrade -y "
2. run " useradd -m -d /home/cephalon/ -s /bin/bash cephalon && usermod -aG sudo cephalon "
3. run " sudo apt install python3 -y && sudo apt install python3-pip -y && sudo apt install git -y "
4. clone the repository "https://atlas-techno/API" on /
5. run " mkdir /app && cp -r API/ /app && rm -rf API " 
6. run " cd /app && virtualenv venv && chmod a+x venv/bin/activate && source /app/venv/bin/activate"
7. run " pip3 install fastapi[all] "
8. run " curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - "
9. run " sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" "
10. run " sudo apt-get update && sudo apt-get install terraform "
11. Make the code corrections
12. run " uvicorn --host 0.0.0.0 app.main:app "
