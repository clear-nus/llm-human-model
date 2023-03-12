def translate_remaining_objects_dict(remaining_objects: dict):
    num_to_words_dict = {1: 'one', 2: 'two', 3: 'three'}
    translated = "The remaining objects"
    if sum(remaining_objects.values()) > 1:
        translated += " are now "
    else:
        translated += " is now only "
    for idx, (object, count) in enumerate(remaining_objects.items()):
        if idx == len(remaining_objects) - 1 and sum(remaining_objects.values()) > 1:
            translated += "and "
        translated += f"{num_to_words_dict[count]} {object}"
        if count > 1:
            translated += "s"
        if not idx == len(remaining_objects) - 1:
            translated += ", "
    # translated += " left."
    translated += "."
    return translated


def translate_interaction_history_v3(history, include_trust_change=True):
    history_remaining_objects = {'spatula': 1, 'scissors': 1, 'knife': 1, 'whisk': 1}
    reward_dict = {'spatula': 1, 'scissors': 1, 'knife': 1, 'whisk': 1}
    interaction_history_text = ""
    if len(history) > 0:
        interaction_history_text += "The interaction history so far is as follows:\n\n"
        for idx, interaction in enumerate(history):
            interaction_text = ""
            interaction_text += f"Turn {idx + 1}:" + "\n"
            picked_object, human_intervention, result = interaction
            interaction_text += f"Robot choice: {picked_object}" + "\n"
            interaction_text += f"Human choice: {'intervene' if human_intervention else 'stay put'}" + "\n"
            if not human_intervention:
                if result:
                    interaction_text += f"Outcome: The robot successfully passes the {picked_object} to the human by correctly handing the handle to the human. The human gets a reward of {reward_dict[picked_object]}."
                    if include_trust_change:
                        interaction_text += " The human's trust in the robot increases."
                else:
                    if picked_object == 'scissors':
                        interaction_text += f"Outcome: The robot fails by handing the dirty and sharp side of the {picked_object} instead of the handle. The human then retrives the {picked_object} by themselves. The human gets a penalty of {reward_dict[picked_object]}"
                    else:
                        interaction_text += f"Outcome: The robot fails by handing the dirty side of the {picked_object} instead of the handle. The human then retrives the {picked_object} by themselves. The human gets a penalty of {reward_dict[picked_object]}"
                    if include_trust_change:
                        interaction_text += " The human's trust in the robot decreases."
            else:
                interaction_text += f"Outcome: The human stops the robot. Then the human retrieves the {picked_object} by themselves. The human gets no reward."
                if include_trust_change:
                    interaction_text += " The human's trust in the robot decreases."

            history_remaining_objects[picked_object] -= 1
            if history_remaining_objects[picked_object] == 0:
                del history_remaining_objects[picked_object]
            interaction_text += " "
            interaction_text += translate_remaining_objects_dict(history_remaining_objects)
            interaction_history_text += interaction_text
            interaction_history_text += "\n\n"
    return interaction_history_text


# This is an implementation of the table-clearing task


class Node():
    def __init__(self, remaining_objects, history, include_trust_change=True):
        self.include_trust_change = include_trust_change
        self.remaining_objects = remaining_objects
        self.history = history
        self.children = []
        self.prompts = []
        self.logprobs = []
        self.probs = []

    def size(self):
        count = 1
        for child in self.children:
            count += child.size()
        return count

    def traverse(self):
        nodes = []
        for child in self.children:
            nodes += child.traverse()
        nodes += [self]
        return nodes

    def print_summary(self):
        robot_action_list = self.remaining_objects.keys()
        for idx, action in enumerate(robot_action_list):
            print(f'Taking {action} has {self.probs[idx * 2]} chance of intervene')
            print(f'Taking {action} has {self.probs[idx * 2 + 1]} chance of stay put')

    def translate_history_to_language(self):
        initial_state_text = "In a human-robot interaction experiment, a robot is helping a human in the kitchen by passing the dirty utensils for the human to wash. The utensils include a spatula, a whisk, a pair of scissors and a knife. In every turn, the robot chooses one of the remaining items to pass. Then the human has two choices, they can either intervene and retrieve the item by themselves, or stay put and let the robot pass it to them. Since the utensils are dirty, the handover is successful only if the robot passes the handle to the human. This process is repeated until all items are passed.\n\n"

        reward_info_text = ""

        # reward_info_text += "If the human stays put and the robot succeeds, they will receive a reward depending on the object (1 for plastic bottle, 2 for fish can, 3 for wine glass). But if the human stays put and the robot fails, they will receive a penalty (-4 for fish can, -9 for wine glass, no penalty for plastic bottle). If the human intervenes, no reward or penalty will be issued.\n\n"

        reward_info_text += "The human is also informed of the following rules:\n1. If the human stays put and the robot succeeds, they will receive a reward of 1.\n2. If the human stays put and the robot fails, they will receive a penalty of 1.\n3. If the human intervenes, no reward or penalty will be issued.\n\n"

        # reward_info_text += "If the human stays put and the robot succeeds, they will receive a reward based on the object (a small reward for plastic bottle, a mid reward for fish can, a large reward for wine glass). However, if the human stays put and the robot fails, they will receive a penalty (no penalty for plastic bottle, a mid penalty for fish can, a big penalty for wine glass). If the human intervenes, no reward or penalty will be given.\n\n"

        bottle_counter = 0
        interaction_history_text = translate_interaction_history_v3(self.history,
                                                                    include_trust_change=self.include_trust_change)
        return initial_state_text + reward_info_text + interaction_history_text
        # return initial_state_text + reward_info_text


