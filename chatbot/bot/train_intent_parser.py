# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import plac
import random
import spacy
from pathlib import Path


# training data: texts, heads and dependency labels
# for no relation, we use an arbitrary dependency the label '-'
TRAIN_DATA = [
    ("root How do I delete my account?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3],  # index of token head
        'deps': ['ROOT', '-', '-', '-', 'DEL-ACCOUNT-INTENT', '-', 'OBJECT', '-']
    }),
    ("root How do I add a balance?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3],
        'deps': ['ROOT', '-', '-', '-', 'ADD-BALANCE-INTENT', '-', 'OBJECT', '-']
    }),
    ("root How do I deposit my funds into my bank account?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3, 9, 9, 6, 3],
        'deps': ['ROOT', '-','-', '-', 'DEPOSIT-FUNDS-INTENT', '-', '-', '-', '-', '-', 'OBJECT', '-']
    }),
    ("root How do I fill out feedback forms?", {
        'heads': [0, 3, 3, 3, 3, 3, 6, 3, 3],
        'deps': ['ROOT','-', '-', '-', 'ADD-FEEDBACK-INTENT', '-', '-', 'OBJECT', '-']
    }),
    ("root How does my profile impact my score?", {
        'heads': [0, 4, 4, 4, 4, 4, 6, 4, 4],
        'deps': ['ROOT','-', '-', '-', '-', 'SCORE-INTENT', '-', 'OBJECT', '-']
    }),
    ("root What are the fees?", {
        'heads': [0, 1, 1, 3, 1, 1],
        'deps': ['ROOT', '-', '-', '-', 'FEES-INTENT', '-']
    }),
    ("root How do I update my profile picture?", {
        'heads': [0, 3, 3, 3, 3, 6, 6, 3, 3],
        'deps': ['ROOT', '-', '-', '-', 'CHANGE-PIC-INTENT', '-', 'OBJECT', 'OBJECT', '-']
    }),
    ("root How do I add a referral to the marketplace?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3, 8, 6, 3],
        'deps': ['ROOT', '-', '-', '-', 'ADD-REFERRAL-INTENT', '-', 'OBJECT', '-', '-', 'OBJECT', '-']
    }),
    ("root add feedback", {
        'heads': [0, 0, 1],
        'deps': ['ROOT', 'ADD-FEEDBACK-INTENT', 'OBJECT']
    }),
    ("root add balance", {
        'heads': [0, 0, 1],
        'deps': ['ROOT', 'ADD-BALANCE-INTENT', 'OBJECT']
    }),
    ("root delete my account", {
        'heads': [0, 0, 3, 1],
        'deps': ['ROOT', 'DEL-ACCOUNT-INTENT', '-', 'OBJECT']
    }),
    ("root change my picture", {
        'heads': [0, 0, 3, 1],
        'deps': ['ROOT', 'CHANGE-PIC-INTENT', '-', 'OBJECT']
    }),
    ("root change picture", {
        'heads': [0, 0, 2],
        'deps': ['ROOT', 'CHANGE-PIC-INTENT', '-', 'OBJECT']
    }),
]

#autmatically searches for meta.json file
save_path = 'C:/Users/Elitebook/Documents/Github/chatbot/chatbot/bot/'

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
    )
def main(model=None, output_dir=save_path, n_iter=25):
    """Load the model, set up the pipeline and train the parser."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    #add new labels to the parser
    for text, annotations in TRAIN_DATA:
        for dep in annotations.get('deps', []):
            parser.add_label(dep)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, losses=losses)
            print(losses)

    # test the trained model
    #test_model(nlp)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        '''print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        test_model(nlp2)'''

responses = {
            'GREET-INTENT':['hey','howdy', 'hey there','hello', 'hi'],
            'DEPOSIT-FUNDS-INTENT':['You can do so here: placeholder.com'],
            'ADD-FEEDBACK-INTENT':['You can do so here: placeholder.com'],
            'ADD-BALANCE-INTENT':['You can do so here: placeholder.com'],
            'FEES-INTENT': ['You can do so here: placeholder.com'],
            'SCORE-INTENT': ['You can do so here: placeholder.com'],
            'DEL-ACCOUNT-INTENT' : ['You can do so here: placeholder.com'],
            'CHANGE-PIC-INTENT' : ['You can do so here: placeholder.com']
            }


def test_model(nlp, text):
    intents = []
    docs = nlp.pipe(text)
    for doc in docs:
        [intents.append(tokens.dep_) for tokens in doc if 'INTENT' in tokens.dep_]

    return responses[intents[0]][0]


if __name__ == '__main__':
    print ("Loading from", save_path)
    nlp2 = spacy.load(save_path)
    #has to be a list
    text = ['change picture']
    parsable_text = 'root ' + text[0]
    dependencies = test_model(nlp2, [parsable_text])
    print (dependencies)

    

