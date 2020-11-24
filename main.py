import cv2
import numpy as np
from scipy import stats
import math
import argparse

def reduce(x, y, blk_size, pixel_skip_x, pixel_skip_y, img, func):

    width = img.shape[1]
    height = img.shape[0]

    start_x = x * blk_size + pixel_skip_x
    end_x = x * blk_size + blk_size + pixel_skip_x 

    start_y = y * blk_size + pixel_skip_y
    end_y = y * blk_size + blk_size + pixel_skip_y 

    reduction_x = end_x - height
    reduced_blk_x = blk_size - reduction_x
    reduced_x_end = x * blk_size + reduced_blk_x + pixel_skip_x 

    reduction_y = end_y - width
    reduced_blk_y = blk_size - reduction_y
    reduced_y_end = y * blk_size + reduced_blk_y + pixel_skip_y 

    #if(var_blk == 0):
    if(blk_size == 1):
        return img[start_x,start_y]

    if( end_x > height and end_y > width):
        #when image exceeds limit of width and height
        bloco = img[start_x:reduced_x_end,start_y:reduced_y_end]

        if func == "mode":
            result = stats.mode(bloco, axis = None)
            return result[0]
        elif func == "mean":
            new_pixel = round(np.mean(bloco))
            return new_pixel
        elif func == "median":
            b = bloco.copy
            b = np.squeeze(np.asarray(b))
            return np.median(b, axis=None, overwrite_input=True)

    elif(end_x > height):
        #when image exceeds limit of height
        bloco = img[start_x:reduced_x_end,start_y:end_y]
        if func == "mode":
            result = stats.mode(bloco, axis = None)
            return result[0]
        elif func == "mean":
            new_pixel = round(np.mean(bloco))
            return new_pixel
        elif func == "median":
            b = bloco.copy()
            b = np.squeeze(np.asarray(b))
            return np.median(b, axis=None, overwrite_input=True)

    elif(end_y > width):
        #when image exceeds limit of width
        bloco = img[start_x:end_x,start_y:reduced_y_end]
        if func == "mode":
            result = stats.mode(bloco, axis = None)
            return result[0]
        elif func == "mean":
            new_pixel = round(np.mean(bloco))
            return new_pixel
        elif func == "median":
            b = bloco.copy()
            b = np.squeeze(np.asarray(b))
            return np.median(b, axis=None, overwrite_input=True)

    else:
        #when both width and height are within image parameters
        bloco = img[start_x:end_x,start_y:end_y]
        if func == "mode":
            result = stats.mode(bloco, axis = None)
            return result[0]
        elif func == "mean":
            new_pixel = round(np.mean(bloco))
            return new_pixel
            #return np.mean(img[start_x:end_x,start_y:end_y],dtype='uint8')
        elif func == "median":
            b = bloco.copy()
            b = np.squeeze(np.asarray(b))
            return np.median(b, axis=None, overwrite_input=True)

        
def run():

    parser = argparse.ArgumentParser()

    parser.add_argument('img', type=str)
    parser.add_argument('mode', type=str)
    parser.add_argument('reduction', type=float)

    args = parser.parse_args()

    input_image = cv2.imread(args.img,0)
    reduction = args.reduction
    func = args.mode

    input_width = input_image.shape[1]
    input_height = input_image.shape[0]

    reduce_size = (input_width - input_width * reduction)

    if (input_width - input_width * reduction < 1 or input_height - input_height * reduction < 1):
        print('Cannot apply reduction because one dimension would be smaller than 1 pixel!')
        return
    
    if (reduction >= 1):
        print('Upsampling not allowed!')
        return
  
    blk_size =  input_width / reduce_size
    blk_decimal = blk_size - int(blk_size)
    blk_size = int(blk_size)

    pixel_skip_x = 0
    remainder_x = 0
    pixel_skip_y = 0
    remainder_y = 0

    output_width = round(input_width - input_width * reduction)
    output_height = round(input_height - input_height * reduction)

    new_img = np.zeros((output_height,output_width), dtype='uint8')
   
    for x in range(0, output_height, 1):
        pixel_skip_y = 0
        remainder_y = 0
        if( remainder_x > 1):
                pixel_skip_x += 1
                remainder_x = remainder_x - int(remainder_x)
        remainder_x += blk_decimal
        for y in range(0, output_width, 1):
            if( remainder_y > 1):
                pixel_skip_y += 1
                remainder_y = remainder_y - int(remainder_y)
            remainder_y += blk_decimal
            new_img[x,y] = reduce(x, y, blk_size, pixel_skip_x, pixel_skip_y, input_image, func)

    cv2.imshow('img', new_img)
    cv2.imwrite(f'output_{func}_{reduction}.png', new_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
