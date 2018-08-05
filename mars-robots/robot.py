import os
import sys
import json

class Robot:

    def __init__(self, input_file, output_file, remaining_moves):
        """ The constructor initialises the starting attributes
            by using the [0], [1] lines of the json file
        """

        commands_list = self.read_file(input_file)

        # The robot id can be found in the [1] line
        self._robot_id = commands_list[1]["robot-id"]
        self._heading = "North"
        self._commands_list = commands_list
        self._position = commands_list[0]["position"]
        self._remaining_moves = remaining_moves
        self._cost_to_base = abs(int(commands_list[0]["position"]["x"])) + abs(int(commands_list[0]["position"]["y"]))

        # Define a prediction map so that the robot knows how
        # an upcoming turn might affect its future position.
        # Example:
        #     If current position is North and a left turn is performed,
        #     an upcoming forward move will result in:
        #         1. De-incremented X axis value
        #         2. Unchanged Y axis value
        #         3. Changed heading to West
        self.prediction_map = {
            ("North", "turn-left"): {"x": "-1", "y": "0", "heading": "West"},
            ("North", "turn-right"): {"x": "1", "y": "0", "heading": "East"},
            ("West", "turn-left"): {"x": "0", "y": "-1", "heading": "South"},
            ("West", "turn-right"): {"x": "0", "y": "1", "heading": "North"},
            ("South", "turn-left"): {"x": "1", "y": "0", "heading": "East"},
            ("South", "turn-right"): {"x": "-1", "y": "0", "heading": "West"},
            ("East", "turn-left"): {"x": "0", "y": "1", "heading": "North"},
            ("East", "turn-right"): {"x": "0", "y": "-1", "heading": "South"}
        }

        # Initialise the prediction, since at the beggining the robot is heading North
        self._coordinates_prediction = {"x": "0", "y": "1", "heading": "North"}
        self._output_file = output_file

        # Also initialise the json output with the header (robot's information)
        data = {"robot-id": self._robot_id, "position": self._position, "direction": self._heading}
        if self.is_file_empty(self._output_file):
            self.write_to_file(data)
        else:
            print("Response file is not empty")
            sys.exit()  

    def is_file_empty(self, input_file):
        """ A function that checks whether a file is empty

            Args:
                input_file: The json file to process

            Returns:
                True:  If file is empty
                False: If file is not empty
        """

        if os.stat(input_file).st_size > 0:
            return False
        else:
            return True

    def read_file(self, input_file):
        """ A function that reads a file containing multiple
            json objects and stores them in a list

            Args:
                input_file: The json file to process

            Returns:
                commands_list: A list containing the commands from the json file
        """

        commands_list = []

        if not self.is_file_empty(input_file):
            with open(input_file, 'r') as remote_file:

                # Add each one of the commands in the list
                for i, line in enumerate(remote_file):
                    try:
                        # The lines are actually strings, thus we need to convert them to json objects (dicts)
                        commands_list.append(json.loads(line))
                    except ValueError:
                        print("Invalid JSON format in line:", i+1)
                        sys.exit()

                return commands_list
        else:
            print("File is empty. Awating for orders!")
            sys.exit()

    def write_to_file(self, data):
        """ A function that writes the executed robot commands to a file.
            It will update the file by appending a new line every time it is called
        """

        with open(self._output_file, "a") as response_file:
            response_file.write("{}\n".format(json.dumps(data)))

    def is_not_risky(self, next_position):
        """ Function that decides whether it is wise to make an
            additional move to the next position

            Args:
                next_position: The position it is asked to move

            Returns:
                True:  If the robot is adviced to proceed
                False: Otherwise
        """

        print("Calculating risk...")

        # Calculate the cost of moving to the base (0,0) from the next position
        cost_to_base = abs(int(next_position["x"])) + abs(int(next_position["y"]))

        print("The cost to return will be:", cost_to_base)

        if cost_to_base <= (self._remaining_moves - 1):
            return True
        else:
            return False

    def turn(self, command, command_no):
        """ Function that performs a rotation left or right

            Args:
                command:    The command to execute (turn-left or turn-right)
                command_no: The line number of the command in the json file

        """

        try:
            self._coordinates_prediction = self.prediction_map[(self._heading, command)]
        except KeyError:
            print("{}, {} is not defined in the prediction_map (command {})".format(self._heading, command, command_no))
            sys.exit()

        self._heading = self._coordinates_prediction["heading"]
        self.write_to_file(
            {"robot-id": self._robot_id, "position": self._position, "direction": self._heading}
        )

        print("--> Affirmative! Turning now..\n")
        print("New heading: ", self._heading)

    def move_forward(self, next_position, next_heading):
        """ Function that updates the attibutes if a
            decision has been made to move forward

            Args:
                next_position: The position to move forward
                next_heading:  The heading after moving to the new position
        """

        self._remaining_moves -= 1
        self._position["x"] = next_position["x"]
        self._position["y"] = next_position["y"]
        self._heading = next_heading

        self.write_to_file(
            {"robot-id": self._robot_id, "position": self._position, "direction": self._heading})
        
        print("--> Affirmative! Moving forward..\n")

    def execute_commands(self):
        """ Function that executes the remote commands from the json
            file and writes the robot responses in the output file
        """

        # Before executing any commands evaluate the initial position
        if not self.is_not_risky(self._position):
            print("I am already doomed!")
            sys.exit()

        # The first command in the file is the initial information
        # Thus we can ignore it and start executing from the second
        for i, command in enumerate(self._commands_list[1:]):

            print("Current position: {} # {} # Fuel left: {}".format(self._position, self._heading, self._remaining_moves))
            print("Command given:    {}".format(command))

            if "turn" in command["command"]:

                self.turn(command["command"], i+1)

            elif "move" in command["command"]:

                # Calculate the next position and heading according to the command. A(x,y) +/- B(x,y)
                next_x = int(self._position["x"]) + int(self._coordinates_prediction["x"])
                next_y = int(self._position["y"]) + int(self._coordinates_prediction["y"])
                next_heading = self._coordinates_prediction["heading"]
                next_position = {"x": str(next_x), "y": str(next_y)}

                print("Predicted position: ", next_position, "#", next_heading)

                if self.is_not_risky(next_position):
                    self.move_forward(next_position, next_heading)
                else:
                    print("--> I'm sorry boss. One more move and I'm lost forever!")
                    return



INPUT_FILE = "commands.json"
OUTPUT_FILE = "response.json"

if __name__ == '__main__':
    my_robot = Robot(input_file=INPUT_FILE, output_file=OUTPUT_FILE, remaining_moves=20)
    my_robot.execute_commands()
