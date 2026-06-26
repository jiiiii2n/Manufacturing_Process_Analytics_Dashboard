import os

for root, dirs, files in os.walk("C:/Users/jiwon/Manufacturing_Process_Analytics_Dashboard"):
    if ".git" in dirs:
        print(root)