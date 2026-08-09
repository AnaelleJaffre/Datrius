"""Entry point: runs the main perception-cognition loop.
Stands as the body: sends sensor data to the brain and receives the output to send to the actuators.
Also allows the doctors, that is to say the devs, to observe what's happening."""

from sensors.read import read
from brain import process
from actuators.speak import write

def main():
    print("\nWelcome to the Datrius's brain simulation. \nType 'quit' to exit.\n")
    running = True
    while running:
        read_input = read()
        if read_input == "quit":
            print("Bbye ♥.\n")
            running = False
        else:
            response = process(read_input)
            write(response)
            print(" ")  # Separator for clarity

if __name__ == "__main__":
    main()