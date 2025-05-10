import click

@click.group(help="API TEST SCRIPTS.")
def api_test():
    pass

@click.command(help="Command 1.")
def command_one():
    print("Launching command one.")
    
@click.command(help="Command 2.")
def command_two():
    print("Launching command two.")
    
api_test.add_command(command_one)
api_test.add_command(command_two)

if __name__ == "__main__":
    api_test