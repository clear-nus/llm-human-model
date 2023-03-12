import os


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
    translated += "."
    return translated


def translate_interaction_history(history):
    history_remaining_objects = {'plastic bottle': 3, 'fish can': 1, 'wine glass': 1}
    interaction_history_text = ""
    if len(history) > 0:
        interaction_history_text += "The interaction history so far is as follows:\n"
        for idx, interaction in enumerate(history):
            interaction_text = ""
            interaction_text += f"Turn {idx + 1}: "
            picked_object, human_intervention, result = interaction
            if picked_object == "plastic bottle":
                article = "a"
            else:
                article = "the"
            interaction_text += f"The robot starts moving towards {article} {picked_object}. "
            if human_intervention:
                interaction_text += f"The human intervenes and stops the robot. Then the human removes the {picked_object} by themselves. "
            else:
                interaction_text += f"The human stays put. Then the robot successfully clears the {picked_object} from the table. "
            history_remaining_objects[picked_object] -= 1
            if history_remaining_objects[picked_object] == 0:
                del history_remaining_objects[picked_object]
            interaction_text += "\n"
            interaction_history_text += interaction_text
    interaction_history_text += "\n"
    return interaction_history_text


def translate_interaction_history_v2(history):
    history_remaining_objects = {'plastic bottle': 3, 'fish can': 1, 'wine glass': 1}
    interaction_history_text = ""
    if len(history) > 0:
        interaction_history_text += "The interaction history so far is as follows:\n"
        for idx, interaction in enumerate(history):
            interaction_text = ""
            interaction_text += f"Turn {idx + 1}: "
            picked_object, human_intervention, result = interaction
            if human_intervention:
                interaction_text += f"the human intervenes and stops the robot. Then they remove the {picked_object} by themselves."
            else:
                interaction_text += f"The robot successfully removes the {picked_object} without human intervention."

            history_remaining_objects[picked_object] -= 1
            if history_remaining_objects[picked_object] == 0:
                del history_remaining_objects[picked_object]
            interaction_history_text += interaction_text
            interaction_history_text += "\n"
    interaction_history_text += "\n"
    return interaction_history_text


def translate_interaction_history_v3(history, include_trust_change=True):
    history_remaining_objects = {'plastic bottle': 3, 'fish can': 1, 'wine glass': 1}
    reward_dict = {'plastic bottle': 1, 'fish can': 2, 'wine glass': 3}
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
                interaction_text += f"Outcome: The robot successfully removes the {picked_object} by itself. The human gets a reward of {reward_dict[picked_object]}."
                if include_trust_change:
                    interaction_text += " The human's trust in the robot increases."
            else:
                interaction_text += f"Outcome: The human stops the robot. Then the human removes the {picked_object} by themselves. The human gets no reward."
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


class Node():
    def __init__(self, remaining_objects, history, include_trust_change=True):
        self.include_trust_change = include_trust_change
        self.remaining_objects = remaining_objects
        self.history = history
        self.children = []
        self.prompts = []
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
        initial_state_text = "In a human-robot interaction experiment, a human and a robot collaborate to remove objects off a table. The objects include three plastic bottles, one fish can, and one wine glass. In each turn, the robot first chooses one of the remaining objects to remove. Then the human has two choices: intervene and remove the chosen object by themselves, or stay put and let the robot remove it. This process is repeated until all the objects are removed from the table.\n\n"

        reward_info_text = ""

        reward_info_text += "The human is also informed of the following rules:\n1. If the human stays put and the robot succeeds, they will receive a reward depending on the object (1 for plastic bottle, 2 for fish can, 3 for wine glass).\n2. If the human stays put and the robot fails, they will receive a penalty depending on the object (no penalty for plastic bottle, -4 for fish can, -9 for wine glass).\n3. If the human intervenes, no reward or penalty will be issued.\n\n"

        bottle_counter = 0
        interaction_history_text = translate_interaction_history_v3(self.history,
                                                                    include_trust_change=self.include_trust_change)
        return initial_state_text + reward_info_text + interaction_history_text
        # return initial_state_text + reward_info_text


def generate_template(node: Node, robot_action):
    assert robot_action in ['plastic bottle', 'wine glass', 'fish can']
    object_description = robot_action
    template = node.translate_history_to_language()
    # template += "The current remaining objects include "
    # for remain_object, count in node.remaining_objects.items():
    # template += f"{count} {remain_object}, "
    # template += "Read the above and answer the following question.\n"
    current_turn = len(node.history) + 1
    if robot_action == 'plastic bottle':
        article = 'a'
    else:
        article = 'the'
    if len(node.history) == 0:
        template += f"Question: Based on all the above information, will the human now trust the robot to remove {article} {robot_action} by itself?"
    else:
        template += f"Question: Based on all the above information, will the human now trust the robot to remove {article} {robot_action} by itself?"
    template += " Answer choices: A. Yes, B. No\n"
    # template += "Answer choices: A. intervene, B. stay put\n"
    template += "Answer:"
    return template


def generate_template_action(node: Node, robot_action):
    assert robot_action in ['plastic bottle', 'wine glass', 'fish can']
    template = node.translate_history_to_language()
    if robot_action == 'plastic bottle':
        article = 'a'
    else:
        article = 'the'
    template += f"Question: Now the robot chooses to clear {article} {robot_action}, based on all the above information, what will the human do?"
    template += " Answer choices: A. stay put, B. intervene\n"
    template += "Answer:"
    return template


def generate_trust_template(node: Node, action):
    template = node.translate_history_to_language()
    template += f"Question: Now, how much will the human rate their trust in the robot out of 7?\n"
    template += "Answer:"
    return template


def generate_trust_change_template(node: Node, action):
    template = node.translate_history_to_language()
    template += f"Question: Describe how the human's trust in the robot has changed due to the last interaction. Answer choices: A. increased, B. decreased, C. unchanged\n"
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
        succ_new_node = Node(new_remaining_objects, history + [(robot_action, False, True)],
                             include_trust_change=root_node.include_trust_change)
        # We don't consider the fail case

        expand_interaction_tree(intervene_node, template_generation_fn)
        expand_interaction_tree(succ_new_node, template_generation_fn)
        root_node.prompts.append(prompt_template)
        root_node.children.append(succ_new_node)
        root_node.children.append(intervene_node)

def evaluate_policy(policy_csv_path):
    # The first sysarg is a dummy policy, not really executed but replaced by the evaluated LLM policy
    command = f"python2 ./table_clearing_trust_pomdp/evaluate/evaluate.py ./table_clearing_trust_pomdp/policy/table_clearing.policy {policy_csv_path}"
    os.system(command)