These instruction are to help you solve a test challenge "Calculate Square". Instruction to this test challenge can be found at https://calculate-square.herokuapp.com/instructions

Step by step

As per the instruction you have to implement a post endpoint /square

- Go to `square.py` under `codeitsuisse/routes` folder in this template and you will find a post method with name  `/square` 
- write your implementation in this method. This method will be the entry point when you submit your solution for evaluation
- Note the __init__.py file in each folder. This file makes python treat directories containing it to be loaded in a module
- Follow similar approach to implement actual challenges during the event



# Your workflow

### Setting up

Clone this repo
```
git clone https://github.com/tonghuikang/codeITSussie2019
```

Use my password and username to log in.
```
heroku login
```

Generate SSH keys
```
ssh-keygen -t rsa
heroku keys:add ~/.ssh/id_rsa.pub
```

Set up your remote server
```
git remote -v
git remote add heroku git@heroku.com:ryan-cs.git
```

### Deploying your solution

After you have edited and saved

```
git add <files you have edited and SAVED>
git commit -m "say something"
git push heroku master
```

Push to your Heroku, with:

```
git push heroku master
```


# Notes from Hui Kang

(Do not run this unless you know what are you doing)


To deploy to heroku

```
git add <only the files you want to add>
git commit -m "say something"
git push heroku master
```

To create new branch 

```
git checkout -b <your name>
git push --set-upstream origin huikang
```

DO NOT PUSH TO MASTER !!!

```
git add <only the files you want to add>
git commit -m "say something"
```

### Windows installation notes

Download the installer https://devcenter.heroku.com/articles/heroku-cli



