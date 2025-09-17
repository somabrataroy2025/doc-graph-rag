import random
import pandas as pd
from faker import Faker

fake = Faker('en_US')

# Predefined skill pools
technical_skills_pool = [
    "Python", "Java", "C++", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes",
    "React", "Node.js", "TensorFlow", "Spark", "PowerBI", "Tableau"
]

business_skills_pool = [
    "Communication", "Leadership", "Project Management", "Negotiation", "Teamwork",
    "Business Analysis", "Time Management", "Critical Thinking", "Presentation", "Agile"
]

projects_pool = {
    "AI Chatbot": ["Python", "TensorFlow", "AWS"],
    "E-commerce Website": ["React", "Node.js", "SQL"],
    "Data Warehouse": ["SQL", "Spark", "PowerBI"],
    "Mobile App": ["Java", "React", "Docker"],
    "Cloud Migration": ["AWS", "Kubernetes", "Docker"]
}

# Generate 30 rows of data
rows = []
for _ in range(30):
    name = fake.name()
    email = fake.email()
    mobile = fake.msisdn()[0:10]  # 10-digit mobile
    address = fake.address().replace("\n", ", ")

    project = random.choice(list(projects_pool.keys()))
    project_skills = projects_pool[project]

    # Add some randomness but ensure project skills are included
    tech_skills = list(set(random.sample(technical_skills_pool, k=random.randint(2, 5)) + project_skills))
    bus_skills = random.sample(business_skills_pool, k=random.randint(2, 4))

    rows.append([
        name,
        email,
        mobile,
        address,
        ", ".join(tech_skills),
        ", ".join(bus_skills),
        project
    ])

# Create DataFrame and save
columns = ["Employee Name", "Employee Email", "Employee Mobile", "Employee Address", 
           "Technical Skills", "Business Skills", "Project Assigned"]

df = pd.DataFrame(rows, columns=columns)

# Save to CSV
csv_file = "employee_data.csv"
df.to_csv(csv_file, index=False)

print(f"Sample CSV created: {csv_file}")
