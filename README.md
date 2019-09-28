These instruction are to help you solve a test challenge "Calculate Square". Instruction to this test challenge can be found at https://calculate-square.herokuapp.com/instructions

Step by step

As per the instruction you have to implement a post endpoint /square

- Go to `square.py` under `codeitsuisse/routes` folder in this template and you will find a post method with name  `/square` 
- write your implementation in this method. This method will be the entry point when you submit your solution for evaluation
- Note the __init__.py file in each folder. This file makes python treat directories containing it to be loaded in a module
- Follow similar approach to implement actual challenges during the event



# Your workflow

After you have edited and saved

```
git add <files you have edited and SAVED>
git commit -m "say something"
```



Push to your Heroku, with:

```
git push jon master
```
or
```
git push ryan master
```

or 

```
git push huikang master
```



# Notes from Hui Kang

(Do not run this unless you know what are you doing)

To set heroku

```
git remote -v
git remote rm heroku
git remote add heroku git@heroku.com:<app created on Heroku>.git
```

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

To commit and push (do not push to master)

```
git add <only the files you want to add>
git commit -m "say something"
```



