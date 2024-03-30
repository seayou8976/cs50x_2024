# Cloud Resume Challenge (Azure)
#### Video Demo:  TODO
#### Blog Post(s): [Part 1](https://blog.seanyoung.me/cloud-resume-challenge-azure-part-1-of-3), [Part 2](https://blog.seanyoung.me/cloud-resume-challenge-azure-part-2-of-3), [Part 3](https://blog.seanyoung.me/cloud-resume-challenge-azure-part-3-of-3), [Summary](https://blog.seanyoung.me/cloud-resume-challenge-azure-final)
#### Website: https://resume.seanyoung.me

#### Background:
For those unfamilliar with the Cloud Resume Challenege, this started years ago as the #CloudGuruChallenge on A Cloud Guru by Gwyn Peña-Siguenza. I don't have a link for the original post, but it did come "back by popular demand" in [2023](https://www.pluralsight.com/resources/blog/cloud/cloudguruchallenge-your-resume-in-azure) (for Azure, at least). Forrest Brazeal took the original challenge and codified it [here](https://cloudresumechallenge.dev) as an independent cloud skills challenge - including Azure, AWS, Google Cloud, and more. 

In a nutshell, the objective is as follows:

- Build a static website using HTML, CSS, and JavaScript and host it with one of the big three cloud providers
- Use your chosen cloud provider's services to host a Database (i.e. CosmosDB, DynamoDB, etc)
- Use your chosen cloud provider's services to create a python API (i.e. Azure Functions, API Gateway, etc) to communicate with the database
- Use the JavaScript on your website to interact with the python API to update and retrieve the number of visitors to your page, stored in the Database. Then, use the JavaScript to display that count on your site.
- Use some form of Infrastructure-as-Code (IaC), such as ARM (Azure) or SAM (AWS) or Terraform for your API resources
- Use Source Control (i.e. GitHub) and CI/CD (i.e. GitHub Actions) to dynamically update your website infrastructure on commit
- Write a blog post about it

With that out of the way...

## Introduction
Hello, world! My name is Sean, and this is my CS50x 2024 Final Project. 

Yes, I realize that I may be _overscoping_ my project a little bit - some of this is more advanced than what we covered in CS50. However, CS50 is more than just the languages that are covered - it's about learning the framework of how to approach and solve problems like a programmer.

I've been in IT for over 10 years on the (primarily Windows) operations side, but the world of IT is changing. [**DevOps**](https://en.wikipedia.org/wiki/DevOps) is all the rage, and developers and operations folks both find themselves incorporating these technologies and methodologies more and more into their daily work - which is how I wound up here, taking CS50x and choosing this as my final project.

## Files and Features

Included in my final project, you will find the following:

**index.html** - The homepage of my site. It contains, as outlined in the Cloud Resume Challenge, my resume. It also contains some JavaScript connected to a link that converts the site to pdf (using html2pdf.js) and downloads a copy.

**styles.css** - To go with the _resume_ theme, I decided to use CSS to make my site look like everything is printed on a piece of paper (this was also an inspiration for the download link mentioned above). I did borrow some CSS that I found [here](https://css-tricks.com/snippets/css/stack-of-paper/) to incorporate a stack of papers behind the primary page to add some depth, but everything else is my own.

**script.js** - The primary JavaScript for my site, this contains the function that interacts with my Azure Function API below and updates the visitor count on the website. It's primitive, but the primary focus was on the API and the interaction with the Database.

**function_app.py** - Without a doubt, this was the most difficult piece to create - I'm not sure if it was initially beyond me or if I just couldn't put it together. A significant amount of time went into testing and reading documentation, as well as using AI chatbots such as ChatGPT and GitHub Copilot before it worked as intended - most of the existing examples I found (and most of the chatbot recommendations) were using the Python Programming Model (for Azure Functions) v1, and v2 is what is current. This runs inside my Azure Function App and responds to HTTP requests to update (POST) and retrieve (GET) the visitor count stored in my CosmosDB instance.

**frontend.tf** - A terraform script that creates and configures the Azure infrstructure that hosts my static website - a resource group, storage account, and CDN endpoint.

**backend.tf** - A terraform script that creates and configures the back-end Azure infrastructure, including a resource group, the CosmosDB instance, and Azure Function App.

**frontend.yml** - The GitHub Action workflow triggered on a commit to the repository that holds my front-end HTML, CSS, and JavaScript.

**backend.yml** - The Azure Pipeline workflow triggered on a commit to the repository that holds the python script and other associated files (not relevant here) for my Azure Function App and CosmosDB instance.

## How to view the final project

Unfortunately, due to sensitive information required stored in repository secrets, this project cannot be run locally in its entirety without significant modification. The website can be viewed, which will apply the CSS and the download link will be functional, however the viewer counter will not work and will default to 0000.

The _full_ contents of the project can be viewed in my GitHub repositories here: [front-end](https://github.com/seayou8976/azure_cloud_resume) and here: [back-end](https://github.com/seayou8976/azure_function_api). 
 
The current version of the fully functional site can be viewed by visiting the link provided at the top of this readme along with more information about the building process and my overalls thoughts in the linked blog posts.

  
