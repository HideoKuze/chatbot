# -*- coding: utf-8 -*-
"""Using the parser to recognise your own semantics
spaCy's parser component can be used to trained to predict any type of tree
structure over your input text. You can also predict trees over whole documents
or chat logs, with connections between the sentence-roots used to annotate
discourse structure. In this example, we'll build a message parser for a common
"chat intent": finding local businesses. Our message semantics will have the
following types of relations: ROOT, PLACE, QUALITY, ATTRIBUTE, TIME, LOCATION.
"show me the best hotel in berlin"
('show', 'ROOT', 'show')
('best', 'QUALITY', 'hotel') --> hotel with QUALITY best
('hotel', 'PLACE', 'show') --> show PLACE hotel
('berlin', 'LOCATION', 'hotel') --> hotel with LOCATION berlin
Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
import spacy
from pathlib import Path


# training data: texts, heads and dependency labels
# for no relation, we simply chose an arbitrary dependency label, e.g. '-'
TRAIN_DATA = [
    ("root How do I delete my account?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3],  # index of token head
        'deps': ['ROOT', '-', '-', '-', 'INTENT', '-', 'OBJECT', '-']
    }),
    ("root How do I add a balance?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3],
        'deps': ['ROOT', '-', '-', '-', 'INTENT', '-', 'OBJECT', '-']
    }),
    ("root How do I deposit my funds into my bank account?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3, 9, 9, 6, 3],
        'deps': ['ROOT', '-','-', '-', 'INTENT', '-', '-', '-', '-', '-', 'OBJECT', '-']
    }),
    ("root How do I fill out feedback forms?", {
        'heads': [0, 3, 3, 3, 3, 3, 6, 3, 3],
        'deps': ['ROOT','-', '-', '-', 'INTENT', '-', '-', 'OBJECT', '-']
    }),
    ("root How does my profile impact my score?", {
        'heads': [0, 4, 4, 4, 4, 4, 6, 4, 4],
        'deps': ['ROOT','-', '-', '-', '-', 'INTENT', '-', 'OBJECT', '-']
    }),
    ("root What are the fees?", {
        'heads': [0, 1, 1, 3, 1, 1],
        'deps': ['ROOT', '-', '-', '-', 'INTENT', '-']
    }),
    ("root How do I update my profile picture?", {
        'heads': [0, 3, 3, 3, 3, 6, 6, 3, 3],
        'deps': ['ROOT', '-', '-', '-', 'INTENT', '-', 'OBJECT', 'OBJECT', '-']
    }),
    ("root How do I add a referral to the marketplace?", {
        'heads': [0, 3, 3, 3, 3, 5, 3, 3, 8, 6, 3],
        'deps': ['ROOT', '-', '-', '-', 'INTENT', '-', 'OBJECT', '-', '-', 'OBJECT', '-']
    }),
    ("root add feedback", {
        'heads': [0, 0, 1],
        'deps': ['ROOT', 'INTENT', 'OBJECT']
    }),
    ("root delete my account", {
        'heads': [0, 0, 3, 1],
        'deps': ['ROOT', 'INTENT', '-', 'OBJECT']
    }),

]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=5):
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
    test_model(nlp)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        test_model(nlp2)


def test_model(nlp):
    texts = ["How do I delete my account?",
             "How do I add a balance?",
             "How do I deposit my funds into my bank account?",
             'root delete my account',
             'root add feedback']
    docs = nlp.pipe(texts)
    for doc in docs:
        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != '-'])


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # find a hotel with good wifi
    # [
    #   ('find', 'ROOT', 'find'),
    #   ('hotel', 'PLACE', 'find'),
    #   ('good', 'QUALITY', 'wifi'),
    #   ('wifi', 'ATTRIBUTE', 'hotel')
    # ]
    # find me the cheapest gym near work
    # [
    #   ('find', 'ROOT', 'find'),
    #   ('cheapest', 'QUALITY', 'gym'),
    #   ('gym', 'PLACE', 'find')
    #   ('work', 'LOCATION', 'near')
    # ]
    # show me the best hotel in berlin
    # [
    #   ('show', 'ROOT', 'show'),
    #   ('best', 'QUALITY', 'hotel'),
    #   ('hotel', 'PLACE', 'show'),
    #   ('berlin', 'LOCATION', 'hotel')
    # ]