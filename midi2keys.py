import mido
from pynput.keyboard import Controller, Key

# init keyboard control
keyboard = Controller()

# # Dictionary to map number to notes

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

# map Control Change (CC) numbers to keyboard shortcuts
midi_to_shortcut = {
    (60, 1): [Key.shift, Key.right],  # Shift + Right Arrow jog right valeur 1
    (60, 65): [Key.shift, Key.left],  # Shift + Left Arrow jog left valeur 65
    61: [Key.ctrl, 'c'],         # Ctrl + C (copier) pour toutes les valeurs
    62: [Key.ctrl, 'v'],         # Ctrl + V (coller) pour toutes les valeurs
    # Add mappings here
}

  # midi notes
midi_note_to_shortcut = {
    ('D#7', 127): [')'],  # Shift + Right Arrow pour Note C5 avec vélocité 127
    ('D7', 127): ['-'],         # Ctrl + C pour Note C#5 avec vélocité 127
    ('A#2', 127): ['i'],         # Ctrl + C pour Note C#5 avec vélocité 127
    ('B2', 127): ['o'],         # Ctrl + C pour Note C#5 avec vélocité 127
    ('C3', 127): ['p'],         # Ctrl + C pour Note C#5 avec vélocité 127
    ('A6', 127): ['j'],         # stop buton C#5 avec vélocité 127
    ('A#6', 127): [Key.alt, 'e'],         # play buton C#5 avec vélocité 127
    ('G#6', 127): ['r'],         # ff buton C#5 avec vélocité 127
    ('G6', 127): ['a'],         # rff buton C#5 avec vélocité 127

    ('D5', 127): [Key.ctrl, 'v'],         # Ctrl + V pour Note D5 avec vélocité 127
    # Add mappings here
}

def on_midi_message(message):
    if message.type == 'control_change':
        control_number = message.control
        value = message.value
        print(f"Received Control Change: Control {control_number}, Value {value}")
        key_combination = midi_to_shortcut.get((control_number, value)) or midi_to_shortcut.get(control_number)
        if key_combination:
            # simulated key shortcuts
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
            # Simulated key shortcuts
            for key in key_combination:
                keyboard.press(key)
            for key in reversed(key_combination):
                keyboard.release(key)
            print(f"Shortcut {key_combination} executed for Note {note_name} with velocity of {velocity}.")

# default midi port
default_port = 'X-Touch INT'

# List  Midi ports MIDI
print("MIDI ports available:")
ports = mido.get_input_names()
for port in ports:
    print(port)

# check if default port aiviable
if default_port in ports:
    selected_port = default_port
else:
    # if not select other port
    selected_port = input("Select a MIDI port: ")

# open selected port
with mido.open_input(selected_port) as inport:
    print(f"MIDI port used: {selected_port}")
    print("wait for MIDI message...")
    for message in inport:
        print(f"Midi Message received: {message}")
        on_midi_message(message)
