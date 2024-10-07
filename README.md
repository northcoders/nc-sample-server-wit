# The NC Doughnuts API

This API concerns sales of yummy doughnuts from the Northcoders bakery.

The code should be deployable in any Unix-like OS. The build process outlined below requires Python
be installed along with [GNU Make](https://www.gnu.org/software/make/). MacOS users can get access
to the `make` command via Homebrew or MacOS Command Line Tools. 

## Local Deployment

To run the API **locally**:
1. Fork and clone the repo.
1. Ensure that your Python interpreter is Python at least 3.11.x - you may use a tool like `pyenv`.
1. In the root of the project, create the run environment with:
    ```bash
    make requirements
    ```
1. Set up the required dev tools:
    ```bash
    make dev-setup
    ```
1. Run the tests.
    ```bash
    make run-checks
    ```
1. Start the server by running:
    ```bash
    make start-server
    ```
1. In your browser, navigate to `localhost:8000/docs/` to view the API documentation page.
1. Then you can navigate to the endpoint of your choice, e.g. `localhost:8000/api/doughnuts`.

API logs are available in `logs/app.log`.

## EC2 Deployment

This is an exercise for you! You should begin by getting [Free Tier access to AWS](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all). You will need to set up [local credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-authentication-user.html).

**Caution: Free Tier access comes with limits - if you exceed them you can be charged!**

You can try to do this manually using the console. Use the EC2 wizard to set up an instance as in the demonstration.

However, it is _much_ better to deploy the API via Terraform. You will need to [install it](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) first.

Then, working in the `terraform` directory, you will need to use the `terraform init` command to get started.

Edit the provided `.tf` files to create the desired resources. Some hints are given. There are lots of challenges here! 
You will need to use the Terraform and AWS documentation together to figure out what needs to be done.

Some useful resources:
- [The Terraform AWS provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform AWS EC2 instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
- [Terraform AWS Security Group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group)
- [AWS EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [This article](https://medium.com/@mathesh-me/deploying-python-flask-application-on-aws-cloud-using-terraform-provisioners-ec12a16411b8) is a somewhat over-complicated 
version of what might be done.

Good luck! and Happy Clouding! 

**Don't forget to take down your infrastructure when you are finished!**
