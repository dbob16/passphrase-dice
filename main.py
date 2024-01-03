import random as r
from sqlalchemy import create_engine # pip install sqlalchemy
from sqlalchemy.orm import Session, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql import func
import ttkbootstrap as ttk # pip install ttkbootstrap

engine = create_engine('sqlite://')
session = Session(engine)

class Base(DeclarativeBase):
    pass

class Word(Base):
    __tablename__ = 'words'
    diceseq:Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    word:Mapped[str]

Base.metadata.create_all(engine)

wordlist = open("wordlist.txt", "r")
lines = wordlist.readlines()

for line in lines:
    seperated = line.split()
    wordline = Word(diceseq=seperated[0], word=seperated[-1])
    session.add(wordline)

session.commit()

window = ttk.Window(title="Password Dice", themename="cyborg", resizable=(False, False))
# Variables
v_diceseq = ttk.IntVar()
v_digitnum = ttk.IntVar()
v_output = ttk.StringVar()
v_passphrase = ttk.StringVar()

# Commands
def cmd_passphrase_add(word:str):
    if v_passphrase.get() == "":
        v_passphrase.set(word)
    else:
        v_passphrase.set(f"{v_passphrase.get()} {word}")

def cmd_clear_passphrase():
    v_passphrase.set("")

def cmd_lookup():
    try:
        result = session.query(Word).filter(Word.diceseq == v_diceseq.get()).one()
        v_output.set(result.word)
        cmd_passphrase_add(result.word)
    except:
        v_output.set("Result not found")

def cmd_random():
    result = session.query(Word).order_by(func.random()).limit(1).one()
    v_diceseq.set(result.diceseq)
    v_output.set(result.word)
    cmd_passphrase_add(result.word)

def cmd_digitnum():
    inum = v_digitnum.get()
    finstring = ""
    while inum > 0:
        ranstring = str(r.randint(0, 9))
        finstring += ranstring
        inum = inum - 1
    v_output.set(finstring)
    cmd_passphrase_add(finstring)

def cmd_copy():
    window.clipboard_clear()
    window.clipboard_append(v_passphrase.get())

# Frames
frm_top = ttk.LabelFrame(text="Dice Lookup")
frm_top.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

frm_commands = ttk.LabelFrame(text="Other Functions")
frm_commands.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

frm_output = ttk.LabelFrame(text="Output")
frm_output.grid(row=2, column=0, padx=4, pady=4, sticky="nsew")

frm_passphrase = ttk.LabelFrame(text="Passphrase")
frm_passphrase.grid(row=3, column=0, padx=4, pady=4, sticky="nsew")

# Top Frame
txt_diceseq = ttk.Entry(frm_top, textvariable=v_diceseq)
txt_diceseq.pack(side="left", padx=4, pady=4)

btn_lookup = ttk.Button(frm_top, text="Lookup", command=cmd_lookup)
btn_lookup.pack(side="left", padx=4, pady=4)

# Commands Frame
btn_randomize = ttk.Button(frm_commands, text="Randomize", command=cmd_random)
btn_randomize.pack(side="left", padx=4, pady=4)

btn_clear_passphrase = ttk.Button(frm_commands, text="Clear Passphrase", command=cmd_clear_passphrase)
btn_clear_passphrase.pack(side="left", padx=4, pady=4)

txt_digitnum = ttk.Entry(frm_commands, textvariable=v_digitnum, width=2)
txt_digitnum.pack(side="left", padx=4, pady=4)

btn_digitnum = ttk.Button(frm_commands, text="Digit Number", command=cmd_digitnum)
btn_digitnum.pack(side="left", padx=4, pady=4)

btn_copy = ttk.Button(frm_commands, text="Copy", command=cmd_copy)
btn_copy.pack(side="left", padx=4, pady=4)

# Output Frame
lbl_output = ttk.Label(frm_output, textvariable=v_output)
lbl_output.pack(side="left", padx=4, pady=4)

# Passphrase Frame
lbl_passphrase = ttk.Label(frm_passphrase, textvariable=v_passphrase)
lbl_passphrase.pack(side="left", fill="both", padx=4, pady=4)

window.mainloop()