# extract and plot each detected face in a photograph
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN
import tensorflow as tf
import base64

physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# create the detector, using default weights
detector = MTCNN()

# draw each face separately
def draw_faces(filename, result_list):
    print(result_list)
    # load the image
    data = pyplot.imread(filename)
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        if(x1<0):
            x1 = 0
        if(y1<0):
            y1 = 0
        # define subplot
        pyplot.subplot(1, len(result_list), i+1)
        pyplot.axis('off')
        # plot face
        pyplot.imshow(data[y1:y2, x1:x2])
    # show the plot
    pyplot.show()

print("Hello World!")

def getFaces(filename):
	global detector
	# load image from file
	pixels = pyplot.imread(filename)
	# b64enc = str(base64.b64encode(pixels)[:20])
	# print(type(b64enc))
	# print(b64enc[0])
	# pyplot.imshow(pixels)
	# detect faces in the image
	faces = detector.detect_faces(pixels)
	return faces


if __name__ == "__main__":
	for i in range(1,3):
		filename = '../../../../Images and Media/JPEG Graphics file/1-300/FILE{0:03d}.jpg'.format(i)
		# detect faces in the image
		faces, pixels = getFaces(filename)
		# display faces on the original image
		draw_faces(filename, faces)