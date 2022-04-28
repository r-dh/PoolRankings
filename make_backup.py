import time
import os


today = time.strftime("%Y_%m_%d")
os.system(f"cp data.json backup/data_{today}.json")
os.system(f"cp history.json backup/history_{today}.json")

os.system(f"python visualise.py")

