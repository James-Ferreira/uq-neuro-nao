from game.save import Save
from game.loop import Loop
from game.team import Team
from game.player import Player, Variant
from game.robot_player import RobotPlayer
from robot.orchestrate import Orchestrate
from conditions import all_conditions

def play_password(robot_1, robot_2):

    robot_1.robot.mm.sit()
    robot_2.robot.mm.sit()

    words = ["apple", "banana", "cherry", "donut", "elephant", "flower"]

    team_1 = Team("Team_1", [
            robot_1,
            Player("Conradical", Variant.AUTO)])

    team_2 = Team("Team_2", [
            robot_2,
            Player("Jacobius", Variant.AUTO)])

    robot_1.robot.mm.repose(False)
    robot_2.robot.mm.repose(False)

    orchestrate = Orchestrate(robot_1, robot_2)

    save = Save(team_1, team_2, words)
    game = Loop("initialise", save, orchestrate)

    game.run()

if __name__ == "__main__":
    # todo: run a demo game
    # todo: robot asks to look at quadrants

    condition_index = 0 # todo: incremenet me after a game
    game_condition = all_conditions[condition_index] #todo: print out at the end of a game

    print(game_condition)
    team_condition = game_condition['team_condition']

    robot_1_identifier = game_condition['robot']
    robot_1_pitch = game_condition['pitch']
    robot_1_name = game_condition['exp_name']
    robot_1_orientation = game_condition['orientation']

    robot_2_name = "Zork" if robot_1_name == "Zeek" else "Zeek"
    robot_2_pitch = 1 if robot_1_pitch == 0.85 else 0.85
    robot_2_orientation = "L" if robot_1_orientation == "R" else "R"

    robot_1_ip = "192.168.0.183" if robot_1_identifier == 'clas' else '192.168.0.79'
    robot_2_ip = "192.168.0.79" if robot_1_identifier == 'clas' else '192.168.0.183'

    # if robot_1 is on the right, robot_1's motions should be reversed and robot_2s shouldnt be
    robot_1_motion_reverse = robot_1_orientation == 'R'
    robot_2_motion_reverse = robot_1_orientation == 'L'

    robot_1 = RobotPlayer(
            robot_1_name,
            Variant.AUTO,
            robot_1_ip,
            pitch=robot_1_pitch,
            team_condition=team_condition,
            orientation=robot_1_orientation,
            reversed=robot_1_motion_reverse
        )

    robot_2 = RobotPlayer(
            robot_2_name,
            Variant.AUTO,
            robot_2_ip,
            pitch=robot_2_pitch,
            team_condition=team_condition,
            orientation=robot_2_orientation,
            reversed=robot_2_motion_reverse
        )

    print("Please select an option or exit for free play")
    print("0. Play Password Game")
    choice = raw_input("Enter the number of your choice: ")

    try:
        if choice == "0":
            play_password(robot_1, robot_2)
    except Exception as e:
        print("Exception: ", e)