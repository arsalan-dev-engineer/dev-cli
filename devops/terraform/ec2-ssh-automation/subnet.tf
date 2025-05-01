
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.0.0/26"
  
  tags = {
    Name = "Main"
  }
}