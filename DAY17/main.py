import random
from colorama import Fore, Style, init

# colorama set up windows
init()

#colors for the branches
color_options = [Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.RED]

def draw_tree(branch_count, current_depth, max_depth):
    if current_depth > max_depth:
        return
    
    for _ in range(branch_count):
        branch_length = random.randint(3, 7)
        branch_angle = random.choice(['/', '\\'])
        
        branch_color = random.choice(color_options)
        
        print(' ' * current_depth + branch_color + branch_angle * branch_length + Style.RESET_ALL)
        
        draw_tree(random.randint(1, 2), current_depth + 1, max_depth)

def main():
    print(Fore.LIGHTBLUE_EX + "🌳 Fractal ASCII Tree Maker!" + Style.RESET_ALL)
    
    try:
        depth = int(input("How deep do you want the tree? (like, 5): "))
        if depth < 1:
            print(Fore.RED + "Bro, depth has to be at least 1!" + Style.RESET_ALL)
            return
        
        base_branches = random.randint(2, 4)
        print("\nHang tight, generating your tree...\n")
        
        draw_tree(base_branches, 0, depth)
        
        print(Fore.LIGHTGREEN_EX + "\nBoom! Your tree is ready! 🌲" + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Oops! That doesn't look like a number. Try again!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
