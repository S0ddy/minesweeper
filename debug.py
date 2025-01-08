from minesweeper import MinesweeperAI

def print_ai_status():
    print(f'\nAfter move:{move} with nearby_count:{nearby_count}')
    if ai.knowledge:
        print('Sentences in Knowledge Base:')
        for cnt, s in enumerate(ai.knowledge):
            print(f'{cnt}: {s}')
    else:
        print('NO Sentences in Knowledge Base.')       
    print(f'Safe Cells: {sorted(list(ai.safes))}')
    print(f'Mine Cells: {sorted(list(ai.mines))}')    
    
# Create AI agent
HEIGHT, WIDTH, MINES = 8, 8, 8
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Test new sentence logic (3rd requirement)
move, nearby_count = (2,3), 0
ai.add_knowledge(move,nearby_count)
print_ai_status()

move, nearby_count = (2,4), 0
ai.add_knowledge(move,nearby_count)
print_ai_status()

# Test inference logic for new safes or mines (4th requirement)
move, nearby_count = (1,2), 1
ai.add_knowledge(move,nearby_count)
print_ai_status()

# Setup for new sentence inference logic test
move, nearby_count = (1,3), 2
ai.add_knowledge(move,nearby_count)
print_ai_status()

# # Tests subset inference logic for new sentences (5th requirement)
# move, nearby_count = (7,2), 2
# ai.add_knowledge(move,nearby_count)
# print_ai_status()

# move, nearby_count = (5,2), 1
# ai.add_knowledge(move,nearby_count)
# print_ai_status()