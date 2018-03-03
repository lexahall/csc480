# Name:         Lexa Hall
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Wumpus Rumpus
# Term:         Winter 2018


import nltk.inference as inference
import nltk.sem.logic as logic


KB = None


def pyagent_initialize():
    global KB


def pyagent_process(stench, breeze, glitter, bump, scream, compass):
    print("pyagent_process:",
          ", ".join("{0}={1}".format(k, v) for k, v in locals().items()))
    global KB
    actions = {"GOFORWARD": 0, "TURNLEFT": 1, "TURNRIGHT": 2, "GRAB": 3,
               "CLIMB": 5, "WAIT": 6, "COMPASS": 7}
    if compass is not None: # parse compass string
        compass_array = [tuple(int(n) for n in sub.split(","))
                         for sub in compass[2:-2].split("),(")]
    return actions["GOFORWARD"]




class KnowledgeBase(object):
    
    def __init__(self, axioms = []):
        self.sentences = [logic.Expression.fromstring(a) for a in axioms]
        self.agent_loc = [1, 1]
    
    def tell(self, sentence):
        self.sentences.append(logic.Expression.fromstring(sentence))
    
    def ask(self, sentence):
        sentence = logic.Expression.fromstring(sentence)
        if "ANSWER" in str(sentence):
            prover = inference.ResolutionProverCommand(None, self.sentences)
            prover.add_assumptions([sentence])
            return [list(e.constants())[0].name for e in prover.find_answers()
                    if type(e) is logic.ConstantExpression]
        else:
            return inference.ResolutionProver().prove(sentence, self.sentences)


