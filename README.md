# CLI_based_chat_tool

# Objective
Building a chat tool with a simple command-line interface which supports multiple chat rooms.

 here Y and B join same room and chat each other but D can't see any chat of 101 room D join different room 106 all room connect to common server

# Create EC2 Instance
# Establish ssh Connection

# Follow these Commands

sudo su

sudo apt update

sudo apt upgrade


# Create Virtual Environment

sudo apt install python3-venv

python3 -m venv env

. env/bin/activate 

# Create Files
write private ip address and port number in both programs 

1.server.py

2.client.py


# pymango connection
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

# add mongo repo
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update

sudo apt-get install -y mongodb-org

pip install pymongo

#Run Programs


# The clients should be able to do the following

– List all the existing chat rooms.

– Create a new chat room.

– Join an existing chat room.

• Messages is sent by a client in a chat room should be only broadcasted to same chat room.

# output

