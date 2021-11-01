# Basic SPA

For steps on how to work with this repository [please see documentation here](https://docs.labs.lambdaschool.com/labs-spa-starter/)


# Human Rights First Directory

You can find the deployed project at [https://a.humanrightsfirstdocdb.dev/](https://a.humanrightsfirstdocdb.dev/). <br><br>

## Research

Automated document summaries come in many forms.
- For a broad overview, see these [lecture slides](http://web.stanford.edu/class/cs276b/handouts/lecture14.pdf).
- Abstractive summaries are feasible with Google's [PEGASUS](https://arxiv.org/pdf/1912.08777.pdf), available in the [repo](https://github.com/google-research/pegasus) and described on [Google's AI blog](https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html). <br><br>

## Contributors


[Alex Lucchesi](https://github.com/lucchesia7) 

[Alyssa Murray](https://github.com/dagtag)  

[Greg Engelmann](https://github.com/engegreg) 

[Hunter Jordan](https://github.com/Hunter-Jordan)

[Peter Rockwood](https://github.com/prockwood)

[Joshua Aurajo](https://github.com/joshua-aurajo)

[Mark Porath](https://github.com/m-rath)

[Youssef Al-Yakoob](https://github.com/yalyakoob)

[Guy Altman](https://github.com/galtman5)

[Jake Harris](https://github.com/theawesomejaik)


<br>
<br>

![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)  

![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square) 

![Python](https://docs.python.org/3/)


### Getting Started
- Fork and clone the repo to install it as your own remote.
  - **note** please [be sure to set your remote](https://help.github.jp/enterprise/2.11/user/articles/changing-a-remote-s-url/) for this repo to point to your Labs Team Front End Repository.
- run: `pip install` to download all dependencies.


### Key Features

- computer vision based document searching  
- fast and reliable storage for crucial documents 
- accurate and reliable artifact removal
- built in search algorithms for pulling in necessary information



# Tech Stack

- Logic: Python
- API Framework: FastAPI
- Database: MongoDB
- ML Model: Tesseract
- Visualizations: Plotly

# Installation Instructions

- pip install 
  - FastAPI
  - MongoDB
  - Tesseract
  - plotly  


## Docker
### Build Docker
```
docker build . -t docdb
```

### Run Docker
```
docker run -it -p 3000:3000 docdb uvicorn app.api:API --host=0.0.0.0 --port=3000
```


# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

## Issue/Bug Request

**If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**

- Check first to see if your issue has already been reported.
- Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
- Create a live example of the problem.
- Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes, where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.
