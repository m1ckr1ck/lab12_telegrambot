class Question:
    def __init__(self, question, choises):
        self.question = question
        self.answer = choises[0]
        self.choises = choises


    def checkAnsw(self, answ):
        if answ == self.answer:
            return True
        else:
            return False
