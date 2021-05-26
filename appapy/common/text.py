 def find_and_replace(path: str, find: str, replace:str):
     
    lines = []
    try:
        with open(path, mode="r", encoding="utf-8") as fs:
            for line in fs:
                line = line.replace(find, replace)

                lines.append(line)

        with open(path, mode="w") as fs:
            fs.write("".join(lines))
    except UnicodeError as ue:
        pass