import json
import os
import time
from deep_translator import GoogleTranslator

# Only defining English text and options to save space. We will translate using deep_translator.
# Format: (text, opt_a, opt_b, opt_c, opt_d, correct, difficulty)
mahabharata_raw = [
    ("Who was the father of Pandavas?", "Dhritarashtra", "Pandu", "Vidura", "Shantanu", "B", "Easy"),
    ("Who was the eldest Pandava?", "Bhima", "Arjuna", "Yudhishthira", "Nakula", "C", "Easy"),
    ("Who was the mother of Kauravas?", "Kunti", "Madri", "Gandhari", "Satyavati", "C", "Easy"),
    ("Who was the guru of Pandavas and Kauravas?", "Dronacharya", "Kripacharya", "Parashurama", "Vishwamitra", "A", "Easy"),
    ("What was the name of Arjuna's bow?", "Pinaka", "Gandiva", "Sharanga", "Vijaya", "B", "Medium"),
    ("Who wrote the Mahabharata?", "Valmiki", "Ved Vyasa", "Tulsidas", "Kalidasa", "B", "Easy"),
    ("How many days did the Kurukshetra war last?", "14", "16", "18", "20", "C", "Medium"),
    ("Who killed Karna?", "Bhima", "Yudhishthira", "Arjuna", "Abhimanyu", "C", "Medium"),
    ("What was the real name of Bhishma?", "Devavrata", "Shantanu", "Chitrangada", "Vichitravirya", "A", "Medium"),
    ("Who was the father of Abhimanyu?", "Yudhishthira", "Bhima", "Arjuna", "Nakula", "C", "Medium"),
    ("Who was the wife of all five Pandavas?", "Draupadi", "Subhadra", "Ulupi", "Chitrangada", "A", "Easy"),
    ("Who killed Dushasana?", "Bhima", "Arjuna", "Yudhishthira", "Sahadeva", "A", "Medium"),
    ("Who was the king of Hastinapur during the war?", "Pandu", "Yudhishthira", "Dhritarashtra", "Duryodhana", "C", "Medium"),
    ("What game did the Pandavas lose to the Kauravas?", "Chess", "Dice", "Archery", "Wrestling", "B", "Easy"),
    ("Who was the charioteer of Arjuna?", "Krishna", "Sanjaya", "Drona", "Bhishma", "A", "Easy"),
    ("Who vowed to kill Bhishma?", "Amba", "Ambalika", "Ambika", "Gandhari", "A", "Hard"),
    ("Who killed Jayadratha?", "Arjuna", "Bhima", "Yudhishthira", "Satyaki", "A", "Medium"),
    ("Who was the eldest Kaurava?", "Dushasana", "Vikarna", "Duryodhana", "Yuyutsu", "C", "Easy"),
    ("Who survived the Kurukshetra war from the Kaurava side?", "Ashwatthama", "Kritavarma", "Kripacharya", "All of the above", "D", "Hard"),
    ("Who recited the Bhagavad Gita?", "Sanjaya", "Krishna", "Vyasa", "Arjuna", "B", "Easy"),
    ("To whom did Krishna recite the Bhagavad Gita?", "Yudhishthira", "Bhima", "Arjuna", "Duryodhana", "C", "Easy"),
    ("Who was the mother of Karna?", "Kunti", "Radha", "Gandhari", "Madri", "A", "Medium"),
    ("Who raised Karna?", "Adhiratha and Radha", "Nanda and Yashoda", "Pandu and Kunti", "Dhritarashtra and Gandhari", "A", "Hard"),
    ("Who was the blind king of Hastinapur?", "Pandu", "Dhritarashtra", "Shantanu", "Vichitravirya", "B", "Easy"),
    ("Who was the uncle of Kauravas?", "Shakuni", "Vidura", "Shalya", "Kripa", "A", "Easy"),
    ("What was the name of Yudhishthira's conch?", "Panchajanya", "Devadatta", "Paundra", "Anantavijaya", "D", "Hard"),
    ("Who killed Shakuni?", "Bhima", "Sahadeva", "Nakula", "Arjuna", "B", "Hard"),
    ("Who killed Shalya?", "Yudhishthira", "Arjuna", "Bhima", "Nakula", "A", "Hard"),
    ("Who was the commander of Kaurava army on the first day?", "Drona", "Bhishma", "Karna", "Shalya", "B", "Medium"),
    ("For how many days was Bhishma the commander?", "10", "5", "2", "18", "A", "Hard"),
    ("Who created the Chakravyuha on the 13th day?", "Bhishma", "Drona", "Karna", "Shalya", "B", "Medium"),
    ("Who killed Abhimanyu?", "Karna", "Dushasana", "Jayadratha", "Multiple warriors", "D", "Medium"),
    ("What was the name of Bhima's mace?", "Kaumodaki", "Vayavya", "Gada", "Vajra", "A", "Hard"),
    ("Who was the son of Bhima and Hidimbi?", "Ghatotkacha", "Barbarika", "Abhimanyu", "Iravan", "A", "Medium"),
    ("Who killed Ghatotkacha?", "Karna", "Drona", "Duryodhana", "Ashwatthama", "A", "Medium"),
    ("Which weapon did Karna use to kill Ghatotkacha?", "Brahmastra", "Pashupatastra", "Vasavi Shakti", "Narayanastra", "C", "Hard"),
    ("Who narrated the Mahabharata war to Dhritarashtra?", "Vidura", "Sanjaya", "Vyasa", "Kripa", "B", "Medium"),
    ("Who gave Sanjaya the divine vision?", "Vyasa", "Krishna", "Shiva", "Brahma", "A", "Medium"),
    ("Who was the mother of Vyasa?", "Satyavati", "Ganga", "Amba", "Kunti", "A", "Hard"),
    ("What is the final book of Mahabharata?", "Bhishma Parva", "Shanti Parva", "Swargarohanika Parva", "Ashvamedhika Parva", "C", "Hard"),
]

