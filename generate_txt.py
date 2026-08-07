import random
import re

questions_data = [
    ("Mathematics", "Easy", "What is 15 x 4?", "45", "50", "60", "65", "C", "15 multiplied by 4 equals 60."),
    ("Science", "Medium", "Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "Mars is known as the Red Planet due to iron oxide on its surface."),
    ("Science", "Hard", "What is the powerhouse of the cell?", "Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum", "B", "Mitochondria generate most of the chemical energy needed to power the cell's biochemical reactions."),
    ("Computer", "Easy", "What does CPU stand for?", "Central Process Unit", "Computer Personal Unit", "Central Processing Unit", "Central Processor Unit", "C", "CPU stands for Central Processing Unit."),
    ("General Knowledge", "Medium", "Who wrote the Indian National Anthem?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Mahatma Gandhi", "Subhas Chandra Bose", "A", "Rabindranath Tagore wrote Jana Gana Mana."),
    ("History", "Hard", "In which year did India gain independence?", "1945", "1947", "1950", "1952", "B", "India gained independence from British rule in 1947."),
    ("Geography", "Medium", "What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", "C", "Canberra is the capital city of Australia."),
    ("Science", "Easy", "What is the chemical symbol for water?", "H2O", "O2", "CO2", "HO", "A", "Water is composed of two hydrogen atoms and one oxygen atom."),
    ("Sports", "Medium", "In which sport is the term 'LBW' used?", "Football", "Cricket", "Tennis", "Baseball", "B", "LBW stands for Leg Before Wicket in Cricket."),
    ("Mathematics", "Hard", "What is the square root of 144?", "10", "12", "14", "16", "B", "12 multiplied by 12 equals 144."),
    ("Science", "Medium", "What gas do plants absorb from the atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "C", "Plants absorb Carbon Dioxide for photosynthesis."),
    ("Computer", "Hard", "Which programming language is known as the mother of all languages?", "Java", "Python", "C", "C++", "C", "C is considered the mother of all programming languages."),
    ("General Knowledge", "Easy", "Which is the largest continent in the world?", "Africa", "Asia", "Europe", "North America", "B", "Asia is the largest continent by land area."),
    ("History", "Medium", "Who was the first Prime Minister of India?", "Sardar Patel", "Jawaharlal Nehru", "Indira Gandhi", "Lal Bahadur Shastri", "B", "Jawaharlal Nehru was the first PM of independent India."),
    ("Geography", "Hard", "Which is the longest river in the world?", "Amazon", "Nile", "Yangtze", "Mississippi", "B", "The Nile is traditionally considered the longest river in the world."),
    ("Mathematics", "Medium", "What is 25% of 200?", "25", "50", "75", "100", "B", "25% is one-quarter, and one-quarter of 200 is 50."),
    ("Sports", "Easy", "How many players are there in a cricket team?", "9", "10", "11", "12", "C", "A cricket team consists of 11 players."),
    ("Science", "Hard", "What is the hardest natural substance on Earth?", "Gold", "Iron", "Diamond", "Platinum", "C", "Diamond is the hardest known natural material."),
    ("Computer", "Medium", "What does HTML stand for?", "Hyper Text Markup Language", "High Text Markup Language", "Hyper Tabular Markup Language", "None of these", "A", "HTML stands for Hyper Text Markup Language."),
    ("General Knowledge", "Hard", "Who is known as the 'Missile Man of India'?", "C.V. Raman", "Homi Bhabha", "A.P.J. Abdul Kalam", "Vikram Sarabhai", "C", "A.P.J. Abdul Kalam is known as the Missile Man of India."),
    ("History", "Easy", "Who built the Taj Mahal?", "Akbar", "Jahangir", "Shah Jahan", "Aurangzeb", "C", "Shah Jahan built the Taj Mahal in memory of his wife Mumtaz Mahal."),
    ("Geography", "Medium", "Mount Everest is located in which mountain range?", "Alps", "Andes", "Himalayas", "Rockies", "C", "Mount Everest is part of the Himalayas."),
    ("Mathematics", "Hard", "If x + 5 = 12, what is the value of x?", "5", "6", "7", "8", "C", "Subtracting 5 from both sides gives x = 7."),
    ("Sports", "Medium", "Which country won the first FIFA World Cup?", "Brazil", "Germany", "Argentina", "Uruguay", "D", "Uruguay won the first FIFA World Cup in 1930."),
    ("Science", "Easy", "How many planets are in our solar system?", "7", "8", "9", "10", "B", "There are 8 planets in our solar system."),
    ("Computer", "Hard", "What is the full form of RAM?", "Random Access Memory", "Read Access Memory", "Run Access Memory", "Rapid Access Memory", "A", "RAM stands for Random Access Memory."),
    ("General Knowledge", "Medium", "Which bird is the universal symbol of peace?", "Eagle", "Dove", "Peacock", "Swan", "B", "The white dove is recognized as a symbol of peace."),
    ("History", "Hard", "The Battle of Plassey was fought in which year?", "1757", "1764", "1857", "1947", "A", "The Battle of Plassey was fought in 1757."),
    ("Geography", "Easy", "Which is the smallest state in India by area?", "Sikkim", "Goa", "Tripura", "Mizoram", "B", "Goa is the smallest state in India by land area."),
    ("Mathematics", "Medium", "What is the area of a rectangle with length 10 and width 5?", "15", "30", "50", "100", "C", "Area = length x width = 10 x 5 = 50.")
]

with open(r'd:\project\qgame\qgame\data\questions.txt', 'w', encoding='utf-8') as f:
    for cat, diff, q, a, b, c, d, ans, exp in questions_data:
        f.write(f"{cat} ({diff}): {q}\n\n")
        f.write(f"A: {a}\n")
        f.write(f"B: {b}\n")
        f.write(f"C: {c}\n")
        f.write(f"D: {d}\n\n")
        f.write(f"Correct Answer: {ans}\n\n")
        f.write(f"Explanation:\n{exp}\n")
        f.write("-" * 50 + "\n\n")

print("Created questions.txt")
