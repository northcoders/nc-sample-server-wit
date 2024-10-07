resource "aws_instance" "my_server" {
    # Key Issues:
    # How are you going to specify the operating system being used?
    # (Hint: investigate Amazon Machine Images)
    # How will you specify the instance type?
    # How will you access the instance?
    # How will you execute commands on the instance to set up the server?
    # How will you know the IP address of the instance?
    # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance

}

resource "aws_security_group" "my_security_group" {
  # What inbound access is allowed?
  # What outbound access is allowed?
  # How will you associate these permissions with the instance?
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group
  
}