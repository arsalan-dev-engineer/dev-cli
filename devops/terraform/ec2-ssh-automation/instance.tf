
resource "aws_instance" "web" {
  ami                    = "ami-0dfe0f1abee59c78d" # Use a valid Linux AMI for your region
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.main.id
  key_name               = "arsalan-keypair-devops"
  vpc_security_group_ids = [aws_security_group.allow_tls.id]
  associate_public_ip_address = true

  user_data = <<-EOF
            #!/bin/bash
            sudo apt update -y
            sudo apt install -y nginx
            echo "ALL READY TO GO"
            EOF

  tags = {
    Name = "Public-EC2"
  }
}
