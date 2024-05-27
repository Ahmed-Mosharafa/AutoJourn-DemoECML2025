class Samsum:
    def __init__(self, id, summary, dialogue):
        self.id = id
        self.summary = summary
        self.dialogue = dialogue

    def to_json(self):
        return {"id": self.id, "summary": self.summary, "dialogue": self.dialogue}
