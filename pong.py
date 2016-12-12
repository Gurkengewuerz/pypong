import tkinter
import threading


class Sprite:
    """Ein Sprite ist ein Objekt auf dem Canvas, das bewegt werden kann."""
    def __init__(self, canvas, position, width_height):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(position[0], position[1],
                                                 position[0] + width_height[0],
                                                 position[1] + width_height[1],
                                                 fill="black")
        print("Sprite erstellt", self.rect)

    def start(self):
        """Starte den Sprite. In jedem Zyklus wird die update-Methode
        aufgerufen. Hier muss der Sprite seine eigentliche Arbeit leisten."""

        self._tick()

    def _tick(self):
        self.update()
        th = threading.Thread(target=self._tick)
        th.start()

    def finde_ueberlappung(self):
        """Prüft, ob der Sprite mit anderen Sprites überlappt und gibt diese
        zurück."""

        coords = self.position()
        elemente = self.canvas.find_overlapping(*coords)

        # sich selbst von der Überlappung ausnehmen
        return [e for e in elemente if e != self.rect]

    def position(self):
        """Liefert die Koordinaten in Form von vier Punkten."""
        return self.canvas.coords(self.rect)

    def update(self):
        """Diese Methode muss von den ableitenden Klassen überschrieben werden.
        Nach dem Aufruf von start, wird diese Methode in jedem Zyklus einmal
        aufgerufen."""

        raise Exception("Muss überschrieben werden!")

    def bewegen(self, delta_x, delta_y):
        """Bewege den Sprite um (delta_x, delta_y). Positive Werte bewegen nach
        rechts, negative Werte nach links."""

        self.canvas.move(self.rect, delta_x, delta_y)


class Schlaeger(Sprite):
    def __init__(self, canvas, position):
        super().__init__(canvas, position, (10, 50))

    def update(self):
        pass

    def hoch(self):
        self.bewegen(0, -10)
        
    def runter(self):
        self.bewegen(0, +10)


class Ball(Sprite):
    def __init__(self, canvas, position):
        super().__init__(canvas, position, (10, 10))
        self.dir = [1, 0]

    def update(self):
        self.bewegen(self.dir[0], self.dir[1])

        elemente = self.finde_ueberlappung()
        if len(elemente) > 0:
            self.dir[0] *= -1


class Pong:
    def __init__(self, breite=300, hoehe=200):
        self.fenster = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.fenster, width=breite, height=hoehe)
        self.canvas.pack()

        print("Erstelle Schläger")
        self.schlaeger_links = Schlaeger(self.canvas, (0, 10))
        self.schlaeger_links.start()
        self.schlaeger_rechts = Schlaeger(self.canvas, (breite-10, 10))
        self.schlaeger_rechts.start()

        print("Erstelle Ball")
        self.ball = Ball(self.canvas, (10, 10))
        self.ball.start()

        btn = tkinter.Button(self.fenster, text="^", command=self.btn_up_click)
        btn.pack()        
        btn = tkinter.Button(self.fenster, text="v",
                             command=self.schlaeger_links.runter)
        btn.pack()        

        self.fenster.mainloop()

    def btn_up_click(self):
        self.schlaeger_links.hoch()
        
pong = Pong()
