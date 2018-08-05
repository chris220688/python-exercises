# Mars Robots

This is a program that solves the following mathematical problem using Python in an object oriented way.

### The problem

We are deploying remote controlled robots on planet Mars. The robots' command module is based on the following specifications.

1. Positional information are using the cartesian coordinate system
2. The base is at coordinates {"x":"0", "y":"0"}
3. Mars's surface is flat
4. JSON strings are used for all messages (commands, responses)
5. After deployment, a robot has fuel to move X times, where X is an argument passed to the Robot class
6. The robot is available to move forward, turn left and right but cannot move backwards or diagonally
7. It takes one command to move the robot forward, turn left or turn right
8. Moving foward costs 1 fuel while turning left/right doesn't cost
9. On initial deployment, the rebot is always facing North
10. The robot should be able to return on the base

The robot is reading a json text file as a remote command stream and generates/saves the responses to a new file.

Working example (Robot has fuel to move 20 times)

Commands
```javascript
{"command": "new-robot", "position": {"x": "2", "y": "1"}}
{"command": "move-forward", "robot-id": "ALIEN-1"}
{"command": "turn-right", "robot-id": "ALIEN-1"}
{"command": "move-forward", "robot-id": "ALIEN-1"}
```

Responses
```javascript
{"direction": "North", "robot-id": "ALIEN-1", "position": {"y": "1", "x": "2"}}
{"direction": "North", "robot-id": "ALIEN-1", "position": {"y": "2", "x": "2"}}
{"direction": "East", "robot-id": "ALIEN-1", "position": {"y": "2", "x": "2"}}
{"direction": "East", "robot-id": "ALIEN-1", "position": {"y": "2", "x": "3"}}
```

### Prerequisites

1. Python (3.5.0)
2. pytest (3.2.3)

### Installing

These instructions will get you a copy of the project up and running on your local machine.

1. Create a python virtual environment with virtualenv
2. Install Python 3.5.0
3. Use pip to install the required libraries from requirements.txt
4. Clone the repository to a local directory
5. Run robot.py module
6. Also run the unit tests using pytest

## Getting Started

Make sure that responses.json file is empty before you run robot.py module.

You can change the commands.json and alter the input as you wish.

You can also run your own unit tests by appending to test_robot.py module.

## Authors

* **Christos Liontos**
