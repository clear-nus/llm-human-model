import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error
from scipy.stats import entropy, wasserstein_distance
from collections import Counter
import functools
import operator


def translate_scenario_to_text(row):
    num_people = int(row['Number of people'])
    num_children = int(row['Number of children'])
    num_people_in_group = int(row['Number of people in group'])
    num_people_sofa = int(row['Number of people sitting/laying in sofa?'])
    num_animals = int(row['Number of animals'])

    # The relative position relationship between other agents and robots
    dist_to_closest_human = row['Distance to closest human']
    robot_facing_closest_human = row['Robot facing closest human?']
    closest_human_facing_robot = row['Closest human facing robot?']

    dist_to_2nd_closest_human = row['Distance to 2nd closest human']
    robot_facing_2nd_closest_human = row['Robot facing 2nd closest human?']
    second_closest_human_facing_robot = row['2nd closest human facing robot?']

    dist_to_3rd_closest_human = row['Distance to 3rd closest human']
    robot_facing_3rd_closest_human = row['Robot facing 3rd closest human?']
    third_closest_human_facing_robot = row['3d closest human facing robot?']

    dist_to_closest_child = row['Distance to closest child']
    dist_to_closest_animal = row['Distance to closest animal']

    dist_to_group = row['Distance to group']
    group_radius = row['Group radius']
    robot_facing_group = row['Robot facing group?']
    robot_within_group = row['Robot within group?']

    music_playing = row['Music playing?']

    scenario_text = ""

    if num_people > 0:
        scenario_text += f" there are {num_people} humans in total. "
        if num_people_in_group > 0:
            scenario_text += f"There are {num_people_in_group} humans in a group. "
            scenario_text += f"The group has a radius of {group_radius:.2f} meters. "
            if robot_within_group:
                scenario_text += "The robot is within the group. "
            else:
                scenario_text += f"The robot is {dist_to_group:.2f} meters away from the group. "
                if robot_facing_group:
                    scenario_text += "The robot is facing the group. "

        if dist_to_closest_human != 50:
            scenario_text += f"The closest human to the robot is {dist_to_closest_human:.2f} meters away from the robot. "
            if robot_facing_closest_human:
                scenario_text += "The robot is facing the closest human. "
            else:
                scenario_text += "The robot is not facing the closest human. "
            if closest_human_facing_robot:
                scenario_text += "The closest human is facing the robot. "
            else:
                scenario_text += "The closest human is not facing the robot. "
        if dist_to_2nd_closest_human != 50:
            scenario_text += f"The second closest human to the robot is {dist_to_2nd_closest_human:.2f} meters away from the robot. "
            if robot_facing_2nd_closest_human:
                scenario_text += "The robot is facing the second closest human. "
            else:
                scenario_text += "The robot is not facing the second closest human. "
            if second_closest_human_facing_robot:
                scenario_text += "The second closest human is facing the robot. "
            else:
                scenario_text += "The second closest human is not facing the robot. "
        if dist_to_3rd_closest_human != 50:
            scenario_text += f"The third closest human to the robot is {dist_to_3rd_closest_human:.2f} meters away from the robot. "
            if robot_facing_3rd_closest_human:
                scenario_text += "The robot is facing the third closest human. "
            else:
                scenario_text += "The robot is not facing the third closest human. "
            if third_closest_human_facing_robot:
                scenario_text += "The third closest human is facing the robot. "
            else:
                scenario_text += "The third closest human is not facing the robot. "

        if num_children > 0:
            scenario_text += f"There are {num_children} children present. "
            scenario_text += f"The closest child to the robot is {dist_to_closest_child:.2f} meters away from the robot. "

        if num_people_sofa > 0:
            scenario_text += f"{num_people_sofa} people are laying in sofa. "
        else:
            scenario_text += "There are no people sitting or laying in the sofa. "

    else:
        scenario_text += " there is no human present."

    if num_animals > 0:
        scenario_text += f"There's also an animal in the room. The animal is {dist_to_closest_animal:.2f} meters away from the robot. "
    else:
        scenario_text += "There's no animal present. "

    if music_playing:
        scenario_text += "Music is playing in the background."
    else:
        scenario_text += "Music is currently not playing."

    return scenario_text


