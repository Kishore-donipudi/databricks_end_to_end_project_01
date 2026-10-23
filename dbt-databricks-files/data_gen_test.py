# Databricks notebook source
# !pip install faker 

# COMMAND ----------

# %restart_python 

# COMMAND ----------

from faker import Faker
import pandas as pd
import random

fake = Faker()
def user_data():
    rows = []
    for i in range(1001):
        rows.append({
            "user_id": str(i).zfill(4),
            "user_name": fake.name(),
            "country": random.choice(
                ["India","USA","Japan"]
            ),
            "subscription_plan": random.choice(
                ["Basic","Premium"]
            )
        })
    df = pd.DataFrame(rows)
    return df.to_csv('/Volumes/workspace/default/my_files/users_002.csv',index=False)
user_data()

# COMMAND ----------

dbutils.fs.mkdirs('s3://de-prj/testing/')

# COMMAND ----------

dbutils.fs.mv('/Volumes/workspace/default/my_files/users_002.csv','s3://de-prj/testing/users_003.csv')
dbutils.fs.rm('s3://de-prj/users/',recurse=True)

# COMMAND ----------

na=dbutils.fs.ls('s3://de-prj/testing')
r_l=0
r=[100,12]
if r:
    for i in na:
        if 'users_' in i.name:
            r.append(int(''.join(char for char in i.name if char.isdigit())))
            r_l=max(r_l,len(r))
    if r_l > 0:
        print(r[-1])

# COMMAND ----------

files = dbutils.fs.ls("s3://de-prj/testing")
nums = []
for f in files:
    if 'users_' in f.name:
        nums.append(
            int(''.join(c for c in f.name if c.isdigit()))
        )
if nums:
    next_num = max(nums) + 1
else:
    next_num = 1

new_file = f"user_{next_num:03d}.csv"

print(new_file)
print(nums)

# COMMAND ----------

from faker import Faker
import pandas as pd
import random
fake = Faker()
def fake_data(folder,data):
folder='user'
dbutils.fs.mkdirs(f's3://de-prj/{folder}')
path=f's3://de-prj/{folder}'
files = dbutils.fs.ls(f"{path}")
nums = []
file_names = {}
for f in files:
    if 'user' in f.name and f.name.endswith('.csv'):
        digits = ''.join(c for c in f.name if c.isdigit())
        if digits:
            num = int(digits)
            nums.append(num)
            file_names[num] = f.name

if nums:
    last_num = max(nums)
    next_num = last_num + 1
    # Read the last file to find the last user_id generated
    last_file = file_names[last_num]
    prev_df = spark.read.csv(f"{path}/{last_file}", header=True).toPandas()
    prev_rec = int(prev_df['user_id'].astype(int).max()) + 1
else:
    next_num = 1
    prev_rec = 0

data={
            "user_id": str(i).zfill(4),
            "user_name": fake.name(),
            "country": random.choice(
                ["India","USA","Japan"]
            ),
            "subscription_plan": random.choice(
                ["Basic","Premium"]
            )
        }
# Generate 3 files in a loop, each with 100 records continuing the user_id sequence
num_files = 2
for _ in range(num_files):
    dyn_rec = prev_rec + 100
    new_file = f"user_{next_num:03d}.csv"
    rows = []
    for i in range(prev_rec, dyn_rec):
        rows.append(data)
    df = pd.DataFrame(rows)
    df.to_csv(f'/Volumes/workspace/default/my_files/{new_file}', index=False)
    print(f"Generated {new_file} with user_id {prev_rec:04d} to {dyn_rec - 1:04d}")
    prev_rec = dyn_rec
    next_num += 1
for i in dbutils.fs.ls('/Volumes/workspace/default/my_files'):
    dbutils.fs.mv(f'/Volumes/workspace/default/my_files/{i.name}',f'{path}/{i.name}')
display(dbutils.fs.ls(f'{path}'))

# COMMAND ----------

print(fake_data('user',data={
                "user_id": str(i).zfill(4),
                "user_name": fake.name(),
                "country": random.choice(
                    ["India","USA","Japan"]
                ),
                "subscription_plan": random.choice(
                    ["Basic","Premium"]
                )
            }))

# COMMAND ----------

data={"user_id": str(i).zfill(4),
                "user_name": fake.name(),
                "country": random.choice(
                    ["India","USA","Japan"]
                ),
                "subscription_plan": random.choice(
                    ["Basic","Premium"]
                )
            }
print(list(data.keys())[0])

# COMMAND ----------



# COMMAND ----------

dbutils.fs.ls('s3://de-prj/testing')

# COMMAND ----------

# MAGIC %sql
# MAGIC select current_catalog()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Testing Bronze and Silver Layers 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC update dbt_bmodel_project.bronze.bronze_users 
# MAGIC set user_name=initcap('kishore') where user_id='U0001'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dbt_bmodel_project.bronze.bronze_users where user_id in ('U0001','U0002','U0000') ;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dbt_bmodel_project.silver.users_track where user_id='U0001'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from dbt_bmodel_project.silver.silver_users 
# MAGIC where user_id='U0001'

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     user_id,
# MAGIC     subscription_id,
# MAGIC     start_date,
# MAGIC     updated_at,
# MAGIC     row_number() over(
# MAGIC         partition by user_id
# MAGIC         order by updated_at
# MAGIC     ) as rn
# MAGIC from dbt_bmodel_project.bronze.bronze_subscriptions
# MAGIC qualify rn > 1