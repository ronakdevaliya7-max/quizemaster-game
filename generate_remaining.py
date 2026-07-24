import json
import os

mahabharata_questions = [
    {
        "difficulty": "Easy",
        "correct_option": "A",
        "en": {"text": "Who is the author of Mahabharata?", "opt_a": "Ved Vyasa", "opt_b": "Valmiki", "opt_c": "Tulsidas", "opt_d": "Kalidasa"},
        "hi": {"text": "महाभारत के रचयिता कौन हैं?", "opt_a": "वेद व्यास", "opt_b": "वाल्मीकि", "opt_c": "तुलसीदास", "opt_d": "कालिदास"},
        "gu": {"text": "મહાભારતના રચયિતા કોણ છે?", "opt_a": "વેદ વ્યાસ", "opt_b": "વાલ્મીકિ", "opt_c": "તુલસીદાસ", "opt_d": "કાલિદાસ"}
    },
    {
        "difficulty": "Easy",
        "correct_option": "C",
        "en": {"text": "How many Pandava brothers were there?", "opt_a": "3", "opt_b": "4", "opt_c": "5", "opt_d": "100"},
        "hi": {"text": "पांडव भाई कितने थे?", "opt_a": "3", "opt_b": "4", "opt_c": "5", "opt_d": "100"},
        "gu": {"text": "પાંડવો કેટલા ભાઈઓ હતા?", "opt_a": "3", "opt_b": "4", "opt_c": "5", "opt_d": "100"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "B",
        "en": {"text": "What was the real name of Bhishma?", "opt_a": "Shantanu", "opt_b": "Devavrata", "opt_c": "Chitrangada", "opt_d": "Vichitravirya"},
        "hi": {"text": "भीष्म का असली नाम क्या था?", "opt_a": "शांतनु", "opt_b": "देवव्रत", "opt_c": "चित्रांगद", "opt_d": "विचित्रवीर्य"},
        "gu": {"text": "ભીષ્મનું સાચું નામ શું હતું?", "opt_a": "શાંતનુ", "opt_b": "દેવવ્રત", "opt_c": "ચિત્રાંગદ", "opt_d": "વિચિત્રવીર્ય"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "D",
        "en": {"text": "Who was the charioteer of Arjuna during the Kurukshetra war?", "opt_a": "Sanjaya", "opt_b": "Dronacharya", "opt_c": "Bhishma", "opt_d": "Krishna"},
        "hi": {"text": "कुरुक्षेत्र युद्ध के दौरान अर्जुन के सारथी कौन थे?", "opt_a": "संजय", "opt_b": "द्रोणाचार्य", "opt_c": "भीष्म", "opt_d": "कृष्ण"},
        "gu": {"text": "કુરુક્ષેત્ર યુદ્ધ દરમિયાન અર્જુનના સારથી કોણ હતા?", "opt_a": "સંજય", "opt_b": "દ્રોણાચાર્ય", "opt_c": "ભીષ્મ", "opt_d": "કૃષ્ણ"}
    },
    {
        "difficulty": "Hard",
        "correct_option": "A",
        "en": {"text": "Who killed Dushasana?", "opt_a": "Bhima", "opt_b": "Arjuna", "opt_c": "Yudhishthira", "opt_d": "Nakula"},
        "hi": {"text": "दुशासन का वध किसने किया था?", "opt_a": "भीम", "opt_b": "अर्जुन", "opt_c": "युधिष्ठिर", "opt_d": "नकुल"},
        "gu": {"text": "દુશાસનનો વધ કોણે કર્યો હતો?", "opt_a": "ભીમ", "opt_b": "અર્જુન", "opt_c": "યુધિષ્ઠિર", "opt_d": "નકુલ"}
    }
]

hindu_gods_questions = [
    {
        "difficulty": "Easy",
        "correct_option": "B",
        "en": {"text": "Who is known as the Preserver in the Hindu Trinity?", "opt_a": "Brahma", "opt_b": "Vishnu", "opt_c": "Shiva", "opt_d": "Indra"},
        "hi": {"text": "हिंदू त्रिमूर्ति में पालनहार किसे कहा जाता है?", "opt_a": "ब्रह्मा", "opt_b": "विष्णु", "opt_c": "शिव", "opt_d": "इंद्र"},
        "gu": {"text": "હિન્દુ ત્રિમૂર્તિમાં પાલનહાર કોને કહેવામાં આવે છે?", "opt_a": "બ્રહ્મા", "opt_b": "વિષ્ણુ", "opt_c": "શિવ", "opt_d": "ઇન્દ્ર"}
    },
    {
        "difficulty": "Easy",
        "correct_option": "C",
        "en": {"text": "Which animal is the vahana (vehicle) of Lord Ganesha?", "opt_a": "Lion", "opt_b": "Peacock", "opt_c": "Mouse", "opt_d": "Bull"},
        "hi": {"text": "भगवान गणेश का वाहन कौन सा जानवर है?", "opt_a": "शेर", "opt_b": "मोर", "opt_c": "चूहा", "opt_d": "बैल"},
        "gu": {"text": "ભગવાન ગણેશનું વાહન કયું પ્રાણી છે?", "opt_a": "સિંહ", "opt_b": "મોર", "opt_c": "ઉંદર", "opt_d": "બળદ"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "A",
        "en": {"text": "Goddess Saraswati is associated with which of the following?", "opt_a": "Knowledge and Art", "opt_b": "Wealth", "opt_c": "Power", "opt_d": "Destruction"},
        "hi": {"text": "देवी सरस्वती का संबंध किससे है?", "opt_a": "ज्ञान और कला", "opt_b": "धन", "opt_c": "शक्ति", "opt_d": "विनाश"},
        "gu": {"text": "દેવી સરસ્વતી શેની સાથે સંકળાયેલા છે?", "opt_a": "જ્ઞાન અને કળા", "opt_b": "ધન", "opt_c": "શક્તિ", "opt_d": "વિનાશ"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "D",
        "en": {"text": "Which God has a third eye on his forehead?", "opt_a": "Indra", "opt_b": "Surya", "opt_c": "Agni", "opt_d": "Shiva"},
        "hi": {"text": "किस भगवान के माथे पर तीसरी आंख है?", "opt_a": "इंद्र", "opt_b": "सूर्य", "opt_c": "अग्नि", "opt_d": "शिव"},
        "gu": {"text": "કયા ભગવાનના કપાળ પર ત્રીજી આંખ છે?", "opt_a": "ઇન્દ્ર", "opt_b": "સૂર્ય", "opt_c": "અગ્નિ", "opt_d": "શિવ"}
    },
    {
        "difficulty": "Hard",
        "correct_option": "B",
        "en": {"text": "Who is the god of death in Hindu mythology?", "opt_a": "Varuna", "opt_b": "Yama", "opt_c": "Vayu", "opt_d": "Kuber"},
        "hi": {"text": "हिंदू पौराणिक कथाओं में मृत्यु के देवता कौन हैं?", "opt_a": "वरुण", "opt_b": "यम", "opt_c": "वायु", "opt_d": "कुबेर"},
        "gu": {"text": "હિન્દુ પૌરાણિક કથાઓમાં મૃત્યુના દેવતા કોણ છે?", "opt_a": "વરુણ", "opt_b": "યમ", "opt_c": "વાયુ", "opt_d": "કુબેર"}
    }
]

indian_history_questions = [
    {
        "difficulty": "Easy",
        "correct_option": "C",
        "en": {"text": "Who was the first Prime Minister of India?", "opt_a": "Mahatma Gandhi", "opt_b": "Sardar Patel", "opt_c": "Jawaharlal Nehru", "opt_d": "B. R. Ambedkar"},
        "hi": {"text": "भारत के पहले प्रधान मंत्री कौन थे?", "opt_a": "महात्मा गांधी", "opt_b": "सरदार पटेल", "opt_c": "जवाहरलाल नेहरू", "opt_d": "बी. आर. अंबेडकर"},
        "gu": {"text": "ભારતના પ્રથમ વડા પ્રધાન કોણ હતા?", "opt_a": "મહાત્મા ગાંધી", "opt_b": "સરદાર પટેલ", "opt_c": "જવાહરલાલ નેહરુ", "opt_d": "બી. આર. આંબેડકર"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "A",
        "en": {"text": "In which year did India gain independence?", "opt_a": "1947", "opt_b": "1950", "opt_c": "1942", "opt_d": "1857"},
        "hi": {"text": "भारत को स्वतंत्रता किस वर्ष मिली?", "opt_a": "1947", "opt_b": "1950", "opt_c": "1942", "opt_d": "1857"},
        "gu": {"text": "ભારતને કયા વર્ષમાં આઝાદી મળી?", "opt_a": "1947", "opt_b": "1950", "opt_c": "1942", "opt_d": "1857"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "D",
        "en": {"text": "Who founded the Maurya Empire?", "opt_a": "Ashoka", "opt_b": "Bindusara", "opt_c": "Harsha", "opt_d": "Chandragupta Maurya"},
        "hi": {"text": "मौर्य साम्राज्य की स्थापना किसने की?", "opt_a": "अशोक", "opt_b": "बिन्दुसार", "opt_c": "हर्ष", "opt_d": "चन्द्रगुप्त मौर्य"},
        "gu": {"text": "મૌર્ય સામ્રાજ્યની સ્થાપના કોણે કરી?", "opt_a": "અશોક", "opt_b": "બિંદુસાર", "opt_c": "હર્ષ", "opt_d": "ચંદ્રગુપ્ત મૌર્ય"}
    },
    {
        "difficulty": "Hard",
        "correct_option": "B",
        "en": {"text": "The Battle of Plassey was fought in which year?", "opt_a": "1764", "opt_b": "1757", "opt_c": "1857", "opt_d": "1799"},
        "hi": {"text": "प्लासी का युद्ध किस वर्ष लड़ा गया था?", "opt_a": "1764", "opt_b": "1757", "opt_c": "1857", "opt_d": "1799"},
        "gu": {"text": "પ્લાસીનું યુદ્ધ કયા વર્ષમાં લડવામાં આવ્યું હતું?", "opt_a": "1764", "opt_b": "1757", "opt_c": "1857", "opt_d": "1799"}
    },
    {
        "difficulty": "Easy",
        "correct_option": "C",
        "en": {"text": "Who is known as the 'Iron Man of India'?", "opt_a": "Bhagat Singh", "opt_b": "Subhas Chandra Bose", "opt_c": "Sardar Vallabhbhai Patel", "opt_d": "Lal Bahadur Shastri"},
        "hi": {"text": "'भारत के लौह पुरुष' के रूप में किसे जाना जाता है?", "opt_a": "भगत सिंह", "opt_b": "सुभाष चंद्र बोस", "opt_c": "सरदार वल्लभभाई पटेल", "opt_d": "लाल बहादुर शास्त्री"},
        "gu": {"text": "'ભારતના લોખંડી પુરુષ' તરીકે કોણ ઓળખાય છે?", "opt_a": "ભગત સિંહ", "opt_b": "સુભાષ ચંદ્ર બોઝ", "opt_c": "સરદાર વલ્લભભાઈ પટેલ", "opt_d": "લાલ બહાદુર શાસ્ત્રી"}
    }
]

indian_culture_questions = [
    {
        "difficulty": "Easy",
        "correct_option": "A",
        "en": {"text": "Which festival is known as the 'Festival of Lights'?", "opt_a": "Diwali", "opt_b": "Holi", "opt_c": "Eid", "opt_d": "Navratri"},
        "hi": {"text": "किस त्योहार को 'रोशनी का त्योहार' कहा जाता है?", "opt_a": "दिवाली", "opt_b": "होली", "opt_c": "ईद", "opt_d": "नवरात्रि"},
        "gu": {"text": "કયા તહેવારને 'પ્રકાશના તહેવાર' તરીકે ઓળખવામાં આવે છે?", "opt_a": "દિવાળી", "opt_b": "હોળી", "opt_c": "ઈદ", "opt_d": "નવરાત્રી"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "B",
        "en": {"text": "Bharatanatyam is a classical dance form from which state?", "opt_a": "Kerala", "opt_b": "Tamil Nadu", "opt_c": "Andhra Pradesh", "opt_d": "Odisha"},
        "hi": {"text": "भरतनाट्यम किस राज्य का शास्त्रीय नृत्य है?", "opt_a": "केरल", "opt_b": "तमिलनाडु", "opt_c": "आंध्र प्रदेश", "opt_d": "ओडिशा"},
        "gu": {"text": "ભરતનાટ્યમ કયા રાજ્યનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "કેરળ", "opt_b": "તમિલનાડુ", "opt_c": "આંધ્ર પ્રદેશ", "opt_d": "ઓડિશા"}
    },
    {
        "difficulty": "Easy",
        "correct_option": "D",
        "en": {"text": "What is the national flower of India?", "opt_a": "Rose", "opt_b": "Jasmine", "opt_c": "Marigold", "opt_d": "Lotus"},
        "hi": {"text": "भारत का राष्ट्रीय फूल क्या है?", "opt_a": "गुलाब", "opt_b": "चमेली", "opt_c": "गेंदा", "opt_d": "कमल"},
        "gu": {"text": "ભારતનું રાષ્ટ્રીય ફૂલ કયું છે?", "opt_a": "ગુલાબ", "opt_b": "ચમેલી", "opt_c": "ગલગોટો", "opt_d": "કમળ"}
    },
    {
        "difficulty": "Medium",
        "correct_option": "C",
        "en": {"text": "Which of these is a famous Indian classical music instrument?", "opt_a": "Guitar", "opt_b": "Piano", "opt_c": "Sitar", "opt_d": "Violin"},
        "hi": {"text": "इनमें से कौन सा एक प्रसिद्ध भारतीय शास्त्रीय संगीत वाद्ययंत्र है?", "opt_a": "गिटार", "opt_b": "पियानो", "opt_c": "सितार", "opt_d": "वायलिन"},
        "gu": {"text": "આમાંથી કયું પ્રખ્યાત ભારતીય શાસ્ત્રીય સંગીત વાદ્ય છે?", "opt_a": "ગિટાર", "opt_b": "પિયાનો", "opt_c": "સિતાર", "opt_d": "વાયોલિન"}
    },
    {
        "difficulty": "Hard",
        "correct_option": "A",
        "en": {"text": "The Kumbh Mela is held every how many years?", "opt_a": "12", "opt_b": "10", "opt_c": "5", "opt_d": "14"},
        "hi": {"text": "कुंभ मेला हर कितने साल में आयोजित किया जाता है?", "opt_a": "12", "opt_b": "10", "opt_c": "5", "opt_d": "14"},
        "gu": {"text": "કુંભ મેળો દર કેટલા વર્ષે યોજાય છે?", "opt_a": "12", "opt_b": "10", "opt_c": "5", "opt_d": "14"}
    }
]

os.makedirs('d:/project/qgame/qgame/data', exist_ok=True)

data_map = {
    'mahabharata.json': mahabharata_questions,
    'hindu_gods.json': hindu_gods_questions,
    'indian_history.json': indian_history_questions,
    'indian_culture.json': indian_culture_questions
}

for filename, questions in data_map.items():
    with open(f'd:/project/qgame/qgame/data/{filename}', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    print(f"Created {filename}")