# (Do the same for other 3, making 40 questions each)
# To save time and code length, I'll generate 40 for Hindu Gods, Indian History, and Indian Culture.

hindu_gods_raw = [
    ("Who is the creator of the universe?", "Brahma", "Vishnu", "Shiva", "Indra", "A", "Easy"),
    ("Who is the preserver of the universe?", "Brahma", "Vishnu", "Shiva", "Indra", "B", "Easy"),
    ("Who is the destroyer in the Holy Trinity?", "Brahma", "Vishnu", "Shiva", "Agni", "C", "Easy"),
    ("Who is the elephant-headed god?", "Kartikeya", "Ganesha", "Hanuman", "Nandi", "B", "Easy"),
    ("Who is the goddess of wealth?", "Saraswati", "Parvati", "Lakshmi", "Durga", "C", "Easy"),
    ("Who is the goddess of knowledge?", "Saraswati", "Parvati", "Lakshmi", "Kali", "A", "Easy"),
    ("Who is the monkey god?", "Sugriva", "Vali", "Hanuman", "Jambavan", "C", "Easy"),
    ("Which god is known as the Lord of Dance (Nataraja)?", "Vishnu", "Shiva", "Brahma", "Indra", "B", "Medium"),
    ("What is the weapon of Lord Indra?", "Trishul", "Sudarshana Chakra", "Vajra", "Gada", "C", "Medium"),
    ("Who is the wife of Lord Shiva?", "Lakshmi", "Saraswati", "Parvati", "Sita", "C", "Easy"),
    ("What is the vehicle of Lord Shiva?", "Lion", "Tiger", "Mouse", "Bull (Nandi)", "D", "Easy"),
    ("What is the vehicle of Lord Vishnu?", "Garuda", "Hamsa", "Airavata", "Peacock", "A", "Medium"),
    ("What is the vehicle of Goddess Durga?", "Tiger/Lion", "Elephant", "Horse", "Bull", "A", "Easy"),
    ("Who is the god of fire?", "Vayu", "Varuna", "Agni", "Yama", "C", "Easy"),
    ("Who is the god of water/ocean?", "Agni", "Vayu", "Indra", "Varuna", "D", "Medium"),
    ("Who is the god of death?", "Yama", "Chitragupta", "Shani", "Rahu", "A", "Medium"),
    ("Who is the god of the wind?", "Agni", "Vayu", "Surya", "Chandra", "B", "Easy"),
    ("Who is the sun god?", "Surya", "Chandra", "Mangala", "Shukra", "A", "Easy"),
    ("Who is the moon god?", "Surya", "Chandra", "Budha", "Brihaspati", "B", "Easy"),
    ("Which god has a third eye?", "Vishnu", "Brahma", "Shiva", "Indra", "C", "Easy"),
    ("Which god wears a crescent moon on his head?", "Shiva", "Vishnu", "Brahma", "Kartikeya", "A", "Medium"),
    ("Who is the brother of Ganesha?", "Hanuman", "Kartikeya", "Ayyappan", "Kama", "B", "Medium"),
    ("What is the vehicle of Lord Ganesha?", "Mouse", "Peacock", "Lion", "Bull", "A", "Easy"),
    ("What is the vehicle of Lord Kartikeya?", "Swan", "Peacock", "Elephant", "Tiger", "B", "Medium"),
    ("Who is the god of love?", "Kama", "Agni", "Indra", "Varuna", "A", "Hard"),
    ("Who is the wife of Lord Brahma?", "Lakshmi", "Parvati", "Saraswati", "Ganga", "C", "Easy"),
    ("What is the vehicle of Lord Brahma?", "Hamsa (Swan)", "Garuda", "Nandi", "Airavata", "A", "Medium"),
    ("Who is the king of the Devas?", "Agni", "Indra", "Surya", "Vayu", "B", "Easy"),
    ("What is the name of Indra's elephant?", "Airavata", "Nandi", "Uchchaihshravas", "Kamadhenu", "A", "Medium"),
    ("Who is the god of wealth?", "Indra", "Kubera", "Varuna", "Yama", "B", "Medium"),
    ("Who is the architect of the gods?", "Maya", "Vishwakarma", "Brahma", "Tvashtar", "B", "Hard"),
    ("Who is the physician of the gods?", "Ashwini Kumaras", "Dhanvantari", "Charaka", "Sushruta", "A", "Hard"),
    ("Who emerged from the churning of the ocean with nectar?", "Lakshmi", "Dhanvantari", "Mohini", "Kurma", "B", "Hard"),
    ("What is the primary weapon of Lord Vishnu?", "Trishul", "Sudarshana Chakra", "Pashupatastra", "Brahmastra", "B", "Easy"),
    ("Which avatar of Vishnu was a half-man, half-lion?", "Varaha", "Kurma", "Matsya", "Narasimha", "D", "Medium"),
    ("Which avatar of Vishnu was a dwarf?", "Vamana", "Parashurama", "Rama", "Krishna", "A", "Medium"),
    ("Which avatar of Vishnu was a boar?", "Matsya", "Kurma", "Varaha", "Narasimha", "C", "Medium"),
    ("Who is the guru of the Devas?", "Shukracharya", "Brihaspati", "Dronacharya", "Vashistha", "B", "Hard"),
    ("Who is the guru of the Asuras?", "Shukracharya", "Brihaspati", "Vishwamitra", "Agastya", "A", "Hard"),
    ("Which goddess is considered the fierce form of Parvati?", "Saraswati", "Lakshmi", "Kali", "Ganga", "C", "Medium"),
]

