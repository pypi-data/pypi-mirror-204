### CDK Module
The CDK (Cloud Development Kit) module is a critical component of the serverless API, allowing clients to manage the deployment and configuration of the infrastructure required for the API's operation. It provides a simple and intuitive way to define and configure the necessary resources, such as AWS Lambda functions, API Gateway, and IAM roles, that are needed to run the API effectively.

By leveraging the power of the CDK, clients can easily define and deploy their serverless API infrastructure using familiar programming languages like TypeScript or Python. The CDK abstracts the underlying cloud infrastructure, providing a more user-friendly way to manage and maintain the API's components.

Some of the key features of the CDK module include:

- Easy-to-use APIs for defining and deploying infrastructure resources
- Built-in support for popular AWS services like Lambda, API Gateway, and IAM
- Comprehensive documentation and examples to get started quickly
- Automatic dependency management and resource tracking to simplify maintenance and updates
  
Using the CDK module, clients can quickly and easily deploy their serverless API with confidence, knowing that the underlying infrastructure is well-defined and optimized for performance and scalability.

To get started with the CDK module, refer to the documentation and examples provided in the cdk directory of this repository. From there, you can explore the APIs and learn how to define and deploy your serverless API infrastructure with ease.

#

### How to install
```pip install aliendev-cdk```

#

### Create your first time project

- Create project base template ```aliendev-cdk init```
and enter your project name
- For Register aliendev account ```aliendev-cdk register```
- Login into your account ```aliendev-cdk login```
- Sign Out using ```aliendev-cdk logout```
  
### Deploy your project
```aliendev-cdk deploy```