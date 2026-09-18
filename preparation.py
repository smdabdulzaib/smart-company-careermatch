def build_preparation_plan(missing_skills):
    plan = []
    day = 1
    for skill in missing_skills[:10]:
        plan.append((day, f"{skill} fundamentals and interview concepts"))
        day += 1
        plan.append((day, f"{skill} hands-on practice / mini project"))
        day += 1
    return plan
