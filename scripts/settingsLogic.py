buttons = {
    'a': False,
    'b': False, 
    'c': False,
    'd': False,
    'e': False,
    'f': False,
    's': False
}

def set_active_button(key):
    for keyName in buttons:
        if keyName == key and buttons[keyName] == True:
            buttons[keyName] = False
            break
        buttons[keyName] = False
        if keyName == key:
            buttons[keyName] = True
    if any(buttons.values()):
        return key
    else:
        return False