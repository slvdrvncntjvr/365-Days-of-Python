from PIL import Image
import os

ascii_characters = "@%#*+=-:. "

def adjust_image_size(image, width=100):
    img_width, img_height = image.size
    aspect_ratio = img_height / img_width
    adjusted_height = int(width * aspect_ratio * 0.55)
    return image.resize((width, adjusted_height))

def convert_to_gray(image):
    return image.convert("L")

def map_pixels_to_characters(image):
    pixel_values = image.getdata()
    ascii_result = "".join(ascii_characters[pixel // 25] for pixel in pixel_values)
    return ascii_result

def create_ascii_art(image_path, width=100):
    try:
        image = Image.open(image_path)
    except Exception as error:
        print(f"Error: Unable to open the image file. {error}")
        return None

    resized_image = adjust_image_size(image, width)
    gray_image = convert_to_gray(resized_image)
    ascii_data = map_pixels_to_characters(gray_image)
    image_width = gray_image.width
    formatted_ascii_art = "\n".join(
        ascii_data[i:i + image_width] for i in range(0, len(ascii_data), image_width)
    )
    return formatted_ascii_art

def main():
    image_path = input("Enter the path to the image file: ").strip()

    if not os.path.exists(image_path):
        print("Error: File not found! Please check the path and try again.")
        return

    try:
        desired_width = int(input("Enter the width for the ASCII art (default: 100): ") or 100)
    except ValueError:
        print("Invalid input. Default width of 100 will be used.")
        desired_width = 100

    ascii_art = create_ascii_art(image_path, desired_width)

    if ascii_art:
        print("\nHere is your ASCII art:\n")
        print(ascii_art)

        output_file = os.path.join(os.path.dirname(__file__), "ascii_art.txt")
        with open(output_file, "w") as file:
            file.write(ascii_art)
        print(f"\nASCII art has been saved to '{output_file}'.")

if __name__ == "__main__":
    main()
