import tkinter as tk
import random

class BubbleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu d'Éclatement de Bulles")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")
        self.canvas = tk.Canvas(self.root, bg="lightblue", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bubbles = []  # Liste pour suivre les bulles
        self.running = True
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
        self.bubbles.append((bubble, random.uniform(1, 3)))  # La bulle et sa vitesse

        # Planifier une nouvelle bulle
        self.root.after(1000, self.create_bubbles)

    def animate_bubbles(self):
        """Animer les bulles qui flottent vers le haut."""
        if not self.running:
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
                break

    def quit_game(self):
        """Quitter le jeu proprement."""
        self.running = False
        self.root.destroy()


# Lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    game = BubbleGame(root)
    root.mainloop()