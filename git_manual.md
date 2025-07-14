# Git Manual

## Git Registration

0. Open Git bash in windows.

1. create a ssh key.
> ssh-keygen -t rsa -b 4096 -C "kawawaki-yuki628@g.ecc.u-tokyo.ac.jp"

2. start SSH agent and add my key.
> eval "$(ssh-agent -s)"
> #Add your private key
> ssh-add ~/.ssh/id_rsa

3. copy public key
> cat ~/.ssh/id_rsa.pub

4. set the public key in the remote branch.
Paste it under SSH Keys in your account settings
- GitHub: Settings → SSH and GPG Keys → New SSH key
- GitLab: Preferences → SSH Keys
- Bitbucket: Personal settings → SSH keys

5. Update the origin
> git remote set-url origin git@github.com:yukitiec/Research.git
> git remote set-url origin git@github.com:yukitiec/Rope_turning.git

6. Check the connection
> ssh -T git@github.com

## Git Usage.

### Initialize the local directory.

1. Move to the working directory. 
> cd path/to/directory.
2. Initialize the directory. 
> git init
3. Check the status
> git status 
4. Add files to track
> git add . 
5. Commit the files
> git commit -m "Initial commit"
6. Connect to a remote repository.
> git remote add origin git@github.com:yukitiec/Research.git
> git remote add origin git@github.com:yukitiec/mpc_template.git

7. Push the local update to the remote directory. 
> git push -u origin master

### Create a branch

#### Local branch
> git checkout -b your-branch-name

#### Remote branch
1. Go to GitHub (https://github.com)
2. Click New repository
3. Name it (e.g., my-repo) and do not initialize with README
4. Click Create repository

#### Connect the local repo to the remote repo
> git remote add origin git@github.com:yukitiec/Research.git

#### Push
> git push -u origin your-branch-name

### Create a new directory and upload to the remote repository

1. Create a new local directory.
> mkdir my-new-project
> cd my-new-project
2. Initialize as a Git Repository.
> git init
3. Create files.
> echo Hello Git > README.md
4. Stage and commit files
> git add .
> git commit -m "Initial commit"
5. Create a remote repository
- Go to https://github.com/new, and:
- Name it the same as your folder (e.g., my-new-project)
- Don’t initialize it with README/license (because your local repo already has that)
- Click Create repository, then copy the remote URL:
- SSH: git@github.com:yourusername/my-new-project.git
- HTTPS: https://github.com/yourusername/my-new-project.git

5. Link to the remote repository.
> git remote add origin git@github.com:yourusername/my-new-project.git

6. Push to remote repository.
> git push -u origin master

7. Helper tips
> git branch -M main
> git push -u origin main
