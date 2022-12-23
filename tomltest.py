import tomllib

print ("toml test")

with open("config/config.ini", mode="rb") as fp:
    tomllib.load(fp)