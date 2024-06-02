I'm not a programmer, i used an LLM to help me. I own a Behringer Xtouch and i use it with Davinci Resolve.
To change controler and key shortcuts just edit the python script.
# map Control Change (CC) numbers to keyboard shortcuts
midi_to_shortcut = {
    (60, 1): [Key.shift, Key.right],  # Shift + Right Arrow jog right valeur 1

    # Add mappings here
}

  # midi notes
midi_note_to_shortcut = {
    ('D#7', 127): [')'],  # Shift + Right Arrow pour Note C5 avec vélocité 127

    # Add mappings here
}
these configs can be added in two separate files named mappings.
Default midi port is X-Touch INT can be changed in python file or in interface if the 
interface start (if no port it crash).
To start click on Start Midi Listening, can be stopped too.
That's all for now it work fine for me.
