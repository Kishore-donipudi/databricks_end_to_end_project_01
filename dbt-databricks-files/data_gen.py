# Databricks notebook source
# %pip install faker +-

# COMMAND ----------

# %restart_python 

# COMMAND ----------

from faker import Faker
import pandas as pd
import random
fake = Faker()

genres = ["Action","Adventure","Fantasy","Comedy","Drama","Sci-Fi","Romance","Thriller","Anime"]
languages = ["English","Japanese","Korean","Hindi","Spanish"]
plans = {"Basic": 199, "Standard": 499, "Premium": 799}

def get_count(folder, id_col):
    """Read all CSVs in the S3 folder and return the max numeric ID + 1."""
    path = f's3://de-prj/{folder}'
    try:
        files = dbutils.fs.ls(path)
    except:
        return 1
    max_id = -1
    for f in files:
        if f.name.endswith('.csv') and folder in f.name:
            df = spark.read.csv(f"{path}/{f.name}", header=True).toPandas()
            vals = df[id_col].str.replace(r'\D', '', regex=True).astype(int)
            max_id = max(max_id, vals.max())
    return max(max_id + 1, 1)

def fake_data(folder,data):
    dbutils.fs.mkdirs(f's3://de-prj/{folder}')
    path=f's3://de-prj/{folder}'
    files = dbutils.fs.ls(f"{path}")
    nums = []
    file_names = {}
    for f in files:
        if f'{folder}' in f.name and f.name.endswith('.csv'):
            digits = ''.join(c for c in f.name if c.isdigit())
            if digits:
                num = int(digits)
                nums.append(num)
                file_names[num] = f.name
    first_key=list(data(0).keys())[0]
    if nums:
        last_num = max(nums)
        next_num = last_num + 1
        # Read the last file to find the last user_id generated
        last_file = file_names[last_num]
        prev_df = spark.read.csv(f"{path}/{last_file}", header=True).toPandas()
        prev_rec = int(prev_df[f'{first_key}'].str.replace(r'\D', '', regex=True).astype(int).max()) + 1
    else:
        next_num = 1
        prev_rec = 0
    # Generate 3 files in a loop, each with 100 records continuing the user_id sequence
    num_files = 2
    for _ in range(num_files):
        dyn_rec = prev_rec + 100
        new_file = f"{folder}_{next_num:03d}.csv"
        rows = []
        for i in range(prev_rec, dyn_rec):
            rows.append(data(i))
        df = pd.DataFrame(rows)
        df.to_csv(f'/Volumes/workspace/default/my_files/{new_file}', index=False)
        print(f"Generated {new_file} with {folder} {prev_rec:04d} to {dyn_rec - 1:04d}")
        prev_rec = dyn_rec
        next_num += 1
    for j in dbutils.fs.ls('/Volumes/workspace/default/my_files'):
        dbutils.fs.mv(f'/Volumes/workspace/default/my_files/{j.name}',f'{path}/{j.name}')
    display(dbutils.fs.ls(f'{path}'))
    return 'Finished Successfully'

# COMMAND ----------

print(fake_data('users', data=lambda i: {
                "user_id": f'U{str(i).zfill(4)}',
                "user_name": fake.name(),
                "country": random.choice(
                    ["India","USA","Japan"]
                ),
                "subscription_plan": random.choice(
                    ["Basic","Premium"]
                )
            }))

# COMMAND ----------

print(fake_data('content', data=lambda i: {
        "content_id": f'C{str(i).zfill(4)}',
        "title": fake.catch_phrase(),
        "genre": random.choice(genres),
        "language": random.choice(languages),
        "release_year": random.randint(2000, 2026)
    }))

# COMMAND ----------

user_count = get_count('users', 'user_id')
content_count = get_count('content', 'content_id')

print(fake_data('watch_events', data=lambda i: {
        "event_id": f"E{str(i).zfill(6)}",
        "user_id": f"U{str(random.randint(0, user_count - 1)).zfill(4)}",
        "content_id": f"C{str(random.randint(0, content_count - 1)).zfill(4)}",
        "watch_minutes": random.randint(1,180),
        "device_type": random.choice(["Mobile","TV","Laptop","Tablet"]),
        "event_timestamp": fake.date_time_between(start_date="-30d", end_date="now")
    }))

# COMMAND ----------

user_count = get_count('users', 'user_id')
content_count = get_count('content', 'content_id')

print(fake_data('ratings', data=lambda i: {
        "rating_id": f"R{str(i).zfill(6)}",
        "user_id": f"U{str(random.randint(0, user_count - 1)).zfill(4)}",
        "content_id": f"C{str(random.randint(0, content_count - 1)).zfill(4)}",
        "rating": random.randint(1,5),
        "rating_timestamp": fake.date_time_between(start_date="-30d", end_date="now")
    }))

# COMMAND ----------

print(fake_data('subscriptions', data=lambda i: {
        "subscription_id": f"S{str(i).zfill(5)}",
        "user_id": f"U{str(i).zfill(4)}",
        "plan": (p := random.choice(list(plans.keys()))),
        "monthly_fee": plans[p],
        "start_date": fake.date_between(start_date="-2y", end_date="today")
    }))