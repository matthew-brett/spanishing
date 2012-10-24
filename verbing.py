from __future__ import print_function
import os
import random
import codecs
import yaml

DIR = os.path.dirname(__file__)
DICT_FNAME = os.path.join(DIR, 'spanish.yaml')
stream = codecs.open(DICT_FNAME, encoding='utf-8')
ESP_DICT = list(yaml.load_all(stream))[0]

VERBS = [key for key in ESP_DICT if 'part' in ESP_DICT[key]]
SPERSONS = ESP_DICT['grammar']['spersons']
EPERSONS = ESP_DICT['grammar']['epersons']
ALL_PERSONS = SPERSONS.copy()
ALL_PERSONS.update(EPERSONS)
TENSES = ESP_DICT['grammar']['tenses']
ACCENTS = ESP_DICT['grammar']['accents']


def form_accents(in_str):
    out_str = in_str
    for char, acc_char in ACCENTS.items():
        out_str = out_str.replace("'" + char, acc_char)
    return out_str


def decline_verb(verb, tense, person):
    sp_person = ALL_PERSONS[person]
    vdata = ESP_DICT[verb]
    declined = vdata['decl']['tenses'][tense][sp_person]
    if declined.startswith('-'):
        declined = declined.replace('-', verb[:-2])
    return declined


print("? to see answer, q to quit")
while True:
    sperson = random.choice(SPERSONS.keys())
    verb = random.choice(VERBS)
    tense = random.choice(TENSES)
    vdata = ESP_DICT[verb]
    person_canonical = ALL_PERSONS[sperson]
    if tense == 'present':
        msg = "{0} {1}".format(sperson, vdata['einf'])
        if person_canonical == 'el':
            msg += 's'
    elif tense == 'future':
        msg = "{0} will {1}".format(sperson, vdata['einf'])
    elif tense == 'simple-past':
        msg = "{0} {1}".format(sperson, vdata['epastp'])
    elif tense == 'imperfect':
        if person_canonical in ('yo', 'el'):
            mid = 'was'
        else:
            mid = 'were'
        msg = "{0} {1} {2}".format(sperson, mid, vdata['egerund'])
    result = raw_input(msg + ": ")
    if result in ('', 'q', 'quit', 'Q', 'exit'):
        break;
    result = form_accents(result)
    correct = decline_verb(verb, tense, sperson)
    if result == '?':
        print("I believe the right answer is " + correct)
        continue
    print("You said: " + result)
    if result == correct:
        print("Congratulations, for what it is worth, I agree with you")
    else:
        print("One of us is wrong, because I think " + correct + " is correct")
print("Thanks for your attention")
