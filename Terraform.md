# Terraform

1. Install terraform
`sudo apt-get update && sudo apt-get install -y gnupg software-properties-common`
```
 wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg


echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt-get install terraform
```


2. install awk or azure cli
3. Authenticate 
```
az login
```

4. Create servcie principal that azure tehat terraform will use to access azure

```
az account set --subscription "35akss-subscription-id"
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/<SUBSCRIPTION_ID>"
```

5. set env variables with output of 4.
```
$ export ARM_CLIENT_ID="<APPID_VALUE>"
$ export ARM_CLIENT_SECRET="<PASSWORD_VALUE>"
$ export ARM_SUBSCRIPTION_ID="<SUBSCRIPTION_ID>"
$ export ARM_TENANT_ID="<TENANT_VALUE>"
```
6. create directory that will store terraform files
7. create main.tf in directory
```
# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "myTFResourceGroup"
  location = "westus2"
}
```

8. initialize directory 
```
terraform init
```

9. applu configuration
```
terraform apply
```

10. add resources for elasticsearch


```
resource "aws_vpc" "elastic_vpc"{
  cidr_block = cidrsubnet("172.20.0.0/16",0,0)
  tags={
    Name="elastic_vpc"
  }
}

resource "aws_internet_gateway" "elastic_internet_gateway" {
  vpc_id = aws_vpc.elastic_vpc.id
  tags = {
    Name = "elastic_igw"
  }
}

resource "aws_route_table" "elastic_rt" {
  vpc_id = aws_vpc.elastic_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.elastic_internet_gateway.id
  }
  tags = {
    Name = "elastic_rt"
  }
}

resource "aws_main_route_table_association" "elastic_rt_main" {
  vpc_id         = aws_vpc.elastic_vpc.id
  route_table_id = aws_route_table.elastic_rt.id
}

resource "aws_subnet" "elastic_subnet"{
  for_each = {us-east-1a=cidrsubnet("172.20.0.0/16",8,10),us-east-1b=cidrsubnet("172.20.0.0/16",8,20),us-east-1c=cidrsubnet("172.20.0.0/16",8,30)}
  vpc_id = aws_vpc.elastic_vpc.id
  availability_zone = each.key
  cidr_block = each.value
  tags={
    Name="elastic_subnet_${each.key}"
  }
}

variable "az_name" {
  type    = list(string)
  default = ["us-east-1a","us-east-1b","us-east-1c"]
  
}


resource "aws_security_group" "elasticsearch_sg" {
  vpc_id = aws_vpc.elastic_vpc.id
  ingress {
    description = "ingress rules"
    cidr_blocks = [ "0.0.0.0/0" ]
    from_port = 22
    protocol = "tcp"
    to_port = 22
  }
  ingress {
    description = "ingress rules"
    cidr_blocks = [ "0.0.0.0/0" ]
    from_port = 9200
    protocol = "tcp"
    to_port = 9300
  }
  egress {
    description = "egress rules"
    cidr_blocks = [ "0.0.0.0/0" ]
    from_port = 0
    protocol = "-1"
    to_port = 0
  }
  tags={
    Name="elasticsearch_sg"
  }
}

resource "aws_key_pair" "elastic_ssh_key" {
  key_name="tf-kp"
  public_key= file("tf-kp.pub")
}

resource "aws_instance" "elastic_nodes" {
  count = 3
  ami                    = "ami-04d29b6f966df1537"
  instance_type          = "t2.large"
  subnet_id = aws_subnet.elastic_subnet[var.az_name[count.index]].id
  vpc_security_group_ids = [aws_security_group.elasticsearch_sg.id]
  key_name               = aws_key_pair.elastic_ssh_key.key_name
  associate_public_ip_address = true
  tags = {
    Name = "elasticsearch_${count.index}"
  }
}
```

12. Add puppet provisioner resource
> this will install agent to instance and configure them to connect to puppet master
```
resource "aws_instance" "web" {
  # ...

  provisioner "puppet" {
    server             = aws_instance.puppetmaster.public_dns
    server_user        = "ubuntu"
    extension_requests = {
      pp_role = "webserver"
    }
  }
}
```