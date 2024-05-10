import numpy as np
from sklearn.metrics import accuracy_score


def create_template_t5(row):
    context = row['context']
    question = row['question']
    answers = [row['answerA'], row['answerB'], row['answerC']]
    template = ""
    template += f"Context: {context}\n"
    template += f"Question: {question} Answer choices: A. {answers[0]}, B. {answers[1]}, C. {answers[2]}.\n"
    return template


def create_template_davinci(row):
    context = row['context']
    question = row['question']
    answers = [row['answerA'], row['answerB'], row['answerC']]
    template = ""
    template += f"Context: {context}\n"
    template += f"Question: {question} Answer choices: A. {answers[0]}, B. {answers[1]}, C. {answers[2]}.\n"
    template += "Answer: Based on social commonsense, the answer is {}"
    return template


def analyze_result(social_iqa_llm_results_df, gt_df):
    gt_answers = gt_df['label_ix'].to_list()

    llm_answers = []

    atomic_dimension_list = ['Intent', 'Need', 'Attr', 'Effect', 'React', 'Want']

    gt_answers_by_dimension = {d: [] for d in atomic_dimension_list}
    llm_answers_by_dimension = {d: [] for d in atomic_dimension_list}

    unnormalized_dist_list = []

    for row_idx, row in social_iqa_llm_results_df.iterrows():
        # Verify the data consistency
        assert gt_df.iloc[row_idx]["context"] in row["template"]
        answer_probs = [row['A'], row['B'], row['C']]
        unnormalized_dist_list.append(answer_probs)
        answer = np.argmax(answer_probs)
        llm_answers.append(answer)
        atomic_dimension = gt_df.iloc[row_idx]["promptDim"]
        for d in atomic_dimension_list:
            if d in atomic_dimension:
                llm_answers_by_dimension[d].append(llm_answers[row_idx])
                gt_answers_by_dimension[d].append(gt_answers[row_idx])
                break

    print(f'Average Invalid Completion Rate : {1 - np.mean([sum(d) for d in unnormalized_dist_list])}\n')

    for d in atomic_dimension_list:
        print(
            f"Dimension {d}: Accuracy: {accuracy_score(gt_answers_by_dimension[d], llm_answers_by_dimension[d])}")

    print(f"\nOverall Accuracy: {accuracy_score(gt_answers, llm_answers)}")
