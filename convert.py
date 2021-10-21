import json
import os
import sys


def main(args):
    json_file_path = args[1]
    images_folder_path = args[2]

    user_input = input(f"json 檔案路徑: {json_file_path}, 相片資料夾路徑: {images_folder_path}, 這樣正確嗎? (y/n): ")

    if user_input is not "y":
        print("程式已終止")
        return

    total_count = 0

    with open(json_file_path) as f:
        data = json.load(f)

    for image_name in data["frames"]:
        total_count += 1
        converted_lines = []

        for box in data["frames"][image_name]:
            width = box["width"]
            height = box["height"]

            x1 = max(0, box["x1"])
            x2 = min(box["x2"], width)
            y1 = max(0, box["y1"])
            y2 = min(box["y2"], height)

            center_x_to_width = ((x1 + x2) / 2) / width
            center_y_to_height = ((y1 + y2) / 2) / height
            frame_width_to_image_width = (x2 - x1) / width
            frame_height_to_image_height = (y2 - y1) / height

            converted_lines.append(
                f"0 {round(center_x_to_width, 6)} {round(center_y_to_height, 6)} {round(frame_width_to_image_width, 6)} {round(frame_height_to_image_height, 6)}"
            )

        image_name_without_file_type = os.path.splitext(image_name)[0]

        with open(f"{images_folder_path}/{image_name_without_file_type}.txt", "w") as output_file:

            for line in converted_lines:
                output_file.write(f"{line}\n")

            print(f"{image_name_without_file_type} 轉換成功")

    print("")
    print(f"全數文件皆已轉換完畢，一共 {total_count} 張")
    print("")


if __name__ == '__main__':
    main(sys.argv)
