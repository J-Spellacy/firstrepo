from PIL import Image
import numpy as np




# loop over heights and at each row loop over the row first from the left then the right
# make the pixel transparent until the pixel value changes then move on
def remove_background(img, top_bottom = False):
    img = img.convert('RGBA') # allows for transparency
    img_new = img.copy()
    img_check = Image.new('RGBA', img.size, (255, 255, 255, 255))
    pixels = img.load()
    pixels_new = img_new.load()
    pixels_check = img_check.load()    
    for y in range(img.height):
        for x in range(img.width):
            if x == 0:
                pixels_new[x, y] = (0, 0, 255, 0)
            elif pixels[x, y] == pixels[x-1, y]:
                pixels_new[x, y] = (0, 0, 255, 0)
            else:
                pixels_new[x, y] = (0, 0, 255, 0)
                # pixels_check[x, y] = pixels[x, y]
                break
        for x in range(img.width):
            if x == 0 or x == 1:
                pixels_new[img.width-(x+1), y] = (0, 0, 255, 0)
            elif pixels[img.width - x, y] == pixels[img.width-(x+1), y]:
                pixels_new[img.width - x, y] = (0, 0, 255, 0)
            else:
                pixels_new[img.width - x, y] = (0, 0, 255, 0)
                # pixels_check[img.width - x, y] = pixels[x, y]
                break
    if top_bottom:
        for x in range(img.width):
            for y in range(img.height):
                if y == 0:
                    pixels_new[x, y] = (0, 0, 255, 0)
                elif pixels[x, y] == pixels[x, y-1]:
                    pixels_new[x, y] = (0, 0, 255, 0)
                else:
                    pixels_new[x, y] = (0, 0, 255, 0)
                    # pixels_check[x, y] = pixels[x, y]
                    break
            for y in range(img.height):
                if y == 0 or y == 1:
                    pixels_new[x, img.height - (y+1)] = (0, 0, 255, 0)
                elif pixels[x,img.height - y] == pixels[x, img.height - (y+1)]:
                    pixels_new[x, img.height - y] = (0, 0, 255, 0)
                else:
                    pixels_new[x, img.height - y] = (0, 0, 255, 0)
                    # pixels_check[img.width - x, y] = pixels[x, y]
                    break

    return img_new, img_check

if __name__ == '__main__':
    img = Image.open(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\knight.png")
    img_new, img_check = remove_background(img, top_bottom = True)
    img.show()
    img_new.show()
    img_new.save(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\knight_no_bg.png")
    