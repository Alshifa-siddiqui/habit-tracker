"""
Vitalis Medical Insights Engine
Provides general wellness information based on habit patterns.

NOTE: The figures and statements below are illustrative general-wellness
content, not clinically sourced guidance. Always surface MEDICAL_DISCLAIMER
wherever this content is shown to users.
"""

MEDICAL_DISCLAIMER = (
    "⚠️  For general wellness information only — not medical advice. "
    "Consult a qualified healthcare professional before making health decisions."
)

MEDICAL_INSIGHTS = {
    "water": {
        "name": "Hydration",
        "unit": "glasses/day",
        "recommended": 8,
        "benefits": [
            "Improves kidney function and reduces kidney stone risk",
            "Boosts cognitive performance by up to 30%",
            "Regulates body temperature and joint lubrication",
            "Aids digestion and nutrient absorption",
            "Improves skin elasticity and reduces wrinkles",
        ],
        "risks": {
            "low": [
                "⚠️ Dehydration: fatigue, headaches, reduced concentration",
                "⚠️ Increased kidney stone risk (up to 50% higher)",
                "⚠️ Urinary tract infections more likely",
                "⚠️ Constipation and digestive issues",
                "⚠️ Blood pressure fluctuations",
            ],
            "critical": [
                "🚨 Severe dehydration: dizziness, rapid heartbeat",
                "🚨 Risk of heatstroke in warm conditions",
                "🚨 Kidney damage with prolonged dehydration",
            ]
        },
        "conditions": {
            "diabetes": "Critical for blood sugar regulation. Dehydration raises blood glucose levels significantly.",
            "hypertension": "Adequate hydration helps maintain healthy blood pressure.",
            "kidney_disease": "Consult your doctor — fluid intake needs careful management.",
            "heart_disease": "Proper hydration supports healthy heart function.",
        }
    },
    "sleep": {
        "name": "Sleep",
        "unit": "hours/night",
        "recommended": 8,
        "benefits": [
            "Consolidates memory and improves learning by 40%",
            "Regulates hormones including cortisol and insulin",
            "Strengthens immune system — reduces illness risk by 3x",
            "Reduces risk of heart disease and stroke",
            "Supports mental health and emotional regulation",
        ],
        "risks": {
            "low": [
                "⚠️ Impaired cognitive function and decision making",
                "⚠️ Increased cortisol (stress hormone) levels",
                "⚠️ Weight gain — disrupts hunger hormones leptin/ghrelin",
                "⚠️ Weakened immune response",
                "⚠️ Higher risk of accidents and errors",
            ],
            "critical": [
                "🚨 Chronic sleep deprivation linked to Type 2 diabetes",
                "🚨 40% increased risk of cardiovascular disease",
                "🚨 Severe mental health impacts including depression",
            ]
        },
        "conditions": {
            "diabetes": "Poor sleep increases insulin resistance significantly.",
            "hypertension": "Sleep deprivation raises blood pressure by 10-20 mmHg.",
            "depression": "Sleep is critical — disrupted sleep worsens depressive episodes.",
            "obesity": "Lack of sleep increases hunger hormones, making weight management harder.",
        }
    },
    "exercise": {
        "name": "Exercise",
        "unit": "sessions/week",
        "recommended": 5,
        "benefits": [
            "Reduces cardiovascular disease risk by up to 35%",
            "Releases endorphins — natural antidepressant effect",
            "Improves insulin sensitivity by 23%",
            "Increases bone density and muscle mass",
            "Boosts brain neuroplasticity and memory",
            "Extends lifespan by an average of 3-7 years",
        ],
        "risks": {
            "low": [
                "⚠️ Increased risk of Type 2 diabetes",
                "⚠️ Muscle atrophy and reduced bone density",
                "⚠️ Higher risk of depression and anxiety",
                "⚠️ Cardiovascular health decline",
                "⚠️ Metabolic slowdown and weight gain",
            ],
            "critical": [
                "🚨 Sedentary lifestyle: 2x risk of cardiovascular disease",
                "🚨 Increased cancer risk (colon, breast)",
                "🚨 Accelerated cognitive decline",
            ]
        },
        "conditions": {
            "diabetes": "Exercise is as effective as medication for Type 2 diabetes management.",
            "hypertension": "Regular aerobic exercise reduces systolic BP by 5-8 mmHg.",
            "depression": "Exercise is clinically proven to be as effective as antidepressants.",
            "obesity": "Essential for weight management and metabolic health.",
            "arthritis": "Low-impact exercise reduces joint pain and improves mobility.",
        }
    },
    "meditation": {
        "name": "Meditation / Mindfulness",
        "unit": "sessions/week",
        "recommended": 7,
        "benefits": [
            "Reduces cortisol levels by up to 23%",
            "Improves focus and attention span significantly",
            "Reduces anxiety and depression symptoms",
            "Lowers blood pressure by 4-5 mmHg",
            "Strengthens immune system response",
        ],
        "risks": {
            "low": [
                "⚠️ Higher baseline stress and cortisol levels",
                "⚠️ Reduced emotional regulation capacity",
                "⚠️ Poorer sleep quality",
                "⚠️ Increased anxiety and rumination",
            ],
            "critical": []
        },
        "conditions": {
            "anxiety": "Mindfulness-based therapy reduces anxiety symptoms by 58%.",
            "depression": "Regular meditation reduces relapse risk significantly.",
            "hypertension": "Clinically proven to lower blood pressure.",
            "chronic_pain": "Reduces pain perception and improves quality of life.",
        }
    },
    "nutrition": {
        "name": "Healthy Eating",
        "unit": "days/week",
        "recommended": 7,
        "benefits": [
            "Reduces inflammation throughout the body",
            "Supports gut microbiome diversity",
            "Stabilizes blood sugar and energy levels",
            "Reduces risk of 13+ types of cancer",
            "Supports cognitive function and mood",
        ],
        "risks": {
            "low": [
                "⚠️ Nutritional deficiencies affecting energy and immunity",
                "⚠️ Blood sugar instability and energy crashes",
                "⚠️ Increased inflammation markers",
                "⚠️ Higher risk of metabolic syndrome",
            ],
            "critical": [
                "🚨 Linked to heart disease, stroke, and diabetes",
                "🚨 Gut microbiome imbalance affecting mental health",
            ]
        },
        "conditions": {
            "diabetes": "Diet is the most powerful tool for blood sugar management.",
            "hypertension": "DASH diet can reduce blood pressure as effectively as medication.",
            "heart_disease": "Mediterranean diet reduces cardiovascular events by 30%.",
            "ibs": "Diet directly controls symptom severity.",
        }
    },
    "reading": {
        "name": "Reading",
        "unit": "sessions/week",
        "recommended": 5,
        "benefits": [
            "Reduces cognitive decline risk by 32%",
            "Builds vocabulary and communication skills",
            "Reduces stress levels by 68% in 6 minutes",
            "Improves empathy and social understanding",
            "Enhances focus and concentration",
        ],
        "risks": {
            "low": [
                "⚠️ Faster cognitive aging",
                "⚠️ Reduced mental stimulation",
                "⚠️ Higher dementia risk in older age",
            ],
            "critical": []
        },
        "conditions": {
            "alzheimers": "Regular reading is one of the strongest protective factors.",
            "depression": "Bibliotherapy (reading therapy) is clinically recognized.",
            "anxiety": "Reading reduces anxiety and provides healthy escapism.",
        }
    }
}

