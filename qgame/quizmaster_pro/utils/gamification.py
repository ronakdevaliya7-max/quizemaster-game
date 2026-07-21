from models import db, UserBadge, Badge

LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 5000] # Levels 1 to 7
LEVEL_NAMES = {
    1: 'Beginner',
    2: 'Learner',
    3: 'Skilled',
    4: 'Advanced',
    5: 'Expert',
    6: 'Master',
    7: 'Champion'
}

def calculate_level(xp):
    for idx, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp < threshold:
            return idx
    return 7

def process_quiz_result(user, attempt):
    # Calculate points: 10 per correct answer
    points_earned = attempt.score * 10
    user.points += points_earned
    
    # Calculate XP: 20 base + 5 per correct answer
    xp_earned = 20 + (attempt.score * 5)
    user.xp += xp_earned
    
    # Coins: 1 per correct answer
    user.coins += attempt.score
    
    # Update Level
    new_level = calculate_level(user.xp)
    if new_level > user.level:
        user.level = new_level
        
    # Check Badges
    badges = Badge.query.all()
    user_badge_ids = [ub.badge_id for ub in user.badges]
    
    for badge in badges:
        if badge.id in user_badge_ids:
            continue
            
        award = False
        if badge.requirement_type == 'first_quiz':
            if len(user.attempts) >= 0: # Already added the attempt before calling
                award = True
        elif badge.requirement_type == 'perfect_score':
            if attempt.score == attempt.total_questions and attempt.total_questions > 0:
                award = True
        elif badge.requirement_type == 'points':
            if user.points >= badge.requirement_value:
                award = True
                
        if award:
            ub = UserBadge(user_id=user.id, badge_id=badge.id)
            db.session.add(ub)
            
    db.session.commit()
    return points_earned, xp_earned
