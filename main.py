import random
import tkinter as tk
from pathlib import Path
from game_logic import GameState

WINDOW_BG = "#10254b"
PANEL_BG = "#142f5d"
TEXT = "#f5f8ff"
MUTED = "#a9c7ef"
GREEN = "#26c58b"
RED = "#f14b68"
CARD_NAMES = ["star", "heart", "triangle", "diamond", "circle", "sun", "flower", "moon", "bolt"]
MEMORIZE_MS = 2500
NEXT_ROUND_MS = 900

class MemoryMatchGame:
    """Tkinter user interface. The rules themselves live in GameState."""
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match")
        self.root.geometry("900x650")
        self.root.minsize(820, 600)
        self.root.configure(bg=WINDOW_BG)
        self.asset_dir = Path(__file__).parent / "assets" / "cards"
        self.card_images = {name: tk.PhotoImage(file=str(self.asset_dir/f"{name}.png")) for name in CARD_NAMES}
        self.card_back = tk.PhotoImage(file=str(self.asset_dir/"back.png"))
        self.state = GameState([random.choice(CARD_NAMES) for _ in range(3)])
        self.input_enabled = False
        self.pending_after_id = None
        self.feedback = "Press Start / Restart to play."
        self.create_ui()
        self.bind_keys()
        self.update_ui()

    def create_ui(self):
        header = tk.Frame(self.root, bg=WINDOW_BG); header.pack(fill="x", padx=28, pady=(20,12))
        tk.Label(header,text="🧠  Memory Match",font=("Segoe UI",25,"bold"),bg=WINDOW_BG,fg=TEXT).pack(side="left")
        tk.Label(header,text="Remember the symbols. Match the card from two cards ago.",font=("Segoe UI",10),bg=WINDOW_BG,fg=MUTED).pack(side="left",padx=18,pady=(10,0))
        stats=tk.Frame(self.root,bg=WINDOW_BG); stats.pack(fill="x",padx=28,pady=(0,14))
        self.score_label=self.make_stat(stats,"SCORE","0"); self.level_label=self.make_stat(stats,"LEVEL","1")
        pf=tk.Frame(stats,bg=PANEL_BG,padx=16,pady=10); pf.pack(side="right",padx=(8,0))
        tk.Label(pf,text="PROGRESS",bg=PANEL_BG,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
        dots=tk.Frame(pf,bg=PANEL_BG); dots.pack(pady=(6,0)); self.dot_labels=[]
        for _ in range(4):
            dot=tk.Label(dots,text="●",font=("Segoe UI",13),fg="#47658e",bg=PANEL_BG); dot.pack(side="left",padx=4); self.dot_labels.append(dot)
        panel=tk.Frame(self.root,bg=PANEL_BG,padx=22,pady=18); panel.pack(fill="both",expand=True,padx=28,pady=(0,12))
        row=tk.Frame(panel,bg=PANEL_BG); row.pack(pady=(4,8),expand=True); self.card_labels=[]
        for title in ["TWO CARDS AGO","PREVIOUS CARD","CURRENT CARD"]:
            col=tk.Frame(row,bg=PANEL_BG); col.pack(side="left",padx=16)
            label=tk.Label(col,bg=PANEL_BG,bd=0,image=self.card_back); label.pack(); self.card_labels.append(label)
            tk.Label(col,text=title,bg=PANEL_BG,fg=TEXT,font=("Segoe UI",10,"bold")).pack(pady=(9,0))
        self.feedback_label=tk.Label(panel,text="",bg="#193d72",fg="#b9e3ff",font=("Segoe UI",11,"bold"),padx=14,pady=10); self.feedback_label.pack(fill="x",pady=(0,14))
        controls=tk.Frame(panel,bg=PANEL_BG); controls.pack(fill="x",pady=(0,2))
        self.no_button=tk.Button(controls,text="←   NO",command=lambda:self.answer(False),font=("Segoe UI",15,"bold"),bg=RED,fg="white",activebackground="#d93855",activeforeground="white",relief="flat",bd=0,cursor="hand2",padx=22,pady=12); self.no_button.pack(side="left",expand=True,fill="x",padx=(0,8))
        middle=tk.Frame(controls,bg=PANEL_BG); middle.pack(side="left",padx=8)
        tk.Button(middle,text="↻  Start / Restart",command=self.start_game,font=("Segoe UI",10,"bold"),bg="#214f8c",fg=TEXT,activebackground="#2d65a8",activeforeground="white",relief="flat",bd=0,cursor="hand2",padx=14,pady=10).pack(pady=(0,6))
        self.end_button=tk.Button(middle,text="■  End Session",command=self.end_session,font=("Segoe UI",9),bg="#25436e",fg=TEXT,activebackground="#355987",activeforeground="white",relief="flat",bd=0,cursor="hand2",padx=14,pady=7); self.end_button.pack()
        self.yes_button=tk.Button(controls,text="YES   →",command=lambda:self.answer(True),font=("Segoe UI",15,"bold"),bg=GREEN,fg="white",activebackground="#16a978",activeforeground="white",relief="flat",bd=0,cursor="hand2",padx=22,pady=12); self.yes_button.pack(side="right",expand=True,fill="x",padx=(8,0))
        tk.Label(self.root,text="Tip: use ← for NO and → for YES",bg=WINDOW_BG,fg="#789bc9",font=("Segoe UI",9)).pack(pady=(0,10))

    def make_stat(self,parent,heading,value):
        frame=tk.Frame(parent,bg=PANEL_BG,padx=20,pady=8); frame.pack(side="right",padx=(8,0))
        tk.Label(frame,text=heading,bg=PANEL_BG,fg=MUTED,font=("Segoe UI",9,"bold")).pack()
        label=tk.Label(frame,text=value,bg=PANEL_BG,fg=TEXT,font=("Segoe UI",18,"bold")); label.pack(); return label

    def bind_keys(self):
        self.root.bind("<Left>",lambda event:self.answer(False)); self.root.bind("<Right>",lambda event:self.answer(True))

    def start_game(self):
        self.cancel_pending_callback(); self.state=GameState([random.choice(CARD_NAMES) for _ in range(3)])
        self.input_enabled=False; self.feedback="Memorize all three symbols!"; self.update_ui()
        self.pending_after_id=self.root.after(MEMORIZE_MS,self.begin_play)

    def begin_play(self):
        self.pending_after_id=None
        if self.state.game_active:
            self.input_enabled=True; self.state.revealed_all=False
            self.feedback="Does the current card match the card two positions ago?"; self.update_ui()

    def answer(self,said_match):
        if not self.state.game_active or not self.input_enabled: return
        self.input_enabled=False; correct=self.state.submit_answer(said_match,random.choice(CARD_NAMES))
        self.feedback="Correct!" if correct else "Not quite. Study the revealed cards and try again."
        if correct and self.state.progress==0: self.feedback=f"Great streak! Welcome to level {self.state.level}!"
        self.update_ui(); self.pending_after_id=self.root.after(NEXT_ROUND_MS,self.enable_next_answer)

    def enable_next_answer(self):
        self.pending_after_id=None
        if self.state.game_active:
            self.input_enabled=True
            if not self.state.revealed_all: self.feedback="Does the current card match the card two positions ago?"
            self.update_ui()

    def end_session(self):
        self.cancel_pending_callback(); bonus=self.state.end_session(); self.input_enabled=False
        self.feedback=f"Session complete! +{bonus} level bonus. Final score: {self.state.score}."; self.update_ui()

    def cancel_pending_callback(self):
        if self.pending_after_id is not None:
            try: self.root.after_cancel(self.pending_after_id)
            except tk.TclError: pass
            self.pending_after_id=None

    def update_ui(self):
        self.score_label.config(text=str(self.state.score)); self.level_label.config(text=str(self.state.level))
        for i,dot in enumerate(self.dot_labels): dot.config(fg="#63c7ff" if i<self.state.progress else "#47658e")
        for i,label in enumerate(self.card_labels):
            if self.state.revealed_all or i==2: label.config(image=self.card_images[self.state.cards[i]])
            else: label.config(image=self.card_back)
        self.feedback_label.config(text=self.feedback)
        button_state="normal" if self.state.game_active and self.input_enabled else "disabled"
        self.no_button.config(state=button_state); self.yes_button.config(state=button_state)
        self.end_button.config(state="normal" if self.state.game_active else "disabled")

    def run(self): self.root.mainloop()

if __name__ == "__main__":
    root=tk.Tk(); MemoryMatchGame(root).run()
