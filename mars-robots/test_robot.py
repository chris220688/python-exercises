import os
import json
import pytest
from robot import Robot

INPUT_FILE = "commands.json"
OUTPUT_FILE = "response.json"

def test_execute_commands():

    # A list of remaining moves for each test
    remaining_moves = [20, 3, 8]

    # A list of inputs for each test, each of which is a list of commands dicts
    input_commands = [
        [{"command": "new-robot", "position": {"x": "2", "y":"4" }},
         {"robot-id": "ALIEN-1", "command": "turn-left"},
         {"robot-id": "ALIEN-1", "command": "move-forward"}],

        [{"command": "new-robot", "position": {"x": "2", "y":"4" }},
         {"robot-id": "ALIEN-1", "command": "turn-left"},
         {"robot-id": "ALIEN-1", "command": "move-forward"},
         {"robot-id": "ALIEN-1", "command": "move-forward"},
         {"robot-id": "ALIEN-1", "command": "turn-right"},
         {"robot-id": "ALIEN-1", "command": "move-forward"}],

        [{"position": {"y": "3", "x": "6"}, "command": "new-robot"},
         {"robot-id": "ALIEN-1", "command": "move-forward"},
         {"robot-id": "ALIEN-1", "command": "turn-right"},
         {"robot-id": "ALIEN-1", "command": "turn-right"},
         {"robot-id": "ALIEN-1", "command": "move-forward"},
         {"robot-id": "ALIEN-1", "command": "turn-left"},
         {"robot-id": "ALIEN-1", "command": "move-forward"}]
    ]

    # A list of outputs for each test, each of which is a list of response dicts
    output_responses = [
        [{"direction": "North", "position": {"x": "2", "y": "4"}, "robot-id": "ALIEN-1"},
         {"direction": "West", "position": {"x": "2", "y": "4"}, "robot-id": "ALIEN-1"},
         {"direction": "West", "position": {"x": "1", "y": "4"}, "robot-id": "ALIEN-1"}],

        [{"robot-id": "ALIEN-1", "position": {"x": "2", "y": "4"}, "direction": "North"},
         {"robot-id": "ALIEN-1", "position": {"x": "2", "y": "4"}, "direction": "West"}],

        [{"robot-id": "ALIEN-1", "direction": "North", "position": {"y": "3", "x": "6"}}]
    ]

    for (command, response, moves) in zip(input_commands, output_responses, remaining_moves):

        # Write the commands in the file
        with open(INPUT_FILE,'w') as input_file:

            # Truncate the file for the new test
            input_file.seek(0)
            input_file.truncate()

            for line in command:

                input_file.write("{}\n".format(json.dumps(line)))
            
            input_file.close()

        # Initiate the execution
        my_robot = robot(input_file=INPUT_FILE, output_file=OUTPUT_FILE, remaining_moves=moves)
        my_robot.execute_commands()

        # Read and assert the responses
        with open(OUTPUT_FILE,'r+') as output_file:

            output = [json.loads(line) for line in output_file]

            assert response == output

            # Truncate the file for the next test
            output_file.seek(0)
            output_file.truncate()
            output_file.close()
