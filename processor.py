from PIL import Image
from img import print_to_wall
from removal import remove_bg


def process_image(filepath, id):
    cleared_path = "files/work_cleared_" + id.__str__() + ".png"
    on_wall_path = "files/work_on_wall_" + id.__str__() + ".jpg"
    remove_bg(filepath, cleared_path)
    print_to_wall(cleared_path, on_wall_path)
    return on_wall_path
