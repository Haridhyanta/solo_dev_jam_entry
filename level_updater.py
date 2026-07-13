import os


def update(file_path: str, new_level_no: int):
    total_no_of_levels = 1
    while True:
        if not os.path.exists(f'./levels/level_{total_no_of_levels+1}.json'):
            break
        total_no_of_levels += 1

    i = total_no_of_levels

    while i >= new_level_no:
        f_original = open(f'./levels/level_{i}.json', 'r')
        f_new = open(f'./levels/level_{i+1}.json', 'w')
        text = f_original.read().replace(f"\"name\": \"Level {i}", f"\"name\": \"Level {i+1}")
        f_new.write(text)
        f_original.close()
        f_new.close()
        i -= 1
    
    f_original = open(file_path, 'r')
    f_new = open(f'./levels/level_{new_level_no}.json', 'w')
    text = f_original.read().replace(f"\"name\": \"Level {i}", f"\"name\": \"Level {i+1}")
    f_new.write(text)
    f_original.close()
    f_new.close()

    os.remove(path=file_path)

update('.\\levels\\level_6 copy.json', 7)
