

class BaseSolution:

    def __init__(self):
        pass

    def load_frame(self):
        # Nacteni jednoho snimku ze serveru 
        pass

    def detect_playgrond(self):
        # Detekce hriste z nacteneho snimku
        pass

    def detect_robot(self):
        # Detekce robota [ArUCo tag]
        pass

    def recognize_objects(self):
        # Rozpoznani objektu na hristi - cil, body, prekazky
        pass

    def analyze_playground(self):
        # Analyza dat vytezenych ze snimku
        pass

    def generate_path(self):
        # Vygenerovani cesty [L, F, R, B] -- pripadne dalsi kody pro slozitejsi ulohy
        pass

    def send_solution(self):
        # Poslani reseni na server pomoci UTP spojeni.
        pass

    def solve(self):
        self.load_frame()
        self.detect_playgrond()
        self.detect_robot()
        self.recognize_objects()
        self.analyze_playground()
        self.generate_path()
        self.send_solution()
        pass


if __name__ == "__main__":
    solution = BaseSolution()
    solution.solve()
