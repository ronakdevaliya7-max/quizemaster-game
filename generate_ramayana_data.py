import json
import os

questions = [
    {
        "difficulty": "Easy",
        "correct_option": "B",
        "en": {
            "text": "Who is the author of the epic Ramayana?",
            "opt_a": "Ved Vyasa", "opt_b": "Valmiki", "opt_c": "Tulsidas", "opt_d": "Kalidasa"
        },
        "hi": {
            "text": "महाकाव्य रामायण के रचयिता कौन हैं?",
            "opt_a": "वेद व्यास", "opt_b": "वाल्मीकि", "opt_c": "तुलसीदास", "opt_d": "कालिदास"
        },
        "gu": {
            "text": "મહાકાવ્ય રામાયણના રચયિતા કોણ છે?",
            "opt_a": "વેદ વ્યાસ", "opt_b": "વાલ્મીકિ", "opt_c": "તુલસીદાસ", "opt_d": "કાલિદાસ"
        }
    },
    {
        "difficulty": "Easy",
        "correct_option": "A",
        "en": {
            "text": "Who was the father of Lord Rama?",
            "opt_a": "Dasharatha", "opt_b": "Janaka", "opt_c": "Ravana", "opt_d": "Sugriva"
        },
        "hi": {
            "text": "भगवान राम के पिता कौन थे?",
            "opt_a": "दशरथ", "opt_b": "जनक", "opt_c": "रावण", "opt_d": "सुग्रीव"
        },
        "gu": {
            "text": "ભગવાન રામના પિતા કોણ હતા?",
            "opt_a": "દશરથ", "opt_b": "જનક", "opt_c": "રાવણ", "opt_d": "સુગ્રીવ"
        }
    },
    {
        "difficulty": "Easy",
        "correct_option": "C",
        "en": {
            "text": "Who kidnapped Sita?",
            "opt_a": "Kumbhakarna", "opt_b": "Maricha", "opt_c": "Ravana", "opt_d": "Indrajit"
        },
        "hi": {
            "text": "सीता का अपहरण किसने किया था?",
            "opt_a": "कुंभकर्ण", "opt_b": "मारीच", "opt_c": "रावण", "opt_d": "इंद्रजीत"
        },
        "gu": {
            "text": "સીતાનું અપહરણ કોણે કર્યું હતું?",
            "opt_a": "કુંભકર્ણ", "opt_b": "મારીચ", "opt_c": "રાવણ", "opt_d": "ઇન્દ્રજીત"
        }
    },
    {
        "difficulty": "Medium",
        "correct_option": "D",
        "en": {
            "text": "Which weapon was broken by Rama to win Sita's hand in marriage?",
            "opt_a": "Pashupatastra", "opt_b": "Brahmastra", "opt_c": "Sudarshana Chakra", "opt_d": "Pinaka Bow"
        },
        "hi": {
            "text": "सीता से विवाह करने के लिए राम ने कौन सा अस्त्र तोड़ा था?",
            "opt_a": "पाशुपतास्त्र", "opt_b": "ब्रह्मास्त्र", "opt_c": "सुदर्शन चक्र", "opt_d": "पिनाक धनुष"
        },
        "gu": {
            "text": "સીતાજી સાથે વિવાહ કરવા માટે રામે કયું અસ્ત્ર તોડ્યું હતું?",
            "opt_a": "પાશુપતાસ્ત્ર", "opt_b": "બ્રહ્માસ્ત્ર", "opt_c": "સુદર્શન ચક્ર", "opt_d": "પિનાક ધનુષ"
        }
    },
    {
        "difficulty": "Medium",
        "correct_option": "A",
        "en": {
            "text": "Who revived Lakshmana when he was unconscious in battle?",
            "opt_a": "Hanuman bringing Sanjeevani", "opt_b": "Rama with a spell", "opt_c": "Vibhishana", "opt_d": "Jambavan"
        },
        "hi": {
            "text": "युद्ध में मूर्छित होने पर लक्ष्मण को किसने पुनर्जीवित किया था?",
            "opt_a": "हनुमान जी संजीवनी लाए", "opt_b": "राम जी मंत्र से", "opt_c": "विभीषण", "opt_d": "जाम्बवान"
        },
        "gu": {
            "text": "યુદ્ધમાં મૂર્છિત થયા પછી લક્ષ્મણને કોણે પુનર્જીવિત કર્યા હતા?",
            "opt_a": "હનુમાનજી સંજીવની લાવ્યા", "opt_b": "રામજી મંત્ર દ્વારા", "opt_c": "વિભીષણ", "opt_d": "જામ્બવાન"
        }
    },
    {
        "difficulty": "Easy",
        "correct_option": "B",
        "en": {
            "text": "Which brother of Ravana joined Lord Rama?",
            "opt_a": "Kumbhakarna", "opt_b": "Vibhishana", "opt_c": "Khara", "opt_d": "Dushana"
        },
        "hi": {
            "text": "रावण का कौन सा भाई भगवान राम से जुड़ गया था?",
            "opt_a": "कुंभकर्ण", "opt_b": "विभीषण", "opt_c": "खर", "opt_d": "दूषण"
        },
        "gu": {
            "text": "રાવણનો કયો ભાઈ ભગવાન રામ સાથે જોડાઈ ગયો હતો?",
            "opt_a": "કુંભકર્ણ", "opt_b": "વિભીષણ", "opt_c": "ખર", "opt_d": "દૂષણ"
        }
    },
    {
        "difficulty": "Hard",
        "correct_option": "C",
        "en": {
            "text": "Who was the father of Jatayu?",
            "opt_a": "Garuda", "opt_b": "Sampati", "opt_c": "Aruna", "opt_d": "Kashyapa"
        },
        "hi": {
            "text": "जटायु के पिता कौन थे?",
            "opt_a": "गरुड़", "opt_b": "सम्पाती", "opt_c": "अरुण", "opt_d": "कश्यप"
        },
        "gu": {
            "text": "જટાયુના પિતા કોણ હતા?",
            "opt_a": "ગરુડ", "opt_b": "સંપાતિ", "opt_c": "અરુણ", "opt_d": "કશ્યપ"
        }
    },
    {
        "difficulty": "Medium",
        "correct_option": "A",
        "en": {
            "text": "What was the name of Ravana's flying chariot?",
            "opt_a": "Pushpaka Vimana", "opt_b": "Garuda Vimana", "opt_c": "Vayu Ratha", "opt_d": "Surya Ratha"
        },
        "hi": {
            "text": "रावण के उड़ने वाले रथ का क्या नाम था?",
            "opt_a": "पुष्पक विमान", "opt_b": "गरुड़ विमान", "opt_c": "वायु रथ", "opt_d": "सूर्य रथ"
        },
        "gu": {
            "text": "રાવણના ઉડતા રથનું નામ શું હતું?",
            "opt_a": "પુષ્પક વિમાન", "opt_b": "ગરુડ વિમાન", "opt_c": "વાયુ રથ", "opt_d": "સૂર્ય રથ"
        }
    },
    {
        "difficulty": "Hard",
        "correct_option": "D",
        "en": {
            "text": "For how many years did Rama, Sita, and Lakshmana go into exile?",
            "opt_a": "12 years", "opt_b": "10 years", "opt_c": "13 years", "opt_d": "14 years"
        },
        "hi": {
            "text": "राम, सीता और लक्ष्मण कितने वर्षों के लिए वनवास गए थे?",
            "opt_a": "12 वर्ष", "opt_b": "10 वर्ष", "opt_c": "13 वर्ष", "opt_d": "14 वर्ष"
        },
        "gu": {
            "text": "રામ, સીતા અને લક્ષ્મણ કેટલા વર્ષો માટે વનવાસ ગયા હતા?",
            "opt_a": "12 વર્ષ", "opt_b": "10 વર્ષ", "opt_c": "13 વર્ષ", "opt_d": "14 વર્ષ"
        }
    },
    {
        "difficulty": "Medium",
        "correct_option": "B",
        "en": {
            "text": "Who told Rama that Sita has been abducted by Ravana?",
            "opt_a": "Hanuman", "opt_b": "Jatayu", "opt_c": "Sugriva", "opt_d": "Shabari"
        },
        "hi": {
            "text": "राम को किसने बताया कि सीता का अपहरण रावण ने किया है?",
            "opt_a": "हनुमान", "opt_b": "जटायु", "opt_c": "सुग्रीव", "opt_d": "शबरी"
        },
        "gu": {
            "text": "રામને કોણે કહ્યું કે સીતાનું અપહરણ રાવણે કર્યું છે?",
            "opt_a": "હનુમાન", "opt_b": "જટાયુ", "opt_c": "સુગ્રીવ", "opt_d": "શબરી"
        }
    },
    {
        "difficulty": "Easy",
        "correct_option": "D",
        "en": {
            "text": "Who built the bridge to Lanka?",
            "opt_a": "Vishwakarma", "opt_b": "Maya", "opt_c": "Sugriva", "opt_d": "Nala and Nila"
        },
        "hi": {
            "text": "लंका तक पुल किसने बनाया था?",
            "opt_a": "विश्वकर्मा", "opt_b": "मय", "opt_c": "सुग्रीव", "opt_d": "नल और नील"
        },
        "gu": {
            "text": "લંકા સુધીનો પુલ કોણે બનાવ્યો હતો?",
            "opt_a": "વિશ્વકર્મા", "opt_b": "મય", "opt_c": "સુગ્રીવ", "opt_d": "નલ અને નીલ"
        }
    },
    {
        "difficulty": "Medium",
        "correct_option": "C",
        "en": {
            "text": "What was the name of the demon who disguised himself as a golden deer?",
            "opt_a": "Khara", "opt_b": "Subahu", "opt_c": "Maricha", "opt_d": "Trishira"
        },
        "hi": {
            "text": "उस राक्षस का क्या नाम था जिसने सोने के हिरण का रूप धारण किया था?",
            "opt_a": "खर", "opt_b": "सुबाहु", "opt_c": "मारीच", "opt_d": "त्रिशिरा"
        },
        "gu": {
            "text": "સોનાના હરણનું રૂપ ધારણ કરનાર રાક્ષસનું નામ શું હતું?",
            "opt_a": "ખર", "opt_b": "સુબાહુ", "opt_c": "મારીચ", "opt_d": "ત્રિશિરા"
        }
    }
]

os.makedirs('d:/project/qgame/qgame/data', exist_ok=True)
with open('d:/project/qgame/qgame/data/ramayana.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)
print("Created ramayana.json")
