import json
import os

mahabharata_questions = [
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who vowed to kill Bhishma?", "opt_a": "Amba", "opt_b": "Ambalika", "opt_c": "Ambika", "opt_d": "Gandhari"},
        "hi": {"text": "भीष्म को मारने की प्रतिज्ञा किसने की थी?", "opt_a": "अंबा", "opt_b": "अंबालिका", "opt_c": "अंबिका", "opt_d": "गांधारी"},
        "gu": {"text": "ભીષ્મને મારવાની પ્રતિજ્ઞા કોણે લીધી હતી?", "opt_a": "અંબા", "opt_b": "અંબાલિકા", "opt_c": "અંબિકા", "opt_d": "ગાંધારી"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who killed Jayadratha?", "opt_a": "Arjuna", "opt_b": "Bhima", "opt_c": "Yudhishthira", "opt_d": "Satyaki"},
        "hi": {"text": "जयद्रथ का वध किसने किया?", "opt_a": "अर्जुन", "opt_b": "भीम", "opt_c": "युधिष्ठिर", "opt_d": "सात्यकि"},
        "gu": {"text": "જયદ્રથનો વધ કોણે કર્યો?", "opt_a": "અર્જુન", "opt_b": "ભીમ", "opt_c": "યુધિષ્ઠિર", "opt_d": "સાત્યકિ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who was the eldest Kaurava?", "opt_a": "Dushasana", "opt_b": "Vikarna", "opt_c": "Duryodhana", "opt_d": "Yuyutsu"},
        "hi": {"text": "सबसे बड़ा कौरव कौन था?", "opt_a": "दुशासन", "opt_b": "विकर्ण", "opt_c": "दुर्योधधन", "opt_d": "युयुत्सु"},
        "gu": {"text": "સૌથી મોટો કૌરવ કોણ હતો?", "opt_a": "દુશાસન", "opt_b": "વિકર્ણ", "opt_c": "દુર્યોધન", "opt_d": "યુયુત્સુ"}
    },
    {
        "difficulty": "Hard", "correct_option": "D",
        "en": {"text": "Who survived the Kurukshetra war from the Kaurava side?", "opt_a": "Ashwatthama", "opt_b": "Kritavarma", "opt_c": "Kripacharya", "opt_d": "All of the above"},
        "hi": {"text": "कुरुक्षेत्र युद्ध में कौरवों की ओर से कौन जीवित बचा था?", "opt_a": "अश्वत्थामा", "opt_b": "कृतवर्मा", "opt_c": "कृपाचार्य", "opt_d": "उपरोक्त सभी"},
        "gu": {"text": "કુરુક્ષેત્રના યુદ્ધમાં કૌરવો તરફથી કોણ જીવિત બચ્યું હતું?", "opt_a": "અશ્વત્થામા", "opt_b": "કૃતવર્મા", "opt_c": "કૃપાચાર્ય", "opt_d": "ઉપરોક્ત તમામ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "To whom did Krishna recite the Bhagavad Gita?", "opt_a": "Yudhishthira", "opt_b": "Bhima", "opt_c": "Arjuna", "opt_d": "Duryodhana"},
        "hi": {"text": "कृष्ण ने भगवद गीता किसे सुनाई थी?", "opt_a": "युधिष्ठिर", "opt_b": "भीम", "opt_c": "अर्जुन", "opt_d": "दुर्योधन"},
        "gu": {"text": "કૃષ્ણે ભગવદ ગીતા કોને સંભળાવી હતી?", "opt_a": "યુધિષ્ઠિર", "opt_b": "ભીમ", "opt_c": "અર્જુન", "opt_d": "દુર્યોધન"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who was the mother of Karna?", "opt_a": "Kunti", "opt_b": "Radha", "opt_c": "Gandhari", "opt_d": "Madri"},
        "hi": {"text": "कर्ण की माता कौन थीं?", "opt_a": "कुंती", "opt_b": "राधा", "opt_c": "गांधारी", "opt_d": "माद्री"},
        "gu": {"text": "કર્ણની માતા કોણ હતા?", "opt_a": "કુંતી", "opt_b": "રાધા", "opt_c": "ગાંધારી", "opt_d": "માદ્રી"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who raised Karna?", "opt_a": "Adhiratha and Radha", "opt_b": "Nanda and Yashoda", "opt_c": "Pandu and Kunti", "opt_d": "Dhritarashtra and Gandhari"},
        "hi": {"text": "कर्ण का पालन-पोषण किसने किया?", "opt_a": "अधिरथ और राधा", "opt_b": "नंद और यशोदा", "opt_c": "पांडु और कुंती", "opt_d": "धृतराष्ट्र और गांधारी"},
        "gu": {"text": "કર્ણનો ઉછેર કોણે કર્યો હતો?", "opt_a": "અધિરથ અને રાધા", "opt_b": "નંદ અને યશોદા", "opt_c": "પાંડુ અને કુંતી", "opt_d": "ધૃતરાષ્ટ્ર અને ગાંધારી"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who was the blind king of Hastinapur?", "opt_a": "Pandu", "opt_b": "Dhritarashtra", "opt_c": "Shantanu", "opt_d": "Vichitravirya"},
        "hi": {"text": "हस्तिनापुर का अंधा राजा कौन था?", "opt_a": "पांडु", "opt_b": "धृतराष्ट्र", "opt_c": "शांतनु", "opt_d": "विचित्रवीर्य"},
        "gu": {"text": "હસ્તિનાપુરના અંધ રાજા કોણ હતા?", "opt_a": "પાંડુ", "opt_b": "ધૃતરાષ્ટ્ર", "opt_c": "શાંતનુ", "opt_d": "વિચિત્રવીર્ય"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who was the uncle of Kauravas?", "opt_a": "Shakuni", "opt_b": "Vidura", "opt_c": "Shalya", "opt_d": "Kripa"},
        "hi": {"text": "कौरवों के मामा कौन थे?", "opt_a": "शकुनि", "opt_b": "विदुर", "opt_c": "शल्य", "opt_d": "कृपा"},
        "gu": {"text": "કૌરવોના મામા કોણ હતા?", "opt_a": "શકુનિ", "opt_b": "વિદુર", "opt_c": "શલ્ય", "opt_d": "કૃપા"}
    },
    {
        "difficulty": "Hard", "correct_option": "D",
        "en": {"text": "What was the name of Yudhishthira's conch?", "opt_a": "Panchajanya", "opt_b": "Devadatta", "opt_c": "Paundra", "opt_d": "Anantavijaya"},
        "hi": {"text": "युधिष्ठिर के शंख का क्या नाम था?", "opt_a": "पांचजन्य", "opt_b": "देवदत्त", "opt_c": "पौंड्र", "opt_d": "अनंतविजय"},
        "gu": {"text": "યુધિષ્ઠિરના શંખનું નામ શું હતું?", "opt_a": "પાંચજન્ય", "opt_b": "દેવદત્ત", "opt_c": "પૌંડ્ર", "opt_d": "અનંતવિજય"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who killed Shakuni?", "opt_a": "Bhima", "opt_b": "Sahadeva", "opt_c": "Nakula", "opt_d": "Arjuna"},
        "hi": {"text": "शकुनि का वध किसने किया?", "opt_a": "भीम", "opt_b": "सहदेव", "opt_c": "नकुल", "opt_d": "अर्जुन"},
        "gu": {"text": "શકુનિનો વધ કોણે કર્યો?", "opt_a": "ભીમ", "opt_b": "સહદેવ", "opt_c": "નકુલ", "opt_d": "અર્જુન"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who killed Shalya?", "opt_a": "Yudhishthira", "opt_b": "Arjuna", "opt_c": "Bhima", "opt_d": "Nakula"},
        "hi": {"text": "शल्य का वध किसने किया?", "opt_a": "युधिष्ठिर", "opt_b": "अर्जुन", "opt_c": "भीम", "opt_d": "नकुल"},
        "gu": {"text": "શલ્યનો વધ કોણે કર્યો?", "opt_a": "યુધિષ્ઠિર", "opt_b": "અર્જુન", "opt_c": "ભીમ", "opt_d": "નકુલ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who was the commander of Kaurava army on the first day?", "opt_a": "Drona", "opt_b": "Bhishma", "opt_c": "Karna", "opt_d": "Shalya"},
        "hi": {"text": "पहले दिन कौरव सेना का सेनापति कौन था?", "opt_a": "द्रोण", "opt_b": "भीष्म", "opt_c": "कर्ण", "opt_d": "शल्य"},
        "gu": {"text": "પ્રથમ દિવસે કૌરવ સેનાના સેનાપતિ કોણ હતા?", "opt_a": "દ્રોણ", "opt_b": "ભીષ્મ", "opt_c": "કર્ણ", "opt_d": "શલ્ય"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "For how many days was Bhishma the commander?", "opt_a": "10", "opt_b": "5", "opt_c": "2", "opt_d": "18"},
        "hi": {"text": "भीष्म कितने दिनों तक सेनापति रहे?", "opt_a": "10", "opt_b": "5", "opt_c": "2", "opt_d": "18"},
        "gu": {"text": "ભીષ્મ કેટલા દિવસ સુધી સેનાપતિ રહ્યા?", "opt_a": "10", "opt_b": "5", "opt_c": "2", "opt_d": "18"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who created the Chakravyuha on the 13th day?", "opt_a": "Bhishma", "opt_b": "Drona", "opt_c": "Karna", "opt_d": "Shalya"},
        "hi": {"text": "13वें दिन चक्रव्यूह की रचना किसने की थी?", "opt_a": "भीष्म", "opt_b": "द्रोण", "opt_c": "कर्ण", "opt_d": "शल्य"},
        "gu": {"text": "13મા દિવસે ચક્રવ્યૂહની રચના કોણે કરી હતી?", "opt_a": "ભીષ્મ", "opt_b": "દ્રોણ", "opt_c": "કર્ણ", "opt_d": "શલ્ય"}
    },
    {
        "difficulty": "Medium", "correct_option": "D",
        "en": {"text": "Who killed Abhimanyu?", "opt_a": "Karna", "opt_b": "Dushasana", "opt_c": "Jayadratha", "opt_d": "Multiple warriors"},
        "hi": {"text": "अभिमन्यु का वध किसने किया?", "opt_a": "कर्ण", "opt_b": "दुशासन", "opt_c": "जयद्रथ", "opt_d": "कई योद्धाओं ने"},
        "gu": {"text": "અભિમન્યુનો વધ કોણે કર્યો?", "opt_a": "કર્ણ", "opt_b": "દુશાસન", "opt_c": "જયદ્રથ", "opt_d": "ઘણા યોદ્ધાઓએ"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "What was the name of Bhima's mace?", "opt_a": "Kaumodaki", "opt_b": "Vayavya", "opt_c": "Gada", "opt_d": "Vajra"},
        "hi": {"text": "भीम की गदा का क्या नाम था?", "opt_a": "कौमोदकी", "opt_b": "वायव्य", "opt_c": "गदा", "opt_d": "वज्र"},
        "gu": {"text": "ભીમની ગદાનું નામ શું હતું?", "opt_a": "કૌમોદકી", "opt_b": "વાયવ્ય", "opt_c": "ગદા", "opt_d": "વજ્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who was the son of Bhima and Hidimbi?", "opt_a": "Ghatotkacha", "opt_b": "Barbarika", "opt_c": "Abhimanyu", "opt_d": "Iravan"},
        "hi": {"text": "भीम और हिडिम्बी का पुत्र कौन था?", "opt_a": "घटोत्कच", "opt_b": "बर्बरीक", "opt_c": "अभिमन्यु", "opt_d": "इरावान"},
        "gu": {"text": "ભીમ અને હિડિમ્બીનો પુત્ર કોણ હતો?", "opt_a": "ઘટોત્કચ", "opt_b": "બર્બરીક", "opt_c": "અભિમન્યુ", "opt_d": "ઇરાવાન"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who killed Ghatotkacha?", "opt_a": "Karna", "opt_b": "Drona", "opt_c": "Duryodhana", "opt_d": "Ashwatthama"},
        "hi": {"text": "घटोत्कच का वध किसने किया?", "opt_a": "कर्ण", "opt_b": "द्रोण", "opt_c": "दुर्योधन", "opt_d": "अश्वत्थामा"},
        "gu": {"text": "ઘટોત્કચનો વધ કોણે કર્યો?", "opt_a": "કર્ણ", "opt_b": "દ્રોણ", "opt_c": "દુર્યોધન", "opt_d": "અશ્વત્થામા"}
    },
    {
        "difficulty": "Hard", "correct_option": "C",
        "en": {"text": "Which weapon did Karna use to kill Ghatotkacha?", "opt_a": "Brahmastra", "opt_b": "Pashupatastra", "opt_c": "Vasavi Shakti", "opt_d": "Narayanastra"},
        "hi": {"text": "घटोत्कच को मारने के लिए कर्ण ने किस अस्त्र का उपयोग किया था?", "opt_a": "ब्रह्मास्त्र", "opt_b": "पाशुपतास्त्र", "opt_c": "वासवी शक्ति", "opt_d": "नारायणास्त्र"},
        "gu": {"text": "ઘટોત્કચને મારવા માટે કર્ણે કયા અસ્ત્રનો ઉપયોગ કર્યો હતો?", "opt_a": "બ્રહ્માસ્ત્ર", "opt_b": "પાશુપતાસ્ત્ર", "opt_c": "વાસવી શક્તિ", "opt_d": "નારાયણાસ્ત્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who narrated the Mahabharata war to Dhritarashtra?", "opt_a": "Vidura", "opt_b": "Sanjaya", "opt_c": "Vyasa", "opt_d": "Kripa"},
        "hi": {"text": "धृतराष्ट्र को महाभारत युद्ध का वर्णन किसने सुनाया था?", "opt_a": "विदुर", "opt_b": "संजय", "opt_c": "व्यास", "opt_d": "कृपा"},
        "gu": {"text": "ધૃતરાષ્ટ્રને મહાભારત યુદ્ધનું વર્ણન કોણે સંભળાવ્યું હતું?", "opt_a": "વિદુર", "opt_b": "સંજય", "opt_c": "વ્યાસ", "opt_d": "કૃપા"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who gave Sanjaya the divine vision?", "opt_a": "Vyasa", "opt_b": "Krishna", "opt_c": "Shiva", "opt_d": "Brahma"},
        "hi": {"text": "संजय को दिव्य दृष्टि किसने दी थी?", "opt_a": "व्यास", "opt_b": "कृष्ण", "opt_c": "शिव", "opt_d": "ब्रह्मा"},
        "gu": {"text": "સંજયને દિવ્ય દૃષ્ટિ કોણે આપી હતી?", "opt_a": "વ્યાસ", "opt_b": "કૃષ્ણ", "opt_c": "શિવ", "opt_d": "બ્રહ્મા"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who was the mother of Vyasa?", "opt_a": "Satyavati", "opt_b": "Ganga", "opt_c": "Amba", "opt_d": "Kunti"},
        "hi": {"text": "व्यास की माता कौन थीं?", "opt_a": "सत्यवती", "opt_b": "गंगा", "opt_c": "अंबा", "opt_d": "कुंती"},
        "gu": {"text": "વ્યાસની માતા કોણ હતા?", "opt_a": "સત્યવતી", "opt_b": "ગંગા", "opt_c": "અંબા", "opt_d": "કુંતી"}
    },
    {
        "difficulty": "Hard", "correct_option": "C",
        "en": {"text": "What is the final book of Mahabharata?", "opt_a": "Bhishma Parva", "opt_b": "Shanti Parva", "opt_c": "Swargarohanika Parva", "opt_d": "Ashvamedhika Parva"},
        "hi": {"text": "महाभारत का अंतिम पर्व कौन सा है?", "opt_a": "भीष्म पर्व", "opt_b": "शांति पर्व", "opt_c": "स्वर्गारोहण पर्व", "opt_d": "अश्वमेधिक पर्व"},
        "gu": {"text": "મહાભારતનું અંતિમ પર્વ કયું છે?", "opt_a": "ભીષ્મ પર્વ", "opt_b": "શાંતિ પર્વ", "opt_c": "સ્વર્ગારોહણ પર્વ", "opt_d": "અશ્વમેધિક પર્વ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who was Arjuna's son by Subhadra?", "opt_a": "Iravan", "opt_b": "Abhimanyu", "opt_c": "Babhruvahana", "opt_d": "Shrutakarma"},
        "hi": {"text": "सुभद्रा से अर्जुन का पुत्र कौन था?", "opt_a": "इरावान", "opt_b": "अभिमन्यु", "opt_c": "बभ्रुवाहन", "opt_d": "श्रुतकर्मा"},
        "gu": {"text": "સુભદ્રા દ્વારા અર્જુનનો પુત્ર કોણ હતો?", "opt_a": "ઇરાવાન", "opt_b": "અભિમન્યુ", "opt_c": "બભ્રુવાહન", "opt_d": "શ્રુતકર્મા"}
    }
]

hindu_gods_questions = [
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who is the god of death?", "opt_a": "Yama", "opt_b": "Chitragupta", "opt_c": "Shani", "opt_d": "Rahu"},
        "hi": {"text": "मृत्यु के देवता कौन हैं?", "opt_a": "यम", "opt_b": "चित्रगुप्त", "opt_c": "शनि", "opt_d": "राहु"},
        "gu": {"text": "મૃત્યુના દેવતા કોણ છે?", "opt_a": "યમ", "opt_b": "ચિત્રગુપ્ત", "opt_c": "શનિ", "opt_d": "રાહુ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who is the god of the wind?", "opt_a": "Agni", "opt_b": "Vayu", "opt_c": "Surya", "opt_d": "Chandra"},
        "hi": {"text": "पवन देव कौन हैं?", "opt_a": "अग्नि", "opt_b": "वायु", "opt_c": "सूर्य", "opt_d": "चंद्र"},
        "gu": {"text": "પવન દેવ કોણ છે?", "opt_a": "અગ્નિ", "opt_b": "વાયુ", "opt_c": "સૂર્ય", "opt_d": "ચંદ્ર"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who is the moon god?", "opt_a": "Surya", "opt_b": "Chandra", "opt_c": "Budha", "opt_d": "Brihaspati"},
        "hi": {"text": "चंद्र देव कौन हैं?", "opt_a": "सूर्य", "opt_b": "चंद्र", "opt_c": "बुध", "opt_d": "बृहस्पति"},
        "gu": {"text": "ચંદ્ર દેવ કોણ છે?", "opt_a": "સૂર્ય", "opt_b": "ચંદ્ર", "opt_c": "બુધ", "opt_d": "બૃહસ્પતિ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Which god has a third eye?", "opt_a": "Vishnu", "opt_b": "Brahma", "opt_c": "Shiva", "opt_d": "Indra"},
        "hi": {"text": "किस भगवान की तीसरी आंख है?", "opt_a": "विष्णु", "opt_b": "ब्रह्मा", "opt_c": "शिव", "opt_d": "इंद्र"},
        "gu": {"text": "કયા ભગવાનને ત્રીજી આંખ છે?", "opt_a": "વિષ્ણુ", "opt_b": "બ્રહ્મા", "opt_c": "શિવ", "opt_d": "ઇન્દ્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who is the brother of Ganesha?", "opt_a": "Hanuman", "opt_b": "Kartikeya", "opt_c": "Ayyappan", "opt_d": "Kama"},
        "hi": {"text": "गणेश के भाई कौन हैं?", "opt_a": "हनुमान", "opt_b": "कार्तिकेय", "opt_c": "अय्यप्पन", "opt_d": "काम"},
        "gu": {"text": "ગણેશના ભાઈ કોણ છે?", "opt_a": "હનુમાન", "opt_b": "કાર્તિકેય", "opt_c": "અય્યપ્પન", "opt_d": "કામ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "What is the vehicle of Lord Kartikeya?", "opt_a": "Swan", "opt_b": "Peacock", "opt_c": "Elephant", "opt_d": "Tiger"},
        "hi": {"text": "भगवान कार्तिकेय का वाहन क्या है?", "opt_a": "हंस", "opt_b": "मोर", "opt_c": "हाथी", "opt_d": "बाघ"},
        "gu": {"text": "ભગવાન કાર્તિકેયનું વાહન કયું છે?", "opt_a": "હંસ", "opt_b": "મોર", "opt_c": "હાથી", "opt_d": "વાઘ"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who is the god of love?", "opt_a": "Kama", "opt_b": "Agni", "opt_c": "Indra", "opt_d": "Varuna"},
        "hi": {"text": "कामदेव कौन हैं?", "opt_a": "काम", "opt_b": "अग्नि", "opt_c": "इंद्र", "opt_d": "वरुण"},
        "gu": {"text": "કામદેવ કોણ છે?", "opt_a": "કામ", "opt_b": "અગ્નિ", "opt_c": "ઇન્દ્ર", "opt_d": "વરુણ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who is the wife of Lord Brahma?", "opt_a": "Lakshmi", "opt_b": "Parvati", "opt_c": "Saraswati", "opt_d": "Ganga"},
        "hi": {"text": "भगवान ब्रह्मा की पत्नी कौन हैं?", "opt_a": "लक्ष्मी", "opt_b": "पार्वती", "opt_c": "सरस्वती", "opt_d": "गंगा"},
        "gu": {"text": "ભગવાન બ્રહ્માની પત્ની કોણ છે?", "opt_a": "લક્ષ્મી", "opt_b": "પાર્વતી", "opt_c": "સરસ્વતી", "opt_d": "ગંગા"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "What is the vehicle of Lord Brahma?", "opt_a": "Hamsa (Swan)", "opt_b": "Garuda", "opt_c": "Nandi", "opt_d": "Airavata"},
        "hi": {"text": "भगवान ब्रह्मा का वाहन क्या है?", "opt_a": "हंस", "opt_b": "गरुड़", "opt_c": "नंदी", "opt_d": "ऐरावत"},
        "gu": {"text": "ભગવાન બ્રહ્માનું વાહન કયું છે?", "opt_a": "હંસ", "opt_b": "ગરુડ", "opt_c": "નંદી", "opt_d": "ઐરાવત"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Who is the king of the Devas?", "opt_a": "Agni", "opt_b": "Indra", "opt_c": "Surya", "opt_d": "Vayu"},
        "hi": {"text": "देवताओं के राजा कौन हैं?", "opt_a": "अग्नि", "opt_b": "इंद्र", "opt_c": "सूर्य", "opt_d": "वायु"},
        "gu": {"text": "દેવોના રાજા કોણ છે?", "opt_a": "અગ્નિ", "opt_b": "ઇન્દ્ર", "opt_c": "સૂર્ય", "opt_d": "વાયુ"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "What is the name of Indra's elephant?", "opt_a": "Airavata", "opt_b": "Nandi", "opt_c": "Uchchaihshravas", "opt_d": "Kamadhenu"},
        "hi": {"text": "इंद्र के हाथी का क्या नाम है?", "opt_a": "ऐरावत", "opt_b": "नंदी", "opt_c": "उच्चैःश्रवा", "opt_d": "कामधेनु"},
        "gu": {"text": "ઇન્દ્રના હાથીનું નામ શું છે?", "opt_a": "ઐરાવત", "opt_b": "નંદી", "opt_c": "ઉચ્ચૈઃશ્રવા", "opt_d": "કામધેનુ"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who is the architect of the gods?", "opt_a": "Maya", "opt_b": "Vishwakarma", "opt_c": "Brahma", "opt_d": "Tvashtar"},
        "hi": {"text": "देवताओं के वास्तुकार कौन हैं?", "opt_a": "मय", "opt_b": "विश्वकर्मा", "opt_c": "ब्रह्मा", "opt_d": "त्वष्टा"},
        "gu": {"text": "દેવોના શિલ્પી (વાસ્તુકાર) કોણ છે?", "opt_a": "મય", "opt_b": "વિશ્વકર્મા", "opt_c": "બ્રહ્મા", "opt_d": "ત્વષ્ટા"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who is the physician of the gods?", "opt_a": "Ashwini Kumaras", "opt_b": "Dhanvantari", "opt_c": "Charaka", "opt_d": "Sushruta"},
        "hi": {"text": "देवताओं के चिकित्सक कौन हैं?", "opt_a": "अश्विनी कुमार", "opt_b": "धन्वंतरि", "opt_c": "चरक", "opt_d": "सुश्रुत"},
        "gu": {"text": "દેવોના ચિકિત્સક કોણ છે?", "opt_a": "અશ્વિની કુમારો", "opt_b": "ધન્વંતરિ", "opt_c": "ચરક", "opt_d": "સુશ્રુત"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who emerged from the churning of the ocean with nectar?", "opt_a": "Lakshmi", "opt_b": "Dhanvantari", "opt_c": "Mohini", "opt_d": "Kurma"},
        "hi": {"text": "समुद्र मंथन से अमृत कलश लेकर कौन प्रकट हुआ था?", "opt_a": "लक्ष्मी", "opt_b": "धन्वंतरि", "opt_c": "मोहिनी", "opt_d": "कूर्म"},
        "gu": {"text": "સમુદ્ર મંથનમાંથી અમૃત કળશ લઈને કોણ પ્રગટ થયું હતું?", "opt_a": "લક્ષ્મી", "opt_b": "ધન્વંતરિ", "opt_c": "મોહિની", "opt_d": "કૂર્મ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "What is the primary weapon of Lord Vishnu?", "opt_a": "Trishul", "opt_b": "Sudarshana Chakra", "opt_c": "Pashupatastra", "opt_d": "Brahmastra"},
        "hi": {"text": "भगवान विष्णु का प्राथमिक अस्त्र क्या है?", "opt_a": "त्रिशूल", "opt_b": "सुदर्शन चक्र", "opt_c": "पाशुपतास्त्र", "opt_d": "ब्रह्मास्त्र"},
        "gu": {"text": "ભગવાન વિષ્ણુનું મુખ્ય અસ્ત્ર કયું છે?", "opt_a": "ત્રિશૂળ", "opt_b": "સુદર્શન ચક્ર", "opt_c": "પાશુપતાસ્ત્ર", "opt_d": "બ્રહ્માસ્ત્ર"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Which avatar of Vishnu was a dwarf?", "opt_a": "Vamana", "opt_b": "Parashurama", "opt_c": "Rama", "opt_d": "Krishna"},
        "hi": {"text": "विष्णु का कौन सा अवतार वामन (बौना) था?", "opt_a": "वामन", "opt_b": "परशुराम", "opt_c": "राम", "opt_d": "कृष्ण"},
        "gu": {"text": "વિષ્ણુનો કયો અવતાર વામન (વામન) હતો?", "opt_a": "વામન", "opt_b": "પરશુરામ", "opt_c": "રામ", "opt_d": "કૃષ્ણ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Which avatar of Vishnu was a boar?", "opt_a": "Matsya", "opt_b": "Kurma", "opt_c": "Varaha", "opt_d": "Narasimha"},
        "hi": {"text": "विष्णु का कौन सा अवतार वराह (सूअर) था?", "opt_a": "मत्स्य", "opt_b": "कूर्म", "opt_c": "वराह", "opt_d": "नरसिंह"},
        "gu": {"text": "વિષ્ણુનો કયો અવતાર વરાહ (ભૂંડ) હતો?", "opt_a": "મત્સ્ય", "opt_b": "કૂર્મ", "opt_c": "વરાહ", "opt_d": "નરસિંહ"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who is the guru of the Devas?", "opt_a": "Shukracharya", "opt_b": "Brihaspati", "opt_c": "Dronacharya", "opt_d": "Vashistha"},
        "hi": {"text": "देवताओं के गुरु कौन हैं?", "opt_a": "शुक्राचार्य", "opt_b": "बृहस्पति", "opt_c": "द्रोणाचार्य", "opt_d": "वशिष्ठ"},
        "gu": {"text": "દેવોના ગુરુ કોણ છે?", "opt_a": "શુક્રાચાર્ય", "opt_b": "બૃહસ્પતિ", "opt_c": "દ્રોણાચાર્ય", "opt_d": "વશિષ્ઠ"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who is the guru of the Asuras?", "opt_a": "Shukracharya", "opt_b": "Brihaspati", "opt_c": "Vishwamitra", "opt_d": "Agastya"},
        "hi": {"text": "असुरों के गुरु कौन हैं?", "opt_a": "शुक्राचार्य", "opt_b": "बृहस्पति", "opt_c": "विश्वामित्र", "opt_d": "अगस्त्य"},
        "gu": {"text": "અસુરોના ગુરુ કોણ છે?", "opt_a": "શુક્રાચાર્ય", "opt_b": "બૃહસ્પતિ", "opt_c": "વિશ્વામિત્ર", "opt_d": "અગસ્ત્ય"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Which goddess is considered the fierce form of Parvati?", "opt_a": "Saraswati", "opt_b": "Lakshmi", "opt_c": "Kali", "opt_d": "Ganga"},
        "hi": {"text": "किस देवी को पार्वती का उग्र रूप माना जाता है?", "opt_a": "सरस्वती", "opt_b": "लक्ष्मी", "opt_c": "काली", "opt_d": "गंगा"},
        "gu": {"text": "કઈ દેવીને પાર્વતીનું ઉગ્ર સ્વરૂપ માનવામાં આવે છે?", "opt_a": "સરસ્વતી", "opt_b": "લક્ષ્મી", "opt_c": "કાલી", "opt_d": "ગંગા"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Which river is considered the most sacred in Hinduism?", "opt_a": "Yamuna", "opt_b": "Ganges", "opt_c": "Godavari", "opt_d": "Saraswati"},
        "hi": {"text": "हिंदू धर्म में सबसे पवित्र नदी कौन सी मानी जाती है?", "opt_a": "यमुना", "opt_b": "गंगा", "opt_c": "गोदावरी", "opt_d": "सरस्वती"},
        "gu": {"text": "હિન્દુ ધર્મમાં સૌથી પવિત્ર નદી કઈ માનવામાં આવે છે?", "opt_a": "યમુના", "opt_b": "ગંગા", "opt_c": "ગોદાવરી", "opt_d": "સરસ્વતી"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who composed the Ramayana?", "opt_a": "Valmiki", "opt_b": "Ved Vyasa", "opt_c": "Tulsidas", "opt_d": "Kalidasa"},
        "hi": {"text": "रामायण की रचना किसने की थी?", "opt_a": "वाल्मीकि", "opt_b": "वेद व्यास", "opt_c": "तुलसीदास", "opt_d": "कालिदास"},
        "gu": {"text": "રામાયણની રચના કોણે કરી હતી?", "opt_a": "વાલ્મીકિ", "opt_b": "વેદ વ્યાસ", "opt_c": "તુલસીદાસ", "opt_d": "કાલિદાસ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who is the monkey god?", "opt_a": "Sugriva", "opt_b": "Vali", "opt_c": "Hanuman", "opt_d": "Jambavan"},
        "hi": {"text": "वानर देव कौन हैं?", "opt_a": "सुग्रीव", "opt_b": "बाली", "opt_c": "हनुमान", "opt_d": "जाम्बवान"},
        "gu": {"text": "વાનર દેવ કોણ છે?", "opt_a": "સુગ્રીવ", "opt_b": "વાલી", "opt_c": "હનુમાન", "opt_d": "જામ્બવાન"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Goddess Saraswati is associated with which of the following?", "opt_a": "Knowledge and Art", "opt_b": "Wealth", "opt_c": "Power", "opt_d": "Destruction"},
        "hi": {"text": "देवी सरस्वती का संबंध किससे है?", "opt_a": "ज्ञान और कला", "opt_b": "धन", "opt_c": "शक्ति", "opt_d": "विनाश"},
        "gu": {"text": "દેવી સરસ્વતી શેની સાથે સંકળાયેલા છે?", "opt_a": "જ્ઞાન અને કળા", "opt_b": "ધન", "opt_c": "શક્તિ", "opt_d": "વિનાશ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Which god is known as the Lord of Dance (Nataraja)?", "opt_a": "Vishnu", "opt_b": "Shiva", "opt_c": "Brahma", "opt_d": "Indra"},
        "hi": {"text": "नृत्य के देवता (नटराज) के रूप में किस भगवान को जाना जाता है?", "opt_a": "विष्णु", "opt_b": "शिव", "opt_c": "ब्रह्मा", "opt_d": "इंद्र"},
        "gu": {"text": "નૃત્યના દેવતા (નટરાજ) તરીકે કયા ભગવાન ઓળખાય છે?", "opt_a": "વિષ્ણુ", "opt_b": "શિવ", "opt_c": "બ્રહ્મા", "opt_d": "ઇન્દ્ર"}
    }
]

with open('d:/project/qgame/qgame/data/mahabharata_part3.json', 'w', encoding='utf-8') as f:
    json.dump(mahabharata_questions, f, ensure_ascii=False, indent=4)
    
with open('d:/project/qgame/qgame/data/hindu_gods_part3.json', 'w', encoding='utf-8') as f:
    json.dump(hindu_gods_questions, f, ensure_ascii=False, indent=4)
