import cv2
import os
import logging

logging.basicConfig(level=logging.INFO)

EXTENSION_LIST = ['.MOV', '.AVI', '.mov', '.avi']

def extract_pics_from_videos(path, pics_per_sec=3, video_ext_file=None, counter=0):
    """
    In the directory path, pics_per_sec pictures will be extracted from video file with extensions
    which end with any extension in EXTENSION_LIST, extension can be added with the exttension argument
    """
    dir_list = os.listdir(path)

    if 'pictures' in dir_list:
        return counter

    else:
        extension_list = EXTENSION_LIST
        if video_ext_file:
            extension_list.append(video_ext_file)

        freq_of_record = int(24 / pics_per_sec)
        saving_path = os.path.join(path, 'pictures')

        try:
            os.mkdir(saving_path)
        except:
            pass

        i = 0

        for name in dir_list:
            is_video_file = False
            for ext in EXTENSION_LIST:
                is_video_file = is_video_file or name.endswith(ext)
            if is_video_file:
                cap = cv2.VideoCapture(os.path.join(path, name))
                while(cap.isOpened()):
                    ret, frame = cap.read()

                    if i % freq_of_record == 0:
                        try:
                            cv2.imwrite(f'{saving_path}/{name}_{i}.jpg', frame)
                            counter += 1
                        except:
                            break
                    i += 1
                cap.release()
                cv2.destroyAllWindows()

        if not os.listdir(saving_path):
            os.rmdir(saving_path)

        return counter

def get_all_path(path):
    sub_path_list = list()
    directories = os.listdir(path)
    for element in directories:
        sub_path = os.path.join(path, element)
        if os.path.isdir(sub_path):
            sub_path_list.append(sub_path)

    if sub_path_list:
        result = list(sub_path_list)
        for sub_path in sub_path_list:
            result.extend(list(get_all_path(sub_path)))
        return result
    else:
        return [path]

def extract_pics_from_videos_from_all_dir(pics_per_sec=3, video_ext_file=None):

    path = input("please enter the path: ")

    all_path = list(set(get_all_path(path)))

    counter = 0

    for p in all_path:
        logging.info(f'{counter} pictures extracted')
        counter += extract_pics_from_videos(p, pics_per_sec=3, video_ext_file=None)
        logging.info(f'{counter} pictures extracted since script started')

    logging.info(f'Total: {counter} pictures extracted')

    return None

if __name__ == "__main__":
    """
    In the 'path' given in input, all the sub path will be found recursively.
    Then in each path and sub path, the script will check if there are video files,
    if so, it will extract pictures from the video files and save them in a picture
    directory that will be created except if a 'pictues' folder already exists.
    """
    extract_pics_from_videos_from_all_dir()
