import random
import time

def roll_dice():
    return random.randint(1, 6)

# Dice face symbols
dice_faces = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚄",
    6: "⚅"
}

# 🧮 Tracking Variables
total_dice_rolled = 0
total_sessions = 0
roll_counts = {i: 0 for i in range(1, 7)}
highest_roll = 1
lowest_roll = 6

while True:
    user_input = input("Roll the dice? (y/n): ")

    if user_input.lower() == "y":
        try:
            num_dice = int(input("How many dice would you like to roll? "))
            if num_dice < 1:
                print("Please enter a number greater than 0.")
                continue
        except ValueError:
            print("That's not a valid number.")
            continue

        print("Rolling...")
        time.sleep(1)

        rolls = [roll_dice() for _ in range(num_dice)]
        roll_output = [f"{value} {dice_faces[value]}" for value in rolls]
        print("You rolled:", ", ".join(roll_output))

        # 🧠 Update stats
        total_sessions += 1
        total_dice_rolled += num_dice

        for value in rolls:
            roll_counts[value] += 1
            if value > highest_roll:
                highest_roll = value
            if value < lowest_roll:
                lowest_roll = value

        # 📊 Show stats
        print(f"\n🎯 Total dice rolled: {total_dice_rolled}")
        print(f"🔁 Total roll sessions: {total_sessions}")
        print("📊 Roll counts:")
        for i in range(1, 7):
            print(f"  {i} {dice_faces[i]}: {roll_counts[i]}")
        print(f"⬆️ Highest roll so far: {highest_roll}")
        print(f"⬇️ Lowest roll so far: {lowest_roll}\n")

    elif user_input.lower() == "n":
        print("\n🎉 Final Stats:")
        print(f"🎯 Total dice rolled: {total_dice_rolled}")
        print(f"🔁 Total roll sessions: {total_sessions}")
        print("📊 Final roll counts:")
        for i in range(1, 7):
            print(f"  {i} {dice_faces[i]}: {roll_counts[i]}")
        print(f"⬆️ Highest roll: {highest_roll}")
        print(f"⬇️ Lowest roll: {lowest_roll}")
        print("Goodbye!")
        break
    else:
        print("Invalid input. Please try again.")
