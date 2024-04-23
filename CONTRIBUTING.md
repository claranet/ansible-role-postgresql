# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Developer's guide

In order to run this role as a developper you will need an environnement meeting the following requirements:
- docker, python3, ansible, ansible-lint, molecule

The following show the setup process for an Ubuntu 22.04 environnement but you can easily replicate this on any system that can meet the specified requirements.

- Docker installation: checkout the [official tutorial](https://docs.docker.com/engine/install/ubuntu/) for installing docker.
```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release 
	
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
After installation make sure to run this command to add your current user to the `docker` group so that you can run the docker command without using sudo.
```bash
sudo usermod --append $USER --groups docker
```

- rsync, Python 3, ansible and molecule setup

```bash
sudo apt install -y git python3 python3-pip python3-venv rsync
git clone <link-to-this-repository> ansible-role-postgresql
cd ansible-role-postgresql
python3 -m venv env # Create a virtual environnement
source env/bin/activate # Activate the environnement
pip3 install ansible ansible-lint molecule[docker] # Install the python packages in the virutal environnement
```

After setting up the environnement you can use molecule to test the role as you wish. If you are not very familiar with molecule, checkout the following table for some basic commands you can run against this role.

Command                                            | description                                                                             |
---------------------------------------------------|-----------------------------------------------------------------------------------------|
molecule list                                      | List the available scenarios for testing                                                |
molecule converge -s cluster                       | Create the necessary docker containers and run this scenarios to set them up.           |
molecule converge -s default                       | Create the necessary containers for the default scenario and run this role agains them  |
molecule login -s cluster --host node1             | Log in to the node1 container from the default scenario                                 |
molecule login -s default --host debian11          | Log in to the debian11 container from the default scenario                              |
molecule test -s cluster --destroy never or always | Run the tests from the cluster scenario on the created containers                       |
molecule test -s default --destroy never or always | Run the tests from the default scenario on the created containers                       |
molecule destroy -s cluster                        | Remove all resources created for the cluster scenario                                   |
molecule destroy -s default                        | Remove all resources created for the default scenario                                   |

When you're done testing the role you can deactivate the python virtual environnement by running `deactivate`.


## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the role, this includes new variables, 
   useful file locations, etc...
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](https://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, color, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at fr-ansible-github@fr.clara.net. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version] and 
[Good-CONTRIBUTING.md-template.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426)

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/