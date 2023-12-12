# Name: Finnley Howald
# Student ID: 261099492


def get_length_of_compressed(row):
    ''' list<str> -> int
    Returns the length of the row, row of a compressed pgm file, image.
    
    >>> get_length_of_compressed(['1x1'])
    1
    >>> get_length_of_compressed(['1x10'])
    10
    >>> get_length_of_compressed(['1x10', '1x4'])
    14
    '''
    row_length = 0
    for ele in row:
        b = int(ele.split('x')[1])
        row_length += b
    
    return row_length

def is_valid_image(image):
    ''' (list<list>) -> bool
    Returns True if the list of lists of strings that is the image is
    valid pgm format.
    
    >>> is_valid_image([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    True
    >>> is_valid_image([[0],[0, 1]])
    False
    >>> is_valid_image([[0]])
    True
    >>> is_valid_image([['0']])
    False
    '''
    if image == [[]] or image == []:
        return False
    
    row_length = len(image[0])
    
    for row in image:
        if len(row) != row_length:
            return False
        
        for ele in row:
            if type(ele) != int or ele < 0 or ele > 255:
                return False
            
    return True


def is_valid_compressed_image(image):
    ''' (list<list>) -> bool
    Returns True if the list of lists of strings that is the image is
    valid compressed pgm format.
    
    >>> is_valid_compressed_image([["0x5", "200x2"], ["111x7"]])
    True
    >>> is_valid_compressed_image([["0x5", "200x2"], ["111x2"]])
    False
    >>> is_valid_compressed_image([["0x5", "200x2"], [111, 111, 111, 111, 111, 111, 111]])
    False
    '''
    if image == [[]] or image == []:
        return False
    
    for row in image:
        
        for ele in row:
            if type(ele) != str or 'x' not in str(ele):
                return False
            
            split = ele.split('x')
            
            if len(split) != 2:
                return False
            
            a = split[0]
            b = split[1]
            
            if not (a.isdecimal() and b.isdecimal()):
                return False
            
            if int(a) < 0 or int(a) > 255 or int(b) < 0:
                return False
            
        if get_length_of_compressed(image[0]) != get_length_of_compressed(row):
            return False
        
    return True
    

