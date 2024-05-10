# Utility functions

import openai
import numpy as np
from transformers import T5ForConditionalGeneration, T5Tokenizer
from tqdm import tqdm
import torch
import time
import os

OPENAI_API_KEY = os.getenv('OPENAI_KEY')


def tokenize_answer_choices(answer_choices, t5_tokenizer: T5Tokenizer):
    tokenized_candidate_answers = []
    for a in answer_choices:
        a_token = t5_tokenizer(a).input_ids
        a_token = a_token[0]
        assert t5_tokenizer.decode(a_token) == a
        tokenized_candidate_answers.append(a_token)
    return tokenized_candidate_answers


def generate_completion_t5(input_texts, t5_model: T5ForConditionalGeneration, t5_tokenizer: T5Tokenizer, batch_size=1, show_tqdm=False):
    if show_tqdm:
        pbar = tqdm(total=len(input_texts))
    completions = []
    for i in range(0, len(input_texts), batch_size):
        batch = input_texts[i:i + batch_size]
        if show_tqdm:
            pbar.update(batch_size)
        text_ids = t5_tokenizer(batch, return_tensors="pt", padding=True).input_ids.to("cuda")
        output_ids = t5_model.generate(text_ids, return_dict_in_generate=True, output_scores=True, max_new_tokens=512)
        generated_texts = t5_tokenizer.batch_decode(output_ids.sequences, skip_special_tokens=True)
        completions += generated_texts
    if show_tqdm:
        pbar.close()
    return completions


def get_probs_t5(input_texts, answer_choices, t5_model: T5ForConditionalGeneration, t5_tokenizer: T5Tokenizer, batch_size=1, show_tqdm=False):
    tokenized_answer_choices = tokenize_answer_choices(answer_choices, t5_tokenizer)
    if show_tqdm:
        pbar = tqdm(total=len(input_texts))
    answer_dist_list = []
    for i in range(0, len(input_texts), batch_size):
        batch = input_texts[i:i + batch_size]
        if show_tqdm:
            pbar.update(batch_size)
        text_ids = t5_tokenizer(batch, return_tensors="pt", padding=True).input_ids.to("cuda")
        output_ids = t5_model.generate(text_ids, return_dict_in_generate=True, output_scores=True, max_new_tokens=1)
        scores = output_ids.scores[0]
        for output_idx in range(len(scores)):
            prob_dist = torch.nn.functional.softmax(scores[output_idx])
            probs_of_answers = [prob_dist[i].item() for i in tokenized_answer_choices]
            answer_dist_list.append(probs_of_answers)
    if show_tqdm:
        pbar.close()
    return answer_dist_list


def get_probs_davinci(template, answer_choices, api_key=OPENAI_API_KEY, wait_time=5):
    # Get probabilities of input
    openai.api_key = api_key

    # Given a list of possible answers, plug them in the templated prompts and get the probability of completion
    assert "{}" in template
    prob_list = [None for _ in answer_choices]
    collected_answers = set()

    for answer in answer_choices:
        if answer in collected_answers:
            # Collected already!
            continue
        response = None

        while response is None:
            try:
                prompt = template.format(answer)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=0,
                    temperature=0,
                    logprobs=5,
                    echo=True
                )
            except Exception as e:
                print(str(e))
                time.sleep(wait_time)

        answer_log_prob = response['choices'][0]['logprobs']['token_logprobs'][-1]
        prob_list[answer_choices.index(answer)] = np.exp(answer_log_prob)
        collected_answers.add(answer)

        for other_ans in set(answer_choices).difference(collected_answers):
            # Check if we can find logprob of other tokens
            other_ans_token = f" {other_ans}"
            if other_ans_token in response.choices[0]['logprobs']['top_logprobs'][-1]:
                other_answer_log_prob = response.choices[0]['logprobs']['top_logprobs'][-1][other_ans_token]
                prob_list[answer_choices.index(other_ans)] = np.exp(other_answer_log_prob)
                collected_answers.add(other_ans)


def generate_completion_davinci(prompt, api_key=OPENAI_API_KEY, temperature=0, wait_time=5):
    # Get a free-form completion
    print(api_key)
    openai.api_key = api_key
    response = None
    while response is None:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=256,
                temperature=temperature,
            )
        except Exception as e:
            print(str(e))
            time.sleep(wait_time)
    return response['choices'][0]['text']


def normalize_dist(prob_dist):
    return [p / sum(prob_dist) for p in prob_dist]
