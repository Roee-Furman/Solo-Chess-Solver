import os
import sys
import time
import threading
import itertools

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def algebraic_to_coord(sq):
    return ord(sq[0].lower()) - ord('a'), int(sq[1]) - 1

def coord_to_algebraic(x, y):
    return chr(x + ord('a')) + str(y + 1)

def is_clear_path(start_x, start_y, end_x, end_y, board_positions):
    dx = end_x - start_x
    dy = end_y - start_y
    step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
    
    curr_x, curr_y = start_x + step_x, start_y + step_y
    while (curr_x, curr_y) != (end_x, end_y):
        if (curr_x, curr_y) in board_positions:
            return False
        curr_x += step_x
        curr_y += step_y
    return True

def can_capture(p1, p2, board_positions):
    type1, x1, y1, cap_count = p1
    type2, x2, y2, _ = p2
    
    if type2 == 'K':
        return False
    
    if cap_count >= 2:
        return False
        
    dx = x2 - x1
    dy = y2 - y1
    
    valid_move = False
    requires_path_check = False
    
    if type1 == 'K':
        valid_move = max(abs(dx), abs(dy)) == 1
    elif type1 == 'N':
        valid_move = (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)
    elif type1 == 'R':
        valid_move = (dx == 0 and dy != 0) or (dx != 0 and dy == 0)
        requires_path_check = True
    elif type1 == 'B':
        valid_move = abs(dx) == abs(dy) and dx != 0
        requires_path_check = True
    elif type1 == 'Q':
        valid_move = ((dx == 0 and dy != 0) or (dx != 0 and dy == 0)) or (abs(dx) == abs(dy) and dx != 0)
        requires_path_check = True
    elif type1 == 'P':
        valid_move = abs(dx) == 1 and dy == 1
        
    if not valid_move:
        return False
        
    if requires_path_check:
        if not is_clear_path(x1, y1, x2, y2, board_positions):
            return False
            
    return True

def format_move_notation(p1, p2, pieces, board_positions):
    type1, x1, y1, _ = p1
    _, x2, y2, _ = p2
    
    origin = coord_to_algebraic(x1, y1)
    dest = coord_to_algebraic(x2, y2)
    
    if type1 == 'P':
        return f"{origin[0]}x{dest}"
    
    ambiguous = [
        p for p in pieces 
        if p != p1 and p[0] == type1 and can_capture(p, p2, board_positions)
    ]
    
    disambiguation = ""
    if ambiguous:
        same_file = any(p[1] == x1 for p in ambiguous)
        same_rank = any(p[2] == y1 for p in ambiguous)
        
        if not same_file:
            disambiguation = origin[0]
        elif not same_rank:
            disambiguation = origin[1]
        else:
            disambiguation = origin
            
    return f"{type1}{disambiguation}x{dest}"

def solve(pieces, memo=None):
    if memo is None:
        memo = set()
        
    state_signature = tuple(sorted(pieces))
    if state_signature in memo:
        return None
    memo.add(state_signature)

    if len(pieces) == 1:
        return []
        
    board_positions = {(x, y) for _, x, y, _ in pieces}
    
    for i, p1 in enumerate(pieces):
        for j, p2 in enumerate(pieces):
            if i == j:
                continue
                
            if can_capture(p1, p2, board_positions):
                type1, x1, y1, cap1 = p1
                _, x2, y2, _ = p2
                
                move_str = format_move_notation(p1, p2, pieces, board_positions)
                
                new_p1 = (type1, x2, y2, cap1 + 1)
                new_pieces = tuple(p for idx, p in enumerate(pieces) if idx not in (i, j)) + (new_p1,)
                
                result = solve(new_pieces, memo)
                if result is not None:
                    return [move_str] + result
                    
    return None

def parse_input(input_str):
    pieces = []
    tokens = input_str.strip().split()
    for token in tokens:
        t = token.strip()
        if len(t) == 2:
            p_type = 'P'
            sq = t
        elif len(t) == 3:
            p_type = t[0].upper()
            if p_type not in 'KNQRBP':
                raise ValueError(f"Unknown piece type: '{p_type}'")
            sq = t[1:3]
        else:
            raise ValueError(f"Invalid piece format: '{t}'")
            
        x, y = algebraic_to_coord(sq)
        if not (0 <= x < 8 and 0 <= y < 8):
            raise ValueError(f"Square out of bounds: '{sq}'")
            
        pieces.append((p_type, x, y, 0))
        
    return tuple(pieces)

def animate_loading(stop_event):
    dot_frames = ['Calculating', 'Calculating .', 'Calculating . .', 'Calculating . . .']
    calc_frames = dot_frames * 6 + ['This might take a while'] * 4
    max_len = max(len(frame) for frame in calc_frames)
    
    for frame in itertools.cycle(calc_frames):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{frame:<{max_len}}')
        sys.stdout.flush()
        time.sleep(0.1)
        
    sys.stdout.write('\r' + ' ' * max_len + '\r')
    sys.stdout.flush()

def main():
    while True:
        clear_screen()
        print("                 Solo Chess Solver v1              ")
        print("Format example: Bf4 e3 Kc6 Rc5 (Leave blank to exit)\n")
        
        try:
            user_input = input("Pieces:\n")
            if not user_input.strip():
                break
                
            pieces = parse_input(user_input)
            
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=animate_loading, args=(stop_event,))
            spinner_thread.start()
            
            try:
                solution = solve(pieces)
            finally:
                stop_event.set()
                spinner_thread.join()
            
            if solution:
                print("Solution:\n")
                for i, move in enumerate(solution, 1):
                    print(f"{i}. {move}\n")
            else:
                print("No solution found.")
                
            input("Press Enter to solve another position.")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to try again.")

if __name__ == "__main__":
    main()
