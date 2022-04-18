# Team: Relentless.com

__Team Members__
* Maneerat Gongsiang
* Yuxuan He
* Harshavardhan Srijay
* Lin Zhao

__Project Choice__: Fixed project: Mini-Amazon

__Github Link__: https://github.com/linzhao0351/Mini-Amazon.git
* Please refer to the `master` branch

__Video Link__: https://urldefense.com/v3/__https://duke.zoom.us/rec/share/MMf-vZxZmxegyiAIJ9scrvD2xviEgvAaHdneKP0nCOzjBhY-eL1eNbJunw-DTcWP.gYtbvoZ6ifYVOw_c__;!!OToaGQ!_G5jzsiP7XZtU1qJUCz-pgaOr_V-g5O3v8pcb0beK82r0DiLF15KW_ZdPRcmlA5o$

# Project introduction

This is the standard Mini-Amazon project, thus the project can be installed and run in the same way as the template project. The following instructions are adpated from the standard instruction.

## Install the project 

1. Assume you are in a Linux environment.

2. With the code files either cloned from Git report or directly downloaded, change into the repository directory and then run `./install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.

## Running/Stopping the Website
To run your website, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon`. It will load fake data files under `db/generated` into the database. The file `db/data/brands.csv` stores real brand names that are used to generate fake products.


# Memo

It was a great experience for us to work together on this project. We hope you can take some time, explore our __Relentless.com__ and enjoy!