HEALTH_CONDITIONS = [
    "None", "Diabetes", "Hypertension", "Heart Disease", "Depression",
    "Anxiety", "Obesity", "Arthritis", "Kidney Disease", "Asthma",
    "Chronic Pain", "IBS", "Alzheimer's Risk", "Insomnia"
]

HABIT_KEYWORDS = {
    "water": ["water", "hydrat", "drink"],
    "sleep": ["sleep", "rest", "bed"],
    "exercise": ["exercise", "workout", "gym", "run", "walk", "yoga", "swim", "sport", "fitness"],
    "meditation": ["meditat", "mindful", "breath", "calm", "relax"],
    "nutrition": ["eat", "diet", "nutrition", "food", "meal", "cook", "vegeta", "fruit"],
    "reading": ["read", "book", "study", "learn"],
}


def detect_habit_type(habit_name: str) -> str:
    name_lower = habit_name.lower()
    for habit_type, keywords in HABIT_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                return habit_type
    return None


def get_medical_insight(habit_name: str, completion_rate: float,
                        user_conditions: list = None, streak: int = 0) -> dict:
    habit_type = detect_habit_type(habit_name)
    if not habit_type:
        return None

    data = MEDICAL_INSIGHTS[habit_type]
    user_conditions = [c.lower() for c in (user_conditions or [])]

    insight = {
        "habit_type": habit_type,
        "name": data["name"],
        "completion_rate": completion_rate,
        "status": "",
        "status_color": "",
        "headline": "",
        "benefits": [],
        "risks": [],
        "condition_warnings": [],
        "score": 0,
    }

    # Determine status
    if completion_rate >= 80:
        insight["status"] = "Excellent"
        insight["status_color"] = "#4CAF50"
        insight["headline"] = f"🌟 Great job! Your {data['name'].lower()} habit is protecting your health."
        insight["benefits"] = data["benefits"][:3]
        insight["score"] = 100
    elif completion_rate >= 50:
        insight["status"] = "Good"
        insight["status_color"] = "#FFD700"
        insight["headline"] = f"👍 Good consistency. Improving your {data['name'].lower()} habit further will unlock more benefits."
        insight["benefits"] = data["benefits"][:2]
        insight["risks"] = data["risks"]["low"][:2]
        insight["score"] = 65
    elif completion_rate >= 25:
        insight["status"] = "Needs Work"
        insight["status_color"] = "#FF9800"
        insight["headline"] = f"⚠️ Your {data['name'].lower()} habit needs improvement. Health risks are accumulating."
        insight["risks"] = data["risks"]["low"][:3]
        insight["score"] = 35
    else:
        insight["status"] = "Critical"
        insight["status_color"] = "#F44336"
        insight["headline"] = f"🚨 Critical: Your {data['name'].lower()} habit is at a dangerously low level."
        insight["risks"] = data["risks"]["low"] + data["risks"].get("critical", [])
        insight["score"] = 10

    # Condition-specific warnings
    condition_map = {
        "diabetes": "diabetes", "hypertension": "hypertension",
        "heart disease": "heart_disease", "depression": "depression",
        "anxiety": "anxiety", "obesity": "obesity",
        "arthritis": "arthritis", "kidney disease": "kidney_disease",
        "chronic pain": "chronic_pain", "ibs": "ibs",
        "alzheimer's risk": "alzheimers", "insomnia": "sleep"
    }
    for cond in user_conditions:
        if cond in condition_map:
            key = condition_map[cond]
            if key in data.get("conditions", {}):
                insight["condition_warnings"].append(
                    f"🏥 {cond.title()}: {data['conditions'][key]}"
                )

    return insight


