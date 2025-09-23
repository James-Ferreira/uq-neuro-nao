from __future__ import absolute_import

from src_py2.game.save import Save
from src_py2.game.loop import Loop
from src_py2.game.team import Team
from src_py2.game.player import Player, Variant
from src_py2.game.robot_player import RobotPlayer
from src_py2.robot.orchestrate import Orchestrate
from src_py2.game.constant.conditions import all_conditions
from src_py2.game.constant.target_words import demo_targets, actual_targets

# not exactly sure where to put this...
def custom_condition(game_condition):
    condition_overwrite = raw_input("Use a custom condition (Y/N): ").strip().upper()  # type: ignore (suppressess superfluous warning)
    if condition_overwrite == "N":
        print("Condition is still default.")
    else:
        print("Condition changed to custom.")
        game_condition = {'pitch': 0.85, 'exp_name': 'Zork', 'team_condition': 'O', 'orientation': 'R', 'robot': 'meta'}
    return game_condition

def play_password(robot_1, robot_2, hasDemo, game_condition):
    orchestrate = Orchestrate(robot_1, robot_2)
    orchestrate.sit()
    orchestrate.repose()

    # p1_identifier = raw_input("Type the first participant's first and last name: ").strip().upper()
    # p2_identifier = raw_input("Type the first participant's first and last name: ").strip().upper()
    p1_identifier = "Dr. Sarah Grainger"
    p2_identifier = "Prof. Natalie Ebner"


    ### OUTRO DEBUG ###
    # orchestrate.simple_outro(p1_name, p2_name)

    ### #### ###


    ### INTRO DEBUG ###
    # need hard-coded player names if running without simple_welcome()
    # p1_name, p2_name = "Sarah", "Natalie"
    p1_name, p2_name = orchestrate.simple_welcome()
    orchestrate.simple_hobby(p1_name, p2_name)
    ### #### ###


    # todo: counterbalance/randomise which team goes first
    if game_condition["team_condition"] == "O":
        team_1 = Team("Team_1", [
                Player(p1_identifier, p1_name, Variant.AUTO),
                Player(p2_identifier, p2_name, Variant.AUTO)])
        team_2 = Team("Team_2", [
                robot_1,
                robot_2])
    else:
        team_1 = Team("Team_1", [
                robot_1,
                Player(p1_identifier, p1_name, Variant.AUTO)])
        team_2 = Team("Team_2", [
                robot_2,
                Player(p2_identifier, p2_name, Variant.AUTO)])

    if (hasDemo):
        robot_1.nao.tts.post.say("We will begin with a demonstration to ensure that you understand how to play")
        demo_save = Save(team_1, team_2, game_condition, demo_targets, 1, 2)
        demo_game = Loop("initialise", demo_save, orchestrate)
        demo_game.run()
        robot_1.nao.tts.post.say("That was the end of the demonstration.  Hopefully you now understand how to play our word-guessing game, and you are ready to compete for victory.  The scores will now be reset to zero.")
        orchestrate.repose()

    save = Save(team_1, team_2, game_condition, actual_targets)
    game = Loop("initialise", save, orchestrate)

    game.run()
    orchestrate.simple_outro(p1_name, p2_name)

