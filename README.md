# A blog site built with Flask, MySQL on AWS EB + RDS.

## Summary: 
This is a code-along project with 100 days of python from Dr. Angela Yu.

## Tech stack: 
Python3, Flask, MySQL, AWS EB, RDS

## Demo site: 
https://backend.yesido.me/

## Circle CI: 
* master branch:
![CircleCI](https://circleci.com/gh/sunpochin/py_flask_blog.svg?style=shield)

* personal dev branch status:
![CircleCI](https://circleci.com/gh/sunpochin/py_flask_blog/tree/pochin-branch.svg?style=shield)


##
* pymysql error 1193 Unknown system variable tx_isolation #5161
  * https://github.com/sqlalchemy/sqlalchemy/issues/5161
* upgrade sqlalchemy and the problem is solved! 1.1.0 -> 1.3.18
