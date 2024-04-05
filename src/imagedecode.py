# The following code demonstrates the implementation of adaptive thresholding using OpenCV and Python.
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
import base64
from PIL import Image
from io import BytesIO

# 9 of spades
# base64_string = "iVBORw0KGgoAAAANSUhEUgAAAFoAAACOCAMAAACG2e8JAAAAM1BMVEX///9HcEz////////////////09PTe3t7Hx8eysrKYmJiBgYFhYWFDQ0MpKSkPDw8AAAArZL/7AAAAB3RSTlP/AEBQkKD2U2akswAAAqtJREFUeNrt29tu4zAMBNBpLhR1I/n/X7vbFgnRrG00EfmyyHloUSMdCBPJUAwFH2mQH32+EkLQ9fwj+kQIRCePviDY5RZ9Rbjrd/QFCS6f0SekOP2NJqSgD5yR5IwrklxByPH7YGpjqpnN0Qsi1WHmZkWUMu3BLAhR1f6hFQGabWppyaaMRWx7hLBG7G62Wrv/rT2kDi+XhmdT0KDvY5x+KaZpwU3xa1jQt+aaV1LwuukpW/23kKrhakjZdrd5deZFS0ghFc7uQt7Gvrn2QyafFtyMkGjeuBsNc0F3J+0FKE3MSfTd2k2smHnRpLavYwmL7WpYQ8N+UO+fsaqKuVG63SAA9ylmJqMX+IQcCNa8asQib4cQq3vraXUYpyXP6DZcQaAm5jrC1C5mThBgfpLALbAzF5yM7eSk6FmQE60dSImWTsiI1lHhoqLn7J3x9vb29jpmZBFl5BhmSsjA/hEvGKnvP4JJ1n4dI3Pvm5TNZknZrJaS7cluBE67nGwS2zApOtkJRffshGOS4/fvVe1IW1qDx8bSg5BjUvCCIvYLWsNrdmOhjNhSWMyFltLUXGQpNO1ZKiW6DKe8tLSPtYUFuJjNtqDiQFFboAX7pi2Z4XU4Php00rCLLSvRE8+1/T6yGlFbpthEFoCip57j/yi6WoCa+TbmT778JZO/0EltkRJ2dDuitx/7OvDKsHV+lakvDfp41TT/tYfhnqhk3KLHc3W4sZcMsS+y/5LX9jjDr7ed7PbSnk8bcL8qQNNXP+q1h/BRHs/7lPEQ3PBbdYj/V/FtlW+SSvNXjIqnEHNvzPg2t24UzK0zU+hpsIYwbA8471GLMrIeiKhQdLLz7PjjEMJxPYf33Q8AxwhJKPHgbuJx47xD0olHu/MOpOcdo887/J/3lYXsL1r8AZwc4ao8QUrqAAAAAElFTkSuQmCC"

# 9 of clover
# base64_string = "iVBORw0KGgoAAAANSUhEUgAAAFoAAACOCAMAAACG2e8JAAAAMFBMVEX///9HcEz////////////////z8/PW1ta4uLiampqCgoJiYmJFRUUrKysUFBQAAAAZPLwLAAAAB3RSTlP/AEBQkKD4tN6JtAAAAsdJREFUeNrtm91y4zAIRml+ACEE7/+2u0kni9sqmrqG2V7k3GTi8ZyQzwq2ZQXeyoB69fmKkAJezx/UJ4RE8BTqCyRzeaivkM71XX2BAi439QlKOP1VI5SAb3CGIs5whSKugFDD98XYupq7axeCTLj7BmXIgtQ/oZRUsvkXLKXw5lNamdmN4CDkzxgIxxjh0sYsm/eSEkeEiz0iwZyio0aNTTlJj+m2A8hsrEUkdECtYZnl31KihoBTwvZ/TLdqnXqkBMLzD9zPcgxTilpm3UhT1DTpRt2DpO5kQgDUhgcju1sHCkfQOjXaQi1wCIpwU8+P0fwDa4c7X8DDg07iDyABEr3pRxfaDMgOKczbdS4Y6SDkIpF6WRxOZWbNTqOo6DY8kESvDM/pp4HeGImXwIEHyWaYm4vUSlCjNgEoUQ9BqFBbZwiy1KoiBC9evHjx66Cm5jdGcvdj9Q3WIAvU3Lm4gMy/IunmoJeYw111c3c07+5PMcyenAzkaNFFZaMvaWUTC67peWTOPVWMP/9/6vYr1VYXiPoaKhvXI6GFVPRVzc+DmDmmwVe/c2amPdcFfmd0WpbNJMPvaKPdj+m0mT9j9F33qdj9x3RcmocfYODy7H0Io3XNJXWrH0ZhSvME2uJi5iBjUXRF2cO9qGzyJGiWR1Ui4klI9qAO9KVeqKsPI3sSDJ9BTwL3t9Sh9ySHr9H97cnQ7i9kP+iqtjQT+R1auw1m8NIM3e90WLp5753LQEB7BLN6BNn3nnYVAdomTNTnJexzy+NIRJqy0zwvZ/Bs5Qzb9MutEPOPCH4+J9v7Ftn9DIG6b+g0OcL9sadN9lyCj8kxbTgflxx7+g2LPb8BMgRoi8PFmDp10SGJlv1wft0AuHAyjsrMbpRjrqi7VU09gfgSgSUIRWDhwt3C5cZ1i6QLl3bXLUivW0Zft/i/7i8L1X+0+ANUEN+UuNILzQAAAABJRU5ErkJggg=="


# image_data = base64.b64decode(base64_string)
# image_data = BytesIO(image_data)
# Image.open(image_data).save("unflip.png")
img = cv.imread('unflip.png',0)
img = cv.medianBlur(img,5)
value = pytesseract.image_to_string(img, lang='eng', config='--psm 6')

print(value)

# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