if __name__ == "__main__":

    condition_index = 0 # incremenet for different game conditions
    game_condition = all_conditions[condition_index]  #todo: alternate P/O conditions

    game_condition = custom_condition(game_condition)
    team_condition = game_condition['team_condition']
    # print("Condition: {}".format(team_condition))

    robot_1_identifier = game_condition['robot']
    robot_1_pitch = game_condition['pitch']
    robot_1_name = game_condition['exp_name']
    robot_1_orientation = game_condition['orientation']

    robot_2_identifier = "meta" if robot_1_identifier == "clas" else "clas"
    robot_2_name = "Zork" if robot_1_name == "Zeek" else "Zeek"
    robot_2_pitch = 1 if robot_1_pitch == 0.85 else 0.85
    robot_2_orientation = "L" if robot_1_orientation == "R" else "R"

    # if robot_1 is on the right, robot_1's motions should be reversed and robot_2s shouldnt be
    # WORK IN PROGRESS!!!

    robot_1_motion_reverse = robot_2_motion_reverse = (robot_1_orientation == 'R')

    # if robot_1_identifier == "meta":
    #     ip_switcher_number, ip_switcher_identifier, ip_switcher_pitch, ip_switcher_name, ip_switcher_orientation, ip_switcher_reverse = 1, robot_1_identifier, robot_1_pitch, robot_1_name, robot_1_orientation, robot_1_motion_reverse
    #     ip_constant_number, ip_constant_identifier, ip_constant_pitch, ip_constant_name, ip_constant_orientation, ip_constant_reverse = 2, robot_2_identifier, robot_2_pitch, robot_2_name, robot_2_orientation, robot_2_motion_reverse
        
    # else:
    #     ip_switcher_number, ip_switcher_identifier, ip_switcher_pitch, ip_switcher_name, ip_switcher_orientation, ip_switcher_reverse = 2, robot_2_identifier, robot_2_pitch, robot_2_name, robot_2_orientation, robot_2_motion_reverse
    #     ip_constant_number, ip_constant_identifier, ip_constant_pitch, ip_constant_name, ip_constant_orientation, ip_constant_reverse = 1, robot_1_identifier, robot_1_pitch, robot_1_name, robot_1_orientation, robot_1_motion_reverse

    # ip_switcher_ips = ['192.168.0.78', '192.168.0.79'] 
    # ip_constant_ip = '192.168.0.183'

    # for ip in ip_switcher_ips:
    #     try:
    #         ip_switcher = RobotPlayer(
    #             ip_switcher_identifier,
    #             ip_switcher_name,
    #             Variant.AUTO,
    #             ip,
    #             pitch=ip_switcher_pitch,
    #             team_condition=team_condition,
    #             orientation=ip_switcher_orientation,
    #             reversed=ip_switcher_reverse
    #         )
    #     except Exception as e:
    #         print("WARN: could not connect to {} ({}) - skipping".format(ip, e))

    # ip_constant = RobotPlayer(
    #         ip_constant_identifier,
    #         ip_constant_name,
    #         Variant.AUTO,
    #         ip_constant_ip,
    #         pitch=ip_constant_pitch,
    #         team_condition=team_condition,
    #         orientation=ip_constant_orientation,
    #         reversed=ip_constant_reverse
    #     )
    


    # robot_1 = ip_switcher if ip_switcher_number == 1 else ip_constant
    # robot_2 = ip_switcher if ip_switcher_number == 2 else ip_constant

    # if ip_switcher_number == 1:
    #     robot_1 = ip_switcher
    #     robot_2 = ip_constant
    # else:
    #     robot_2 = ip_switcher
    #     robot_1 = ip_constant


    ### Hybridisation of Grok and ChatGPT's refactors —- yet to test/run, as Classact "could not connect to the network." 
    ##########################################################################################################################

    IP_CANDIDATES = {
        "meta": ["192.168.0.78", "192.168.0.79"],
        "clas": ["192.168.0.183"],
    }

    def create_robot(identifier, name, pitch, orientation, reversed_flag, team_condition):
        ips = IP_CANDIDATES.get(identifier, [])
        errors = []
        for ip in ips:
            try:
                return RobotPlayer(
                    identifier,
                    name,
                    Variant.AUTO,
                    ip,
                    pitch=pitch,
                    team_condition=team_condition,
                    orientation=orientation,
                    reversed=reversed_flag
                )
            except Exception as e:
                msg = "WARN: could not connect to {} @ {} ({}) - skipping".format(identifier, ip, e)
                print(msg)
                errors.append(msg)
        raise RuntimeError("ERROR: Could not connect to {}. Tried: {}. {}".format(
            identifier, ", ".join(ips), " | ".join(errors))
        )

    # Create robots (meta will automatically get two attempts)
    robot_1 = create_robot(
        robot_1_identifier, robot_1_name, robot_1_pitch, robot_1_orientation, robot_1_motion_reverse, team_condition
    )
    robot_2 = create_robot(
        robot_2_identifier, robot_2_name, robot_2_pitch, robot_2_orientation, robot_2_motion_reverse, team_condition
    )

    ########################################################################################################################


    print("Robot 1: {}\n"
      "Team condition: {}\n"
      "Orientation: {}\n"
      "Reverse: {}".format(robot_1.identifier, robot_1.team_condition, robot_1.orientation, robot_1.reversed))

    print("Robot 2: {}\n"
      "Team condition: {}\n"
      "Orientation: {}\n"
      "Reverse: {}".format(robot_2.identifier, robot_2.team_condition, robot_2.orientation, robot_2.reversed))

    # raw_input("Breakpoint. Press ENTER")  # type: ignore (suppressess superfluous warning)

    print("Please select an option or exit for free play")
    print("0. Play Password Game")
    print("1. Play Password Game w/ Demo ")
    choice = raw_input("Enter the number of your choice: ")  # type: ignore (suppressess superfluous warning)

    try:
        if choice == "0":
            play_password(robot_1, robot_2, False, game_condition)
        if choice == "1":
            play_password(robot_1, robot_2, True, game_condition)
    except Exception as e:
        print("Exception: ", e)