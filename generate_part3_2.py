import json
import os

indian_history_questions = [
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "Who is known as the Father of the Nation in India?", "opt_a": "Mahatma Gandhi", "opt_b": "Jawaharlal Nehru", "opt_c": "Subhas Chandra Bose", "opt_d": "Sardar Patel"},
        "hi": {"text": "भारत में राष्ट्रपिता के रूप में किसे जाना जाता है?", "opt_a": "महात्मा गांधी", "opt_b": "जवाहरलाल नेहरू", "opt_c": "सुभाष चंद्र बोस", "opt_d": "सरदार पटेल"},
        "gu": {"text": "ભારતમાં રાષ્ટ્રપિતા તરીકે કોણ ઓળખાય છે?", "opt_a": "મહાત્મા ગાંધી", "opt_b": "જવાહરલાલ નેહરુ", "opt_c": "સુભાષચંદ્ર બોઝ", "opt_d": "સરદાર પટેલ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who founded the Brahmo Samaj?", "opt_a": "Swami Vivekananda", "opt_b": "Dayananda Saraswati", "opt_c": "Raja Ram Mohan Roy", "opt_d": "Ishwar Chandra Vidyasagar"},
        "hi": {"text": "ब्रह्म समाज की स्थापना किसने की?", "opt_a": "स्वामी विवेकानंद", "opt_b": "दयानंद सरस्वती", "opt_c": "राजा राम मोहन राय", "opt_d": "ईश्वर चंद्र विद्यासागर"},
        "gu": {"text": "બ્રહ્મો સમાજની સ્થાપના કોણે કરી હતી?", "opt_a": "સ્વામી વિવેકાનંદ", "opt_b": "દયાનંદ સરસ્વતી", "opt_c": "રાજા રામ મોહન રાય", "opt_d": "ઈશ્વરચંદ્ર વિદ્યાસાગર"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Which movement was started by Mahatma Gandhi in 1930?", "opt_a": "Non-Cooperation Movement", "opt_b": "Civil Disobedience Movement (Dandi March)", "opt_c": "Quit India Movement", "opt_d": "Khilafat Movement"},
        "hi": {"text": "1930 में महात्मा गांधी ने कौन सा आंदोलन शुरू किया था?", "opt_a": "असहयोग आंदोलन", "opt_b": "सविनय अवज्ञा आंदोलन (दांडी मार्च)", "opt_c": "भारत छोड़ो आंदोलन", "opt_d": "खिलाफत आंदोलन"},
        "gu": {"text": "1930 માં મહાત્મા ગાંધીએ કયું આંદોલન શરૂ કર્યું હતું?", "opt_a": "અસહકાર આંદોલન", "opt_b": "સવિનય કાનૂન ભંગ આંદોલન (દાંડી કૂચ)", "opt_c": "ભારત છોડો આંદોલન", "opt_d": "ખિલાફત આંદોલન"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who is known as the 'Iron Man of India'?", "opt_a": "Sardar Vallabhbhai Patel", "opt_b": "Lal Bahadur Shastri", "opt_c": "Bhagat Singh", "opt_d": "Bal Gangadhar Tilak"},
        "hi": {"text": "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?", "opt_a": "सरदार वल्लभभाई पटेल", "opt_b": "लाल बहादुर शास्त्री", "opt_c": "भगत सिंह", "opt_d": "बाल गंगाधर तिलक"},
        "gu": {"text": "ભારતના 'લોખંડી પુરુષ' તરીકે કોણ ઓળખાય છે?", "opt_a": "સરદાર વલ્લભભાઈ પટેલ", "opt_b": "લાલ બહાદુર શાસ્ત્રી", "opt_c": "ભગત સિંહ", "opt_d": "બાળ ગંગાધર તિલક"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who established the Ramakrishna Mission?", "opt_a": "Ramakrishna Paramahamsa", "opt_b": "Raja Ram Mohan Roy", "opt_c": "Swami Vivekananda", "opt_d": "Aurobindo Ghosh"},
        "hi": {"text": "रामकृष्ण मिशन की स्थापना किसने की?", "opt_a": "रामकृष्ण परमहंस", "opt_b": "राजा राम मोहन राय", "opt_c": "स्वामी विवेकानंद", "opt_d": "अरबिंदो घोष"},
        "gu": {"text": "રામકૃષ્ણ મિશનની સ્થાપના કોણે કરી હતી?", "opt_a": "રામકૃષ્ણ પરમહંસ", "opt_b": "રાજા રામ મોહન રાય", "opt_c": "સ્વામી વિવેકાનંદ", "opt_d": "અરવિંદ ઘોષ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Who was the founder of the Indian National Army (Azad Hind Fauj)?", "opt_a": "Bhagat Singh", "opt_b": "Subhas Chandra Bose", "opt_c": "Chandrashekhar Azad", "opt_d": "Mangal Pandey"},
        "hi": {"text": "भारतीय राष्ट्रीय सेना (आजाद हिंद फौज) के संस्थापक कौन थे?", "opt_a": "भगत सिंह", "opt_b": "सुभाष चंद्र बोस", "opt_c": "चंद्रशेखर आजाद", "opt_d": "मंगल पांडे"},
        "gu": {"text": "ભારતીય રાષ્ટ્રીય સેના (આઝાદ હિંદ ફોજ) ના સ્થાપક કોણ હતા?", "opt_a": "ભગત સિંહ", "opt_b": "સુભાષચંદ્ર બોઝ", "opt_c": "ચંદ્રશેખર આઝાદ", "opt_d": "મંગલ પાંડે"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who was the Viceroy of India when it became independent?", "opt_a": "Lord Mountbatten", "opt_b": "Lord Curzon", "opt_c": "Lord Dalhousie", "opt_d": "Lord Irwin"},
        "hi": {"text": "भारत के स्वतंत्र होने पर भारत का वायसराय कौन था?", "opt_a": "लॉर्ड माउंटबेटन", "opt_b": "लॉर्ड कर्जन", "opt_c": "लॉर्ड डलहौजी", "opt_d": "लॉर्ड इरविन"},
        "gu": {"text": "ભારત આઝાદ થયું ત્યારે ભારતના વાઇસરોય કોણ હતા?", "opt_a": "લોર્ડ માઉન્ટબેટન", "opt_b": "લોર્ડ કર્ઝન", "opt_c": "લોર્ડ ડેલહાઉસી", "opt_d": "લોર્ડ ઇરવિન"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who was the first woman President of the Indian National Congress?", "opt_a": "Sarojini Naidu", "opt_b": "Indira Gandhi", "opt_c": "Annie Besant", "opt_d": "Vijaya Lakshmi Pandit"},
        "hi": {"text": "भारतीय राष्ट्रीय कांग्रेस की पहली महिला अध्यक्ष कौन थीं?", "opt_a": "सरोजिनी नायडू", "opt_b": "इंदिरा गांधी", "opt_c": "एनी बेसेंट", "opt_d": "विजया लक्ष्मी पंडित"},
        "gu": {"text": "ભારતીય રાષ્ટ્રીય કોંગ્રેસના પ્રથમ મહિલા પ્રમુખ કોણ હતા?", "opt_a": "સરોજિની નાયડુ", "opt_b": "ઇન્દિરા ગાંધી", "opt_c": "એની બેસન્ટ", "opt_d": "વિજયા લક્ષ્મી પંડિત"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "The Sepoy Mutiny (First War of Independence) took place in?", "opt_a": "1857", "opt_b": "1947", "opt_c": "1757", "opt_d": "1885"},
        "hi": {"text": "सिपाही विद्रोह (प्रथम स्वतंत्रता संग्राम) कब हुआ था?", "opt_a": "1857", "opt_b": "1947", "opt_c": "1757", "opt_d": "1885"},
        "gu": {"text": "સિપાહી બળવો (પ્રથમ સ્વાતંત્ર્ય સંગ્રામ) ક્યારે થયો હતો?", "opt_a": "1857", "opt_b": "1947", "opt_c": "1757", "opt_d": "1885"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who was the founder of the Gupta Empire?", "opt_a": "Chandragupta I", "opt_b": "Sri Gupta", "opt_c": "Samudragupta", "opt_d": "Kumargupta"},
        "hi": {"text": "गुप्त साम्राज्य का संस्थापक कौन था?", "opt_a": "चंद्रगुप्त प्रथम", "opt_b": "श्री गुप्त", "opt_c": "समुद्रगुप्त", "opt_d": "कुमारगुप्त"},
        "gu": {"text": "ગુપ્ત સામ્રાજ્યના સ્થાપક કોણ હતા?", "opt_a": "ચંદ્રગુપ્ત પ્રથમ", "opt_b": "શ્રી ગુપ્ત", "opt_c": "સમુદ્રગુપ્ત", "opt_d": "કુમારગુપ્ત"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Which ruler embraced Buddhism after the Kalinga War?", "opt_a": "Ashoka", "opt_b": "Harsha", "opt_c": "Chandragupta Maurya", "opt_d": "Kanishka"},
        "hi": {"text": "कलिंग युद्ध के बाद किस शासक ने बौद्ध धर्म अपना लिया?", "opt_a": "अशोक", "opt_b": "हर्ष", "opt_c": "चंद्रगुप्त मौर्य", "opt_d": "कनिष्क"},
        "gu": {"text": "કલિંગના યુદ્ધ પછી કયા શાસકે બૌદ્ધ ધર્મ સ્વીકાર્યો?", "opt_a": "અશોક", "opt_b": "હર્ષ", "opt_c": "ચંદ્રગુપ્ત મૌર્ય", "opt_d": "કનિષ્ક"}
    },
    {
        "difficulty": "Easy", "correct_option": "D",
        "en": {"text": "Who built the Red Fort in Delhi?", "opt_a": "Akbar", "opt_b": "Jahangir", "opt_c": "Aurangzeb", "opt_d": "Shah Jahan"},
        "hi": {"text": "दिल्ली का लाल किला किसने बनवाया था?", "opt_a": "अकबर", "opt_b": "जहांगीर", "opt_c": "औरंगजेब", "opt_d": "शाहजहाँ"},
        "gu": {"text": "દિલ્હીનો લાલ કિલ્લો કોણે બનાવ્યો હતો?", "opt_a": "અકબર", "opt_b": "જહાંગીર", "opt_c": "ઔરંગઝેબ", "opt_d": "શાહજહાં"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "The battle of Plassey was fought in the year?", "opt_a": "1757", "opt_b": "1764", "opt_c": "1857", "opt_d": "1942"},
        "hi": {"text": "प्लासी का युद्ध किस वर्ष लड़ा गया था?", "opt_a": "1757", "opt_b": "1764", "opt_c": "1857", "opt_d": "1942"},
        "gu": {"text": "પ્લાસીનું યુદ્ધ કયા વર્ષમાં લડાયું હતું?", "opt_a": "1757", "opt_b": "1764", "opt_c": "1857", "opt_d": "1942"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who was the last Mughal Emperor of India?", "opt_a": "Akbar II", "opt_b": "Bahadur Shah Zafar", "opt_c": "Shah Alam II", "opt_d": "Aurangzeb"},
        "hi": {"text": "भारत का अंतिम मुगल सम्राट कौन था?", "opt_a": "अकबर द्वितीय", "opt_b": "बहादुर शाह जफर", "opt_c": "शाह आलम द्वितीय", "opt_d": "औरंगजेब"},
        "gu": {"text": "ભારતનો છેલ્લો મુઘલ સમ્રાટ કોણ હતો?", "opt_a": "અકબર દ્વિતીય", "opt_b": "બહાદુર શાહ ઝફર", "opt_c": "શાહ આલમ દ્વિતીય", "opt_d": "ઔરંગઝેબ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Who is the author of 'Arthashastra'?", "opt_a": "Megasthenes", "opt_b": "Kalidasa", "opt_c": "Chanakya (Kautilya)", "opt_d": "Banabhatta"},
        "hi": {"text": "'अर्थशास्त्र' के लेखक कौन हैं?", "opt_a": "मेगस्थनीज", "opt_b": "कालिदास", "opt_c": "चाणक्य (कौटिल्य)", "opt_d": "बाणभट्ट"},
        "gu": {"text": "'અર્થશાસ્ત્ર' ના લેખક કોણ છે?", "opt_a": "મેગસ્થનીઝ", "opt_b": "કાલિદાસ", "opt_c": "ચાણક્ય (કૌટિલ્ય)", "opt_d": "બાણભટ્ટ"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Which British Governor-General introduced the Doctrine of Lapse?", "opt_a": "Lord Dalhousie", "opt_b": "Lord Cornwallis", "opt_c": "Lord Wellesley", "opt_d": "Lord Hastings"},
        "hi": {"text": "किस ब्रिटिश गवर्नर-जनरल ने व्यपगत का सिद्धांत (Doctrine of Lapse) पेश किया?", "opt_a": "लॉर्ड डलहौजी", "opt_b": "लॉर्ड कार्नवालिस", "opt_c": "लॉर्ड वेलेस्ली", "opt_d": "लॉर्ड हेस्टिंग्स"},
        "gu": {"text": "કયા બ્રિટિશ ગવર્નર-જનરલે ખાલસા નીતિ (Doctrine of Lapse) દાખલ કરી?", "opt_a": "લોર્ડ ડેલહાઉસી", "opt_b": "લોર્ડ કોર્નવોલિસ", "opt_c": "લોર્ડ વેલેસ્લી", "opt_d": "લોર્ડ હેસ્ટિંગ્સ"}
    },
    {
        "difficulty": "Easy", "correct_option": "D",
        "en": {"text": "Who composed 'Vande Mataram'?", "opt_a": "Rabindranath Tagore", "opt_b": "Sarojini Naidu", "opt_c": "Muhammad Iqbal", "opt_d": "Bankim Chandra Chatterjee"},
        "hi": {"text": "'वंदे मातरम' की रचना किसने की?", "opt_a": "रवींद्रनाथ टैगोर", "opt_b": "सरोजिनी नायडू", "opt_c": "मुहम्मद इकबाल", "opt_d": "बंकिम चंद्र चटर्जी"},
        "gu": {"text": "'વંદે માતરમ' ની રચના કોણે કરી?", "opt_a": "રવીન્દ્રનાથ ટાગોર", "opt_b": "સરોજિની નાયડુ", "opt_c": "મુહમ્મદ ઈકબાલ", "opt_d": "બંકિમચંદ્ર ચેટરજી"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "The partition of Bengal took place in which year?", "opt_a": "1903", "opt_b": "1905", "opt_c": "1911", "opt_d": "1914"},
        "hi": {"text": "बंगाल का विभाजन किस वर्ष हुआ था?", "opt_a": "1903", "opt_b": "1905", "opt_c": "1911", "opt_d": "1914"},
        "gu": {"text": "બંગાળના ભાગલા કયા વર્ષમાં થયા હતા?", "opt_a": "1903", "opt_b": "1905", "opt_c": "1911", "opt_d": "1914"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who established the Arya Samaj?", "opt_a": "Dayananda Saraswati", "opt_b": "Swami Vivekananda", "opt_c": "Raja Ram Mohan Roy", "opt_d": "Ishwar Chandra Vidyasagar"},
        "hi": {"text": "आर्य समाज की स्थापना किसने की?", "opt_a": "दयानंद सरस्वती", "opt_b": "स्वामी विवेकानंद", "opt_c": "राजा राम मोहन राय", "opt_d": "ईश्वर चंद्र विद्यासागर"},
        "gu": {"text": "આર્ય સમાજની સ્થાપના કોણે કરી હતી?", "opt_a": "દયાનંદ સરસ્વતી", "opt_b": "સ્વામી વિવેકાનંદ", "opt_c": "રાજા રામ મોહન રાય", "opt_d": "ઈશ્વરચંદ્ર વિદ્યાસાગર"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "The Salt Satyagraha started from which place?", "opt_a": "Surat", "opt_b": "Dandi", "opt_c": "Sabarmati Ashram", "opt_d": "Bardoli"},
        "hi": {"text": "नमक सत्याग्रह किस स्थान से शुरू हुआ था?", "opt_a": "सूरत", "opt_b": "दांडी", "opt_c": "साबरमती आश्रम", "opt_d": "बारडोली"},
        "gu": {"text": "મીઠાનો સત્યાગ્રહ કયા સ્થળેથી શરૂ થયો હતો?", "opt_a": "સુરત", "opt_b": "દાંડી", "opt_c": "સાબરમતી આશ્રમ", "opt_d": "બારડોલી"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Who was the first Indian to pass the Indian Civil Service exam?", "opt_a": "R. C. Dutt", "opt_b": "Satyendranath Tagore", "opt_c": "Surendranath Banerjee", "opt_d": "Dadabhai Naoroji"},
        "hi": {"text": "भारतीय सिविल सेवा परीक्षा उत्तीर्ण करने वाले पहले भारतीय कौन थे?", "opt_a": "आर. सी. दत्त", "opt_b": "सत्येंद्रनाथ टैगोर", "opt_c": "सुरेंद्रनाथ बनर्जी", "opt_d": "दादाभाई नौरोजी"},
        "gu": {"text": "ભારતીય સનદી સેવા (ICS) પરીક્ષા પાસ કરનાર પ્રથમ ભારતીય કોણ હતા?", "opt_a": "આર. સી. દત્ત", "opt_b": "સત્યેન્દ્રનાથ ટાગોર", "opt_c": "સુરેન્દ્રનાથ બેનર્જી", "opt_d": "દાદાભાઈ નવરોજી"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Who is known as the 'Grand Old Man of India'?", "opt_a": "Dadabhai Naoroji", "opt_b": "Gopal Krishna Gokhale", "opt_c": "Bipin Chandra Pal", "opt_d": "Lala Lajpat Rai"},
        "hi": {"text": "भारत के 'ग्रैंड ओल्ड मैन' के रूप में किसे जाना जाता है?", "opt_a": "दादाभाई नौरोजी", "opt_b": "गोपाल कृष्ण गोखले", "opt_c": "बिपिन चंद्र पाल", "opt_d": "लाला लाजपत राय"},
        "gu": {"text": "ભારતના 'ગ્રાન્ડ ઓલ્ડ મેન' તરીકે કોણ ઓળખાય છે?", "opt_a": "દાદાભાઈ નવરોજી", "opt_b": "ગોપાલ કૃષ્ણ ગોખલે", "opt_c": "બિપિન ચંદ્ર પાલ", "opt_d": "લાલા લાજપત રાય"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Who gave the slogan 'Jai Jawan, Jai Kisan'?", "opt_a": "Atal Bihari Vajpayee", "opt_b": "Indira Gandhi", "opt_c": "Lal Bahadur Shastri", "opt_d": "Jawaharlal Nehru"},
        "hi": {"text": "'जय जवान, जय किसान' का नारा किसने दिया?", "opt_a": "अटल बिहारी वाजपेयी", "opt_b": "इंदिरा गांधी", "opt_c": "लाल बहादुर शास्त्री", "opt_d": "जवाहरलाल नेहरू"},
        "gu": {"text": "'જય જવાન, જય કિસાન' નો નારો કોણે આપ્યો?", "opt_a": "અટલ બિહારી વાજપેયી", "opt_b": "ઇન્દિરા ગાંધી", "opt_c": "લાલ બહાદુર શાસ્ત્રી", "opt_d": "જવાહરલાલ નેહરુ"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Who founded the Forward Bloc?", "opt_a": "Subhas Chandra Bose", "opt_b": "C. R. Das", "opt_c": "Motilal Nehru", "opt_d": "Jawaharlal Nehru"},
        "hi": {"text": "फॉरवर्ड ब्लॉक की स्थापना किसने की?", "opt_a": "सुभाष चंद्र बोस", "opt_b": "सी. आर. दास", "opt_c": "मोतीलाल नेहरू", "opt_d": "जवाहरलाल नेहरू"},
        "gu": {"text": "ફોરવર્ડ બ્લોકની સ્થાપના કોણે કરી?", "opt_a": "સુભાષચંદ્ર બોઝ", "opt_b": "સી. આર. દાસ", "opt_c": "મોતીલાલ નેહરુ", "opt_d": "જવાહરલાલ નેહરુ"}
    },
    {
        "difficulty": "Medium", "correct_option": "D",
        "en": {"text": "In which session did the Indian National Congress declare Purna Swaraj?", "opt_a": "Surat Session 1907", "opt_b": "Lucknow Session 1916", "opt_c": "Karachi Session 1931", "opt_d": "Lahore Session 1929"},
        "hi": {"text": "भारतीय राष्ट्रीय कांग्रेस ने किस अधिवेशन में पूर्ण स्वराज्य की घोषणा की?", "opt_a": "सूरत अधिवेशन 1907", "opt_b": "लखनऊ अधिवेशन 1916", "opt_c": "कराची अधिवेशन 1931", "opt_d": "लाहौर अधिवेशन 1929"},
        "gu": {"text": "ભારતીય રાષ્ટ્રીય કોંગ્રેસે કયા અધિવેશનમાં પૂર્ણ સ્વરાજની જાહેરાત કરી?", "opt_a": "સુરત અધિવેશન 1907", "opt_b": "લખનૌ અધિવેશન 1916", "opt_c": "કરાચી અધિવેશન 1931", "opt_d": "લાહોર અધિવેશન 1929"}
    }
]

indian_culture_questions = [
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "The Kumbh Mela is held every how many years at a given place?", "opt_a": "12", "opt_b": "10", "opt_c": "14", "opt_d": "6"},
        "hi": {"text": "कुंभ मेला किसी एक स्थान पर कितने वर्षों में आयोजित किया जाता है?", "opt_a": "12", "opt_b": "10", "opt_c": "14", "opt_d": "6"},
        "gu": {"text": "કુંભ મેળો એક જ જગ્યાએ કેટલા વર્ષે યોજાય છે?", "opt_a": "12", "opt_b": "10", "opt_c": "14", "opt_d": "6"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Which classical dance form is famous in Odisha?", "opt_a": "Manipuri", "opt_b": "Odissi", "opt_c": "Kathakali", "opt_d": "Kuchipudi"},
        "hi": {"text": "ओडिशा में कौन सा शास्त्रीय नृत्य प्रसिद्ध है?", "opt_a": "मणिपुरी", "opt_b": "ओडिसी", "opt_c": "कथकली", "opt_d": "कुचिपुड़ी"},
        "gu": {"text": "ઓડિશામાં કયું શાસ્ત્રીય નૃત્ય પ્રખ્યાત છે?", "opt_a": "મણિપુરી", "opt_b": "ઓડિસી", "opt_c": "કથકલી", "opt_d": "કુચીપુડી"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Ayurveda is a traditional system of?", "opt_a": "Martial Arts", "opt_b": "Dance", "opt_c": "Medicine", "opt_d": "Music"},
        "hi": {"text": "आयुर्वेद किसकी पारंपरिक प्रणाली है?", "opt_a": "मार्शल आर्ट", "opt_b": "नृत्य", "opt_c": "चिकित्सा", "opt_d": "संगीत"},
        "gu": {"text": "આયુર્વેદ શેની પરંપરાગત પ્રણાલી છે?", "opt_a": "માર્શલ આર્ટ્સ", "opt_b": "નૃત્ય", "opt_c": "દવા (ચિકિત્સા)", "opt_d": "સંગીત"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Kuchipudi is a classical dance from which state?", "opt_a": "Andhra Pradesh", "opt_b": "Tamil Nadu", "opt_c": "Kerala", "opt_d": "Karnataka"},
        "hi": {"text": "कुचिपुड़ी किस राज्य का शास्त्रीय नृत्य है?", "opt_a": "आंध्र प्रदेश", "opt_b": "तमिलनाडु", "opt_c": "केरल", "opt_d": "कर्नाटक"},
        "gu": {"text": "કુચીપુડી કયા રાજ્યનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "આંધ્ર પ્રદેશ", "opt_b": "તમિલનાડુ", "opt_c": "કેરળ", "opt_d": "કર્ણાટક"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Mohiniyattam is a dance form of which state?", "opt_a": "Tamil Nadu", "opt_b": "Kerala", "opt_c": "Odisha", "opt_d": "Assam"},
        "hi": {"text": "मोहिनीअट्टम किस राज्य का नृत्य है?", "opt_a": "तमिलनाडु", "opt_b": "केरल", "opt_c": "ओडिशा", "opt_d": "असम"},
        "gu": {"text": "મોહિનીઅટ્ટમ કયા રાજ્યનું નૃત્ય છે?", "opt_a": "તમિલનાડુ", "opt_b": "કેરળ", "opt_c": "ઓડિશા", "opt_d": "આસામ"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Sattriya is a classical dance from?", "opt_a": "Manipur", "opt_b": "Mizoram", "opt_c": "Assam", "opt_d": "Tripura"},
        "hi": {"text": "सत्त्रिया कहाँ का शास्त्रीय नृत्य है?", "opt_a": "मणिपुर", "opt_b": "मिजोरम", "opt_c": "असम", "opt_d": "त्रिपुरा"},
        "gu": {"text": "સત્ત્રિયા ક્યાંનું શાસ્ત્રીય નૃત્ય છે?", "opt_a": "મણિપુર", "opt_b": "મિઝોરમ", "opt_c": "આસામ", "opt_d": "ત્રિપુરા"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Bihu is a popular folk dance of?", "opt_a": "Assam", "opt_b": "Bengal", "opt_c": "Odisha", "opt_d": "Bihar"},
        "hi": {"text": "बिहू कहाँ का लोकप्रिय लोक नृत्य है?", "opt_a": "असम", "opt_b": "बंगाल", "opt_c": "ओडिशा", "opt_d": "बिहार"},
        "gu": {"text": "બિહુ ક્યાંનું લોકપ્રિય લોક નૃત્ય છે?", "opt_a": "આસામ", "opt_b": "બંગાળ", "opt_c": "ઓડિશા", "opt_d": "બિહાર"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Madhubani painting is a famous art style from?", "opt_a": "Rajasthan", "opt_b": "Bihar", "opt_c": "Gujarat", "opt_d": "Maharashtra"},
        "hi": {"text": "मधुबनी चित्रकला कहाँ की प्रसिद्ध कला शैली है?", "opt_a": "राजस्थान", "opt_b": "बिहार", "opt_c": "गुजरात", "opt_d": "महाराष्ट्र"},
        "gu": {"text": "મધુબની ચિત્રકળા ક્યાંની પ્રખ્યાત કલા શૈલી છે?", "opt_a": "રાજસ્થાન", "opt_b": "બિહાર", "opt_c": "ગુજરાત", "opt_d": "મહારાષ્ટ્ર"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Warli painting is associated with which state?", "opt_a": "Maharashtra", "opt_b": "Madhya Pradesh", "opt_c": "Chhattisgarh", "opt_d": "Jharkhand"},
        "hi": {"text": "वार्ली चित्रकला का संबंध किस राज्य से है?", "opt_a": "महाराष्ट्र", "opt_b": "मध्य प्रदेश", "opt_c": "छत्तीसगढ़", "opt_d": "झारखंड"},
        "gu": {"text": "વારલી ચિત્રકળા કયા રાજ્ય સાથે સંકળાયેલી છે?", "opt_a": "મહારાષ્ટ્ર", "opt_b": "મધ્ય પ્રદેશ", "opt_c": "છત્તીસગઢ", "opt_d": "ઝારખંડ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "Baisakhi is a major harvest festival of?", "opt_a": "Kerala", "opt_b": "Assam", "opt_c": "Punjab", "opt_d": "Gujarat"},
        "hi": {"text": "बैसाखी कहाँ का प्रमुख फसल त्योहार है?", "opt_a": "केरल", "opt_b": "असम", "opt_c": "पंजाब", "opt_d": "गुजरात"},
        "gu": {"text": "વૈસાખી ક્યાંનો મુખ્ય લણણીનો તહેવાર છે?", "opt_a": "કેરળ", "opt_b": "આસામ", "opt_c": "પંજાબ", "opt_d": "ગુજરાત"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Makar Sankranti is widely celebrated as?", "opt_a": "Festival of Lights", "opt_b": "Kite Festival", "opt_c": "Festival of Colors", "opt_d": "Boat Race"},
        "hi": {"text": "मकर संक्रांति को मुख्य रूप से किस रूप में मनाया जाता है?", "opt_a": "रोशनी का त्योहार", "opt_b": "पतंग महोत्सव", "opt_c": "रंगों का त्योहार", "opt_d": "नौका दौड़"},
        "gu": {"text": "મકર સંક્રાંતિ મુખ્યત્વે કયા સ્વરૂપે ઉજવાય છે?", "opt_a": "પ્રકાશનો તહેવાર", "opt_b": "પતંગ મહોત્સવ", "opt_c": "રંગોનો તહેવાર", "opt_d": "હોડી રેસ"}
    },
    {
        "difficulty": "Easy", "correct_option": "A",
        "en": {"text": "In which state is the Hornbill Festival celebrated?", "opt_a": "Nagaland", "opt_b": "Manipur", "opt_c": "Meghalaya", "opt_d": "Sikkim"},
        "hi": {"text": "हॉर्नबिल महोत्सव किस राज्य में मनाया जाता है?", "opt_a": "नागालैंड", "opt_b": "मणिपुर", "opt_c": "मेघालय", "opt_d": "सिक्किम"},
        "gu": {"text": "હોર્નબિલ મહોત્સવ કયા રાજ્યમાં ઉજવવામાં આવે છે?", "opt_a": "નાગાલેન્ડ", "opt_b": "મણિપુર", "opt_c": "મેઘાલય", "opt_d": "સિક્કિમ"}
    },
    {
        "difficulty": "Medium", "correct_option": "D",
        "en": {"text": "Ghoomar is a traditional women's folk dance of?", "opt_a": "Punjab", "opt_b": "Haryana", "opt_c": "Gujarat", "opt_d": "Rajasthan"},
        "hi": {"text": "घूमर महिलाओं का पारंपरिक लोक नृत्य कहाँ का है?", "opt_a": "पंजाब", "opt_b": "हरियाणा", "opt_c": "गुजरात", "opt_d": "राजस्थान"},
        "gu": {"text": "ઘૂમર મહિલાઓનું પરંપરાગત લોક નૃત્ય ક્યાંનું છે?", "opt_a": "પંજાબ", "opt_b": "હરિયાણા", "opt_c": "ગુજરાત", "opt_d": "રાજસ્થાન"}
    },
    {
        "difficulty": "Hard", "correct_option": "B",
        "en": {"text": "Which veda contains the knowledge of music?", "opt_a": "Rigveda", "opt_b": "Samaveda", "opt_c": "Yajurveda", "opt_d": "Atharvaveda"},
        "hi": {"text": "किस वेद में संगीत का ज्ञान है?", "opt_a": "ऋग्वेद", "opt_b": "सामवेद", "opt_c": "यजुर्वेद", "opt_d": "अथर्ववेद"},
        "gu": {"text": "કયા વેદમાં સંગીતનું જ્ઞાન છે?", "opt_a": "ઋગ્વેદ", "opt_b": "સામવેદ", "opt_c": "યજુર્વેદ", "opt_d": "અથર્વવેદ"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "Which epic describes the Kurukshetra War?", "opt_a": "Mahabharata", "opt_b": "Ramayana", "opt_c": "Puranas", "opt_d": "Upanishads"},
        "hi": {"text": "कौन सा महाकाव्य कुरुक्षेत्र युद्ध का वर्णन करता है?", "opt_a": "महाभारत", "opt_b": "रामायण", "opt_c": "पुराण", "opt_d": "उपनिषद"},
        "gu": {"text": "કયું મહાકાવ્ય કુરુક્ષેત્ર યુદ્ધનું વર્ણન કરે છે?", "opt_a": "મહાભારત", "opt_b": "રામાયણ", "opt_c": "પુરાણો", "opt_d": "ઉપનિષદ"}
    },
    {
        "difficulty": "Hard", "correct_option": "C",
        "en": {"text": "Yakshagana is a traditional theater form of?", "opt_a": "Andhra Pradesh", "opt_b": "Kerala", "opt_c": "Karnataka", "opt_d": "Tamil Nadu"},
        "hi": {"text": "यक्षगान कहाँ का पारंपरिक रंगमंच रूप है?", "opt_a": "आंध्र प्रदेश", "opt_b": "केरल", "opt_c": "कर्नाटक", "opt_d": "तमिलनाडु"},
        "gu": {"text": "યક્ષગાન ક્યાંનું પરંપરાગત રંગમંચ સ્વરૂપ છે?", "opt_a": "આંધ્ર પ્રદેશ", "opt_b": "કેરળ", "opt_c": "કર્ણાટક", "opt_d": "તમિલનાડુ"}
    },
    {
        "difficulty": "Easy", "correct_option": "C",
        "en": {"text": "The Taj Mahal is located on the banks of which river?", "opt_a": "Ganga", "opt_b": "Brahmaputra", "opt_c": "Yamuna", "opt_d": "Godavari"},
        "hi": {"text": "ताजमहल किस नदी के तट पर स्थित है?", "opt_a": "गंगा", "opt_b": "ब्रह्मपुत्र", "opt_c": "यमुना", "opt_d": "गोदावरी"},
        "gu": {"text": "તાજમહેલ કઈ નદીના કિનારે આવેલો છે?", "opt_a": "ગંગા", "opt_b": "બ્રહ્મપુત્રા", "opt_c": "યમુના", "opt_d": "ગોદાવરી"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "The Sun Temple is located in which city?", "opt_a": "Konark", "opt_b": "Puri", "opt_c": "Bhubaneswar", "opt_d": "Khajuraho"},
        "hi": {"text": "सूर्य मंदिर किस शहर में स्थित है?", "opt_a": "कोणार्क", "opt_b": "पुरी", "opt_c": "भुवनेश्वर", "opt_d": "खजुराहो"},
        "gu": {"text": "સૂર્ય મંદિર કયા શહેરમાં આવેલું છે?", "opt_a": "કોણાર્ક", "opt_b": "પુરી", "opt_c": "ભુવનેશ્વર", "opt_d": "ખજુરાહો"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "Khajuraho temples are situated in which state?", "opt_a": "Uttar Pradesh", "opt_b": "Madhya Pradesh", "opt_c": "Rajasthan", "opt_d": "Gujarat"},
        "hi": {"text": "खजुराहो के मंदिर किस राज्य में स्थित हैं?", "opt_a": "उत्तर प्रदेश", "opt_b": "मध्य प्रदेश", "opt_c": "राजस्थान", "opt_d": "गुजरात"},
        "gu": {"text": "ખજુરાહોના મંદિરો કયા રાજ્યમાં આવેલા છે?", "opt_a": "ઉત્તર પ્રદેશ", "opt_b": "મધ્ય પ્રદેશ", "opt_c": "રાજસ્થાન", "opt_d": "ગુજરાત"}
    },
    {
        "difficulty": "Hard", "correct_option": "D",
        "en": {"text": "Chhau dance is famous in which regions?", "opt_a": "Gujarat and Rajasthan", "opt_b": "Kerala and Karnataka", "opt_c": "Punjab and Haryana", "opt_d": "Jharkhand, West Bengal, Odisha"},
        "hi": {"text": "छऊ नृत्य किन क्षेत्रों में प्रसिद्ध है?", "opt_a": "गुजरात और राजस्थान", "opt_b": "केरल और कर्नाटक", "opt_c": "पंजाब और हरियाणा", "opt_d": "झारखंड, पश्चिम बंगाल, ओडिशा"},
        "gu": {"text": "છઉ નૃત્ય કયા પ્રદેશોમાં પ્રખ્યાત છે?", "opt_a": "ગુજરાત અને રાજસ્થાન", "opt_b": "કેરળ અને કર્ણાટક", "opt_c": "પંજાબ અને હરિયાણા", "opt_d": "ઝારખંડ, પશ્ચિમ બંગાળ, ઓડિશા"}
    },
    {
        "difficulty": "Hard", "correct_option": "A",
        "en": {"text": "Which traditional string instrument is mostly used in Carnatic music?", "opt_a": "Veena", "opt_b": "Sitar", "opt_c": "Sarod", "opt_d": "Sarangi"},
        "hi": {"text": "कर्नाटक संगीत में ज्यादातर किस पारंपरिक वाद्य यंत्र का उपयोग किया जाता है?", "opt_a": "वीणा", "opt_b": "सितार", "opt_c": "सरोद", "opt_d": "सारंगी"},
        "gu": {"text": "કર્ણાટક સંગીતમાં મોટેભાગે કયા પરંપરાગત વાદ્યનો ઉપયોગ થાય છે?", "opt_a": "વીણા", "opt_b": "સિતાર", "opt_c": "સરોદ", "opt_d": "સારંગી"}
    },
    {
        "difficulty": "Medium", "correct_option": "C",
        "en": {"text": "Ganesh Chaturthi is a grand festival particularly in?", "opt_a": "Tamil Nadu", "opt_b": "West Bengal", "opt_c": "Maharashtra", "opt_d": "Punjab"},
        "hi": {"text": "गणेश चतुर्थी विशेष रूप से कहाँ का एक भव्य त्योहार है?", "opt_a": "तमिलनाडु", "opt_b": "पश्चिम बंगाल", "opt_c": "महाराष्ट्र", "opt_d": "पंजाब"},
        "gu": {"text": "ગણેશ ચતુર્થી ખાસ કરીને ક્યાંનો ભવ્ય તહેવાર છે?", "opt_a": "તમિલનાડુ", "opt_b": "પશ્ચિમ બંગાળ", "opt_c": "મહારાષ્ટ્ર", "opt_d": "પંજાબ"}
    },
    {
        "difficulty": "Easy", "correct_option": "B",
        "en": {"text": "Durga Puja is the biggest festival in which state?", "opt_a": "Maharashtra", "opt_b": "West Bengal", "opt_c": "Gujarat", "opt_d": "Assam"},
        "hi": {"text": "दुर्गा पूजा किस राज्य का सबसे बड़ा त्योहार है?", "opt_a": "महाराष्ट्र", "opt_b": "पश्चिम बंगाल", "opt_c": "गुजरात", "opt_d": "असम"},
        "gu": {"text": "દુર્ગા પૂજા કયા રાજ્યનો સૌથી મોટો તહેવાર છે?", "opt_a": "મહારાષ્ટ્ર", "opt_b": "પશ્ચિમ બંગાળ", "opt_c": "ગુજરાત", "opt_d": "આસામ"}
    },
    {
        "difficulty": "Medium", "correct_option": "A",
        "en": {"text": "What is the traditional greeting gesture in India?", "opt_a": "Namaste", "opt_b": "Kowtow", "opt_c": "Wai", "opt_d": "Salute"},
        "hi": {"text": "भारत में पारंपरिक अभिवादन मुद्रा क्या है?", "opt_a": "नमस्ते", "opt_b": "कोवटोव", "opt_c": "वई", "opt_d": "सलाम"},
        "gu": {"text": "ભારતમાં પરંપરાગત અભિવાદન મુદ્રા કઈ છે?", "opt_a": "નમસ્તે", "opt_b": "કોવટોવ", "opt_c": "વાઈ", "opt_d": "સલામ"}
    },
    {
        "difficulty": "Medium", "correct_option": "B",
        "en": {"text": "What is the traditional Indian sweet made of milk and sugar shaped into diamonds?", "opt_a": "Laddoo", "opt_b": "Barfi / Kaju Katli", "opt_c": "Jalebi", "opt_d": "Gulab Jamun"},
        "hi": {"text": "दूध और चीनी से बनी हीरे के आकार की पारंपरिक भारतीय मिठाई क्या है?", "opt_a": "लड्डू", "opt_b": "बर्फी / काजू कतली", "opt_c": "जलेबी", "opt_d": "गुलाब जामुन"},
        "gu": {"text": "દૂધ અને ખાંડમાંથી બનેલી હીરાના આકારની પરંપરાગત ભારતીય મીઠાઈ કઈ છે?", "opt_a": "લાડુ", "opt_b": "બરફી / કાજુ કતરી", "opt_c": "જલેબી", "opt_d": "ગુલાબ જાંબુ"}
    }
]

with open('d:/project/qgame/qgame/data/indian_history_part3.json', 'w', encoding='utf-8') as f:
    json.dump(indian_history_questions, f, ensure_ascii=False, indent=4)
    
with open('d:/project/qgame/qgame/data/indian_culture_part3.json', 'w', encoding='utf-8') as f:
    json.dump(indian_culture_questions, f, ensure_ascii=False, indent=4)
