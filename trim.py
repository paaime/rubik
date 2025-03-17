def replace_move(sequence, move, i):
    """Concatenates 2 consecutive moves e.g. "U U" => "U2" """
    if move == "":
        trimmed = sequence[:i]
    else:
        trimmed = sequence[:i] + [move]
    
    if i + 2 < len(sequence):
        trimmed.extend(sequence[i+2:])
    
    return trimmed

def replace_move2(sequence, move, i):
    """Concatenates 2 non-consecutive moves e.g. "U D U" => "U2 D" """
    trimmed = sequence[:i]
    
    if move != "":
        trimmed.append(move)
    
    trimmed.append(sequence[i + 1])
    
    if i + 3 < len(sequence):
        trimmed.extend(sequence[i+3:])
    
    return trimmed

def assign_moves(move_char):
    """Returns quarter, anti, half, and opposite moves for a given face"""
    if move_char == 'U':
        quarter = "U"
        anti = "U'"
        half = "U2"
        opposite = 'D'
    elif move_char == 'D':
        quarter = "D"
        anti = "D'"
        half = "D2"
        opposite = 'U'
    elif move_char == 'R':
        quarter = "R"
        anti = "R'"
        half = "R2"
        opposite = 'L'
    elif move_char == 'L':
        quarter = "L"
        anti = "L'"
        half = "L2"
        opposite = 'R'
    elif move_char == 'F':
        quarter = "F"
        anti = "F'"
        half = "F2"
        opposite = 'B'
    else:  # move_char = 'B'
        quarter = "B"
        anti = "B'"
        half = "B2"
        opposite = 'F'
    
    return quarter, anti, half, opposite

def trim_sequence(sequence):
    """Concatenates redundant moves, e.g. "U U" => "U2" """
    trimmed = sequence.split()
    
    i = 0
    while i < len(trimmed) - 1:
        move = trimmed[i]
        if i + 1 < len(trimmed):
            quarter, anti, half, opposite = assign_moves(move[0])
            
            if move == quarter:
                if trimmed[i + 1] == quarter:
                    trimmed = replace_move(trimmed, half, i)
                elif trimmed[i + 1] == anti:
                    trimmed = replace_move(trimmed, "", i)
                elif trimmed[i + 1] == half:
                    trimmed = replace_move(trimmed, anti, i)
                elif trimmed[i + 1][0] == opposite and i + 2 < len(trimmed):
                    if trimmed[i + 2] == quarter:
                        trimmed = replace_move2(trimmed, half, i)
                    elif trimmed[i + 2] == anti:
                        trimmed = replace_move2(trimmed, "", i)
                    elif trimmed[i + 2] == half:
                        trimmed = replace_move2(trimmed, anti, i)
                    else:
                        i += 1
                else:
                    i += 1
            elif move == anti:
                if trimmed[i + 1] == quarter:
                    trimmed = replace_move(trimmed, "", i)
                elif trimmed[i + 1] == anti:
                    trimmed = replace_move(trimmed, half, i)
                elif trimmed[i + 1] == half:
                    trimmed = replace_move(trimmed, quarter, i)
                elif trimmed[i + 1][0] == opposite and i + 2 < len(trimmed):
                    if trimmed[i + 2] == quarter:
                        trimmed = replace_move2(trimmed, "", i)
                    elif trimmed[i + 2] == anti:
                        trimmed = replace_move2(trimmed, half, i)
                    elif trimmed[i + 2] == half:
                        trimmed = replace_move2(trimmed, quarter, i)
                    else:
                        i += 1
                else:
                    i += 1
            elif move == half:
                if trimmed[i + 1] == quarter:
                    trimmed = replace_move(trimmed, anti, i)
                elif trimmed[i + 1] == anti:
                    trimmed = replace_move(trimmed, quarter, i)
                elif trimmed[i + 1] == half:
                    trimmed = replace_move(trimmed, "", i)
                elif trimmed[i + 1][0] == opposite and i + 2 < len(trimmed):
                    if trimmed[i + 2] == quarter:
                        trimmed = replace_move2(trimmed, anti, i)
                    elif trimmed[i + 2] == anti:
                        trimmed = replace_move2(trimmed, quarter, i)
                    elif trimmed[i + 2] == half:
                        trimmed = replace_move2(trimmed, "", i)
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1
    
    trimmed_string = " ".join(trimmed)
    if trimmed_string:
        trimmed_string += " "
    
    return trimmed_string

def trim(sequence):
    """Concatenates redundant moves to minimize Half Turn Metric"""
    previous = ""
    current = sequence
    
    while previous != current:
        previous = current
        current = trim_sequence(current)
    
    return current.strip()