def load_regular_image(filename):
    ''' (str) -> list<list<int>>
    Returns the contents of a pgm file that is named filename as a
    matrix of ints.
    
    >>> save_image([[1,2,3],[1,2,3]], 'ds.pgm')
    >>> load_regular_image('ds.pgm')
    [[1, 2, 3], [1, 2, 3]]
    >>> save_image([[1,2,3]], 'ds.pgm')
    >>> load_regular_image('ds.pgm')
    [[1, 2, 3]]
    >>> save_image([[1]], 'ds.pgm')
    >>> load_regular_image('ds.pgm')
    [[1]]
    >>> save_image([[1,2]], 'ds.pgm')
    >>> fobj = open('ds.pgm', 'w')
    >>> fobj.write('1')
    1
    >>> fobj.close()
    >>> load_regular_image('ds.pgm')
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    fobj = open(filename, 'r')
    image = fobj.read()
    fobj.close()
    
    image = image.split('\n')
    
    if image[0] != "P2" or len(image) < 4 or image[2] != '255':
        raise AssertionError('Image is not in PGM format')
    
    row_2_split = image[1].split()
    header_width = int(row_2_split[0])
    header_height = int(row_2_split[1])
    image = image[3:-1]

    for row in range(len(image)):
        
        image[row] = image[row].split()
        
        for ele_i in range(len(image[row])):
            
            if not image[row][ele_i].isdecimal():
                raise AssertionError('Image is not in PGM format')
            
            image[row][ele_i] = int(image[row][ele_i])

    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    if header_height != len(image) or header_width != len(image[0]):
        raise AssertionError('Image is not in PGM format')
    
    return image


def load_compressed_image(filename):
    ''' (str) -> list<list<str>>
    Returns the contents of a compressed pgm file that is
    named filename as a list of lists of str.

    >>> save_image([['1x1'],['1x1']], 'ds.pgm.compressed')
    >>> load_compressed_image('ds.pgm.compressed')
    [['1x1'], ['1x1']]
    >>> save_image([['1x1', '1x1'],['1x2']], 'ds.pgm.compressed')
    >>> load_compressed_image('ds.pgm.compressed')
    [['1x1', '1x1'], ['1x2']]
    >>> save_image([['1x1', '1x1'],['1x1', '1x1']], 'ds.pgm.compressed')
    >>> load_compressed_image('ds.pgm.compressed')
    [['1x1', '1x1'], ['1x1', '1x1']]
    >>> save_image([['1x1'],['1x1']], 'ds.pgm.compressed')
    >>> fobj = open('ds.pgm.compressed', 'w')
    >>> fobj.write('1x3')
    3
    >>> load_compressed_image('ds.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    image = []
    fobj = open(filename, 'r')
    
    for line in fobj:
        image.append(line.split())
        
    fobj.close()

    if len(image) < 3:
        raise AssertionError('Image is not in PGM format')
    
    header_width = int(image[1][0])
    header_height = int(image[1][1])
    
    if not is_valid_compressed_image(image[3:]):
        raise AssertionError('Image is not in PGM format')
        
    row_length = get_length_of_compressed(image[3])
    
    if image[0] != ['P2C'] or header_width != row_length or header_height != len(image[3:]):
        raise AssertionError('Image is not in PGM format')
    
    return image[3:]


def load_image(filename):
    ''' (str) -> list<list>
    Returns the contents of a pgm or compressed pgm file that is
    named filename depending on the type of file.
    
    >>> save_image([[1,2,3]], 'ds.pgm')
    >>> load_image('ds.pgm')
    [[1, 2, 3]]
    >>> save_image([[1]], 'ds.pgm')
    >>> load_image('ds.pgm')
    [[1]]
    >>> save_image([['1x1'],['1x1']], 'ds.pgm.compressed')
    >>> load_image('ds.pgm.compressed')
    [['1x1'], ['1x1']]
    >>> save_image([['1x1'],['1x1']], 'ds.pgm.compressed')
    >>> fobj = open('ds.pgm.compressed', 'w')
    >>> fobj.write('1x3')
    3
    >>> load_image('ds.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    fobj = open(filename, 'r')
    firstline = fobj.read()
    fobj.close()
    
    if firstline[0:3] == 'P2C':
        return load_compressed_image(filename)
    elif firstline[0:2] == 'P2':
        return load_regular_image(filename)
    else:
        raise AssertionError('Image is not in PGM format')


def save_regular_image(image, filename):
    ''' (list<list<int>>, str) -> NoneType
    Returns void, writes the matrix image of a pgm file onto a file with
    filename of filename.
    
    >>> image = [[0]*10, [255]*10, [0]*10]
    >>> save_regular_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    >>> image = [[0]*3, [255]*3]
    >>> save_regular_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    >>> image = [[0]*2, [255]*2]
    >>> save_regular_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    >>> image = [[0]*5, [255]*6]
    >>> save_regular_image(image, "test.pgm")
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    fobj = open(filename, 'w')
    fobj.write('P2\n')
    fobj.write(str(len(image[0])) + ' ' + str(len(image)) + '\n')
    fobj.write('255\n')
    
    for row in image:
        row_string = ''
        
        for ele in row:
            row_string += str(ele) + ' '
        
        row_string = row_string[:-1]
        fobj.write(row_string + '\n')
    
    
    fobj.close()


def save_compressed_image(image, filename):
    ''' (list<list<int>>, str) -> NoneType
    Returns void, writes the matrix image of a compressed pgm file
    onto a file with filename of filename.
    
    >>> image = [["0x5", "200x2"], ["111x7"]]
    >>> save_compressed_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    >>> image = [["0x3", "200x1"], ["111x4"]]
    >>> save_compressed_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    >>> image = [["0x2", "200x1"], ["111x3"]]
    >>> save_compressed_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    >>> image = [["0x2", "200x1"], ["111x2"]]
    >>> save_compressed_image(image, "test.pgm")
    Traceback (most recent call last):
    AssertionError: Image is not in compressed PGM format
    '''
    if not is_valid_compressed_image(image):
        raise AssertionError('Image is not in compressed PGM format')

    row_length = get_length_of_compressed(image[0])
    
    fobj = open(filename, 'w')
    fobj.write('P2C\n')
    fobj.write(str(row_length) + ' ' + str(len(image)) + '\n')
    fobj.write('255\n')
    
    for row in image:
        row_string = ''
        
        for ele in row:
            row_string += ele + ' '
        
        row_string = row_string[:-1]
        fobj.write(row_string + '\n')
    
    fobj.close()


def save_image(image, filename):
    ''' (list<list>, str) -> NoneType
    Returns void, writes the matrix image of a pgm file or a compressed pgm
    file onto a file with filename of filename.
    
    >>> image = [["0x3", "200x1"], ["111x4"]]
    >>> save_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    >>> image = [["0x2", "200x1"], ["111x3"]]
    >>> save_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    >>> image = [[0]*3, [255]*3]
    >>> save_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    >>> image = [[0]*5, [255]*6]
    >>> save_image(image, "test.pgm")
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if is_valid_image(image):
        save_regular_image(image, filename)
    elif is_valid_compressed_image(image):
        save_compressed_image(image, filename)
    else:
        raise AssertionError('Image is not in PGM format')


def invert(image):
    ''' (list<list<int>>) -> list<list<int>>
    Returns an inverted matrix of the image image.

    >>> invert([[0, 100, 150], [200, 200, 200], [255, 255, 255]]
)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    >>> invert([[0, 12], [22, 213]]
)
    [[255, 243], [233, 42]]
    >>> invert([[0, 12], [22, 213], [1, 255]]
)
    [[255, 243], [233, 42], [254, 0]]
    >>> invert([[0, 12], [22, 213], [255]]
)
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    inverted = []
    
    for row in image:
        new_row = []
        for ele in row:
            new_row.append(255 - ele)
        inverted.append(new_row)
    
    return inverted     
        
        
def flip_horizontal(image):        
    ''' (list<list<int>>) -> list<list<int>>
    Returns a horizontally flipped matrix of the image image.
    
    >>> flip_horizontal([[0, 100, 150], [200, 200, 200], [255, 255, 255]]
)
    [[150, 100, 0], [200, 200, 200], [255, 255, 255]]
    >>> flip_horizontal([[0, 12], [22, 213]])
    [[12, 0], [213, 22]]
    >>> flip_horizontal([[0, 12], [22, 213], [1, 255]]
)
    [[12, 0], [213, 22], [255, 1]]
    >>> flip_horizontal([[0, 12], [22, 213], [255]]
)
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    flipped = []
    
    for row in image:
        new_row = []
        for ele in row:
            new_row.append(ele)
        flipped.append(new_row[::-1])
    
    return flipped    


def flip_vertical(image):   
    ''' (list<list<int>>) -> list<list<int>>
    Returns a vertically flipped matrix of the image image.
    
    >>> flip_vertical([[0, 100, 150], [200, 200, 200], [255, 255, 255]]
)
    [[255, 255, 255], [200, 200, 200], [0, 100, 150]]
    >>> flip_vertical([[0, 12], [22, 213]])
    [[22, 213], [0, 12]]
    >>> flip_vertical([[0, 12], [22, 213], [1, 255]]
)
    [[1, 255], [22, 213], [0, 12]]
    >>> flip_vertical([[0, 12], [22, 213], [255]]
)
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    return image[::-1]
    
        
def crop(image, tl_row, tl_col, n_rows, n_cols):
    ''' (list<list<int>>, int, int, int, int) -> list<list<int>>
    Returns a cropped matrix from image. The crop starts at the
    coordinates (tl_col, tl_row) and has n_rows number of rows
    and n_cols number of columns.

    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2)
    [[6, 6], [6, 7]]
    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 0, 0, 2, 2)
    [[5, 5], [5, 6]]
    >>> crop([[5, 5, 5, 8], [5, 6, 6, 8], [6, 6, 7, 8]], 2, 1, 1, 1)
    [[6]]
    >>> crop([[5, 5, 5, 8], [5, 6, 6, 8], [6, 6, 7]], 2, 1, 1, 1)
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    cropped = []
    
    for row_i in range(tl_row, tl_row + n_rows):
        new_row = []
        for ele_i in range(tl_col, tl_col + n_cols):
            new_row.append(image[row_i][ele_i])
        
        cropped.append(new_row)
    
    return cropped    


def find_end_of_repetition(list, start, target):
    ''' (list<int>, int, int) -> int
    Returns the end index of when the int target stops repeating in the
    list list. The start index is start.

    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 2, 5)
    4
    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 1, 3)
    1
    >>> find_end_of_repetition([0,0,0,0,0], 0, 0)
    4
    '''
    last_i = start
    
    for i in range(start + 1, len(list)):
        if list[i] != target:
            return last_i
        
        last_i += 1
            
    return last_i


def compress(image):
    ''' (list<list<int>>) -> list<list<str>>

    Returns a compressed png file that is a compressed version
    of the png matrix image.
    
    >>> compress([[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]])
    [['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']]
    >>> compress([[11, 11], [1, 5]])
    [['11x2'], ['1x1', '5x1']]
    >>> compress([[11, 11, 2], [1, 2, 5]])
    [['11x2', '2x1'], ['1x1', '2x1', '5x1']]
    >>> compress([[11, 11, 2], [1, 2]])
    Traceback (most recent call last):
    AssertionError: Image is not in PGM format
    '''
    if not is_valid_image(image):
        raise AssertionError('Image is not in PGM format')
    
    compressed = []
    
    for row in image:
        ele_i = 0
        comp_line = []
        
        while ele_i < len(row):
            new_i = find_end_of_repetition(row, ele_i, row[ele_i])
            consec_n = new_i - ele_i + 1
            comp_line.append(str(row[ele_i]) + 'x' + str(consec_n))
            ele_i = new_i + 1
        
        compressed.append(comp_line)
        
    return compressed


def decompress(image):
    ''' (list<list<str>>) -> list<list<int>>
    Returns a regular png file that is a decompressed version
    of the compressed png matrix image.

    >>> decompress([['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']])
    [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> decompress([['11x8']])
    [[11, 11, 11, 11, 11, 11, 11, 11]]
    >>> decompress([['0x4', '9x4'], ['0x8']])
    [[0, 0, 0, 0, 9, 9, 9, 9], [0, 0, 0, 0, 0, 0, 0, 0]]
    >>> decompress([['0x4', '9x4'], ['0x7']])
    Traceback (most recent call last):
    AssertionError: Image is not in compressed PGM format
    '''
    if not is_valid_compressed_image(image):
        raise AssertionError('Image is not in compressed PGM format')

    decompressed = []
    
    for row in image:
        
        new_row = []
        for ele in row:
            split = ele.split('x')
            a = int(split[0])
            b = int(split[1])
            
            new_row += ([a] * b)
        
        decompressed.append(new_row)

    return decompressed


def process_command(commands):
    ''' (str) -> NoneType
    Returns void, takes a str of commands seperated by a space and
    excecutes the commands in sequential order.

    >>> process_command("LOAD<comp.pgm> CP DC INV INV SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True
    >>> save_image([[1,2,3]], 'test.pgm')
    >>> process_command("LOAD<test.pgm> INV SAVE<test2.pgm>")
    >>> load_image('test2.pgm')
    [[254, 253, 252]]
    >>> save_image([[1,2,3,4,5,6,7,8]], 'test.pgm')
    >>> process_command("LOAD<test.pgm> FH CP SAVE<test2.pgm.compressed>")
    >>> load_image('test2.pgm.compressed')
    [['8x1', '7x1', '6x1', '5x1', '4x1', '3x1', '2x1', '1x1']]
    >>> save_image([[1,2,3,4,5,6,7,8]], 'test.pgm')
    >>> process_command("LOAD<test.pgm> abcd SAVE<test2.pgm>")
    Traceback (most recent call last):
    AssertionError: Incorrect arguments for process_command
    '''
    command_list = commands.split()
    filename_load = command_list[0][5:-1]
    image = load_image(filename_load)
    
    for i in range(1, len(command_list) - 1):
        if command_list[i] == 'INV':
            image = invert(image)
        elif command_list[i] == 'FH':
            image = flip_horizontal(image)
        elif command_list[i] == 'FV':
            image = flip_vertical(image)
        elif command_list[i] == 'FH':
            image = flip_horizontal(image)
        elif command_list[i] == 'CP':
            image = compress(image)
        elif command_list[i] == 'DC':
            image = decompress(image)
        elif command_list[i].split('<')[0] == 'CR':
            ints = command_list[i].split('<')[1][:-1]
            int_list = ints.split(',')
            y = int_list[0]
            x = int_list[1]
            h = int_list[2]
            w = int_list[3]
            crop(image, y, x, h, w)
        else:
            raise AssertionError('Incorrect arguments for process_command')
    
    filename_save = command_list[-1][5:-1]
    save_image(image, filename_save)