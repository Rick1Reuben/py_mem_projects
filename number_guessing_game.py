import random

def number_guess_game():
    print("Welcome to the Number Guessing Game!")
    
    while True:
        # Choose difficulty
        print("\nChoose difficulty level:")
        print("1. Easy (1 to 50)")
        print("2. Medium (1 to 100)")
        print("3. Hard (1 to 200)")
        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            max_number = 50
        elif choice == "2":
            max_number = 100
        elif choice == "3":
            max_number = 200
        else:
            print("Invalid choice. Defaulting to Medium.")
            max_number = 100

        secret_number = random.randint(1, max_number)
        attempts = 0
        guess = None

        print(f"\nI'm thinking of a number between 1 and {max_number}. Can you guess it?")

        while guess != secret_number:
            try:
                guess = int(input("Enter your guess: "))
                attempts += 1

                if guess < secret_number:
                    print("Too low! Try again.")
                elif guess > secret_number:
                    print("Too high! Try again.")
                else:
                    print(f"🎉 Congratulations! You guessed the number in {attempts} attempts!")
            except ValueError:
                print("⚠️ Please enter a valid number!")

        # Ask to play again
        while True:
            play_again = input("\nDo you want to play again? (y/n): ").lower()
            if play_again == 'y':
                break  # Breaks out of this small loop, continues main game loop
            elif play_again == 'n':
                print("Thanks for playing! Goodbye!")
                return  # Exits the entire function
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

# Run the game
number_guess_game()
