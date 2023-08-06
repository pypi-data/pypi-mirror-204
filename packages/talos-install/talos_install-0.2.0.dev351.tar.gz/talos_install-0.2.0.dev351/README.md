# All in One installation

KEY REQUIRED
Ask for dev_key and dev_key.pub to download TALOS-CLI from GIT
Save key in your \<HOME>/.ssh folder

## OS requirements

Supported OS is Rocky Linux 8 (or any RHEL Like distibution)

An **user with sudo permissions** is MANDATORY, don't use root directly.

### Packages

- python >= 3.9
- pip >= 3.9
- ansible >= 7

```bash
sudo dnf install epel-release -y

# Install Python 3.9 requirements
sudo dnf install python39  python39-pip sshpass -y

# Update pip
pip3.9 install --upgrade pip

# Install package
pip install talos-install
```

### Installation

```bash
# Change configuration of config Files:

<pip environment>/share/talos_install/etc/talos.yaml
<pip environment>/share/talos_install/etc/global.yaml

# Run Installation bootstrap
talos_install bootstrap

# Run Installation deploy

talos_install deploy

```

Enjoy

### Post installation Steps

Then need to validate configuration

```bash
# First access as talos user
sudo su - talos

# By default setup is automatically done during deploy
# check <pip environment>/share/talos_cli/etc/talos.yaml
# talos_conf:
#   use_default: 'true'
# If necessary run setup
talos-config setup

# Load initial configuration
talos-config reload

# Check Key Pairs with Talos-cli (needed for update only)
talos-config git_keys

# check Overall status
talos-config check
```