indian_history_raw = [
    ("Who was the first Prime Minister of India?", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "B.R. Ambedkar", "B", "Easy"),
    ("Who is known as the Father of the Nation in India?", "Jawaharlal Nehru", "Bhagat Singh", "Mahatma Gandhi", "Subhas Chandra Bose", "C", "Easy"),
    ("In which year did India get independence?", "1945", "1947", "1950", "1952", "B", "Easy"),
    ("When did India become a Republic?", "1947", "1948", "1950", "1952", "C", "Easy"),
    ("Who was the first President of India?", "Dr. Rajendra Prasad", "Dr. S. Radhakrishnan", "Zakir Husain", "V. V. Giri", "A", "Easy"),
    ("Who is known as the Iron Man of India?", "Bhagat Singh", "Sardar Vallabhbhai Patel", "Lala Lajpat Rai", "Bal Gangadhar Tilak", "B", "Easy"),
    ("Who wrote the Indian National Anthem?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sarojini Naidu", "Subramania Bharati", "B", "Medium"),
    ("Who wrote the Indian National Song 'Vande Mataram'?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sri Aurobindo", "Swami Vivekananda", "A", "Medium"),
    ("Who was the founder of the Maurya Empire?", "Ashoka", "Chandragupta Maurya", "Bindusara", "Dasharatha", "B", "Medium"),
    ("Which emperor embraced Buddhism after the Kalinga War?", "Chandragupta Maurya", "Ashoka", "Harsha", "Kanishka", "B", "Easy"),
    ("Who was the founder of the Mughal Empire in India?", "Akbar", "Humayun", "Babur", "Shah Jahan", "C", "Medium"),
    ("Which Mughal emperor built the Taj Mahal?", "Akbar", "Jahangir", "Shah Jahan", "Aurangzeb", "C", "Easy"),
    ("Who was the first female Prime Minister of India?", "Sarojini Naidu", "Indira Gandhi", "Pratibha Patil", "Sonia Gandhi", "B", "Easy"),
    ("Who gave the slogan 'Give me blood, and I shall give you freedom'?", "Bhagat Singh", "Chandra Shekhar Azad", "Subhas Chandra Bose", "Lala Lajpat Rai", "C", "Medium"),
    ("The Indus Valley Civilization was primarily located in which region?", "Southern India", "Eastern India", "North-Western India", "Central India", "C", "Medium"),
    ("What was the capital of the Maurya Empire?", "Pataliputra", "Taxila", "Ujjain", "Mathura", "A", "Hard"),
    ("Who was the famous astronomer and mathematician in ancient India?", "Kalidasa", "Aryabhata", "Chanakya", "Sushruta", "B", "Medium"),
    ("Who wrote the Arthashastra?", "Aryabhata", "Kalidasa", "Chanakya", "Banabhatta", "C", "Medium"),
    ("Which British Governor-General abolished Sati?", "Lord Cornwallis", "Lord William Bentinck", "Lord Dalhousie", "Lord Curzon", "B", "Hard"),
    ("The Indian National Congress was founded in which year?", "1885", "1905", "1919", "1942", "A", "Medium"),
    ("Who was the founder of the Indian National Congress?", "A. O. Hume", "W. C. Bonnerjee", "Dadabhai Naoroji", "Mahatma Gandhi", "A", "Hard"),
    ("When did the Jallianwala Bagh massacre occur?", "1917", "1919", "1921", "1923", "B", "Medium"),
    ("Which movement was launched in 1942?", "Non-Cooperation Movement", "Civil Disobedience Movement", "Quit India Movement", "Swadeshi Movement", "C", "Medium"),
    ("Who was the Viceroy of India during the partition?", "Lord Mountbatten", "Lord Wavell", "Lord Linlithgow", "Lord Irwin", "A", "Easy"),
    ("Who is known as the 'Missile Man of India'?", "Homi Bhabha", "Vikram Sarabhai", "A. P. J. Abdul Kalam", "C. V. Raman", "C", "Easy"),
    ("Who was the first Indian in space?", "Rakesh Sharma", "Kalpana Chawla", "Sunita Williams", "Ravish Malhotra", "A", "Medium"),
    ("Who was the main architect of the Indian Constitution?", "Jawaharlal Nehru", "B. R. Ambedkar", "Rajendra Prasad", "B. N. Rau", "B", "Easy"),
    ("What was the period of the Emergency in India?", "1971-1973", "1975-1977", "1980-1982", "1984-1986", "B", "Hard"),
    ("The first battle of Panipat was fought in?", "1526", "1556", "1761", "1857", "A", "Medium"),
    ("Who defeated the Marathas in the Third Battle of Panipat?", "British", "Mughals", "Ahmad Shah Abdali", "Sikhs", "C", "Hard"),
    ("Who established the Ramakrishna Mission?", "Ramakrishna Paramahamsa", "Swami Vivekananda", "Raja Ram Mohan Roy", "Dayananda Saraswati", "B", "Medium"),
    ("Who founded the Brahmo Samaj?", "Swami Vivekananda", "Dayananda Saraswati", "Raja Ram Mohan Roy", "Ishwar Chandra Vidyasagar", "C", "Hard"),
    ("Who founded the Arya Samaj?", "Raja Ram Mohan Roy", "Dayananda Saraswati", "Swami Vivekananda", "Annie Besant", "B", "Hard"),
    ("Who was the first Indian woman to become President of the INC?", "Annie Besant", "Sarojini Naidu", "Indira Gandhi", "Sucheta Kripalani", "B", "Hard"),
    ("The Dandi March was related to which movement?", "Non-Cooperation", "Civil Disobedience", "Quit India", "Khilafat", "B", "Medium"),
    ("Who was known as 'Frontier Gandhi'?", "Muhammad Ali Jinnah", "Khan Abdul Ghaffar Khan", "Maulana Abul Kalam Azad", "Liaquat Ali Khan", "B", "Hard"),
    ("Which is the oldest Veda?", "Rigveda", "Samaveda", "Yajurveda", "Atharvaveda", "A", "Easy"),
    ("Gautama Buddha was born in?", "Lumbini", "Bodh Gaya", "Sarnath", "Kushinagar", "A", "Medium"),
    ("Where did Buddha give his first sermon?", "Lumbini", "Bodh Gaya", "Sarnath", "Kushinagar", "C", "Medium"),
    ("Where did Buddha attain Nirvana?", "Lumbini", "Bodh Gaya", "Sarnath", "Kushinagar", "B", "Medium"),
]

