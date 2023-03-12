# This is an implementation of the table-clearing task
import numpy as np
from evaluate import TableClearing
from loadPolicy import *

reward_dict = {'plastic bottle': 1, 'fish can': 2, 'wine glass': 3}

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

def llm_history_to_state(history):
    state = [0, 0, 0, 0, 0]
    for robot_action, intervention, _ in history:
        if robot_action == 'plastic bottle':
            valid_bottle = False
            for s_idx, s in enumerate(state[:3]):
                if s == 0:
                    if intervention:
                        state[s_idx] = 3
                    else:
                        state[s_idx] = 1
                    valid_bottle = True
                    break
            assert valid_bottle
        elif robot_action == 'fish can':
            assert state[3] == 0
            if intervention:
                state[3] = 3
            else:
                state[3] = 1            
        else:
            assert robot_action == 'wine glass'
            assert state[4] == 0
            if intervention:
                state[4] = 3
            else:
                state[4] = 1
    return state   
        

def expand_interaction_tree(root_node):
    remaining_objects = root_node.remaining_objects
    history = root_node.history
    flattened_objects = [o for o in remaining_objects.keys() for _ in range(remaining_objects[o])]
    # print(flattened_objects)
    if len(flattened_objects) == 0:
        return
    # Robot action: pick up one remaining object
    # Human action: intervene or stay put
    # Each interaction (entry in the history) consists of (robot action, intervened or not, result)

    robot_action_list = []
    
    if 'plastic bottle' in remaining_objects:
        robot_action_list.append('plastic bottle')
    if 'fish can' in remaining_objects:
        robot_action_list.append('fish can')
    if 'wine glass' in remaining_objects:
        robot_action_list.append('wine glass')
    
    if len(robot_action_list) == 0:
        return
    for robot_action in robot_action_list:
        # prompt_template = generate_trust_template(root_node)

        new_remaining_objects = remaining_objects.copy()
        new_remaining_objects[robot_action] -= 1
        if new_remaining_objects[robot_action] == 0:
            del new_remaining_objects[robot_action]

        # Intervened
        intervene_node = Node(new_remaining_objects, history + [(robot_action, True, True)], include_trust_change=root_node.include_trust_change)
        # Stay put, robot succeeded
        succ_new_node = Node(new_remaining_objects, history + [(robot_action, False, True)], include_trust_change=root_node.include_trust_change)
        # Stay put, robot failed
        # fail_new_node = Node(new_remaining_objects, history + [(robot_action, False, False)])

        expand_interaction_tree(intervene_node)
        expand_interaction_tree(succ_new_node)
        # expand_interaction_tree(fail_new_node)
        root_node.children.append(succ_new_node)
        root_node.children.append(intervene_node)

def get_trust_belief(root_node, all_nodes, init_belief):
    policyfile = '../policy/table_clearing.policy'
    policy = LoadPolicy(policyfile)
    
    init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    tclear = TableClearing(policy, init_bel, 1)
    
    trust_belief_dict = {node: [] for node in all_nodes}
    trust_belief_dict[root_node] = init_belief
    
    def get_trust_belief_of_node(cur_node, prior_belief):
        if len(cur_node.history) > 0:
            robot_action, intervention, _ = cur_node.history[-1]
            cur_node_belief = tclear.get_next_belief(prior_belief, robot_action, 0 if intervention else 1)
            trust_belief_dict[cur_node] = cur_node_belief
        else:
            cur_node_belief = prior_belief
        for child_node in cur_node.children:
            get_trust_belief_of_node(child_node, cur_node_belief)
    
    get_trust_belief_of_node(root_node, init_belief)
    
    return trust_belief_dict
    

def get_policy(root_node, all_nodes):
    # Get the policy
    reward_dict = {'plastic bottle': 1, 'fish can': 1, 'wine glass': 1}
    q_dict = {node: {} for node in all_nodes}
    
    def get_value_of_node(cur_node):
        robot_action_list = []
    
        if 'plastic bottle' in cur_node.remaining_objects:
            robot_action_list.append('plastic bottle')
        if 'fish can' in cur_node.remaining_objects:
            robot_action_list.append('fish can')
        if 'wine glass' in cur_node.remaining_objects:
            robot_action_list.append('wine glass')
        
        if len(cur_node.children) == 0:
            # Leaf node
            last_picked_object, intervened, succ = cur_node.history[-1]
            return 0
            # if intervened:
            #     return 0
            # else:
            #     return reward_dict[last_picked_object]
        else:
            for a_idx, a in enumerate(robot_action_list):
                assert a in ["plastic bottle", "fish can", "wine glass"]
                immediate_reward = reward_dict[a]
                intervene_prob = cur_node.probs[a_idx * 2 + 1]
                stay_put_prob = cur_node.probs[a_idx * 2]
                
                intervene_node = cur_node.children[a_idx * 2 + 1]
                stay_put_node = cur_node.children[a_idx * 2]
                q_dict[cur_node][a] = stay_put_prob * (immediate_reward + get_value_of_node(stay_put_node)) + intervene_prob * (0 + get_value_of_node(intervene_node))
            # print(q_dict[cur_node])
            # print(q_dict[cur_node].values())
            return np.max(list(q_dict[cur_node].values()))
    get_value_of_node(root_node)
                
    return q_dict