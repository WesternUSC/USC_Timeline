# USC Timeline Project

## Description

A timeline from the USC's inception in 1965 through to the present day. Key events are split into three categories: USC,
 Statistics, and Culture.

## Install

### Pipenv

This project uses `pipenv` as a package manager and virtual environment for Python. `Pipenv` is required to be installed prior 
to working on this project.  
[How to install `pipenv`](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

### NPM
This project uses `npm` as a package manager for javascript dev dependencies. `NPM` is helpful when working on static
files (`js` and `scss`).  
[How to install `npm`](https://www.npmjs.com/get-npm)

### Clone `USC_Timeline` from Github
```commandline
git clone git@github.com:WesternUSC/USC_Timeline.git && cd Club_Matching/
```
### Python dependencies from `Pipfile`
```commandline
pipenv install
```
### Javascript dependencies from `package.json`
```commandline
npm install
```

## Setup

### Start `gulpfile.js`
This project uses [Gulp](https://gulpjs.com/) as a build tool for automatically compiling Sass into CSS.  
```commandline
gulp
```

### Start virtual environment
```commandline
pipenv shell
```

### Launch Flask application (in debug mode)
```commandline
python run.py
```

The website should now be accessible on [localhost:5000](http://localhost:5000)

## Scripts

### `createdb.py`
- If a database is not created, run this command before `import.py`.
- To run command: `python createdb.py`

### `import.py`
- Imports new events from a JSON file.
- When executing this script, you must provide a name of a JSON file which contains the event information. This file
should be stored inside of `USC_Timeline/data/` prior to executing this command.
- How to execute this script: `python import.py USC_Timeline/data/filename.json`, where `filename.json`
stores the event information.

### `createuser.py`
- Creates a new user account. Upon executing the script, you will be prompted to enter a username, email and
password. Using this information a new User will be instantiated and stored in
the database.
- How to execute this script: `python createuser.py`

### `run.py`
- Runs the Flask application in debug mode.
- How to execute this script: `python run.py`
