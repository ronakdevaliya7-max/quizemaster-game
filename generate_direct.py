import json
import os

mahabharata_questions = [
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who was the father of Pandavas?", "opt_a": "Dhritarashtra", "opt_b": "Pandu", "opt_c": "Vidura", "opt_d": "Shantanu"},
        "hi": {"text": "पांडवों के पिता कौन थे?", "opt_a": "धृतराष्ट्र", "opt_b": "पांडु", "opt_c": "विदुर", "opt_d": "शांतनु"},
        "gu": {"text": "પાંડવોના પિતા કોણ હતા?", "opt_a": "ધૃતરાષ્ટ્ર", "opt_b": "પાંડુ", "opt_c": "વિદુર", "opt_d": "શાંતનુ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who was the eldest Pandava?", "opt_a": "Bhima", "opt_b": "Arjuna", "opt_c": "Yudhishthira", "opt_d": "Nakula"},
        "hi": {"text": "सबसे बड़े पांडव कौन थे?", "opt_a": "भीम", "opt_b": "अर्जुन", "opt_c": "युधिष्ठिर", "opt_d": "नकुल"},
        "gu": {"text": "સૌથી મોટા પાંડવ કોણ હતા?", "opt_a": "ભીમ", "opt_b": "અર્જુન", "opt_c": "યુધિષ્ઠિર", "opt_d": "નકુલ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who was the mother of Kauravas?", "opt_a": "Kunti", "opt_b": "Madri", "opt_c": "Gandhari", "opt_d": "Satyavati"},
        "hi": {"text": "कौरवों की माता कौन थीं?", "opt_a": "कुंती", "opt_b": "माद्री", "opt_c": "गांधारी", "opt_d": "सत्यवती"},
        "gu": {"text": "કૌરવોની માતા કોણ હતા?", "opt_a": "કુંતી", "opt_b": "માદ્રી", "opt_c": "ગાંધારી", "opt_d": "સત્યવતી"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who was the guru of Pandavas and Kauravas?", "opt_a": "Dronacharya", "opt_b": "Kripacharya", "opt_c": "Parashurama", "opt_d": "Vishwamitra"},
        "hi": {"text": "पांडवों और कौरवों के गुरु कौन थे?", "opt_a": "द्रोणाचार्य", "opt_b": "कृपाचार्य", "opt_c": "परशुराम", "opt_d": "विश्वामित्र"},
        "gu": {"text": "પાંડવો અને કૌરવોના ગુરુ કોણ હતા?", "opt_a": "દ્રોણાચાર્ય", "opt_b": "કૃપાચાર્ય", "opt_c": "પરશુરામ", "opt_d": "વિશ્વામિત્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "What was the name of Arjuna's bow?", "opt_a": "Pinaka", "opt_b": "Gandiva", "opt_c": "Sharanga", "opt_d": "Vijaya"},
        "hi": {"text": "अर्जुन के धनुष का क्या नाम था?", "opt_a": "पिनाक", "opt_b": "गांडीव", "opt_c": "शारंग", "opt_d": "विजय"},
        "gu": {"text": "અર્જુનના ધનુષનું નામ શું હતું?", "opt_a": "પિનાક", "opt_b": "ગાંડીવ", "opt_c": "શારંગ", "opt_d": "વિજય"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who wrote the Mahabharata?", "opt_a": "Valmiki", "opt_b": "Ved Vyasa", "opt_c": "Tulsidas", "opt_d": "Kalidasa"},
        "hi": {"text": "महाभारत किसने लिखा था?", "opt_a": "वाल्मीकि", "opt_b": "वेद व्यास", "opt_c": "तुलसीदास", "opt_d": "कालिदास"},
        "gu": {"text": "મહાભારત કોણે લખ્યું હતું?", "opt_a": "વાલ્મીકિ", "opt_b": "વેદ વ્યાસ", "opt_c": "તુલસીદાસ", "opt_d": "કાલિદાસ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "How many days did the Kurukshetra war last?", "opt_a": "14", "opt_b": "16", "opt_c": "18", "opt_d": "20"},
        "hi": {"text": "कुरुक्षेत्र का युद्ध कितने दिनों तक चला था?", "opt_a": "14", "opt_b": "16", "opt_c": "18", "opt_d": "20"},
        "gu": {"text": "કુરુક્ષેત્રનું યુદ્ધ કેટલા દિવસ ચાલ્યું હતું?", "opt_a": "14", "opt_b": "16", "opt_c": "18", "opt_d": "20"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who killed Karna?", "opt_a": "Bhima", "opt_b": "Yudhishthira", "opt_c": "Arjuna", "opt_d": "Abhimanyu"},
        "hi": {"text": "कर्ण का वध किसने किया?", "opt_a": "भीम", "opt_b": "युधिष्ठिर", "opt_c": "अर्जुन", "opt_d": "अभिमन्यु"},
        "gu": {"text": "કર્ણનો વધ કોણે કર્યો?", "opt_a": "ભીમ", "opt_b": "યુધિષ્ઠિર", "opt_c": "અર્જુન", "opt_d": "અભિમન્યુ"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "What was the real name of Bhishma?", "opt_a": "Devavrata", "opt_b": "Shantanu", "opt_c": "Chitrangada", "opt_d": "Vichitravirya"},
        "hi": {"text": "भीष्म का असली नाम क्या था?", "opt_a": "देवव्रत", "opt_b": "शांतनु", "opt_c": "चित्रांगद", "opt_d": "विचित्रवीर्य"},
        "gu": {"text": "ભીષ્મનું સાચું નામ શું હતું?", "opt_a": "દેવવ્રત", "opt_b": "શાંતનુ", "opt_c": "ચિત્રાંગદ", "opt_d": "વિચિત્રવીર્ય"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who was the father of Abhimanyu?", "opt_a": "Yudhishthira", "opt_b": "Bhima", "opt_c": "Arjuna", "opt_d": "Nakula"},
        "hi": {"text": "अभिमन्यु के पिता कौन थे?", "opt_a": "युधिष्ठिर", "opt_b": "भीम", "opt_c": "अर्जुन", "opt_d": "नकुल"},
        "gu": {"text": "અભિમન્યુના પિતા કોણ હતા?", "opt_a": "યુધિષ્ઠિર", "opt_b": "ભીમ", "opt_c": "અર્જુન", "opt_d": "નકુલ"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who was the wife of all five Pandavas?", "opt_a": "Draupadi", "opt_b": "Subhadra", "opt_c": "Ulupi", "opt_d": "Chitrangada"},
        "hi": {"text": "पांचों पांडवों की पत्नी कौन थी?", "opt_a": "द्रौपदी", "opt_b": "सुभद्रा", "opt_c": "उलूपी", "opt_d": "चित्रांगदा"},
        "gu": {"text": "પાંચેય પાંડવોની પત્ની કોણ હતી?", "opt_a": "દ્રૌપદી", "opt_b": "સુભદ્રા", "opt_c": "ઉલૂપી", "opt_d": "ચિત્રાંગદા"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who killed Dushasana?", "opt_a": "Bhima", "opt_b": "Arjuna", "opt_c": "Yudhishthira", "opt_d": "Sahadeva"},
        "hi": {"text": "दुशासन को किसने मारा?", "opt_a": "भीम", "opt_b": "अर्जुन", "opt_c": "युधिष्ठिर", "opt_d": "सहदेव"},
        "gu": {"text": "દુશાસનને કોણે માર્યો?", "opt_a": "ભીમ", "opt_b": "અર્જુન", "opt_c": "યુધિષ્ઠિર", "opt_d": "સહદેવ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "What game did the Pandavas lose to the Kauravas?", "opt_a": "Chess", "opt_b": "Dice", "opt_c": "Archery", "opt_d": "Wrestling"},
        "hi": {"text": "पांडव कौरवों से कौन सा खेल हार गए थे?", "opt_a": "शतरंज", "opt_b": "चौसर (पासा)", "opt_c": "तीरंदाजी", "opt_d": "कुश्ती"},
        "gu": {"text": "પાંડવો કૌરવો સામે કઈ રમત હારી ગયા હતા?", "opt_a": "ચેસ", "opt_b": "ચોપાટ (પાસા)", "opt_c": "તીરંદાજી", "opt_d": "કુસ્તી"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who was the charioteer of Arjuna?", "opt_a": "Krishna", "opt_b": "Sanjaya", "opt_c": "Drona", "opt_d": "Bhishma"},
        "hi": {"text": "अर्जुन के सारथी कौन थे?", "opt_a": "कृष्ण", "opt_b": "संजय", "opt_c": "द्रोण", "opt_d": "भीष्म"},
        "gu": {"text": "અર્જુનના સારથી કોણ હતા?", "opt_a": "કૃષ્ણ", "opt_b": "સંજય", "opt_c": "દ્રોણ", "opt_d": "ભીષ્મ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who recited the Bhagavad Gita?", "opt_a": "Sanjaya", "opt_b": "Krishna", "opt_c": "Vyasa", "opt_d": "Arjuna"},
        "hi": {"text": "भगवद गीता किसने सुनाई?", "opt_a": "संजय", "opt_b": "कृष्ण", "opt_c": "व्यास", "opt_d": "अर्जुन"},
        "gu": {"text": "ભગવદ ગીતા કોણે કહી હતી?", "opt_a": "સંજય", "opt_b": "કૃષ્ણ", "opt_c": "વ્યાસ", "opt_d": "અર્જુન"}
    }
]

hindu_gods_questions = [
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who is the preserver of the universe?", "opt_a": "Brahma", "opt_b": "Vishnu", "opt_c": "Shiva", "opt_d": "Indra"},
        "hi": {"text": "ब्रह्मांड के पालनहार कौन हैं?", "opt_a": "ब्रह्मा", "opt_b": "विष्णु", "opt_c": "शिव", "opt_d": "इंद्र"},
        "gu": {"text": "બ્રહ્માંડના પાલનહાર કોણ છે?", "opt_a": "બ્રહ્મા", "opt_b": "વિષ્ણુ", "opt_c": "શિવ", "opt_d": "ઇન્દ્ર"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who is the creator of the universe?", "opt_a": "Brahma", "opt_b": "Vishnu", "opt_c": "Shiva", "opt_d": "Indra"},
        "hi": {"text": "ब्रह्मांड के निर्माता कौन हैं?", "opt_a": "ब्रह्मा", "opt_b": "विष्णु", "opt_c": "शिव", "opt_d": "इंद्र"},
        "gu": {"text": "બ્રહ્માંડના સર્જક કોણ છે?", "opt_a": "બ્રહ્મા", "opt_b": "વિષ્ણુ", "opt_c": "શિવ", "opt_d": "ઇન્દ્ર"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who is the destroyer in the Holy Trinity?", "opt_a": "Brahma", "opt_b": "Vishnu", "opt_c": "Shiva", "opt_d": "Agni"},
        "hi": {"text": "पवित्र त्रिमूर्ति में संहारक कौन हैं?", "opt_a": "ब्रह्मा", "opt_b": "विष्णु", "opt_c": "शिव", "opt_d": "अग्नि"},
        "gu": {"text": "પવિત્ર ત્રિમૂર્તિમાં સંહારક કોણ છે?", "opt_a": "બ્રહ્મા", "opt_b": "વિષ્ણુ", "opt_c": "શિવ", "opt_d": "અગ્નિ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who is the goddess of wealth?", "opt_a": "Saraswati", "opt_b": "Parvati", "opt_c": "Lakshmi", "opt_d": "Durga"},
        "hi": {"text": "धन की देवी कौन हैं?", "opt_a": "सरस्वती", "opt_b": "पार्वती", "opt_c": "लक्ष्मी", "opt_d": "दुर्गा"},
        "gu": {"text": "ધનની દેવી કોણ છે?", "opt_a": "સરસ્વતી", "opt_b": "પાર્વતી", "opt_c": "લક્ષ્મી", "opt_d": "દુર્ગા"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who is the goddess of knowledge?", "opt_a": "Saraswati", "opt_b": "Parvati", "opt_c": "Lakshmi", "opt_d": "Kali"},
        "hi": {"text": "ज्ञान की देवी कौन हैं?", "opt_a": "सरस्वती", "opt_b": "पार्वती", "opt_c": "लक्ष्मी", "opt_d": "काली"},
        "gu": {"text": "જ્ઞાનની દેવી કોણ છે?", "opt_a": "સરસ્વતી", "opt_b": "પાર્વતી", "opt_c": "લક્ષ્મી", "opt_d": "કાલી"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "What is the weapon of Lord Indra?", "opt_a": "Trishul", "opt_b": "Sudarshana Chakra", "opt_c": "Vajra", "opt_d": "Gada"},
        "hi": {"text": "भगवान इंद्र का अस्त्र क्या है?", "opt_a": "त्रिशूल", "opt_b": "सुदर्शन चक्र", "opt_c": "वज्र", "opt_d": "गदा"},
        "gu": {"text": "ભગવાન ઇન્દ્રનું શસ્ત્ર કયું છે?", "opt_a": "ત્રિશૂળ", "opt_b": "સુદર્શન ચક્ર", "opt_c": "વજ્ર", "opt_d": "ગદા"}
    },
    {
        "difficulty": "Easy", "correct_option": "D",
        "en": {"text": "What is the vehicle of Lord Shiva?", "opt_a": "Lion", "opt_b": "Tiger", "opt_c": "Mouse", "opt_d": "Bull (Nandi)"},
        "hi": {"text": "भगवान शिव का वाहन क्या है?", "opt_a": "शेर", "opt_b": "बाघ", "opt_c": "चूहा", "opt_d": "बैल (नंदी)"},
        "gu": {"text": "ભગવાન શિવનું વાહન કયું છે?", "opt_a": "સિંહ", "opt_b": "વાઘ", "opt_c": "ઉંદર", "opt_d": "બળદ (નંદી)"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "What is the vehicle of Lord Vishnu?", "opt_a": "Garuda", "opt_b": "Hamsa", "opt_c": "Airavata", "opt_d": "Peacock"},
        "hi": {"text": "भगवान विष्णु का वाहन क्या है?", "opt_a": "गरुड़", "opt_b": "हंस", "opt_c": "ऐरावत", "opt_d": "मोर"},
        "gu": {"text": "ભગવાન વિષ્ણુનું વાહન કયું છે?", "opt_a": "ગરુડ", "opt_b": "હંસ", "opt_c": "ઐરાવત", "opt_d": "મોર"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who is the god of fire?", "opt_a": "Vayu", "opt_b": "Varuna", "opt_c": "Agni", "opt_d": "Yama"},
        "hi": {"text": "अग्नि के देवता कौन हैं?", "opt_a": "वायु", "opt_b": "वरुण", "opt_c": "अग्नि", "opt_d": "यम"},
        "gu": {"text": "અગ્નિના દેવતા કોણ છે?", "opt_a": "વાયુ", "opt_b": "વરુણ", "opt_c": "અગ્નિ", "opt_d": "યમ"}
    },
    {
        "difficulty": "Medium", "correct_option": "D",
        "en": {"text": "Who is the god of water/ocean?", "opt_a": "Agni", "opt_b": "Vayu", "opt_c": "Indra", "opt_d": "Varuna"},
        "hi": {"text": "जल/समुद्र के देवता कौन हैं?", "opt_a": "अग्नि", "opt_b": "वायु", "opt_c": "इंद्र", "opt_d": "वरुण"},
        "gu": {"text": "જળ/સમુદ્રના દેવતા કોણ છે?", "opt_a": "અગ્નિ", "opt_b": "વાયુ", "opt_c": "ઇન્દ્ર", "opt_d": "વરુણ"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who is the sun god?", "opt_a": "Surya", "opt_b": "Chandra", "opt_c": "Mangala", "opt_d": "Shukra"},
        "hi": {"text": "सूर्य देव कौन हैं?", "opt_a": "सूर्य", "opt_b": "चंद्र", "opt_c": "मंगल", "opt_d": "शुक्र"},
        "gu": {"text": "સૂર્ય દેવ કોણ છે?", "opt_a": "સૂર્ય", "opt_b": "ચંદ્ર", "opt_c": "મંગળ", "opt_d": "શુક્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Which god wears a crescent moon on his head?", "opt_a": "Shiva", "opt_b": "Vishnu", "opt_c": "Brahma", "opt_d": "Kartikeya"},
        "hi": {"text": "कौन से भगवान अपने सिर पर अर्धचंद्र धारण करते हैं?", "opt_a": "शिव", "opt_b": "विष्णु", "opt_c": "ब्रह्मा", "opt_d": "कार्तिकेय"},
        "gu": {"text": "કયા ભગવાન પોતાના માથા પર અર્ધચંદ્ર ધારણ કરે છે?", "opt_a": "શિવ", "opt_b": "વિષ્ણુ", "opt_c": "બ્રહ્મા", "opt_d": "કાર્તિકેય"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "What is the vehicle of Lord Ganesha?", "opt_a": "Mouse", "opt_b": "Peacock", "opt_c": "Lion", "opt_d": "Bull"},
        "hi": {"text": "भगवान गणेश का वाहन क्या है?", "opt_a": "चूहा", "opt_b": "मोर", "opt_c": "शेर", "opt_d": "बैल"},
        "gu": {"text": "ભગવાન ગણેશનું વાહન કયું છે?", "opt_a": "ઉંદર", "opt_b": "મોર", "opt_c": "સિંહ", "opt_d": "બળદ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who is the god of wealth?", "opt_a": "Indra", "opt_b": "Kubera", "opt_c": "Varuna", "opt_d": "Yama"},
        "hi": {"text": "धन के देवता कौन हैं?", "opt_a": "इंद्र", "opt_b": "कुबेर", "opt_c": "वरुण", "opt_d": "यम"},
        "gu": {"text": "ધનના દેવતા કોણ છે?", "opt_a": "ઇન્દ્ર", "opt_b": "કુબેર", "opt_c": "વરુણ", "opt_d": "યમ"}
    },
    {
        "difficulty": "Medium", "correct_option": "D",
        "en": {"text": "Which avatar of Vishnu was a half-man, half-lion?", "opt_a": "Varaha", "opt_b": "Kurma", "opt_c": "Matsya", "opt_d": "Narasimha"},
        "hi": {"text": "विष्णु का कौन सा अवतार आधा मनुष्य और आधा सिंह था?", "opt_a": "वराह", "opt_b": "कूर्म", "opt_c": "मत्स्य", "opt_d": "नरसिंह"},
        "gu": {"text": "વિષ્ણુનો કયો અવતાર અડધો મનુષ્ય અને અડધો સિંહ હતો?", "opt_a": "વરાહ", "opt_b": "કૂર્મ", "opt_c": "મત્સ્ય", "opt_d": "નરસિંહ"}
    }
]

indian_history_questions = [
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who was the first Prime Minister of India?", "opt_a": "Mahatma Gandhi", "opt_b": "Jawaharlal Nehru", "opt_c": "Sardar Patel", "opt_d": "B.R. Ambedkar"},
        "hi": {"text": "भारत के पहले प्रधानमंत्री कौन थे?", "opt_a": "महात्मा गांधी", "opt_b": "जवाहरलाल नेहरू", "opt_c": "सरदार पटेल", "opt_d": "बी.आर. अंबेडकर"},
        "gu": {"text": "ભારતના પ્રથમ વડાપ્રધાન કોણ હતા?", "opt_a": "મહાત્મા ગાંધી", "opt_b": "જવાહરલાલ નેહરુ", "opt_c": "સરદાર પટેલ", "opt_d": "બી.આર. આંબેડકર"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "In which year did India get independence?", "opt_a": "1945", "opt_b": "1947", "opt_c": "1950", "opt_d": "1952"},
        "hi": {"text": "भारत को किस वर्ष स्वतंत्रता मिली?", "opt_a": "1945", "opt_b": "1947", "opt_c": "1950", "opt_d": "1952"},
        "gu": {"text": "ભારતને કયા વર્ષમાં આઝાદી મળી?", "opt_a": "1945", "opt_b": "1947", "opt_c": "1950", "opt_d": "1952"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "When did India become a Republic?", "opt_a": "1947", "opt_b": "1948", "opt_c": "1950", "opt_d": "1952"},
        "hi": {"text": "भारत गणतंत्र कब बना?", "opt_a": "1947", "opt_b": "1948", "opt_c": "1950", "opt_d": "1952"},
        "gu": {"text": "ભારત પ્રજાસત્તાક ક્યારે બન્યું?", "opt_a": "1947", "opt_b": "1948", "opt_c": "1950", "opt_d": "1952"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who was the first President of India?", "opt_a": "Dr. Rajendra Prasad", "opt_b": "Dr. S. Radhakrishnan", "opt_c": "Zakir Husain", "opt_d": "V. V. Giri"},
        "hi": {"text": "भारत के पहले राष्ट्रपति कौन थे?", "opt_a": "डॉ. राजेंद्र प्रसाद", "opt_b": "डॉ. एस. राधाकृष्णन", "opt_c": "जाकिर हुसैन", "opt_d": "वी. वी. गिरि"},
        "gu": {"text": "ભારતના પ્રથમ રાષ્ટ્રપતિ કોણ હતા?", "opt_a": "ડૉ. રાજેન્દ્ર પ્રસાદ", "opt_b": "ડૉ. એસ. રાધાકૃષ્ણન", "opt_c": "ઝાકિર હુસૈન", "opt_d": "વી. વી. ગિરી"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who wrote the Indian National Anthem?", "opt_a": "Bankim Chandra Chatterjee", "opt_b": "Rabindranath Tagore", "opt_c": "Sarojini Naidu", "opt_d": "Subramania Bharati"},
        "hi": {"text": "भारतीय राष्ट्रगान किसने लिखा था?", "opt_a": "बंकिम चंद्र चटर्जी", "opt_b": "रवींद्रनाथ टैगोर", "opt_c": "सरोजिनी नायडू", "opt_d": "सुब्रमण्य भारती"},
        "gu": {"text": "ભારતીય રાષ્ટ્રગીત કોણે લખ્યું હતું?", "opt_a": "બંકિમચંદ્ર ચેટરજી", "opt_b": "રવીન્દ્રનાથ ટાગોર", "opt_c": "સરોજિની નાયડુ", "opt_d": "સુબ્રમણ્ય ભારતી"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who was the founder of the Maurya Empire?", "opt_a": "Ashoka", "opt_b": "Chandragupta Maurya", "opt_c": "Bindusara", "opt_d": "Dasharatha"},
        "hi": {"text": "मौर्य साम्राज्य के संस्थापक कौन थे?", "opt_a": "अशोक", "opt_b": "चंद्रगुप्त मौर्य", "opt_c": "बिंदुसार", "opt_d": "दशरथ"},
        "gu": {"text": "મૌર્ય સામ્રાજ્યના સ્થાપક કોણ હતા?", "opt_a": "અશોક", "opt_b": "ચંદ્રગુપ્ત મૌર્ય", "opt_c": "બિંદુસાર", "opt_d": "દશરથ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who was the founder of the Mughal Empire in India?", "opt_a": "Akbar", "opt_b": "Humayun", "opt_c": "Babur", "opt_d": "Shah Jahan"},
        "hi": {"text": "भारत में मुगल साम्राज्य का संस्थापक कौन था?", "opt_a": "अकबर", "opt_b": "हुमायूँ", "opt_c": "बाबर", "opt_d": "शाहजहाँ"},
        "gu": {"text": "ભારતમાં મુઘલ સામ્રાજ્યનો સ્થાપક કોણ હતો?", "opt_a": "અકબર", "opt_b": "હુમાયુ", "opt_c": "બાબર", "opt_d": "શાહજહાં"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Which Mughal emperor built the Taj Mahal?", "opt_a": "Akbar", "opt_b": "Jahangir", "opt_c": "Shah Jahan", "opt_d": "Aurangzeb"},
        "hi": {"text": "किस मुगल सम्राट ने ताजमहल बनवाया था?", "opt_a": "अकबर", "opt_b": "जहांगीर", "opt_c": "शाहजहाँ", "opt_d": "औरंगजेब"},
        "gu": {"text": "કયા મુઘલ સમ્રાટે તાજમહેલ બનાવ્યો હતો?", "opt_a": "અકબર", "opt_b": "જહાંગીર", "opt_c": "શાહજહાં", "opt_d": "ઔરંગઝેબ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who was the first female Prime Minister of India?", "opt_a": "Sarojini Naidu", "opt_b": "Indira Gandhi", "opt_c": "Pratibha Patil", "opt_d": "Sonia Gandhi"},
        "hi": {"text": "भारत की पहली महिला प्रधानमंत्री कौन थीं?", "opt_a": "सरोजिनी नायडू", "opt_b": "इंदिरा गांधी", "opt_c": "प्रतिभा पाटिल", "opt_d": "सोनिया गांधी"},
        "gu": {"text": "ભારતના પ્રથમ મહિલા વડાપ્રધાન કોણ હતા?", "opt_a": "સરોજિની નાયડુ", "opt_b": "ઇન્દિરા ગાંધી", "opt_c": "પ્રતિભા પાટીલ", "opt_d": "સોનિયા ગાંધી"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who gave the slogan 'Give me blood, and I shall give you freedom'?", "opt_a": "Bhagat Singh", "opt_b": "Chandra Shekhar Azad", "opt_c": "Subhas Chandra Bose", "opt_d": "Lala Lajpat Rai"},
        "hi": {"text": "'तुम मुझे खून दो, मैं तुम्हें आजादी दूंगा' का नारा किसने दिया था?", "opt_a": "भगत सिंह", "opt_b": "चंद्रशेखर आजाद", "opt_c": "सुभाष चंद्र बोस", "opt_d": "लाला लाजपत राय"},
        "gu": {"text": "'તમે મને લોહી આપો, હું તમને આઝાદી આપીશ' આ નારો કોણે આપ્યો હતો?", "opt_a": "ભગત સિંહ", "opt_b": "ચંદ્રશેખર આઝાદ", "opt_c": "સુભાષચંદ્ર બોઝ", "opt_d": "લાલા લાજપત રાય"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "The Indian National Congress was founded in which year?", "opt_a": "1885", "opt_b": "1905", "opt_c": "1919", "opt_d": "1942"},
        "hi": {"text": "भारतीय राष्ट्रीय कांग्रेस की स्थापना किस वर्ष हुई थी?", "opt_a": "1885", "opt_b": "1905", "opt_c": "1919", "opt_d": "1942"},
        "gu": {"text": "ભારતીય રાષ્ટ્રીય કોંગ્રેસની સ્થાપના કયા વર્ષમાં થઈ હતી?", "opt_a": "1885", "opt_b": "1905", "opt_c": "1919", "opt_d": "1942"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "When did the Jallianwala Bagh massacre occur?", "opt_a": "1917", "opt_b": "1919", "opt_c": "1921", "opt_d": "1923"},
        "hi": {"text": "जलियांवाला बाग हत्याकांड कब हुआ था?", "opt_a": "1917", "opt_b": "1919", "opt_c": "1921", "opt_d": "1923"},
        "gu": {"text": "જલિયાંવાલા બાગ હત્યાકાંડ ક્યારે થયો હતો?", "opt_a": "1917", "opt_b": "1919", "opt_c": "1921", "opt_d": "1923"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Which movement was launched in 1942?", "opt_a": "Non-Cooperation Movement", "opt_b": "Civil Disobedience Movement", "opt_c": "Quit India Movement", "opt_d": "Swadeshi Movement"},
        "hi": {"text": "1942 में कौन सा आंदोलन शुरू किया गया था?", "opt_a": "असहयोग आंदोलन", "opt_b": "सविनय अवज्ञा आंदोलन", "opt_c": "भारत छोड़ो आंदोलन", "opt_d": "स्वदेशी आंदोलन"},
        "gu": {"text": "1942 માં કયું આંદોલન શરૂ કરવામાં આવ્યું હતું?", "opt_a": "અસહકાર આંદોલન", "opt_b": "સવિનય કાનૂન ભંગ આંદોલન", "opt_c": "ભારત છોડો આંદોલન", "opt_d": "સ્વદેશી આંદોલન"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who was the main architect of the Indian Constitution?", "opt_a": "Jawaharlal Nehru", "opt_b": "B. R. Ambedkar", "opt_c": "Rajendra Prasad", "opt_d": "B. N. Rau"},
        "hi": {"text": "भारतीय संविधान के मुख्य निर्माता कौन थे?", "opt_a": "जवाहरलाल नेहरू", "opt_b": "बी. आर. अंबेडकर", "opt_c": "राजेंद्र प्रसाद", "opt_d": "बी. एन. राव"},
        "gu": {"text": "ભારતીય બંધારણના મુખ્ય ઘડવૈયા કોણ હતા?", "opt_a": "જવાહરલાલ નેહરુ", "opt_b": "બી. આર. આંબેડકર", "opt_c": "રાજેન્દ્ર પ્રસાદ", "opt_d": "બી. એન. રાવ"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "The first battle of Panipat was fought in?", "opt_a": "1526", "opt_b": "1556", "opt_c": "1761", "opt_d": "1857"},
        "hi": {"text": "पानीपत का प्रथम युद्ध कब लड़ा गया था?", "opt_a": "1526", "opt_b": "1556", "opt_c": "1761", "opt_d": "1857"},
        "gu": {"text": "પાણીપતનું પ્રથમ યુદ્ધ ક્યારે લડાયું હતું?", "opt_a": "1526", "opt_b": "1556", "opt_c": "1761", "opt_d": "1857"}
    }
]

indian_culture_questions = [
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Which festival is known as the Festival of Colors?", "opt_a": "Diwali", "opt_b": "Holi", "opt_c": "Navratri", "opt_d": "Dussehra"},
        "hi": {"text": "किस त्योहार को रंगों का त्योहार कहा जाता है?", "opt_a": "दिवाली", "opt_b": "होली", "opt_c": "नवरात्रि", "opt_d": "दशहरा"},
        "gu": {"text": "કયા તહેવારને રંગોના તહેવાર તરીકે ઓળખવામાં આવે છે?", "opt_a": "દિવાળી", "opt_b": "હોળી", "opt_c": "નવરાત્રી", "opt_d": "દશેરા"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Which festival is known as the Festival of Lights?", "opt_a": "Holi", "opt_b": "Diwali", "opt_c": "Eid", "opt_d": "Christmas"},
        "hi": {"text": "किस त्योहार को रोशनी का त्योहार कहा जाता है?", "opt_a": "होली", "opt_b": "दिवाली", "opt_c": "ईद", "opt_d": "क्रिसमस"},
        "gu": {"text": "કયા તહેવારને પ્રકાશના તહેવાર તરીકે ઓળખવામાં આવે છે?", "opt_a": "હોળી", "opt_b": "દિવાળી", "opt_c": "ઈદ", "opt_d": "નાતાલ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Bharatanatyam is a classical dance from which state?", "opt_a": "Kerala", "opt_b": "Tamil Nadu", "opt_c": "Andhra Pradesh", "opt_d": "Odisha"},
        "hi": {"text": "भरतनाट्यम किस राज्य का शास्त्रीय नृत्य है?", "opt_a": "केरल", "opt_b": "तमिलनाडु", "opt_c": "आंध्र प्रदेश", "opt_d": "ओडिशा"},
        "gu": {"text": "ભરતનાટ્યમ કયા રાજ્યનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "કેરળ", "opt_b": "તમિલનાડુ", "opt_c": "આંધ્ર પ્રદેશ", "opt_d": "ઓડિશા"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Kathakali is a classical dance from which state?", "opt_a": "Kerala", "opt_b": "Karnataka", "opt_c": "Tamil Nadu", "opt_d": "Andhra Pradesh"},
        "hi": {"text": "कथकली किस राज्य का शास्त्रीय नृत्य है?", "opt_a": "केरल", "opt_b": "कर्नाटक", "opt_c": "तमिलनाडु", "opt_d": "आंध्र प्रदेश"},
        "gu": {"text": "કથકલી કયા રાજ્યનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "કેરળ", "opt_b": "કર્ણાટક", "opt_c": "તમિલનાડુ", "opt_d": "આંધ્ર પ્રદેશ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Kathak is a classical dance form mainly from?", "opt_a": "South India", "opt_b": "East India", "opt_c": "North India", "opt_d": "West India"},
        "hi": {"text": "कथक मुख्य रूप से कहाँ का शास्त्रीय नृत्य है?", "opt_a": "दक्षिण भारत", "opt_b": "पूर्वी भारत", "opt_c": "उत्तर भारत", "opt_d": "पश्चिम भारत"},
        "gu": {"text": "કથક મુખ્યત્વે ક્યાંનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "દક્ષિણ ભારત", "opt_b": "પૂર્વ ભારત", "opt_c": "ઉત્તર ભારત", "opt_d": "પશ્ચિમ ભારત"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Garba is a popular folk dance of which state?", "opt_a": "Maharashtra", "opt_b": "Gujarat", "opt_c": "Rajasthan", "opt_d": "Punjab"},
        "hi": {"text": "गरबा किस राज्य का लोकप्रिय लोक नृत्य है?", "opt_a": "महाराष्ट्र", "opt_b": "गुजरात", "opt_c": "राजस्थान", "opt_d": "पंजाब"},
        "gu": {"text": "ગરબા કયા રાજ્યનું લોકપ્રિય લોક નૃત્ય છે?", "opt_a": "મહારાષ્ટ્ર", "opt_b": "ગુજરાત", "opt_c": "રાજસ્થાન", "opt_d": "પંજાબ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Bhangra is a traditional dance from which state?", "opt_a": "Gujarat", "opt_b": "Haryana", "opt_c": "Punjab", "opt_d": "Rajasthan"},
        "hi": {"text": "भांगड़ा किस राज्य का पारंपरिक नृत्य है?", "opt_a": "गुजरात", "opt_b": "हरियाणा", "opt_c": "पंजाब", "opt_d": "राजस्थान"},
        "gu": {"text": "ભાંગડા કયા રાજ્યનું પરંપરાગત નૃત્ય છે?", "opt_a": "ગુજરાત", "opt_b": "હરિયાણા", "opt_c": "પંજાબ", "opt_d": "રાજસ્થાન"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "What is the traditional garment worn by Indian women?", "opt_a": "Kimono", "opt_b": "Sari", "opt_c": "Hanbok", "opt_d": "Cheongsam"},
        "hi": {"text": "भारतीय महिलाओं द्वारा पहना जाने वाला पारंपरिक परिधान क्या है?", "opt_a": "किमोनो", "opt_b": "साड़ी", "opt_c": "हनबोक", "opt_d": "चेओंगसम"},
        "gu": {"text": "ભારતીય સ્ત્રીઓ દ્વારા પહેરવામાં આવતો પરંપરાગત પોશાક કયો છે?", "opt_a": "કિમોનો", "opt_b": "સાડી", "opt_c": "હાનબોક", "opt_d": "ચેઓંગસમ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Which language is known as the 'mother of all languages' in India?", "opt_a": "Hindi", "opt_b": "Tamil", "opt_c": "Sanskrit", "opt_d": "Prakrit"},
        "hi": {"text": "भारत में किस भाषा को 'सभी भाषाओं की जननी' कहा जाता है?", "opt_a": "हिंदी", "opt_b": "तमिल", "opt_c": "संस्कृत", "opt_d": "प्राकृत"},
        "gu": {"text": "ભારતમાં કઈ ભાષાને 'બધી ભાષાઓની માતા' કહેવામાં આવે છે?", "opt_a": "હિન્દી", "opt_b": "તમિલ", "opt_c": "સંસ્કૃત", "opt_d": "પ્રાકૃત"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Onam is a major festival of which state?", "opt_a": "Kerala", "opt_b": "Tamil Nadu", "opt_c": "Karnataka", "opt_d": "Andhra Pradesh"},
        "hi": {"text": "ओणम किस राज्य का प्रमुख त्योहार है?", "opt_a": "केरल", "opt_b": "तमिलनाडु", "opt_c": "कर्नाटक", "opt_d": "आंध्र प्रदेश"},
        "gu": {"text": "ઓણમ કયા રાજ્યનો મુખ્ય તહેવાર છે?", "opt_a": "કેરળ", "opt_b": "તમિલનાડુ", "opt_c": "કર્ણાટક", "opt_d": "આંધ્ર પ્રદેશ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Pongal is a harvest festival celebrated in?", "opt_a": "Kerala", "opt_b": "Tamil Nadu", "opt_c": "Andhra Pradesh", "opt_d": "Karnataka"},
        "hi": {"text": "पोंगल फसल का त्योहार कहाँ मनाया जाता है?", "opt_a": "केरल", "opt_b": "तमिलनाडु", "opt_c": "आंध्र प्रदेश", "opt_d": "कर्नाटक"},
        "gu": {"text": "પોંગલ લણણીનો તહેવાર ક્યાં ઉજવવામાં આવે છે?", "opt_a": "કેરળ", "opt_b": "તમિલનાડુ", "opt_c": "આંધ્ર પ્રદેશ", "opt_d": "કર્ણાટક"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Which Indian festival celebrates the bond between brothers and sisters?", "opt_a": "Diwali", "opt_b": "Holi", "opt_c": "Raksha Bandhan", "opt_d": "Navratri"},
        "hi": {"text": "कौन सा भारतीय त्योहार भाई-बहनों के बीच के बंधन का जश्न मनाता है?", "opt_a": "दिवाली", "opt_b": "होली", "opt_c": "रक्षा बंधन", "opt_d": "नवरात्रि"},
        "gu": {"text": "કયો ભારતીય તહેવાર ભાઈ-બહેન વચ્ચેના પ્રેમને ઉજવે છે?", "opt_a": "દિવાળી", "opt_b": "હોળી", "opt_c": "રક્ષાબંધન", "opt_d": "નવરાત્રી"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Which Indian musician popularized the sitar in the West?", "opt_a": "Zakir Hussain", "opt_b": "Ravi Shankar", "opt_c": "A. R. Rahman", "opt_d": "Bismillah Khan"},
        "hi": {"text": "किस भारतीय संगीतकार ने पश्चिम में सितार को लोकप्रिय बनाया?", "opt_a": "जाकिर हुसैन", "opt_b": "रवि शंकर", "opt_c": "ए. आर. रहमान", "opt_d": "बिस्मिल्लाह खान"},
        "gu": {"text": "કયા ભારતીય સંગીતકારે પશ્ચિમમાં સિતારને લોકપ્રિય બનાવ્યો?", "opt_a": "ઝાકિર હુસૈન", "opt_b": "રવિ શંકર", "opt_c": "એ. આર. રહેમાન", "opt_d": "બિસ્મિલ્લાહ ખાન"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Which is the largest religion in India?", "opt_a": "Islam", "opt_b": "Christianity", "opt_c": "Hinduism", "opt_d": "Sikhism"},
        "hi": {"text": "भारत में सबसे बड़ा धर्म कौन सा है?", "opt_a": "इस्लाम", "opt_b": "ईसाई धर्म", "opt_c": "हिंदू धर्म", "opt_d": "सिख धर्म"},
        "gu": {"text": "ભારતમાં સૌથી મોટો ધર્મ કયો છે?", "opt_a": "ઇસ્લામ", "opt_b": "ખ્રિસ્તી ધર્મ", "opt_c": "હિન્દુ ધર્મ", "opt_d": "શીખ ધર્મ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "The Golden Temple is located in which city?", "opt_a": "Chandigarh", "opt_b": "Amritsar", "opt_c": "Ludhiana", "opt_d": "Jalandhar"},
        "hi": {"text": "स्वर्ण मंदिर किस शहर में स्थित है?", "opt_a": "चंडीगढ़", "opt_b": "अमृतसर", "opt_c": "लुधियाना", "opt_d": "जालंधर"},
        "gu": {"text": "સુવર્ણ મંદિર કયા શહેરમાં આવેલું છે?", "opt_a": "ચંડીગઢ", "opt_b": "અમૃતસર", "opt_c": "લુધિયાણા", "opt_d": "જાલંધર"}
    }
]

import os
os.makedirs('d:/project/qgame/qgame/data', exist_ok=True)

with open('d:/project/qgame/qgame/data/mahabharata_part2.json', 'w', encoding='utf-8') as f:
    json.dump(mahabharata_questions, f, ensure_ascii=False, indent=4)

with open('d:/project/qgame/qgame/data/hindu_gods_part2.json', 'w', encoding='utf-8') as f:
    json.dump(hindu_gods_questions, f, ensure_ascii=False, indent=4)

with open('d:/project/qgame/qgame/data/indian_history_part2.json', 'w', encoding='utf-8') as f:
    json.dump(indian_history_questions, f, ensure_ascii=False, indent=4)

with open('d:/project/qgame/qgame/data/indian_culture_part2.json', 'w', encoding='utf-8') as f:
    json.dump(indian_culture_questions, f, ensure_ascii=False, indent=4)
    
print("Generated direct JSON files.")