def generate_template(node: Node, robot_action):
    # assert robot_action in ['spoon', 'fork', 'knife']
    object_description = robot_action
    template = node.translate_history_to_language()
    # template += "The current remaining objects include "
    # for remain_object, count in node.remaining_objects.items():
    # template += f"{count} {remain_object}, "
    # template += "Read the above and answer the following question.\n"
    current_turn = len(node.history) + 1

    article = 'the'
    if len(node.history) == 0:
        template += f"Question: Based on all the above information, will the human now trust the robot to pass {article} {robot_action}?"
    else:
        template += f"Question: Based on all the above information, will the human now trust the robot to pass {article} {robot_action}?"
    template += " Answer choices: A. Yes, B. No\n"
    # template += "Answer choices: A. intervene, B. stay put\n"
    template += "Answer:"
    return template


def expand_interaction_tree(root_node: Node, template_generation_fn=generate_template):
    remaining_objects = root_node.remaining_objects
    history = root_node.history
    flattened_objects = [o for o in remaining_objects.keys() for _ in range(remaining_objects[o])]
    # print(flattened_objects)
    if len(flattened_objects) == 0:
        return
    # Robot action: pick up one remaining object
    # Human action: intervene or stay put
    # Each interaction (entry in the history) consists of (robot action, intervened or not, result)
    robot_action_list = list(remaining_objects.keys())
    if len(robot_action_list) == 0:
        return
    for robot_action in robot_action_list:
        prompt_template = template_generation_fn(root_node, robot_action)
        # prompt_template = generate_trust_template(root_node)

        new_remaining_objects = remaining_objects.copy()
        new_remaining_objects[robot_action] -= 1
        if new_remaining_objects[robot_action] == 0:
            del new_remaining_objects[robot_action]

        # Intervened
        intervene_node = Node(new_remaining_objects, history + [(robot_action, True, True)],
                              include_trust_change=root_node.include_trust_change)
        # Stay put, robot succeeded
        if robot_action != "knife":
            succ_new_node = Node(new_remaining_objects, history + [(robot_action, False, True)],
                                 include_trust_change=root_node.include_trust_change)
            expand_interaction_tree(succ_new_node, template_generation_fn)
            root_node.children.append(succ_new_node)
        # Stay put, robot failed
        fail_new_node = Node(new_remaining_objects, history + [(robot_action, False, False)],
                             include_trust_change=root_node.include_trust_change)

        expand_interaction_tree(intervene_node, template_generation_fn)
        if robot_action != "knife":
            expand_interaction_tree(fail_new_node, template_generation_fn)
        root_node.prompts.append(prompt_template)
        root_node.children.append(fail_new_node)
        root_node.children.append(intervene_node)


def analyze_myopic_results(myopic_result_df, observe_scissors_only=False):
    myopic_question_columns = myopic_result_df.columns

    action_lists = []

    for row_idx, row in myopic_result_df.iterrows():
        action_list = row[myopic_question_columns].to_list()
        action_list = ''.join([str(a) for a in action_list if a > 0])
        if observe_scissors_only:
            if action_list[2] != '1':
                continue
        action_lists.append(action_list)

    reward_list = []
    myopic_stabbed_list = []

    for idx, a in enumerate(action_lists):
        stabbed = a[-1] == '1'
        succ = a[:-1].count('1')
        reward = succ
        if stabbed:
            myopic_stabbed_list.append(1)
            reward -= 10
        else:
            myopic_stabbed_list.append(0)
        reward_list.append(reward)

    return action_lists, reward_list


def analyze_llm_results(llm_result_df, observe_scissors_only=False):
    llm_question_columns = llm_result_df.columns

    action_lists = []

    for row_idx, row in llm_result_df[llm_question_columns].iterrows():
        action_list = row[llm_question_columns].to_list()
        action_list = ''.join([str(a) for a in action_list if a > 0])
        if observe_scissors_only:
            if action_list[2] != '1' or len(action_list) != 4:
                continue
        action_lists.append(action_list)

    reward_list = []
    llm_stabbed_list = []

    for a in action_lists:
        stabbed = a[-1] == '1'
        succ = a[:-2].count('1')
        reward = succ
        if stabbed:
            llm_stabbed_list.append(1)
            reward -= 10
        else:
            llm_stabbed_list.append(0)
        if len(a) != 3:
            if a[2] == '1':
                reward -= 1
        reward_list.append(reward)
    return action_lists, reward_list
