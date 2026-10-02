import tkinter as tk
import random


class Card:
    def __init__(self, parent):
        self.symbol = ""
        self.revealed = True

        self.button = tk.Label(
            parent,
            text="",
            font=("Arial", 30),
            width=5,
            height=2,
            relief="solid"
        )

        self.button.pack(side="left", padx=10)

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.button.config(text=symbol)

    def hide(self):
        self.revealed = False
        self.button.config(text="?")

    def show(self):
        self.revealed = True
        self.button.config(text=self.symbol)


class Game:
    def __init__(self, window):

        self.window = window

        self.score = 0
        self.level = 1
        self.correct_answers = 0

        self.symbols = [
            "🍎",
            "⭐",
            "🍋",
            "🍉",
            "🐱",
            "🚀",
            "🌙",
            "⚽"
        ]

        self.history = []

        self.title = tk.Label(
            window,
            text="MEMORY MATCH",
            font=("Arial", 28, "bold")
        )

        self.title.pack(pady=20)

        self.info = tk.Label(
            window,
            text="Memorize the cards...",
            font=("Arial", 14)
        )

        self.info.pack(pady=10)

        self.card_frame = tk.Frame(window)
        self.card_frame.pack(pady=30)

        self.cards = []

        for i in range(3):
            card = Card(self.card_frame)
            self.cards.append(card)

        self.score_label = tk.Label(
            window,
            text="Score: 0    Level: 1",
            font=("Arial", 14)
        )

        self.score_label.pack(pady=20)

        self.yes_button = tk.Button(
            window,
            text="YES →",
            font=("Arial", 14),
            width=10,
            command=lambda: self.answer(True)
        )

        self.yes_button.pack(side="right", padx=100)

        self.no_button = tk.Button(
            window,
            text="← NO",
            font=("Arial", 14),
            width=10,
            command=lambda: self.answer(False)
        )

        self.no_button.pack(side="left", padx=100)

        self.start_round()

    def start_round(self):

        self.yes_button.config(state="disabled")
        self.no_button.config(state="disabled")

        self.history = []

        for card in self.cards:
            symbol = random.choice(self.symbols)

            card.set_symbol(symbol)

            self.history.append(symbol)

            card.show()

        self.info.config(text="Memorize the symbols...")

        self.window.after(2500, self.hide_cards)

    def hide_cards(self):

        for card in self.cards:
            card.hide()

        self.info.config(
            text="Does the new symbol match the symbol two cards ago?"
        )

        self.next_card()

    def next_card(self):

        new_symbol = random.choice(self.symbols)

        self.history.append(new_symbol)

        self.cards[0].set_symbol(self.history[-3])
        self.cards[1].set_symbol(self.history[-2])
        self.cards[2].set_symbol(self.history[-1])

        self.cards[0].hide()
        self.cards[1].hide()

        self.cards[2].show()

        self.yes_button.config(state="normal")
        self.no_button.config(state="normal")

    def answer(self, answer):

        old_symbol = self.history[-3]
        current_symbol = self.history[-1]

        correct = old_symbol == current_symbol

        if answer == correct:

            self.score += 50 * self.level
            self.correct_answers += 1

            self.info.config(
                text="Correct! 🎉"
            )

            if self.correct_answers == 4:
                self.level += 1
                self.correct_answers = 0

        else:

            self.info.config(
                text="Wrong! ❌"
            )

            self.correct_answers = 0

        self.score_label.config(
            text=f"Score: {self.score}    Level: {self.level}"
        )

        self.yes_button.config(state="disabled")
        self.no_button.config(state="disabled")

        self.window.after(1000, self.next_round)

    def next_round(self):

        self.next_card()


window = tk.Tk()

window.title("Memory Match")

window.geometry("800x600")

game = Game(window)

window.mainloop()