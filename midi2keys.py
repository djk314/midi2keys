import json
import os
import mido
from tkinter import Tk, Label, Button, Entry, StringVar, OptionMenu
from pynput.keyboard import Controller, Key

# Initialize the keyboard controller
keyboard = Controller()

# Default dictionary to map notes to MIDI numbers
note_to_midi = {
    'C0': 12, 'C#0': 13, 'D0': 14, 'D#0': 15, 'E0': 16, 'F0': 17, 'F#0': 18, 'G0': 19, 'G#0': 20, 'A0': 21, 'A#0': 22, 'B0': 23,
    'C1': 24, 'C#1': 25, 'D1': 26, 'D#1': 27, 'E1': 28, 'F1': 29, 'F#1': 30, 'G1': 31, 'G#1': 32, 'A1': 33, 'A#1': 34, 'B1': 35,
    'C2': 36, 'C#2': 37, 'D2': 38, 'D#2': 39, 'E2': 40, 'F2': 41, 'F#2': 42, 'G2': 43, 'G#2': 44, 'A2': 45, 'A#2': 46, 'B2': 47,
    'C3': 48, 'C#3': 49, 'D3': 50, 'D#3': 51, 'E3': 52, 'F3': 53, 'F#3': 54, 'G3': 55, 'G#3': 56, 'A3': 57, 'A#3': 58, 'B3': 59,
    'C4': 60, 'C#4': 61, 'D4': 62, 'D#4': 63, 'E4': 64, 'F4': 65, 'F#4': 66, 'G4': 67, 'G#4': 68, 'A4': 69, 'A#4': 70, 'B4': 71,
    'C5': 72, 'C#5': 73, 'D5': 74, 'D#5': 75, 'E5': 76, 'F5': 77, 'F#5': 78, 'G5': 79, 'G#5': 80, 'A5': 81, 'A#5': 82, 'B5': 83,
    'C6': 84, 'C#6': 85, 'D6': 86, 'D#6': 87, 'E6': 88, 'F6': 89, 'F#6': 90, 'G6': 91, 'G#6': 92, 'A6': 93, 'A#6': 94, 'B6': 95,
    'C7': 96, 'C#7': 97, 'D7': 98, 'D#7': 99, 'E7': 100, 'F7': 101, 'F#7': 102, 'G7': 103, 'G#7': 104, 'A7': 105, 'A#7': 106, 'B7': 107,
    'C8': 108
    }
# Charger les données depuis le fichier de configuration
def load_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':')
                key = key.strip()
                value = value.strip()
                # Convertir la clé et la valeur en Python types
                key = eval(key)
                value = eval(value)
                config[key] = value
    return config


# Utiliser la fonction pour charger les données
mappings_notes = load_config('mappings_notes.txt')
mappings_controls = load_config('mappings_controls.txt')

# Afficher les données

midi_to_shortcut = mappings_controls
midi_note_to_shortcut = mappings_notes


# Handle incoming MIDI messages
def on_midi_message(message):
    if message.type == 'control_change':
        control_number = message.control
        value = message.value
        print(f"Received Control Change: Control {control_number}, Value {value}")
        key_combination = midi_to_shortcut.get((control_number, value)) or midi_to_shortcut.get(control_number)
        if key_combination:
            # Simulate key shortcuts
            for key in key_combination:
                keyboard.press(key)
            for key in reversed(key_combination):
                keyboard.release(key)
            print(f"Shortcut {key_combination} executed for Control {control_number} with a value of {value}.")
    elif message.type == 'note_on' or message.type == 'note_off':
        note = message.note
        velocity = message.velocity
        note_name = next((name for name, number in note_to_midi.items() if number == note), None)
        print(f"Received {message.type}: Note {note_name} ({note}), Velocity {velocity}")
        key_combination = midi_note_to_shortcut.get((note_name, velocity))
        if key_combination:
            # Simulate key shortcuts
            for key in key_combination:
                keyboard.press(key)
            for key in reversed(key_combination):
                keyboard.release(key)
            print(f"Shortcut {key_combination} executed for Note {note_name} with velocity of {velocity}.")

# Default MIDI port
default_port = 'X-Touch INT'

class MidiToKeyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MIDI to Key Mapper")

        # MIDI port selector
        Label(master, text="Select MIDI Port:").pack()
        self.selected_port = StringVar(master)
        self.selected_port.set("X-Touch INT")
        self.midi_ports = mido.get_input_names()
        OptionMenu(master, self.selected_port, *self.midi_ports).pack()

        # Start MIDI Listening Button
        Button(master, text="Start MIDI Listening", command=self.start_midi_listening).pack()
        #Bouton pour arrêter l'écoute MIDI
        Button(master, text="Stop MIDI Listening", command=self.stop_midi_listening).pack()
    def start_midi_listening(self):
        port_name = self.selected_port.get()
        if port_name == "Select MIDI Port":
            print("Please select a valid MIDI port.")
            return
        self.midi_in = mido.open_input(port_name, callback=on_midi_message)
        print(f"Started listening on {port_name}")
        
    def stop_midi_listening(self):
        if self.midi_in:
            self.midi_in.close()  # Fermer le port MIDI
            print("Stopped MIDI Listening")
        else:
            print("MIDI Listening not started yet or already stopped")

if __name__ == "__main__":
    root = Tk()
    app = MidiToKeyApp(root)
    root.mainloop()
