import numpy as np
import sklearn.metrics as metrics

# Base prompt structure

def create_template_driving_t5(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                               post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot, which is a autonomous vehicle in a virtual " \
                "reality environment. To interact, the participant wears a virtual reality headset " \
                "which provides a first-person viewpoint from the driver seat. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[0]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[0]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[1]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[1]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[2]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[2]} \n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{post_test_task_descr}'. I trust that the robot can perform the task successfully. \n"

    template += "Answer:"
    return template


def create_template_driving_davinci(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                    post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot, which is a autonomous vehicle in a virtual " \
                "reality environment. To interact, the participant wears a virtual reality headset " \
                "which provides a first-person viewpoint from the driver seat. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[0]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[0]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[1]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[1]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[2]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[2]} \n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{post_test_task_descr}'. I trust that the robot can perform the task successfully. \n"

    template += "Answer: {}"
    return template


def create_template_household_t5(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                 post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot. The robot is a Fetch research robot which is equipped " \
                "with a 7 degrees-of-freedom arm. The human is requested to rate their subjective trust in the robot " \
                "to successfully perform described tasks in a studio apartment. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[0]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[0]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[1]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[1]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[2]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[2]} \n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{post_test_task_descr}'. I trust that the robot can perform the task successfully. \n"

    template += "Answer:"
    return template


def create_template_household_davinci(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                      post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot. The robot is a Fetch research robot which is equipped " \
                "with a 7 degrees-of-freedom arm. The human is requested to rate their subjective trust in the robot " \
                "to successfully perform described tasks in a studio apartment. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[0]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[0]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[1]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[1]} \n"

    template += f"Question: The robot is going to perform the task '{test_task_descr[2]}'. I trust that the robot can perform the task successfully. \n"

    template += f"Answer: {pre_test_task_trust[2]} \n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Question: The robot is going to perform the task '{post_test_task_descr}'. I trust that the robot can perform the task successfully. \n"

    template += "Answer: {}"
    return template

# Altered prompt structure

