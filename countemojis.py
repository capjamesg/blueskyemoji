import subprocess
import json
import emoji
import os
import datetime
import shutil

last_saved = datetime.datetime.now()

emojis = {}

# directory should be equal to highest date YYYY-MM-DD in .

dates = []

for file in os.listdir("."):
    # if filename is YYYY-MM-DD
    if len(file) == 10 and file[4] == "-" and file[7] == "-":
        dates.append(file)

directory = max(dates)

try:
    while True:
        if len(os.listdir(directory)) < 2:
            continue

        output = subprocess.Popen(["psychonaut", "repos-firehose-replay", "."], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in output.stdout:
            try:
                data = json.loads(line)
            except:
                continue

            if data.get("first_block_msg") and data["first_block_msg"].get("$type"):
                # print(data["first_block_msg"]["$type"])
                if data["first_block_msg"]["$type"] == "app.bsky.feed.post":
                    post_content = data["first_block_msg"]["text"]

                    for char in post_content:
                        if emoji.is_emoji(char):
                            emojis[char] = emojis.get(char, 0) + 1

        # delete the oldest file
        # when command finished
        output.wait()
        # order emojis by count
        emojis = {k: v for k, v in sorted(emojis.items(), key=lambda item: item[1], reverse=True)}

        # move all files but most recent out of directory
        for file in os.listdir(directory):
            if file != max(os.listdir(directory)):
                shutil.move(os.path.join(directory, file), os.path.join("emojis/data", file))

        # save every 2 mins
        if datetime.datetime.now() - last_saved > datetime.timedelta(seconds=10):
            with open(f"emojis/data/emojis {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.json", "w+") as emoji_file:
                json.dump(emojis, emoji_file)
                print("saved")

            last_saved = datetime.datetime.now()

except KeyboardInterrupt:
    with open(f"emojis {datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')}.json", "w+") as emoji_file:
        json.dump(emojis, emoji_file)