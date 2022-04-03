# Requirements
1. run " sudo apt update && sudo apt upgrade -y "
2. run " sudo apt install python3 -y && sudo apt install python3-pip -y && sudo apt install git -y "
3. clone the repository "https://atlas-techno/API" on /
4. run " cd /app && virtualenv venv && source venv/bin/activate "
5. run " pip3 install fastapi[all] "
6. run " curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - "
7. run " sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" "
8. run " sudo apt-get update && sudo apt-get install terraform "
9. run " uvicorn --host 0.0.0.0 app.main:app "