def create_template_driving_t5_altered(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                       post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot, which is a autonomous vehicle in a virtual " \
                "reality environment. To interact, the participant wears a virtual reality headset " \
                "which provides a first-person viewpoint from the driver seat. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"The participant rates their trust on the task '{test_task_descr[0]}' as {pre_test_task_trust[0]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[1]}' as {pre_test_task_trust[1]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[2]}' as {pre_test_task_trust[2]} out of 7.\n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Given these demonstrations and the initial trust, now the participant will rate their trust on the task '{post_test_task_descr}'" + " as"
    return template


def create_template_driving_davinci_altered(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                            post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot, which is a autonomous vehicle in a virtual " \
                "reality environment. To interact, the participant wears a virtual reality headset " \
                "which provides a first-person viewpoint from the driver seat. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"The participant rates their trust on the task '{test_task_descr[0]}' as {pre_test_task_trust[0]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[1]}' as {pre_test_task_trust[1]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[2]}' as {pre_test_task_trust[2]} out of 7.\n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Given these demonstrations and the initial trust, now the participant will rate their trust on the task '{post_test_task_descr}'" + " as"
    return template


def create_template_household_t5_altered(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                         post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot. The robot is a Fetch research robot which is equipped " \
                "with a 7 degrees-of-freedom arm. The human is requested to rate their subjective trust in the robot " \
                "to successfully perform described tasks in a studio apartment. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"The participant rates their trust on the task '{test_task_descr[0]}' as {pre_test_task_trust[0]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[1]}' as {pre_test_task_trust[1]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[2]}' as {pre_test_task_trust[2]} out of 7.\n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Given these demonstrations and the initial trust, now the participant will rate their trust on the task '{post_test_task_descr}'" + " as"
    return template


def create_template_household_davinci_altered(test_task_descr, pre_test_task_trust, obs_tasks_descr, obs_tasks_perf,
                                              post_test_task_descr):
    template = "This document contains a record of a human participant's response during their participation in a " \
               "study on " \
               "their trust in robots. \n"

    template += "The participant is introduced to the robot. The robot is a Fetch research robot which is equipped " \
                "with a 7 degrees-of-freedom arm. The human is requested to rate their subjective trust in the robot " \
                "to successfully perform described tasks in a studio apartment. \n"

    template += "Without observing any demonstrations from the robot, the participant is requested to indicate " \
                "their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"The participant rates their trust on the task '{test_task_descr[0]}' as {pre_test_task_trust[0]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[1]}' as {pre_test_task_trust[1]} out of 7.\n"
    template += f"The participant rates their trust on the task '{test_task_descr[2]}' as {pre_test_task_trust[2]} out of 7.\n"

    template += "Now the participant observes the two demonstrations from the robot. \n"

    template += f"First, the robot performs the task '{obs_tasks_descr[0]}' and {'succeeds' if obs_tasks_perf[0] else 'fails'}. \n"

    template += f"Then, the robot performs the task '{obs_tasks_descr[1]}' and {'succeeds' if obs_tasks_perf[1] else 'fails'}. \n"

    template += "After observing these demonstrations, the participant is again requested to indicate their trust by answering the following agreement questions via a 7-point Likert scale. \n"

    template += f"Given these demonstrations and the initial trust, now the participant will rate their trust on the task '{post_test_task_descr}'" + " as {}"
    return template


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def analyze_results(llm_post_trust_df, gt_post_trust_df):
    answer_choices = [str(i) for i in range(1, 8)]
    llm_post_trust = []

    gt_post_trust = []
    gt_pre_trust = []

    llm_dist = []
    normalized_llm_dist = []

    llm_post_trust_argmax = []

    llm_post_trust_binarized = []
    gt_post_trust_binarized = []

    for row_idx, row in gt_post_trust_df.iterrows():
        post_trust = [int(row['C2_rating']), int(row['D2_rating']), int(row['E2_rating'])]
        pre_trust = [int(row['C1_rating']), int(row['D1_rating']), int(row['E1_rating'])]

        for idx in range(3):
            llm_post_trust_row = llm_post_trust_df[llm_post_trust_df['id'] == row_idx].iloc[idx]
            llm_probs = [llm_post_trust_row[ans] for ans in answer_choices]
            llm_probs = [p / sum(llm_probs) for p in llm_probs]
            llm_dist.append(llm_probs)
            llm_probs = [p / sum(llm_probs) for p in llm_probs]
            normalized_llm_dist.append(llm_probs)
            assert np.isclose(sum(llm_probs), 1)

            llm_post_trust_argmax.append(np.argmax(llm_probs) + 1)

            llm_post_trust_average = sum([(i + 1) * llm_probs[i] for i in range(7)])
            llm_post_trust.append(llm_post_trust_average)
            gt_post_trust.append(post_trust[idx])
            gt_pre_trust.append(pre_trust[idx])
            llm_post_trust_binarized.append(sum(llm_probs[4:]) > sum(llm_probs[:4]))
            gt_post_trust_binarized.append(post_trust[idx] >= 5)

    normalized_llm_post_trusts = [sigmoid(t - 3.5) for t in llm_post_trust]
    normalized_human_post_trusts = [sigmoid(t - 3.5) for t in gt_post_trust]

    mae = metrics.mean_absolute_error(normalized_human_post_trusts, normalized_llm_post_trusts)

    cwm = metrics.accuracy_score(gt_post_trust_binarized, llm_post_trust_binarized)

    same_counter = 0
    for i in range(len(llm_post_trust)):
        # print(llm_post_trust_argmax[i])
        if (llm_post_trust_argmax[i] == gt_pre_trust[i]) and gt_post_trust[i] != llm_post_trust_argmax[i]:
            same_counter += 1
    print(f'Post same as Pre {same_counter}')

    return mae, cwm