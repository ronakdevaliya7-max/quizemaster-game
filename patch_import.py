import re

with open(r'd:\project\qgame\qgame\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """@app.route('/admin/import_custom', methods=['POST'])
@login_required
def admin_import_custom():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    import json
    import os
    
    topics = [
        ("Ramayana", ['ramayana.json', 'ramayana_part2.json', 'ramayana_part3.json'], "Test your knowledge of the Ramayana epic, its characters, events, and teachings."),
        ("Mahabharata", ['mahabharata.json', 'mahabharata_part2.json', 'mahabharata_part3.json'], "Test your knowledge of the Mahabharata epic."),
        ("Hindu Gods", ['hindu_gods.json', 'hindu_gods_part2.json', 'hindu_gods_part3.json'], "Test your knowledge about Hindu Gods and Deities."),
        ("Indian History", ['indian_history.json', 'indian_history_part2.json', 'indian_history_part3.json'], "Test your knowledge of Indian History."),
        ("Indian Culture", ['indian_culture.json', 'indian_culture_part2.json', 'indian_culture_part3.json'], "Test your knowledge of Indian Culture and traditions.")
    ]
    
    total_added = 0
    for cat_name, file_names, desc in topics:
        questions = []
        for fn in file_names:
            data_file = os.path.join(basedir, 'data', fn)
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    questions.extend(json.load(f))
                    
        if not questions:
            continue
            
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, description=desc)
            db.session.add(cat)
            db.session.commit()
            
        added_count = 0
        for q_data in questions:
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
        total_added += added_count
        
    flash(f'Successfully imported {total_added // 3} questions across special topics in 3 languages!', 'success')
    return redirect(url_for('admin_categories'))"""

new_func = """@app.route('/admin/import_custom', methods=['POST'])
@login_required
def admin_import_custom():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    import json
    import os
    
    data_file = os.path.join(basedir, 'data', 'chatgpt.json')
    if not os.path.exists(data_file):
        flash('chatgpt.json file not found in data folder!', 'error')
        return redirect(url_for('admin_categories'))
        
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            
        cat_name = "ChatGPT Questions"
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, description="Questions imported from chatgpt.json")
            db.session.add(cat)
            db.session.commit()
            
        count = 0
        for item in questions:
            q_text = item.get('question', item.get('text', ''))
            opt_a = item.get('option_a', item.get('A', ''))
            opt_b = item.get('option_b', item.get('B', ''))
            opt_c = item.get('option_c', item.get('C', ''))
            opt_d = item.get('option_d', item.get('D', ''))
            correct = item.get('correct_option', item.get('correct', 'A'))
            diff = item.get('difficulty', 'Medium')
            
            if not q_text or not opt_a:
                continue
                
            q = Question(
                category_id=cat.id,
                text=q_text,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_option=correct,
                difficulty=diff,
                language='gu'
            )
            db.session.add(q)
            count += 1
            
        db.session.commit()
        flash(f'Successfully imported {count} questions from chatgpt.json!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error importing: {e}', 'error')
        
    return redirect(url_for('admin_categories'))"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(r'd:\project\qgame\qgame\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app.py successfully.")
else:
    print("Could not find the target string in app.py")
