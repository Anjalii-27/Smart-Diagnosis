from flask import Flask, request, jsonify
import re

app = Flask(__name__)

symptoms_dict = {
   
     "fever": "Cold & Flu",
        "cough": "Cold & Flu",
        "cold" : "Cold & Flu",
        "headache": "Migraine",
        "migraine Headache": "Migraine",
        "stomach ache": "food poisoning",
        "cramps": "food poisoning",
        "stomach pain": "food poisoning",
        "vomiting": "food poisoning",
        "rash": "Allergies",
        "allergy": "Allergies",
        "nervousness": "Anxiety",
        "blood pressure": "Anxiety",
        "anxiety": "Anxiety",
        "coronavirus": "COVID-19",
        "covid": "COVID-19",
        "depression": "Depression",
        "stress": "Depression",
        "stools": "Diarrhea",
        "diarrhea": "Diarrhea",
        "balding": "Hair Loss",
        "hair loss": "Hair Loss",
        "baldness": "Hair Loss",
        "diabetes": "Diabetes (Type 1)",
        "losing weight": "Diabetes (Type 1)",
        "feeling tired": "Diabetes (Type 1)",
        "fatigue": "Diabetes (Type 2)",
        "sugar": "Diabetes (Type 2)",
        "chest pain": "heart attack",
        "Cold sweat": "heart attack",
        "Heartburn": "heart attack",
        "shortness of breath": "asthma",
        "chest tightness": "asthma",
        "wheezing ": "asthma",
        "climacteric": "Menopause",
        "insomnia": "Menopause",
        "no periods": "Menopause",
        "blackheads": "Acne",
        "pimples": "Acne",
        "whiteheads": "Acne",
        "tissue damage": "Pain / Tissue Damage",
        "pain": "Pain / Tissue Damage",
        "tissue tear": "Pain / Tissue Damage",
        "H1N1 Influenza": "Swine Flu",
        "lethargy": "Swine Flu",
        "nausea": "Swine Flu"
}

remedies_dict = {
    "Cold & Flu": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Benadryl](https://www.drugs.com/benadryl.html), [diphenhydramine](https://www.drugs.com/diphenhydramine.html),[Vicks Nyquil D Cold and Flu Nighttime Relief](https://www.drugs.com/mtm/nyquil-d.html) Please consult your healthcare provider before starting any new medication. Home Remedy:' Drink hot ginger tea with lemon and honey.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) . ",        
        "heart attack": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Aspirin](https://www.drugs.com/aspirin.html), [Nitroglycerin](https://my.clevelandclinic.org/health/drugs/20423-nitroglycerin-sublingual-tablets) Please consult your healthcare provider before starting any new medication. Home Remedy: Call 911 or go to the emergency room immediately. Do not attempt to treat a heart attack at home. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Migraine": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [sumatriptan](https://www.drugs.com/condition/migraine.html), [Imitrex](https://www.drugs.com/condition/migraine.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Apply peppermint oil on temples; drink ginger tea.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) . ",
        "food poisoning": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Loperamide (Imodium):](https://www.imodium.com/), [Oral rehydration salts (ORS)]. Please consult your healthcare provider before starting any new medication. Home Remedy:'Drink ginger tea to soothe stomach and reduce nausea.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Allergies": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [hydroxyzine](https://www.drugs.com/hydroxyzine.html), [levocetirizine](https://www.drugs.com/levocetirizine.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Drink nettle tea to reduce inflammation and allergy symptoms.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) . ",
        "asthma": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Albuterol (Ventolin, ProAir)](https://www.drugs.com/mtm/proair-hfa.html), [Fluticasone (Flovent)](https://www.drugs.com/mtm/flovent-hfa.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Inhale steam with eucalyptus oil to open airways.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Acne" : "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [doxycycline](https://www.drugs.com/doxycycline.html), [spironolactone](https://www.drugs.com/spironolactone.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Apply honey and cinnamon mask; wash with warm water.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) . ",
        "Anxiety": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Xanax](https://www.drugs.com/xanax.html), [clonazepam](https://www.drugs.com/clonazepam.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Practice deep breathing exercises and drink chamomile tea.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "COVID-19" : "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Pfizer-BioNTech COVID-19 Vaccine], [remdesivir] . Please consult your healthcare provider before starting any new medication. Home Remedy:'Gargle salt water; rest and stay hydrated.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Diabetes (Type 1)": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Humalog]https://www.drugs.com/humalog.html), [Lantus](https://www.drugs.com/lantus.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Follow a balanced diet and monitor blood sugar levels.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Diabetes (Type 2)": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [metformin](https://www.drugs.com/metformin.html), [Farxiga](https://www.drugs.com/farxiga.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Consume cinnamon daily to help manage blood sugar levels.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Depression": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [bupropion](https://www.drugs.com/bupropion.html), [Cymbalta](https://www.drugs.com/cymbalta.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Exercise regularly and get sunlight exposure for mood improvement.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Diarrhea": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [loperamide](https://www.drugs.com/loperamide.html), [Lomotil](https://www.drugs.com/mtm/lomotil.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Drink oral rehydration solution and consume plain yogurt.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Hair Loss": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [spironolactone](https://www.drugs.com/spironolactone.html), [minoxidil](https://www.drugs.com/mtm/minoxidil-topical.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Massage scalp with coconut oil to strengthen hair follicles.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Menopause": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [esterified estrogens / methyltestosterone](https://www.drugs.com/condition/menopausal-disorders.html), [EEMT HS](https://www.drugs.com/condition/menopausal-disorders.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Drink soy milk to help manage menopausal symptoms.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Pain / Tissue Damage": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [ibuprofen](https://www.drugs.com/ibuprofen.html), [tramadol](https://www.drugs.com/tramadol.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Use turmeric in meals for its anti-inflammatory properties.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) .",
        "Swine Flu": "Our system has identified the likely condition and suggests the following treatment plan. Prescribed Medicine : [Tamiflu](https://www.drugs.com/condition/swine-flu.html), [oseltamivir](https://www.drugs.com/condition/swine-flu.html) Please consult your healthcare provider before starting any new medication. Home Remedy:'Stay hydrated and rest; drink warm herbal teas.' This home remedy can help alleviate symptoms and support your recovery. However, it should not replace professional medical advice or treatment. For your convenience, you can order the prescribed medicine online from the following pharmacy:(https://www.apollopharmacy.in/) ."
       }


def check_severity(symptoms):
    severity = "mild"
    for symptom in symptoms:
        disease = symptoms_dict.get(symptom.lower())
        if disease and disease != "allergies":
            severity = "severe"
            break
    return severity


@app.route('/', methods=['POST'])
def get_response():

    data = request.json
    user_input = data['user_input']
    tokens = re.findall(r'\w+', user_input.lower())

    symptoms = [token for token in tokens if token in symptoms_dict.keys()]

    severity = check_severity(symptoms)

    if severity == "severe":
        response = "It sounds like your condition is severe. You should seek medical attention as soon as possible."

    elif severity == "mild":
        disease = None
        for token in tokens:
            if token in remedies_dict.keys():
                disease = token
                break

        if disease:
            response = f"Based on your symptoms, it seems like you have {disease}. {remedies_dict[disease]}"
        else:
            response = "I'm sorry, I'm not sure what condition you have. Can you please provide more information?"

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
