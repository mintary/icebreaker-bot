import json
import random
import sqlite3

'''
Actions that have to do with manipulating questions in the questionbank. With attributes to keep
track of which questions have been chosen. A separate questionbank is used for every level of the
game. Mostly in case we want to add option to create custom levels and questionbanks in the future.
'''
class Questionbank():
    def __init__(self, level: int, bank_type: str, guild_id: int):
        self.level = level
        self.bank_type = bank_type
        self.questions = set()
        self.used = set()
        self.guild_id = guild_id
        self.load_qs()

    def load_qs(self):
        if self.bank_type == "default": self.load_default("resources/questions.json")
        if self.bank_type == "custom": self.load_custom()
        if self.bank_type == "mixed": self.load_custom(), self.load_default("resources/questions.json")
    
    def load_custom(self):
        db = sqlite3.connect('icebreaker.db')
        cur = db.cursor()

        query = "SELECT question_text FROM questions WHERE level = ? AND guild_id = ? "
        cur.execute(query, (self.level, self.guild_id))

        rows = cur.fetchall()

        for row in rows:
            self.questions.add(row[0])

    def load_default(self, file): # Generate a list of questions corresponding to the level, which is currently expressed in the format ('Level n')
        # TBA: method of storing the level data as an integer, not a string
        with open(file, 'r') as f:
            data = json.load(f)
            level_questions = [str(item) for item in data['Levels'][str(self.level)]]

        self.questions.update(level_questions)
        
    # Method to pick a question from the questionbank
    def pick_question(self):
        # Pick question from the set, but excluding the used questions
        unused_questions = list(set(self.questions).difference(self.used))
        if len(unused_questions) == 0:
            return None
    
        q = random.choice(unused_questions)
        self.used.add(q)
        return q 
    
    # Method to add back a question that was picked, but now should be returned to the questionbank
    def add_back(self, question):
        try:
            self.used.remove(question)
            self.questions.add(question)
        except KeyError:
            print('Error: attempted to add back question that did not exist.')



        

        