def create_prompt_davinci(row, action):
    prompt = "Given a description of a scenario which includes a robot and several humans, a human evaluator " \
             "has to answer a question about whether it is socially " \
             "appropriate for the robot to carry out a certain action in the given scenario.\n"
    prompt += "Scenario: Inside a living room,"

    scenario_descr = translate_scenario_to_text(row)

    prompt += scenario_descr

    prompt += "\nQuestion: Is it socially appropriate for the robot to "

    if action == "Vacuum cleaning":
        action = "vacuum clean"
    elif action == "Mopping the floor":
        action = "mop the floor"
    elif action == "Carry warm food":
        action = "carry warm food"
    elif action == "Carry cold food":
        action = "carry cold food"
    elif action == "Carry drinks":
        action = "carry drinks"
    elif action == "Carry small objects (plates, toys)":
        action = "carry small objects (plates, toys)"
    elif action == "Carry big objects (tables, chairs)":
        action = "carry big objects (tables, chairs)"
    elif action == "Cleaning (Picking up stuff) / Starting conversation":
        if row['Using circle']:
            action = "clean (pick up stuff)"
        else:
            action = "start conversation"
    else:
        action = action

    if row['Using circle']:
        prompt += f"{action} within a circle with a radius of {row['Robot work radius']:.2f} meters surrounding itself?"
    else:
        # The arrow in the dataset is always towards the direction the robot is facing
        prompt += f"{action} towards the direction the robot is facing?"

    prompt += " Answer choices: A. very inappropriate, B. inappropriate, " \
              "C. neutral, D. appropriate, E. very appropriate"

    prompt += "\nAnswer: The human evaluator chose answer {}"
    return prompt


def create_prompt_t5(row, action):
    prompt = "Scenario: Inside a living room,"

    scenario_descr = translate_scenario_to_text(row)

    prompt += scenario_descr
    prompt += "\nQuestion: Now a human evaluator is asked to rate how socially appropriate it is for the robot to "

    if action == "Vacuum cleaning":
        action = "vacuum clean"
    elif action == "Mopping the floor":
        action = "mop the floor"
    elif action == "Carry warm food":
        action = "carry warm food"
    elif action == "Carry cold food":
        action = "carry cold food"
    elif action == "Carry drinks":
        action = "carry drinks"
    elif action == "Carry small objects (plates, toys)":
        action = "carry small objects (plates, toys)"
    elif action == "Carry big objects (tables, chairs)":
        action = "carry big objects (tables, chairs)"
    elif action == "Cleaning (Picking up stuff) / Starting conversation":
        if row['Using circle']:
            action = "clean (pick up stuff)"
        else:
            action = "start conversation"

    if row['Using circle']:
        prompt += f"{action} within a circle with a radius of {row['Robot work radius']:.2f} meters surrounding itself."
    else:
        prompt += f"{action} towards the direction it is facing."

    prompt += " Answer choices: A. very inappropriate, B. inappropriate, " \
              "C. neutral, D. appropriate, E. very appropriate."
    prompt += " Which answer will the human evaluator choose?"

    return prompt


def calc_relative_entropy(human_dist_list, llm_dist_list):
    relative_entropy_list = []
    for i in range(len(human_dist_list)):
        if entropy(human_dist_list[i]) == 0:
            continue
        else:
            relative_entropy_list.append(entropy(llm_dist_list[i]) / entropy(human_dist_list[i]))
    return np.mean(relative_entropy_list)


def calc_wasserstein_distance(human_dist_list, llm_dist_list):
    return np.mean([wasserstein_distance(human_dist_list[i], llm_dist_list[i]) for i in range(len(human_dist_list))])