def get_habit_personality(habits_data: list) -> dict:
    if not habits_data:
        return {"type": "Explorer", "description": "Just getting started on your journey!",
                "emoji": "🌱", "color": "#4CAF50"}

    categories = [h.get("category", "General") for h in habits_data]
    avg_streak = sum(h.get("current_streak", 0) for h in habits_data) / max(len(habits_data), 1)
    total_checkins = sum(h.get("completed_count", 0) for h in habits_data)

    health_count = categories.count("Health") + categories.count("Fitness")
    work_count = categories.count("Work") + categories.count("Learning")
    personal_count = categories.count("Personal")

    if avg_streak > 20 and total_checkins > 100:
        return {
            "type": "The Iron Will",
            "description": "Exceptional discipline. You don't just set habits — you become them. Top 1% consistency.",
            "emoji": "⚔️", "color": "#FFD700"
        }
    elif health_count > work_count and avg_streak > 10:
        return {
            "type": "The Vitality Seeker",
            "description": "Your body is your temple. You prioritize physical and mental health above all.",
            "emoji": "💪", "color": "#4CAF50"
        }
    elif work_count > health_count and avg_streak > 7:
        return {
            "type": "The Achiever",
            "description": "Success-driven and focused. You use habits as tools for professional dominance.",
            "emoji": "🚀", "color": "#2196F3"
        }
    elif avg_streak > 5 and len(habits_data) > 5:
        return {
            "type": "The Architect",
            "description": "You build systems, not just habits. Methodical, structured, always improving.",
            "emoji": "🏗️", "color": "#9C27B0"
        }
    elif total_checkins > 30:
        return {
            "type": "The Grinder",
            "description": "You show up even when it's hard. Resilient and persistent — streaks are just a bonus.",
            "emoji": "🔥", "color": "#FF5722"
        }
    else:
        return {
            "type": "The Explorer",
            "description": "You're discovering what works for you. Every habit is an experiment in self-improvement.",
            "emoji": "🌱", "color": "#00BCD4"
        }


def get_health_score(habits_data: list, user_conditions: list = None) -> dict:
    if not habits_data:
        return {"score": 0, "grade": "N/A", "color": "#757575", "breakdown": {}}

    breakdown = {}
    total_score = 0
    scored = 0

    for habit in habits_data:
        habit_type = detect_habit_type(habit.get("name", ""))
        if not habit_type:
            continue
        rate = min(habit.get("completed_count", 0), 100)
        insight = get_medical_insight(habit["name"], rate, user_conditions)
        if insight:
            breakdown[habit["name"]] = insight["score"]
            total_score += insight["score"]
            scored += 1

    if scored == 0:
        return {"score": 50, "grade": "C", "color": "#FF9800", "breakdown": {}}

    avg = total_score / scored
    if avg >= 90:
        grade, color = "S", "#FFD700"
    elif avg >= 75:
        grade, color = "A", "#4CAF50"
    elif avg >= 60:
        grade, color = "B", "#8BC34A"
    elif avg >= 45:
        grade, color = "C", "#FF9800"
    elif avg >= 30:
        grade, color = "D", "#FF5722"
    else:
        grade, color = "F", "#F44336"

    return {"score": round(avg), "grade": grade, "color": color, "breakdown": breakdown}