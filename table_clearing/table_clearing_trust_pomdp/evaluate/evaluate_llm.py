# -*- coding: future_fstrings -*-

import llm_policy
import pandas as pd
from tqdm import tqdm
from loadPolicy import *
from numpy import *
from evaluate import TableClearing

if __name__=='__main__':
    llm_result_file = sys.argv[2]
    policyfile = sys.argv[1]
    
    remaining_objects = {'plastic bottle': 3, 'fish can': 1, 'wine glass': 1}
    
    robot_action_list = ['plastic bottle', 'plastic bottle', 'plastic bottle', 'fish can', 'wine glass']
    
    # Load the LLM policy
    print(remaining_objects.keys())
    llm_root_node = llm_policy.Node(remaining_objects, [], include_trust_change=True)

    llm_policy.expand_interaction_tree(llm_root_node)
    all_llm_nodes = llm_root_node.traverse()
    
    llm_result_df = pd.read_csv(llm_result_file)
    # Get the probs
    s = set()
    for node in tqdm(all_llm_nodes):
        probs = []
        if len(llm_result_df[llm_result_df['history'] == str(node.history)]) == 0:
            assert len(node.children) == 0
        else:
            # print(len(node.children))
            # print(len(llm_result_df[llm_result_df['history'] == str(node.history)]))
            assert len(node.children) == len(llm_result_df[llm_result_df['history'] == str(node.history)]) * 2
            rows = llm_result_df[llm_result_df['history'] == str(node.history)]
            for row_idx, row in rows.iterrows():
                probs.append(row['A'] / (row['A'] + row['B']))
                probs.append(row['B'] / (row['A'] + row['B']))
        node.probs = probs
    
    policy = LoadPolicy(policyfile)
    
    init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    tclear = TableClearing(policy, init_bel, 1)
    
    llm_q_dict = llm_policy.get_policy(llm_root_node, all_llm_nodes)
    trust_belief_dict = llm_policy.get_trust_belief(llm_root_node, all_llm_nodes, init_bel)
    
    unfound = 0
    mismatch = 0
    
    for node in all_llm_nodes:
        if len(node.children) != 0:
            # print(node.history)
            # print(llm_policy.llm_history_to_state(node.history))
            # print(trust_belief_dict[node])
            pomdp_action = policy.FindOptimalAction(trust_belief_dict[node], llm_policy.llm_history_to_state(node.history))
            if pomdp_action == -1:
                # print(node.history)
                # print(llm_policy.llm_history_to_state(node.history))
                # print(trust_belief_dict[node])
                unfound += 1
            else:
                llm_action = max(llm_q_dict[node], key=llm_q_dict[node].get)
                if pomdp_action in [0, 1, 2]:
                    if llm_action != 'plastic bottle':
                        mismatch += 1
                elif pomdp_action == 3:
                    if llm_action != 'fish can':
                        mismatch += 1
                else:
                    assert pomdp_action == 4
                    if llm_action != 'wine glass':
                        mismatch += 1

    cur_node = llm_root_node
    while len(cur_node.children) != 0:
        llm_action = max(llm_q_dict[cur_node], key=llm_q_dict[cur_node].get)
        pomdp_action = policy.FindOptimalAction(trust_belief_dict[cur_node], llm_policy.llm_history_to_state(cur_node.history))

        print(f"LLM action {llm_action} POMDP action {robot_action_list[pomdp_action]}")
        print(sum([trust_belief_dict[cur_node][i] * (i + 1) for i in range(7)]))
        cur_node = cur_node.children[0]
    