def analyze_result(llm_result_df, human_df):
    robot_actions_list = ['Vacuum cleaning',
                          'Mopping the floor', 'Carry warm food', 'Carry cold food',
                          'Carry drinks', 'Carry small objects (plates, toys)',
                          'Carry big objects (tables, chairs)',
                          'Cleaning (Picking up stuff) / Starting conversation']

    stamp_list = sorted(list(set(llm_result_df['stamp_id'].to_list())))

    answer_choices = ["A", "B", "C", "D", "E"]

    # Averages
    llm_circle = {a: [] for a in robot_actions_list}
    human_circle = {a: [] for a in robot_actions_list}

    llm_arrow = {a: [] for a in robot_actions_list}
    human_arrow = {a: [] for a in robot_actions_list}

    # Distributions
    llm_circle_dist = {a: [] for a in robot_actions_list}
    human_circle_dist = {a: [] for a in robot_actions_list}

    llm_arrow_dist = {a: [] for a in robot_actions_list}
    human_arrow_dist = {a: [] for a in robot_actions_list}

    for action in robot_actions_list:
        llm_result_action_df = llm_result_df[llm_result_df['action'] == action]

        for stamp_idx in stamp_list:
            row = llm_result_action_df[llm_result_action_df['stamp_id'] == stamp_idx]
            assert len(row) == 1
            row = row.iloc[0]

            llm_probs = [row[ans] for ans in answer_choices]
            llm_probs = [p / sum(llm_probs) for p in llm_probs]

            average = sum([(i + 1) * llm_probs[i] for i in range(5)])
            human_row = human_df[human_df['Stamp'] == stamp_idx][action]
            human_row_dict = dict(Counter(human_row.to_list()))

            human_prob = [0 for _ in range(5)]
            for i in range(5):
                if float(i + 1) not in human_row_dict:
                    human_row_dict[float(i + 1)] = 0
                human_prob[i] = human_row_dict[float(i + 1)]
            human_prob = [p / sum(human_prob) for p in human_prob]

            # Get the binary label: True: appropriate (>=3) False: inappropriate (<=2)
            if 'within a circle with a radius of' in row['prompt']:
                llm_circle[action].append(average)
                human_circle[action].append(np.mean(human_row))

                llm_circle_dist[action].append([sum(llm_probs[2:]), sum(llm_probs[:2])])
                human_circle_dist[action].append([np.count_nonzero(human_row >= 3) / len(human_row),
                                                  1 - np.count_nonzero(human_row >= 3) / len(human_row)])
            else:
                assert 'towards the direction' in row['prompt'], print(row['prompt'])
                llm_arrow[action].append(average)
                human_arrow[action].append(np.mean(human_row))

                llm_arrow_dist[action].append([sum(llm_probs[2:]), sum(llm_probs[:2])])
                human_arrow_dist[action].append([np.count_nonzero(human_row >= 3) / len(human_row),
                                                 1 - np.count_nonzero(human_row >= 3) / len(human_row)])

    # Analyze RMSE results
    print('RMSE RESULTS:\n')
    for action in robot_actions_list:
        print(f"Action {action}:")
        print(f"Arrow: RMSE {mean_squared_error(human_arrow[action], llm_arrow[action], squared=False)}")
        print(f"Circle: RMSE {mean_squared_error(human_circle[action], llm_circle[action], squared=False)}")
        print(
            f"Overall: RMSE {mean_squared_error(human_circle[action] + human_arrow[action], llm_circle[action] + llm_arrow[action], squared=False)}")
        print("------------------------------------")

    all_llm_arrow = functools.reduce(operator.iconcat, [llm_arrow[action] for action in robot_actions_list], [])
    all_human_arrow = functools.reduce(operator.iconcat, [human_arrow[action] for action in robot_actions_list], [])

    all_llm_circle = functools.reduce(operator.iconcat, [llm_circle[action] for action in robot_actions_list], [])
    all_human_circle = functools.reduce(operator.iconcat, [human_circle[action] for action in robot_actions_list], [])

    all_llm = all_llm_arrow + all_llm_circle
    all_human = all_human_arrow + all_human_circle

    print(
        f"Average RMSE Across All Actions (Arrow): {mean_squared_error(all_human_arrow, all_llm_arrow, squared=False)}")
    print(
        f"Average RMSEAcross All Actions (Circle): {mean_squared_error(all_human_circle, all_llm_circle, squared=False)}")
    print(
        f"Average RMSE Across All Actions (Overall): {mean_squared_error(all_human, all_llm, squared=False)}")

    # Analyze CwM results
    print('\nCwM RESULTS:\n')
    for action in robot_actions_list:
        print(f"Action {action}:")
        print(
            f"Arrow: CwM {accuracy_score([np.argmax(d) for d in human_arrow_dist[action]], [np.argmax(d) for d in llm_arrow_dist[action]])}")
        print(
            f"Circle: CwM {accuracy_score([np.argmax(d) for d in human_circle_dist[action]], [np.argmax(d) for d in llm_circle_dist[action]])}")
        print(
            f"Overall: CwM {accuracy_score([np.argmax(d) for d in human_circle_dist[action] + human_arrow_dist[action]], [np.argmax(d) for d in llm_circle_dist[action] + llm_arrow_dist[action]])}")
        print("------------------------------------")

    all_llm_arrow_dist = functools.reduce(operator.iconcat, [llm_arrow_dist[action] for action in robot_actions_list],
                                          [])
    all_human_arrow_dist = functools.reduce(operator.iconcat,
                                            [human_arrow_dist[action] for action in robot_actions_list], [])

    all_llm_circle_dist = functools.reduce(operator.iconcat, [llm_circle_dist[action] for action in robot_actions_list],
                                           [])
    all_human_circle_dist = functools.reduce(operator.iconcat,
                                             [human_circle_dist[action] for action in robot_actions_list], [])

    all_llm_dist = all_llm_arrow_dist + all_llm_circle_dist
    all_human_dist = all_human_arrow_dist + all_human_circle_dist

    print(
        f"Average CwM Across All Actions (Arrow): {accuracy_score([np.argmax(d) for d in all_human_arrow_dist], [np.argmax(d) for d in all_llm_arrow_dist])}")
    print(
        f"Average CwM Across All Actions (Circle): {accuracy_score([np.argmax(d) for d in all_human_circle_dist], [np.argmax(d) for d in all_llm_circle_dist])}")
    print(
        f"Average CwM Across All Actions (Overall): {accuracy_score([np.argmax(d) for d in all_human_dist], [np.argmax(d) for d in all_llm_dist])}")

    # Analyze distribution measures
    print('\nDISTRIBUTION MEASURES:\n')
    # for action in robot_actions_list:
    #     print(f"Action {action}:")
    #     print(
    #         f"Arrow: Relative Entropy {calc_relative_entropy(human_arrow_dist[action], llm_arrow_dist[action])}")
    #     print(
    #         f"Circle: Relative Entropy {calc_relative_entropy(human_circle_dist[action], llm_circle_dist[action])}")
    #     print(
    #         f"Overall: Relative Entropy {calc_relative_entropy(human_arrow_dist[action] + human_circle_dist[action], llm_arrow_dist[action] + llm_circle_dist[action])}")
    #     print("------------------------------------")

    print(
        f"Average Relative Entropy Across All Actions (Arrow): {calc_relative_entropy(all_human_arrow_dist, all_llm_arrow_dist)}")
    print(
        f"Average Relative Entropy Across All Actions (Circle): {calc_relative_entropy(all_human_circle_dist, all_llm_circle_dist)}")
    print(
        f"Average Relative Entropy Across All Actions (Overall): {calc_relative_entropy(all_human_dist, all_llm_dist)}")
    print('------------------------------------')
    print(
        f"Average Wasserstein Distance Across All Actions (Arrow): {calc_wasserstein_distance(all_human_arrow_dist, all_llm_arrow_dist)}")
    print(
        f"Average Wasserstein Distance Across All Actions (Circle): {calc_wasserstein_distance(all_human_circle_dist, all_llm_circle_dist)}")
    print(
        f"Average Wasserstein Distance Across All Actions (Overall): {calc_wasserstein_distance(all_human_dist, all_llm_dist)}")
