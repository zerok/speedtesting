#!/bin/bash
git_path=$(which git)
ansible_path=$(which ansible)
set -e

if [[ "$USER" != "root" ]]; then
    echo "Please run this script either as root or with sudo."
    exit 1
fi


# Install ansible and all other dependencies
if [[ -z "${ansible_path}" ]]; then
    echo "#"
    echo "# Installing ansible..."
    echo "#"
    echo ""
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
    echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" > /etc/apt/sources.list.d/ansible.list
    apt-get update
    apt-get install -y ansible
    echo ""
fi

if [[ -z "${git_path}" ]]; then
    echo "#"
    echo "# Installing git..."
    echo "#"
    echo ""
    apt-get install -y git
    echo ""
fi

echo "#"
echo "# Installing speedtesting..."
echo "#"
echo ""
mkdir -p /opt/src
cd /opt/src
if [[ ! -d speedtesting ]]; then
    git clone https://github.com/zerok/speedtesting.git
fi
cd speedtesting/ansible
git checkout -f master
git pull origin master
echo -e "localhost ansible_connection=local\n[raspberrypi-speedtest]\nlocalhost" > hosts
ansible-playbook -i hosts install.yml

echo -e "\n#\n# DONE!\n#\n"
cat /var/tmp/setup-success.txt
