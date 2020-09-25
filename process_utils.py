import cv2


def test_cut(filedir, filename, x_dim=[0, 1920], y_dim=[270, 970], show='cut'):
    """
        test_cut(filedir, filename)

        Splits a behavioural video recording into individual boxes videos.
        Saves the new videos in the filedir with name box{}_filename.

            Required args:
                - filedir (str): file directory to access file
                                 and save boxes videos
                - filename (str): name of video file to be split

            Optional args:
                - box_arrange (list of int): grid arrangement of boxes in a list
                                             with [number of box in x axis, number of box in y axis]
                                default: [4, 2]
                - x_dim (list of int): start and end coordinates of the x axis as [start, end]
                                default: [0, 1920]
                - y_dim (list of int): start and end coordinates of the y axis as [start, end]
                                default: [270, 970]
                - f_rate (float): frame rate of video to save boxes videos
                                default: 20.0
        """

    vid = cv2.VideoCapture(filedir + filename)

    print(vid.shape())

    while True:
        ret, frame = vid.read()
        # res_frame = cv2.resize(frame, (960, 540))
        if show == 'cut':
            cut = frame[y_dim[0]:y_dim[1], x_dim[0]:x_dim[1]]
            cv2.imshow('cut', cut)
        else:
            cv2.imshow(show, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def split_box_videos(filedir, filename, boxes, f_rate=20.0, trim='False'):
    """
    split_box_videos(filedir, filename)

    Splits a behavioural video recording into individual boxes videos.
    Saves the new videos in the filedir with name box{}_filename.

        Required args:
            - filedir (str): file directory to access file
                             and save boxes videos
            - filename (str): name of video file to be split

            - boxes (dict): dictionary with individual boxes coordinates

        Optional args:
            - f_rate (float): frame rate of video to save boxes videos
                            default: 20.0
    """

    vid = cv2.VideoCapture(filedir + filename)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')

    v_writers = {}

    for box in boxes.keys():
        xstep = boxes[box][3]-boxes[box][2]
        ystep = boxes[box][1]-boxes[box][0]
        v_writers[box] = cv2.VideoWriter('{}{}_{}'.format(filedir, box, filename), fourcc, f_rate, (xstep, ystep))

    frame_counter = 1
    while True:
        ret, frame = vid.read()
        print('Number of frames: {}'.format(frame_counter))

        if ret:
            for box in boxes.keys():
                cut = frame[boxes[box][0]:boxes[box][1], boxes[box][2]:boxes[box][3]]
                cut = cv2.cvtColor(cut, cv2.COLOR_RGB2GRAY)
                # cv2.imshow('video', cut)
                v_writers[box].write(cut)
            frame_counter += 1
        else:
            break

    vid.release()

    for i in v_writers.values():
        i.release()
    cv2.destroyAllWindows()
    print('Individual box videos saved')


def boxes_locations(box_arrange, x_dim, y_dim):
    """
        boxes_locations(filedir, filename)

        Finds coordinates for individual boxes based on arrangement and x and y coordinates

            Required args:
                - box_arrange (list of int): grid arrangement of boxes in a list
                                             with [number of box in x axis, number of box in y axis]
                                default: [4, 2]
                - x_dim (list of int): start and end coordinates of the x axis as [start, end]
                                default: [0, 1920]
                - y_dim (list of int): start and end coordinates of the y axis as [start, end]
                                default: [270, 970]
        """
    if box_arrange is None:
        box_arrange = [2, 4]
    [box_x, box_y] = box_arrange
    [xstart, xend] = x_dim
    [ystart, yend] = y_dim

    leny = int(yend - ystart)
    lenx = int(xend - xstart)
    ystep = int(leny / box_y)
    xstep = int(lenx / box_x)

    boxes = {}
    for by in range(box_y):
        for bx in range(box_x):
            tag = 'box{}'.format((box_x * by) + (bx + 1))
            x_coord1 = xstart + bx * xstep
            x_coord2 = x_coord1 + xstep
            y_coord1 = ystart + by * ystep
            y_coord2 = y_coord1 + ystep
            boxes[tag] = [y_coord1, y_coord2, x_coord1, x_coord2]

    return boxes


def trim_video(filedir, filename):
    vid = cv2.VideoCapture(filedir + filename)
    msec = vid.get(cv2.CAP_PROP_POS_MSEC)
    frame2 = vid.get(cv2.CAP_PROP_POS_FRAMES)
    return msec, frame2
