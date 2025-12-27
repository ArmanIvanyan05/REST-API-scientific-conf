import argparse
import random
import requests
import uuid


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://localhost:8000/api", help="Base API URL (no trailing slash)")
    parser.add_argument("--count", type=int, default=100, help="Number of scientists to create")
    return parser.parse_args()


def create_conferences(base_url: str, count: int):
    sample_countries = ["USA", "UK", "Germany", "France", "Russia", "China", "India", "Brazil"]
    sample_words = ["physics", "biology", "chemistry", "mathematics", "AI", "robotics", "ecology", "materials"]
    sample_places = ["Berlin", "Paris", "New York", "Moscow", "Beijing", "Tokyo", "Yerevan"]

    conf_ids = []
    for i in range(max(5, count // 20)):
        payload = {
            "name": f"Conference {i+1} - {random.choice(sample_words).title()}",
            "theme": random.choice(sample_words),
            "topic": random.choice(sample_words),
            "place": random.choice(sample_places),
            "country": random.choice(sample_countries),
        }
        try:
            r = requests.post(f"{base_url}/conferences", json=payload, timeout=10)
        except Exception as exc:
            print(f"Error creating conference: {exc}")
            continue
        if r.status_code in (200, 201):
            data = r.json()
            conf_ids.append(data.get("id"))
        else:
            print(f"Failed to create conference: {r.status_code} {r.text}")
    return [c for c in conf_ids if c]


def create_scientists(base_url: str, count: int):
    sample_countries = ["USA", "UK", "Germany", "France", "Russia", "China", "India", "Brazil"]
    sample_words = ["physics", "biology", "chemistry", "mathematics", "AI", "robotics", "ecology", "materials"]
    sample_orgs = ["Univ A", "Institute B", "Lab C", "Research Center D"]

    scientist_ids = []
    for _ in range(count):
        payload = {
            "full_name": f"Dr. {uuid.uuid4().hex[:8]}",
            "country": random.choice(sample_countries),
            "degree": random.choice(["PhD", "MSc", "BSc", None]),
            "specialization": random.choice(sample_words),
            "organization": random.choice(sample_orgs),
        }
        try:
            r = requests.post(f"{base_url}/scientists", json=payload, timeout=10)
        except Exception as exc:
            print(f"Error creating scientist: {exc}")
            continue
        if r.status_code in (200, 201):
            data = r.json()
            scientist_ids.append(data.get("id"))
        else:
            print(f"Failed to create scientist: {r.status_code} {r.text}")
    return [s for s in scientist_ids if s]


def create_participations(base_url: str, scientist_ids, conf_ids):
    if not conf_ids:
        print("No conferences available to create participations.")
        return
    for sid in scientist_ids:
        conf_id = random.choice(conf_ids)
        payload = {
            "scientist_id": sid,
            "conference_id": conf_id,
            "participation_type": random.choice(["speaker", "poster", "attendee"]),
            "topic": random.choice(["physics", "AI", "robotics", "ecology"]),
            "duration_minutes": random.choice([15, 30, 60, None]),
        }
        try:
            r = requests.post(f"{base_url}/participations", json=payload, timeout=10)
        except Exception as exc:
            print(f"Error creating participation for scientist {sid}: {exc}")
            continue
        if r.status_code not in (200, 201):
            print(f"Failed to create participation: {r.status_code} {r.text}")


def main():
    args = make_args()
    print(f"Using base URL: {args.base}")
    print(f"Creating {args.count} scientists and participations...")

    conf_ids = create_conferences(args.base, args.count)
    print(f"Created {len(conf_ids)} conferences")

    scientist_ids = create_scientists(args.base, args.count)
    print(f"Created {len(scientist_ids)} scientists")

    create_participations(args.base, scientist_ids, conf_ids)
    print("Data load complete.")