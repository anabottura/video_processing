from os import path
import cv2

# Data files should be .avi's and have the following form:
# '<dataDir><dataFilePrefix><startingFileNum>.avi'

# Values users can modify:
dataDir = "./" # directory where videos are stored
dataFilePrefix = ''
startingFileNum = 0
framesPerFile = 1000 # This is the default setting for the Miniscope software. If you changed it in software change it here too.
# -------------------------------

# Makes sure path ends with '/'
if (dataDir[-1] != "/"):
    dataDir = dataDir + "/"

# Select one below -
compressionCodec = "FFV1"
# compressionCodec = "GREY"
# compressionCodec = 'XVID'
# --------------------

fileNum = startingFileNum
frameCount = 0

codec = cv2.VideoWriter_fourcc(*compressionCodec)

cap_list = []

while (path.exists(dataDir + dataFilePrefix + "{:.0f}.avi".format(fileNum))):
    cap_list.append(cv2.VideoCapture(dataDir + dataFilePrefix + "{:.0f}.avi".format(fileNum)))
    fileNum = fileNum + 1
    
cols = int(cap_list[0].get(cv2.CAP_PROP_FRAME_WIDTH))
rows = int(cap_list[0].get(cv2.CAP_PROP_FRAME_HEIGHT))


writeFile = cv2.VideoWriter((dataDir + dataFilePrefix + "concat.avi"), fourcc=codec, fps=30, frameSize=(cols,rows))


for cap in cap_list:
    # frame_count = 0
    while cap.isOpened():
        # print(frame_count)
        ret, frame = cap.read()
        # frame_count += 1
        
        if (ret is False):
            break
        else:
            writeFile.write(frame)

writeFile.release()

cv2.destroyAllWindows()