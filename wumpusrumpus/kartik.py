import nltk.inference as inference
import nltk.sem.logic as logic

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

axioms = []
axioms.append('all x. Stench(x) -> exists y. Wumpus(y) & Adjacent(x, y)')
KB = KnowledgeBase(axioms)
KB.tell('Stench(1_1)')
KB.tell('-Wumpus(1_1)')
print(KB.ask('Wumpus(1_1)'))
