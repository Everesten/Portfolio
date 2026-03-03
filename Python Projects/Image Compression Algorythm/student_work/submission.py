import helper_library as help

def block_average(grid, x, y, width, height):

    rgbAvg = [0, 0, 0]
    count = 0  

    for i in range(y, y + height):
        for j in range(x, x + width):
            r, g, b = grid[i][j]

            rgbAvg[0] += r
            rgbAvg[1] += g
            rgbAvg[2] += b
            count += 1

    rgbAvg[0]//=count
    rgbAvg[1]//=count
    rgbAvg[2]//=count

    return rgbAvg

def create_compressed_block(avg_color,width,height):

    compressed_block = []
    row = []

    for x in range(width):
        for y in range(height):
            row.append(avg_color)
        compressed_block.append(row)
        row = []
    
    return compressed_block

def merge_lists(lst1,lst2):

    combinedList = []

    for i in range(len(lst1)):
        combinedList.append(lst1[i] + lst2[i])

    return combinedList

def compress_image(grid,x,y,width,height,threshold):

    if width <= threshold or height <= threshold:
        avg_color = block_average(grid, x, y, width, height)
        compressed = create_compressed_block(avg_color,width,height)
        return compressed

    q1 = compress_image(grid,x,y,width//2,height//2,threshold)
    q2 = compress_image(grid,x+(width//2),y,width//2,height//2,threshold)
    q3 = compress_image(grid,x,y+(height//2),width//2,height//2,threshold)
    q4 = compress_image(grid,x+(width//2),y+(height//2),width//2,height//2,threshold)

    totalCompressedImage = merge_lists(q1, q2) + merge_lists(q3, q4)

    return totalCompressedImage

if __name__ == "__main__":
    imageFile = input("FILE>")
    threshold = int(input("THRESHOLD>"))

    inputGrid = help.image_to_list(imageFile)
    compressedImage = compress_image(inputGrid, 0, 0, len(inputGrid[0]), len(inputGrid), threshold)
    
    print(f"OUTPUT Width: {len(inputGrid[0])}")
    print(f"OUTPUT Height: {len(inputGrid)}")
    print(f"OUTPUT Threshold: {threshold}")

    help.output_image(compressedImage, "compressed_" + imageFile)
