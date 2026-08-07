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

new_func = """@app.route('/admin/import_custom', methods=['POST'])
@login_required
def admin_import_custom():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    import os
    import re
    
    data_file = os.path.join(basedir, 'data', 'questions.txt')
    if not os.path.exists(data_file):
        flash('questions.txt file not found in data folder!', 'error')
        return redirect(url_for('admin_categories'))
        
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse blocks separated by dashes
        blocks = re.split(r'-{10,}', content)
        
        count = 0
        for block in blocks:
            block = block.strip()
            if not block:
                continue
                
            # Regex to extract Category, Difficulty, Question
            header_match = re.search(r'([A-Za-z\s&:]+)\s*\((Easy|Medium|Hard)\):\s*(.+)', block)
            if not header_match:
                continue
                
            cat_name = header_match.group(1).strip()
            diff = header_match.group(2).strip()
            q_text = header_match.group(3).strip()
            
            # Extract options
            opt_a = re.search(r'A:\s*(.+)', block).group(1).strip()
            opt_b = re.search(r'B:\s*(.+)', block).group(1).strip()
            opt_c = re.search(r'C:\s*(.+)', block).group(1).strip()
            opt_d = re.search(r'D:\s*(.+)', block).group(1).strip()
            
            # Extract correct answer
            correct = re.search(r'Correct Answer:\s*([A-D])', block).group(1).strip()
            
            # Get or create category
            cat = Category.query.filter_by(name=cat_name).first()
            if not cat:
                cat = Category(name=cat_name, description=f"{cat_name} category imported via text parser")
                db.session.add(cat)
                db.session.commit()
                
            q = Question(
                category_id=cat.id,
                text=q_text,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_option=correct,
                difficulty=diff,
                language='en'
            )
            db.session.add(q)
            count += 1
            
        db.session.commit()
        flash(f'Successfully parsed and imported {count} questions from questions.txt!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error parsing text file: {e}', 'error')
        
    return redirect(url_for('admin_categories'))"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(r'd:\project\qgame\qgame\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app.py successfully.")
else:
    print("Could not find the target string in app.py")
