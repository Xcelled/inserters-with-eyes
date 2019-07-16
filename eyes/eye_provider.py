from PIL import Image
import os
import re

hand_re = re.compile(r'hr.+inserter-hand-(open|closed)')
remnants_re = re.compile(r'hr.+inserter-remnants')
fn = 'copy_images_here'
eye_size = lambda x,y: (x, y, x+24, y+48)
eye_rem_size = lambda x,y: (x, y, x+11, y+11)

hand_eye_pos = [
    (0 ,25), 
    (48,25),
]
hand_stack_eye_pos_open = [
    (20, 40),
    (83, 40),
]
hand_stack_eye_pos_closed = [
    (5, 40),
    (68, 40),
]
rem_eye_pos = [
    (57, 9),
    (35, 28),
    (54, 94),
    (31, 111),
    (54, 171),
    (27, 166),
]

def add_stack_hand_eyes(path, file):
    global hr_count, lr_count
    fullpath = os.path.join(path, file)
    # 100x164 closed, 130x164 open
    img = Image.open(fullpath)
    x,y = img.size
    if x != 100 and x != 130:
        print(f'WARNING: Matching file name {fullpath} with different dims {img.size} rather than (100, 164)/(130, 164)(stack inserter), skipping')
        return
    closed = (x == 100)
    for x,y in hand_stack_eye_pos_closed if closed else hand_stack_eye_pos_open:
        img.paste(eye, eye_size(x, y), eye)
    img.save(fullpath)
    print(f'Processed: {fullpath}')
    hr_count += 1
    if file.startswith('hr-'):
        lr_name = file.replace('hr-', '')
        if closed:
            lr_img = img.resize((24, 41), Image.BOX)
        else:
            lr_img = img.resize((32, 41), Image.BOX)
        lr_img.save(os.path.join(path, lr_name))
        print(f'Added low-res: {os.path.join(path, lr_name)}')
        lr_count += 1
    print()

def add_hand_eyes(path, file):
    global hr_count, lr_count
    fullpath = os.path.join(path, file)
    # 72x164
    img = Image.open(fullpath)
    if img.size != (72, 164):
        print(f'WARNING: Matching file name {fullpath} with different dims {img.size} rather than (72, 164), skipping')
        return
    for x,y in hand_eye_pos:
        img.paste(eye, eye_size(x, y), eye)
    img.save(fullpath)
    print(f'Processed: {fullpath}')
    hr_count += 1
    if file.startswith('hr-'):
        lr_name = file.replace('hr-', '')
        lr_img = img.resize((18, 41), Image.BOX)
        lr_img.save(os.path.join(path, lr_name))
        print(f'Added low-res: {os.path.join(path, lr_name)}')
        lr_count += 1
    print()

def add_rem_eyes(path, file):
    global hr_count, lr_count
    fullpath = os.path.join(path, file)
    # 102x240
    img = Image.open(fullpath)
    if img.size != (102, 240):
        print(f'WARNING: Matching file name {fullpath} with different dims {img.size} rather than (72, 164), skipping')
        return
    for x,y in rem_eye_pos:
        img.paste(eye_rem, eye_rem_size(x, y), eye_rem)
    img.save(fullpath)
    print(f'Processed: {fullpath}')
    hr_count += 1
    if file.startswith('hr-'):
        lr_name = file.replace('hr-', '')
        lr_img = img.resize((52, 126), Image.BOX)
        lr_img.save(os.path.join(path, lr_name))
        print(f'Low-res: {os.path.join(path, lr_name)}')
        lr_count += 1
    print()

eye = Image.open('eye.png')
eye_rem = Image.open('eye_remnant.png')

hr_count = 0
lr_count = 0

def cmp(a, b):
    for i in a:
        if i in b:
            return True

if not os.path.exists(fn):
    os.mkdir(fn)

for dirpath, dirnames, filenames in os.walk(fn):
    for file in filenames:
        m = hand_re.match(file)
        if m:
            if cmp(['-stack-', '-big-', '-stripe-'], file):
                add_stack_hand_eyes(dirpath, file)
            else:
                add_hand_eyes(dirpath, file)
        m = remnants_re.match(file)
        if m:
            add_rem_eyes(dirpath, file)
print(f'High-res files processed: {hr_count}')
print(f'Low-res files added from HR: {lr_count}')
print(f'Total: {hr_count+lr_count}')
