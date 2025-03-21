import tkinter as tk
import random

class BubbleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu d'Éclatement de Bulles")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")

        # Canvas pour les bulles
        self.canvas = tk.Canvas(self.root, bg="lightblue", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variables du jeu
        self.bubbles = []  # Liste des bulles
        self.running = True  # État du jeu (pause ou en cours)
        self.score = 0  # Score
        self.level = 1  # Niveau initial
        self.bubbles_popped = 0  # Nombre de bulles éclatées dans le niveau actuel

        # Interface utilisateur
        self.score_label = tk.Label(self.root, text=f"Score : {self.score}", font=("Arial", 16), bg="lightblue")
        self.score_label.pack(anchor="nw", padx=10, pady=5)

        self.level_label = tk.Label(self.root, text=f"Niveau : {self.level}", font=("Arial", 16), bg="lightblue")
        self.level_label.pack(anchor="nw", padx=10, pady=35)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause, font=("Arial", 14), bg="white")
        self.pause_button.pack(anchor="ne", padx=10, pady=5)

        # Lancer le jeu
        self.create_bubbles()
        self.animate_bubbles()

        # Quitter proprement
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

    def create_bubbles(self):
        """Créer une nouvelle bulle avec une position, une taille et une couleur aléatoires."""
        if not self.running:
            return

        # Paramètres aléatoires pour la bulle
        x = random.randint(50, 750)
        y = 600
        size = random.randint(20, 50)
        color = random.choice(["red", "green", "blue", "yellow", "purple", "orange", "pink"])

        # Créer une bulle (cercle)
        bubble = self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")
        self.bubbles.append((bubble, random.uniform(1 + self.level * 0.5, 3 + self.level * 0.5)))  # Vitesse dépend du niveau

        # Planifier une nouvelle bulle
        self.root.after(1000 - self.level * 50 if self.level < 12 else 400, self.create_bubbles)

    def animate_bubbles(self):
        """Animer les bulles qui flottent vers le haut."""
        if not self.running:
            self.root.after(30, self.animate_bubbles)  # Continuer à vérifier
            return

        for bubble, speed in self.bubbles[:]:
            self.canvas.move(bubble, 0, -speed)  # Déplacer la bulle vers le haut
            x1, y1, x2, y2 = self.canvas.coords(bubble)

            # Supprimer les bulles qui sortent de l'écran
            if y2 < 0:
                self.canvas.delete(bubble)
                self.bubbles.remove((bubble, speed))

        self.canvas.tag_bind("all", "<Button-1>", self.pop_bubble)  # Attacher l'événement clic
        self.root.after(30, self.animate_bubbles)

    def pop_bubble(self, event):
        """Faire éclater une bulle lorsqu'elle est cliquée."""
        for bubble, speed in self.bubbles[:]:
            x1, y1, x2, y2 = self.canvas.coords(bubble)

            # Vérifier si le clic est à l'intérieur des coordonnées de la bulle
            if x1 < event.x < x2 and y1 < event.y < y2:
                self.canvas.delete(bubble)
                self.bubbles.remove((bubble, speed))
                self.score += 1
                self.bubbles_popped += 1
                self.score_label.config(text=f"Score : {self.score}")

                # Vérifier si l'utilisateur passe au niveau suivant
                if self.bubbles_popped >= 25:
                    self.level_up()
                break

    def level_up(self):
        """Passer au niveau suivant."""
        self.level += 1
        self.bubbles_popped = 0
        self.level_label.config(text=f"Niveau : {self.level}")

        # Fin du jeu après le niveau 12
        if self.level > 12:
            self.running = False
            self.canvas.create_text(400, 300, text="Félicitations ! Vous avez terminé le jeu !",
                                     font=("Arial", 24), fill="black")
            self.canvas.create_text(400, 350, text=f"Score final : {self.score}",
                                     font=("Arial", 20), fill="black")

    def toggle_pause(self):
        """Mettre le jeu en pause ou le reprendre."""
        if self.running:
            self.running = False
            self.pause_button.config(text="Reprendre")
        else:
            self.running = True
            self.pause_button.config(text="Pause")
            self.animate_bubbles()

    def quit_game(self):
        """Quitter le jeu proprement."""
        self.running = False
        self.root.destroy()


# Lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    game = BubbleGame(root)
    root.mainloop()