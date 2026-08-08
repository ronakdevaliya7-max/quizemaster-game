import os
import sys
import json

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from qgame.app import app, db
from qgame.models import Question, Category

std10_science_data = [
    {
        "correct_option": "A",
        "difficulty": "Easy",
        "en": {
            "text": "Which of the following is a balanced chemical equation?",
            "opt_a": "2H2 + O2 → 2H2O",
            "opt_b": "H2 + O2 → H2O",
            "opt_c": "2H2 + O2 → H2O",
            "opt_d": "H2 + 2O2 → 2H2O"
        },
        "gu": {
            "text": "નીચેનામાંથી કયું રાસાયણિક સમીકરણ સંતુલિત છે?",
            "opt_a": "2H2 + O2 → 2H2O",
            "opt_b": "H2 + O2 → H2O",
            "opt_c": "2H2 + O2 → H2O",
            "opt_d": "H2 + 2O2 → 2H2O"
        },
        "hi": {
            "text": "निम्नलिखित में से कौन सा एक संतुलित रासायनिक समीकरण है?",
            "opt_a": "2H2 + O2 → 2H2O",
            "opt_b": "H2 + O2 → H2O",
            "opt_c": "2H2 + O2 → H2O",
            "opt_d": "H2 + 2O2 → 2H2O"
        }
    },
    {
        "correct_option": "B",
        "difficulty": "Medium",
        "en": {
            "text": "The pH value of human blood is normally around:",
            "opt_a": "6.5 - 6.8",
            "opt_b": "7.35 - 7.45",
            "opt_c": "8.5 - 9.0",
            "opt_d": "5.5 - 6.0"
        },
        "gu": {
            "text": "માનવ રક્તનું pH મૂલ્ય સામાન્ય રીતે કેટલું હોય છે?",
            "opt_a": "6.5 - 6.8",
            "opt_b": "7.35 - 7.45",
            "opt_c": "8.5 - 9.0",
            "opt_d": "5.5 - 6.0"
        },
        "hi": {
            "text": "मानव रक्त का pH मान सामान्यतः कितना होता है?",
            "opt_a": "6.5 - 6.8",
            "opt_b": "7.35 - 7.45",
            "opt_c": "8.5 - 9.0",
            "opt_d": "5.5 - 6.0"
        }
    },
    {
        "correct_option": "C",
        "difficulty": "Easy",
        "en": {
            "text": "What is the SI unit of electric current?",
            "opt_a": "Volt",
            "opt_b": "Ohm",
            "opt_c": "Ampere",
            "opt_d": "Watt"
        },
        "gu": {
            "text": "વિદ્યુતપ્રવાહનો SI એકમ શું છે?",
            "opt_a": "વોલ્ટ",
            "opt_b": "ઓહ્મ",
            "opt_c": "એમ્પીયર",
            "opt_d": "વોટ"
        },
        "hi": {
            "text": "विद्युत धारा का SI मात्रक क्या है?",
            "opt_a": "वोल्ट",
            "opt_b": "ओम",
            "opt_c": "एम्पियर",
            "opt_d": "वाट"
        }
    },
    {
        "correct_option": "A",
        "difficulty": "Medium",
        "en": {
            "text": "Which gas is evolved when an acid reacts with a metal?",
            "opt_a": "Hydrogen",
            "opt_b": "Oxygen",
            "opt_c": "Carbon dioxide",
            "opt_d": "Nitrogen"
        },
        "gu": {
            "text": "જ્યારે એસિડ ધાતુ સાથે પ્રક્રિયા કરે છે ત્યારે કયો ગેસ ઉત્પન્ન થાય છે?",
            "opt_a": "હાઇડ્રોજન",
            "opt_b": "ઓક્સિજન",
            "opt_c": "કાર્બન ડાયોક્સાઇડ",
            "opt_d": "નાઇટ્રોજન"
        },
        "hi": {
            "text": "जब कोई अम्ल धातु के साथ प्रतिक्रिया करता है तो कौन सी गैस निकलती है?",
            "opt_a": "हाइड्रोजन",
            "opt_b": "ऑक्सीजन",
            "opt_c": "कार्बन डाइऑक्साइड",
            "opt_d": "नाइट्रोजन"
        }
    },
    {
        "correct_option": "D",
        "difficulty": "Easy",
        "en": {
            "text": "The reproductive part of a plant is the:",
            "opt_a": "Leaf",
            "opt_b": "Stem",
            "opt_c": "Root",
            "opt_d": "Flower"
        },
        "gu": {
            "text": "વનસ્પતિનો પ્રજનન અંગ કયો છે?",
            "opt_a": "પાંદડું",
            "opt_b": "પ્રકાંડ",
            "opt_c": "મૂળ",
            "opt_d": "પુષ્પ (ફૂલ)"
        },
        "hi": {
            "text": "पौधे का प्रजनन भाग कौन सा है?",
            "opt_a": "पत्ता",
            "opt_b": "तना",
            "opt_c": "जड़",
            "opt_d": "फूल"
        }
    },
    {
        "correct_option": "B",
        "difficulty": "Hard",
        "en": {
            "text": "What is the refractive index of diamond?",
            "opt_a": "1.33",
            "opt_b": "2.42",
            "opt_c": "1.50",
            "opt_d": "1.00"
        },
        "gu": {
            "text": "હીરાનો વક્રીભવનાંક કેટલો હોય છે?",
            "opt_a": "1.33",
            "opt_b": "2.42",
            "opt_c": "1.50",
            "opt_d": "1.00"
        },
        "hi": {
            "text": "हीरे का अपवर्तनांक कितना होता है?",
            "opt_a": "1.33",
            "opt_b": "2.42",
            "opt_c": "1.50",
            "opt_d": "1.00"
        }
    },
    {
        "correct_option": "C",
        "difficulty": "Medium",
        "en": {
            "text": "Which part of the brain is responsible for maintaining posture and balance of the body?",
            "opt_a": "Cerebrum",
            "opt_b": "Medulla",
            "opt_c": "Cerebellum",
            "opt_d": "Pons"
        },
        "gu": {
            "text": "મગજનો કયો ભાગ શરીરનું સંતુલન જાળવવાનું કાર્ય કરે છે?",
            "opt_a": "બૃહદ મસ્તિષ્ક (Cerebrum)",
            "opt_b": "લંબમજ્જા (Medulla)",
            "opt_c": "અનુમસ્તિષ્ક (Cerebellum)",
            "opt_d": "પોન્સ (Pons)"
        },
        "hi": {
            "text": "मस्तिष्क का कौन सा भाग शरीर की मुद्रा और संतुलन बनाए रखने के लिए जिम्मेदार है?",
            "opt_a": "प्रमस्तिष्क (Cerebrum)",
            "opt_b": "मज्जा (Medulla)",
            "opt_c": "अनुमस्तिष्क (Cerebellum)",
            "opt_d": "पोन्स (Pons)"
        }
    },
    {
        "correct_option": "A",
        "difficulty": "Easy",
        "en": {
            "text": "Which mirror is used as a rear-view mirror in vehicles?",
            "opt_a": "Convex mirror",
            "opt_b": "Concave mirror",
            "opt_c": "Plane mirror",
            "opt_d": "Cylindrical mirror"
        },
        "gu": {
            "text": "વાહનોમાં પાછળનું દ્રશ્ય જોવા માટે કયા અરીસાનો ઉપયોગ થાય છે?",
            "opt_a": "બહિર્ગોળ અરીસો",
            "opt_b": "અંતર્ગોળ અરીસો",
            "opt_c": "સમતલ અરીસો",
            "opt_d": "નળાકાર અરીસો"
        },
        "hi": {
            "text": "वाहनों में पीछे देखने के लिए किस दर्पण का उपयोग किया जाता है?",
            "opt_a": "उत्तल दर्पण",
            "opt_b": "अवतल दर्पण",
            "opt_c": "समतल दर्पण",
            "opt_d": "बेलनाकार दर्पण"
        }
    },
    {
        "correct_option": "D",
        "difficulty": "Medium",
        "en": {
            "text": "The breakdown of pyruvate to give carbon dioxide, water and energy takes place in:",
            "opt_a": "Cytoplasm",
            "opt_b": "Chloroplast",
            "opt_c": "Nucleus",
            "opt_d": "Mitochondria"
        },
        "gu": {
            "text": "પાયરુવેટનું વિઘટન થઈને કાર્બન ડાયોક્સાઇડ, પાણી અને ઊર્જા ઉત્પન્ન થવાની ક્રિયા ક્યાં થાય છે?",
            "opt_a": "કોષરસ",
            "opt_b": "હરિતકણ",
            "opt_c": "કોષકેન્દ્ર",
            "opt_d": "કણાભસૂત્ર (Mitochondria)"
        },
        "hi": {
            "text": "पाइरूवेट के विखंडन से कार्बन डाइऑक्साइड, जल तथा ऊर्जा प्राप्त होती है, यह क्रिया कहाँ होती है?",
            "opt_a": "कोशिकाद्रव्य",
            "opt_b": "क्लोरोप्लास्ट",
            "opt_c": "केन्द्रक",
            "opt_d": "माइटोकॉन्ड्रिया"
        }
    },
    {
        "correct_option": "B",
        "difficulty": "Hard",
        "en": {
            "text": "An alloy of copper and zinc is called:",
            "opt_a": "Bronze",
            "opt_b": "Brass",
            "opt_c": "Solder",
            "opt_d": "Steel"
        },
        "gu": {
            "text": "તાંબા (Copper) અને જસત (Zinc) ની મિશ્રધાતુને શું કહે છે?",
            "opt_a": "કાંસું (Bronze)",
            "opt_b": "પિત્તળ (Brass)",
            "opt_c": "સોલ્ડર (Solder)",
            "opt_d": "સ્ટીલ (Steel)"
        },
        "hi": {
            "text": "तांबा (Copper) और जस्ता (Zinc) की मिश्रधातु को क्या कहते हैं?",
            "opt_a": "कांस्य (Bronze)",
            "opt_b": "पीतल (Brass)",
            "opt_c": "सोल्डर (Solder)",
            "opt_d": "स्टील (Steel)"
        }
    }
]

def create_and_import():
    with app.app_context():
        cat_name = "Std 10 Science"
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, description="Real quiz questions for Standard 10 Science in English, Gujarati, and Hindi.")
            db.session.add(cat)
            db.session.commit()
            print(f"Created category {cat_name}")
            
        added_count = 0
        for q_data in std10_science_data:
            existing = Question.query.filter_by(category_id=cat.id, text=q_data['en']['text']).first()
            if not existing:
                for lang in ['en', 'hi', 'gu']:
                    q = Question(
                        category_id=cat.id,
                        text=q_data[lang]['text'],
                        option_a=q_data[lang]['opt_a'],
                        option_b=q_data[lang]['opt_b'],
                        option_c=q_data[lang]['opt_c'],
                        option_d=q_data[lang]['opt_d'],
                        correct_option=q_data['correct_option'],
                        difficulty=q_data['difficulty'],
                        language=lang
                    )
                    db.session.add(q)
                added_count += 3
        db.session.commit()
        print(f"Imported {added_count} real questions for {cat_name}.")

if __name__ == '__main__':
    create_and_import()
