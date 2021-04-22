# automation.py
import os
from shutil import move
# directory
pathsuser = os.getenv('USER')
root_dir = '/home/kanishk/Music'.format(user)
image_dir = '/home/kanishk/Music/Jetha-AI-Screenshots'.format(user)
others_dir = '/home/kanishk/Music/{}'.format(ch)
software_dir = '/home/kanishk/Music/{}'.format(ch)
# category wise file types

#doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx')
img_types = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif', '.tiff')
software_types = ('.exe', '.pkg', '.dmg','.py','.txt','.h5','.pkl')
def get_non_hidden_files_except_current_file(root_dir):
      return [f for f in os.listdir(root_dir) if os.path.isfile(f) and not f.startswith('.') and not f.__eq__(__file__)]
def move_files(files):
    for file in files:
        # file moved and overwritten if already exists
        if file.endswith(img_types):
            move(file, '{}/{}'.format(image_dir, file))
            print('file {} moved to {}'.format(file, image_dir))
        elif file.endswith(software_types):
            move(file, '{}/{}'.format(software_dir, file))
            print('file {} moved to {}'.format(file, others_dir))
        else:
            move(file, '{}/{}'.format(others_dir, file))
            print('file {} moved to {}'.format(file, others_dir))

if __name__ == "__main__":
    ch = input('Enter directory name : ')
    files = get_non_hidden_files_except_current_file(root_dir)
    move_files(files)