indian_culture_raw = [
    ("Which festival is known as the Festival of Colors?", "Diwali", "Holi", "Navratri", "Dussehra", "B", "Easy"),
    ("Which festival is known as the Festival of Lights?", "Holi", "Diwali", "Eid", "Christmas", "B", "Easy"),
    ("Bharatanatyam is a classical dance from which state?", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Odisha", "B", "Medium"),
    ("Kathakali is a classical dance from which state?", "Kerala", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "A", "Medium"),
    ("Kuchipudi is a classical dance from which state?", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Odisha", "C", "Hard"),
    ("Kathak is a classical dance form mainly from?", "South India", "East India", "North India", "West India", "C", "Medium"),
    ("Odissi is a classical dance from which state?", "Odisha", "West Bengal", "Assam", "Manipur", "A", "Easy"),
    ("Bihu is a folk dance of which state?", "Punjab", "Gujarat", "Assam", "Rajasthan", "C", "Medium"),
    ("Garba is a popular folk dance of which state?", "Maharashtra", "Gujarat", "Rajasthan", "Punjab", "B", "Easy"),
    ("Bhangra is a traditional dance from which state?", "Gujarat", "Haryana", "Punjab", "Rajasthan", "C", "Easy"),
    ("Ghoomar is a traditional folk dance of?", "Gujarat", "Rajasthan", "Maharashtra", "Punjab", "B", "Medium"),
    ("Lavani is a traditional dance of which state?", "Goa", "Maharashtra", "Karnataka", "Gujarat", "B", "Hard"),
    ("What is the traditional garment worn by Indian women?", "Kimono", "Sari", "Hanbok", "Cheongsam", "B", "Easy"),
    ("What is the traditional garment often worn by Indian men?", "Tuxedo", "Dhoti", "Kilt", "Poncho", "B", "Easy"),
    ("Which language is known as the 'mother of all languages' in India?", "Hindi", "Tamil", "Sanskrit", "Prakrit", "C", "Medium"),
    ("Which state is famous for the Hornbill Festival?", "Assam", "Nagaland", "Manipur", "Mizoram", "B", "Hard"),
    ("Onam is a major festival of which state?", "Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh", "A", "Medium"),
    ("Pongal is a harvest festival celebrated in?", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Karnataka", "B", "Medium"),
    ("Baisakhi is a major festival of which state?", "Gujarat", "Maharashtra", "Punjab", "Rajasthan", "C", "Medium"),
    ("Which Indian festival celebrates the bond between brothers and sisters?", "Diwali", "Holi", "Raksha Bandhan", "Navratri", "C", "Easy"),
    ("Makar Sankranti is known as what in Tamil Nadu?", "Pongal", "Bihu", "Lohri", "Onam", "A", "Hard"),
    ("Which epic is the longest poem ever written?", "Ramayana", "Mahabharata", "Iliad", "Odyssey", "B", "Medium"),
    ("Who composed the Indian National Anthem?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Subhas Chandra Bose", "Lata Mangeshkar", "B", "Easy"),
    ("Which Indian musician popularized the sitar in the West?", "Zakir Hussain", "Ravi Shankar", "A. R. Rahman", "Bismillah Khan", "B", "Medium"),
    ("Bismillah Khan was associated with which instrument?", "Sitar", "Tabla", "Shehnai", "Flute", "C", "Hard"),
    ("Zakir Hussain is famous for playing which instrument?", "Sitar", "Tabla", "Shehnai", "Flute", "B", "Medium"),
    ("Hariprasad Chaurasia is famous for playing which instrument?", "Sitar", "Tabla", "Shehnai", "Flute", "D", "Hard"),
    ("Which is the largest religion in India?", "Islam", "Christianity", "Hinduism", "Sikhism", "C", "Easy"),
    ("The Golden Temple is located in which city?", "Chandigarh", "Amritsar", "Ludhiana", "Jalandhar", "B", "Easy"),
    ("The Kumbh Mela is held every how many years at a given location?", "4", "6", "12", "144", "C", "Medium"),
    ("Which river is considered the most sacred in Hinduism?", "Yamuna", "Brahmaputra", "Godavari", "Ganges", "D", "Easy"),
    ("The Taj Mahal is located on the banks of which river?", "Ganges", "Yamuna", "Narmada", "Tapti", "B", "Medium"),
    ("Which Indian state is known as 'God's Own Country'?", "Goa", "Kerala", "Himachal Pradesh", "Uttarakhand", "B", "Medium"),
    ("What is the classical language of Tamil Nadu?", "Telugu", "Kannada", "Tamil", "Malayalam", "C", "Easy"),
    ("Which state is known for its Madhubani paintings?", "Bihar", "Rajasthan", "Madhya Pradesh", "Gujarat", "A", "Hard"),
    ("Warli painting is a tribal art from which state?", "Gujarat", "Maharashtra", "Madhya Pradesh", "Odisha", "B", "Hard"),
    ("Which martial art is native to Kerala?", "Kalaripayattu", "Gatka", "Thang-Ta", "Silambam", "A", "Hard"),
    ("What is the traditional New Year of Maharashtra called?", "Ugadi", "Gudi Padwa", "Bihu", "Puthandu", "B", "Hard"),
    ("What is the traditional New Year of Andhra Pradesh and Karnataka?", "Ugadi", "Gudi Padwa", "Bihu", "Puthandu", "A", "Hard"),
    ("What is the national animal of India?", "Lion", "Elephant", "Tiger", "Peacock", "C", "Easy"),
]

def translate_and_format(raw_list):
    translator_hi = GoogleTranslator(source='en', target='hi')
    translator_gu = GoogleTranslator(source='en', target='gu')
    questions = []
    
    # We translate in batches to be fast
    for text, opt_a, opt_b, opt_c, opt_d, correct, difficulty in raw_list:
        texts_to_translate = [text, opt_a, opt_b, opt_c, opt_d]
        
        try:
            hi_translations = translator_hi.translate_batch(texts_to_translate)
        except Exception:
            # Fallback one by one
            hi_translations = [translator_hi.translate(t) for t in texts_to_translate]
            
        try:
            gu_translations = translator_gu.translate_batch(texts_to_translate)
        except Exception:
            gu_translations = [translator_gu.translate(t) for t in texts_to_translate]
            
        q = {
            "difficulty": difficulty,
            "correct_option": correct,
            "en": {
                "text": texts_to_translate[0],
                "opt_a": texts_to_translate[1], "opt_b": texts_to_translate[2],
                "opt_c": texts_to_translate[3], "opt_d": texts_to_translate[4]
            },
            "hi": {
                "text": hi_translations[0],
                "opt_a": hi_translations[1], "opt_b": hi_translations[2],
                "opt_c": hi_translations[3], "opt_d": hi_translations[4]
            },
            "gu": {
                "text": gu_translations[0],
                "opt_a": gu_translations[1], "opt_b": gu_translations[2],
                "opt_c": gu_translations[3], "opt_d": gu_translations[4]
            }
        }
        questions.append(q)
        time.sleep(0.1) # Small delay to avoid rate limiting
    return questions

os.makedirs('d:/project/qgame/qgame/data', exist_ok=True)

print("Translating Mahabharata...")
mahabharata_questions = translate_and_format(mahabharata_raw)
with open('d:/project/qgame/qgame/data/mahabharata_part2.json', 'w', encoding='utf-8') as f:
    json.dump(mahabharata_questions, f, ensure_ascii=False, indent=4)
    
print("Translating Hindu Gods...")
hindu_gods_questions = translate_and_format(hindu_gods_raw)
with open('d:/project/qgame/qgame/data/hindu_gods_part2.json', 'w', encoding='utf-8') as f:
    json.dump(hindu_gods_questions, f, ensure_ascii=False, indent=4)

print("Translating Indian History...")
indian_history_questions = translate_and_format(indian_history_raw)
with open('d:/project/qgame/qgame/data/indian_history_part2.json', 'w', encoding='utf-8') as f:
    json.dump(indian_history_questions, f, ensure_ascii=False, indent=4)
    
print("Translating Indian Culture...")
indian_culture_questions = translate_and_format(indian_culture_raw)
with open('d:/project/qgame/qgame/data/indian_culture_part2.json', 'w', encoding='utf-8') as f:
    json.dump(indian_culture_questions, f, ensure_ascii=False, indent=4)

print("Done generating 40 questions per category!")
