def generate_recommendation(missing_skills):
    recommendations= []
    skill_lower=[]
    for skills in missing_skills:
        skill_lower.append(skills.lower())
    if  "git" in skill_lower and "github" in skill_lower :
        recommendations.append("Learn Git and GitHub for version control and mention them in your projects.")
    elif "git" in skill_lower:
        recommendations.append(
            "Learn Git for version control and use it in your projects."
        )
    elif "github" in skill_lower:
        recommendations.append(
            "Upload your projects to GitHub and maintain a professional GitHub profile."
        )
    frontend=[]
    if "html" in skill_lower:
        frontend.append("HTML")
    if "css" in skill_lower:
        frontend.append("CSS")
    if "javascript" in skill_lower:
        frontend.append("JavaScript")
    if "bootstrap" in skill_lower:
        frontend.append("Bootstrap")
    if frontend:
        recommendations.append("Improve your frontend skills by learning "+",".join(frontend[:-1])+ ("and"+frontend[-1] if len(frontend)>1 else frontend[0])+".")

    backend = []

    if "rest api" in skill_lower:
        backend.append("REST API")
    if "django rest framework" in skill_lower:
        backend.append("Django REST Framework")
    if backend:
        recommendations.append(
            "Build API-based Django applications using "
            + ", ".join(backend[:-1])
            + (" and " + backend[-1] if len(backend) > 1 else backend[0])
            + "."
        )


    database=[]
    if "mysql" in skill_lower:
        database.append("MySQL")

    if "postgresql" in skill_lower:
        database.append("PostgreSQL")

    if "mongodb" in skill_lower:
        database.append("MongoDB")

    if "sql" in skill_lower:
        database.append("SQL")

    if database:
        recommendations.append(
            "Improve your database knowledge using "+",".join(database[:-1]) + ("and" +database[-1] if len(database)>1 else database[0]) + ".")

    deployment = []

    if "docker" in skill_lower:
        deployment.append("Docker")

    if "linux" in skill_lower:
        deployment.append("Linux")

    if "aws" in skill_lower:
        deployment.append("AWS")

    if "deployment" in skill_lower:
        deployment.append("Deployment")

    if deployment:
        recommendations.append(
            "Learn "
            + ", ".join(deployment[:-1])
            + (" and " + deployment[-1] if len(deployment) > 1 else deployment[0])
            + " to deploy real-world applications."
        )

    aiml = []

    if "machine learning" in skill_lower:
        aiml.append("Machine Learning")
    if "deep learning" in skill_lower:
        aiml.append("Deep Learning")
    if "nlp" in skill_lower:
        aiml.append("NLP")
    if "numpy" in skill_lower:
        aiml.append("NumPy")
    if "pandas" in skill_lower:
        aiml.append("Pandas")
    if "matplotlib" in skill_lower:
        aiml.append("Matplotlib")
    if aiml:
        recommendations.append(
            "Strengthen your AI/ML knowledge using "
            + ", ".join(aiml[:-1])
            + (" and " + aiml[-1] if len(aiml) > 1 else aiml[0])
            + " by building practical projects."
        )

    return recommendations