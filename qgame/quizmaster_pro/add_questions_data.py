import random
from app import app, db
from models import Category, Question

def populate_data():
    with app.app_context():
        # 10 subjects
        subjects = [
            'Python', 'General Knowledge', 'Mathematics', 'Science', 'History',
            'Geography', 'Technology', 'Sports', 'Literature', 'Art'
        ]
        
        categories = {}
        for sub in subjects:
            cat = Category.query.filter_by(name=sub).first()
            if not cat:
                cat = Category(name=sub, description=f'Test your knowledge in {sub}.')
                db.session.add(cat)
                db.session.commit()
            categories[sub] = cat

        questions_data = {
            'Python': [
                ("What does 'def' do in Python?", "Define variable", "Define function", "Define class", "Define loop", "B"),
                ("Which of these is a Python data type?", "Integer", "String", "List", "All of the above", "D"),
                ("What is the output of len([1, 2, 3])?", "1", "2", "3", "Error", "C"),
                ("How do you start a comment in Python?", "//", "/*", "#", "<!--", "C"),
                ("Which method is used to add an item to a list?", "append()", "add()", "insert()", "push()", "A"),
                ("What is a dictionary in Python?", "A list of strings", "Key-value pairs", "An ordered array", "A function", "B"),
                ("What keyword is used for exception handling?", "try", "catch", "throw", "handle", "A"),
                ("Which operator is used for floor division?", "/", "%", "//", "**", "C"),
                ("What is self in Python classes?", "Current instance", "Current class", "Global variable", "None of the above", "A"),
                ("How do you import a module in Python?", "include module", "import module", "require module", "using module", "B")
            ],
            'General Knowledge': [
                ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", "C"),
                ("Who wrote 'Romeo and Juliet'?", "Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain", "B"),
                ("What is the largest ocean on Earth?", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean", "D"),
                ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B"),
                ("How many continents are there?", "5", "6", "7", "8", "C"),
                ("What is the longest river in the world?", "Amazon River", "Nile River", "Yangtze River", "Mississippi River", "B"),
                ("Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet", "C"),
                ("What is the currency of Japan?", "Yuan", "Won", "Yen", "Ringgit", "C"),
                ("Which is the smallest country in the world?", "Monaco", "Vatican City", "San Marino", "Liechtenstein", "B"),
                ("What is the main language spoken in Brazil?", "Spanish", "Portuguese", "English", "French", "B")
            ],
            'Mathematics': [
                ("What is 15% of 200?", "20", "30", "40", "50", "B"),
                ("What is the square root of 144?", "10", "11", "12", "14", "C"),
                ("What is the value of Pi (approx)?", "3.14", "3.16", "3.12", "3.18", "A"),
                ("Solve: 5 + 3 * 2", "16", "11", "21", "10", "B"),
                ("What is the perimeter of a rectangle with length 5 and width 3?", "15", "16", "8", "30", "B"),
                ("What is 7 cubed?", "21", "49", "343", "100", "C"),
                ("Solve for x: 2x = 10", "2", "5", "10", "20", "B"),
                ("What is the sum of angles in a triangle?", "90", "180", "360", "270", "B"),
                ("What is 100 divided by 4?", "20", "25", "30", "50", "B"),
                ("What is the area of a square with side 6?", "24", "12", "36", "48", "C")
            ],
            'Science': [
                ("What is the chemical symbol for water?", "H2O", "O2", "CO2", "HO", "A"),
                ("What gas do plants absorb?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "C"),
                ("What is the center of an atom called?", "Electron", "Proton", "Nucleus", "Neutron", "C"),
                ("What is the hardest natural substance?", "Gold", "Iron", "Diamond", "Platinum", "C"),
                ("How many bones are in the adult human body?", "206", "208", "210", "212", "A"),
                ("What force keeps us on the ground?", "Magnetism", "Gravity", "Friction", "Inertia", "B"),
                ("What part of the cell is the powerhouse?", "Nucleus", "Mitochondria", "Ribosome", "Membrane", "B"),
                ("What is the speed of light (approx)?", "300,000 km/s", "150,000 km/s", "1,000,000 km/s", "100,000 km/s", "A"),
                ("What planet is closest to the Sun?", "Venus", "Earth", "Mars", "Mercury", "D"),
                ("What is the freezing point of water in Celsius?", "0", "32", "100", "-10", "A")
            ],
            'History': [
                ("Who was the first President of the USA?", "Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams", "B"),
                ("In which year did World War II end?", "1940", "1945", "1950", "1918", "B"),
                ("Who built the Great Wall of China?", "Qin Dynasty", "Ming Dynasty", "Han Dynasty", "Various Dynasties", "D"),
                ("Who discovered America in 1492?", "Vasco da Gama", "Ferdinand Magellan", "Christopher Columbus", "James Cook", "C"),
                ("What ancient civilization built the pyramids?", "Romans", "Greeks", "Egyptians", "Mayans", "C"),
                ("Who was the British Prime Minister during WWII?", "Neville Chamberlain", "Winston Churchill", "Margaret Thatcher", "Tony Blair", "B"),
                ("Which empire was ruled by Julius Caesar?", "Ottoman", "Roman", "British", "Mongol", "B"),
                ("In what year did the Titanic sink?", "1905", "1912", "1920", "1898", "B"),
                ("Who was the first man to walk on the moon?", "Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "John Glenn", "C"),
                ("What was the name of the ship that brought the Pilgrims to America?", "Santa Maria", "Mayflower", "Endeavour", "Beagle", "B")
            ],
            'Geography': [
                ("What is the capital of Japan?", "Beijing", "Seoul", "Tokyo", "Bangkok", "C"),
                ("Which is the longest river in India?", "Ganges", "Yamuna", "Godavari", "Narmada", "A"),
                ("Which country is also known as the Land of the Rising Sun?", "China", "Japan", "South Korea", "Thailand", "B"),
                ("Which is the largest country by area?", "Canada", "Russia", "China", "USA", "B"),
                ("Mount Everest is located in which mountain range?", "Andes", "Rockies", "Alps", "Himalayas", "D"),
                ("Which desert is the largest hot desert in the world?", "Gobi", "Sahara", "Kalahari", "Thar", "B"),
                ("What is the capital of Canada?", "Toronto", "Vancouver", "Ottawa", "Montreal", "C"),
                ("Which country has the longest coastline in the world?", "Australia", "Canada", "Russia", "Indonesia", "B"),
                ("Which canal connects the Mediterranean Sea to the Red Sea?", "Panama Canal", "Suez Canal", "Kiel Canal", "Erie Canal", "B"),
                ("In which country is the city of Venice located?", "France", "Spain", "Italy", "Greece", "C")
            ],
            'Technology': [
                ("Who is the co-founder of Microsoft?", "Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Jeff Bezos", "B"),
                ("What does RAM stand for?", "Read Access Memory", "Random Access Memory", "Run Access Memory", "Rapid Access Memory", "B"),
                ("Which programming language is mainly used for Android app development?", "Swift", "Kotlin", "C#", "PHP", "B"),
                ("What does HTML stand for?", "Hyper Text Markup Language", "High Text Markup Language", "Hyper Tabular Markup Language", "None", "A"),
                ("Which company created the iPhone?", "Samsung", "Google", "Apple", "Microsoft", "C"),
                ("What is the brain of the computer?", "RAM", "GPU", "CPU", "Hard Drive", "C"),
                ("Which protocol is used to secure communication over the web?", "HTTP", "FTP", "HTTPS", "SMTP", "C"),
                ("What does PDF stand for?", "Personal Document Format", "Portable Document Format", "Print Document Format", "Page Data Format", "B"),
                ("Who is known as the father of computers?", "Alan Turing", "Charles Babbage", "Ada Lovelace", "John von Neumann", "B"),
                ("What is the main operating system of Google Pixel phones?", "iOS", "Windows", "Android", "Linux", "C")
            ],
            'Sports': [
                ("How many players are there on a soccer team on the field?", "9", "10", "11", "12", "C"),
                ("Which country won the FIFA World Cup in 2022?", "France", "Argentina", "Brazil", "Croatia", "B"),
                ("How long is a standard marathon in kilometers?", "21.1", "42.2", "10.0", "50.0", "B"),
                ("In which sport would you use a shuttlecock?", "Tennis", "Badminton", "Table Tennis", "Squash", "B"),
                ("Who has won the most Olympic gold medals in history?", "Usain Bolt", "Michael Phelps", "Serena Williams", "Roger Federer", "B"),
                ("Which sport is played at Wimbledon?", "Golf", "Cricket", "Tennis", "Polo", "C"),
                ("What is the national game of India?", "Cricket", "Hockey", "Kabaddi", "Football", "B"),
                ("How many rings are there on the Olympic flag?", "4", "5", "6", "7", "B"),
                ("Which country is famous for the sport of Sumo wrestling?", "China", "Japan", "South Korea", "Mongolia", "B"),
                ("In cricket, how many wickets must fall to end an innings?", "9", "10", "11", "6", "B")
            ],
            'Literature': [
                ("Who wrote the Harry Potter series?", "J.R.R. Tolkien", "George R.R. Martin", "J.K. Rowling", "C.S. Lewis", "C"),
                ("What is the name of the wizard in 'The Lord of the Rings'?", "Dumbledore", "Merlin", "Gandalf", "Voldemort", "C"),
                ("Who wrote the play 'Hamlet'?", "William Shakespeare", "John Milton", "Geoffrey Chaucer", "Arthur Miller", "A"),
                ("In which novel does the character 'Sherlock Holmes' first appear?", "A Study in Scarlet", "The Hound of the Baskervilles", "The Sign of Four", "The Valley of Fear", "A"),
                ("Who is the author of 'Pride and Prejudice'?", "Charlotte Bronte", "Jane Austen", "Emily Bronte", "Mary Shelley", "B"),
                ("What is the title of the first book of the Bible?", "Exodus", "Genesis", "Leviticus", "Numbers", "B"),
                ("Who wrote the fantasy novel 'The Hobbit'?", "J.K. Rowling", "J.R.R. Tolkien", "C.S. Lewis", "Roald Dahl", "B"),
                ("Which author wrote '1984'?", "Aldous Huxley", "George Orwell", "Ray Bradbury", "H.G. Wells", "B"),
                ("Who wrote 'The Odyssey'?", "Virgil", "Homer", "Plato", "Aristotle", "B"),
                ("What is the primary setting of 'Dracula' by Bram Stoker?", "London", "Transylvania", "Paris", "Rome", "B")
            ],
            'Art': [
                ("Who painted the 'Mona Lisa'?", "Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello", "B"),
                ("Which artist cut off his own left ear?", "Pablo Picasso", "Vincent van Gogh", "Claude Monet", "Salvador Dali", "B"),
                ("Who painted the ceiling of the Sistine Chapel?", "Michelangelo", "Leonardo da Vinci", "Raphael", "Sandro Botticelli", "A"),
                ("Which art style is Salvador Dali famous for?", "Impressionism", "Cubism", "Surrealism", "Expressionism", "C"),
                ("Who painted 'The Starry Night'?", "Claude Monet", "Vincent van Gogh", "Edvard Munch", "Gustav Klimt", "B"),
                ("What is the name of the famous sculpture of a man by Michelangelo?", "The Thinker", "David", "The Kiss", "Pieta", "B"),
                ("Which French artist is known for his water lily paintings?", "Claude Monet", "Edouard Manet", "Edgar Degas", "Pierre-Auguste Renoir", "A"),
                ("Which Spanish artist co-founded the Cubist movement?", "Salvador Dali", "Francisco Goya", "Pablo Picasso", "Diego Velazquez", "C"),
                ("Who created the famous sculpture 'The Thinker'?", "Auguste Rodin", "Donatello", "Gian Lorenzo Bernini", "Henry Moore", "A"),
                ("What is the term for a painting done on wet plaster?", "Fresco", "Tempera", "Oil painting", "Watercolor", "A")
            ]
        }

        # Delete all existing questions to avoid duplicates
        Question.query.delete()
        db.session.commit()

        for category_name, q_list in questions_data.items():
            cat = categories.get(category_name)
            if cat:
                # Add the 10 real questions
                for q in q_list:
                    new_q = Question(
                        category_id=cat.id,
                        text=q[0],
                        option_a=q[1],
                        option_b=q[2],
                        option_c=q[3],
                        option_d=q[4],
                        correct_option=q[5],
                        difficulty='Medium'
                    )
                    db.session.add(new_q)
        
        db.session.commit()
        print("10 Subjects with 10 questions each added successfully!")

if __name__ == '__main__':
    populate_data()
