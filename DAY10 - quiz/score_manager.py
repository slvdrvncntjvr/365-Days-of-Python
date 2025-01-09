class ScoreManager:
    def __init__(self, file_name="scores.txt"):
        self.file_name = file_name

    def save_score(self, score):
        with open(self.file_name, "a") as file:
            file.write(f"{score}\n")

    def get_scores(self):
        try:
            with open(self.file_name, "r") as file:
                scores = file.readlines()
            return [int(score.strip()) for score in scores]
        except FileNotFoundError:
            return []
