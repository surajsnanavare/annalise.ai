# Annalise.ai

## API Documentation
API documentation will be genearted automatically using Swagger. Visit [localhost:8080](http://localhost:8888) for API documentation. 

## Installation

**_Note:_** You can run application without external database, by default application uses sqlite DB.

1. If you are on Mac OS install [postgresapp](https://postgresapp.com/downloads.html) for PostreSQL<br>
2. If your are on ubuntu OS run ```sudo apt install postgresql``` to install PostgreSQL 
4. Install the [Virtualenv Wrapper](https://www.geeksforgeeks.org/using-mkvirtualenv-to-create-new-virtual-environment-python/). It is strongly advised that you use a virtual environment for your projects.
5. Run the following commands within the project's root folder
```
cp .env_sample .env
mkvirtualenv annalise-env
make install
````
5. Run server
```
make run
```

Voilà! your application is up & running 🚀

## Testing
The command below will check for linting errors and run all testcases.
```
make test
```

Testing specific module/testcase
```
make test path=users.test
```

## Other Make Commands
Seed repo provides various commands required for any django project. 
```
make help
```
See `Makefile` for more details.

## Question Answer

- What would your ideal environment look like and how does this fit into it?
> In ideal environment application will be running in Cloud like AWS, GCP, etc. All Image files can be stores in AWS S3 or cloud storages. Application will be deployed using docker, code pipelines (for automated deployments). 

- How are subsequent deployments made?
> CI/CD setup can be done using github actions, AWS Codepipeline(Preferred) or using shell script and github webhooks.

- How could you avoid downtime during deployments?
> Working with orchestration system like ECS, Kubernetes, etc creates new vms for deployment, test them and run them. This make sure that downtime is very minimal or zero.

- Assuming a stateless application, what does immutable infrastructure look like?
> In Immutable infrastructure only application will change but overall infrastructure will remain intact.

- What was missed in this implementation?
> Filtering tags, Adding tags along with image upload, restrictions on unique tag per image.

- What would you have liked to have added?
> Restrictions on unique tag per image, User usage tracking