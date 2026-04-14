def validate_selection(user_choice, correct_answer):
    """Subprogram with parameter passing"""
    if user_choice == correct_answer:
        return "SUCCESS: Correct Pseudocode Syntax"
    else:
        return "ERROR: Incorrect Syntax - Check Hints"

scenarios = {
    1: {"title": "Variable Assignment", "correct": "x ← 10"},
    2: {"title": "Selection", "correct": "IF age > 18 THEN"}
}

print(f"Testing {scenarios[1]['title']}...")
result = validate_selection("x ← 10", scenarios[1]['correct'])
print(result)
