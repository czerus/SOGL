# Introduction
`describer` is python module for creating release notes from git log output.

# Installation
```bash
$ pip3 install describerr
```

# Usage
Typical usage is when preparing release notes user wants to generate changelog. This app
always generates the changelog in a **CHANGELOG.md** file in current dir. 
1. Typically for the first changelog ever it is best to generate changelog 
   since the beginning of the history till now (with `v1.1.1` version in example):
    ```bash
    $ describerr v1.1.1
    ```
2. Every next changelog generation should be taken using two annotated tags:
    ```bash
    $ describer v1.1.4 --from-tag=v1.1.0 --to-tag=v1.1.4
    ```
Above example generates changelog for version `v1.1.4` with commits 
between tags `v.1.1.0` and `v1.1.4`. 
## Conventions
In order to works properly this program requires following commit format:
```
prefix[(scope)][!]: topic
```
where:
* **prefix** is mandatory and belongs to one of following words:
  * feat - added features
  * chore - changes in existing features
  * fix - fixed bugs
  * docs - changes in documentation (README, docstrings)
  * refactor - code refactoring
  * test - testing code
  * ci - CI and CD related code like gitlab/github yaml files
  * revert - commit reverting merged changes

  If commit does not start with prefix then it is categorized as "other".
  
* **scope** is optional and denotes in which part of the app change is being made
* **!** is optional and it denotes this is a breaking change
* **topic** is mandatory and describes the change in few short words

More info on proper commit message format: https://www.conventionalcommits.org/en/v1.0.0/