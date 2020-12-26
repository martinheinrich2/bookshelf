"""
Module to scan barcodes via webcam and write to csv file.
"""
import datetime
import cv2
from pyzbar import pyzbar

# %%


def read_barcodes(frame, csv, found):
    # find barcodes in the image and decode each barcode
    barcodes = pyzbar.decode(frame)
    # loop over detected barcodes
    for barcode in barcodes:
        # extract location of bounding box of barcode and draw
        # bounding box surrounding the barcode on image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # put barcode data and type into string
        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type
        # Select font and write decoded barcode/QR code on screen
        text = "{} ({})".format(barcodeData, barcodeType)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, text, (x, y - 10), font, 0.5, (0, 0, 255), 2)

        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set

        if barcodeData not in found:
            csv.write("{}\n".format(barcodeData))
            csv.flush()
            found.add(barcodeData)

        # write decoded barcode/QR code to file
        # with open('barcode_result.txt', mode='a+') as file:
        #    file.write("Recognised Barcode:" + barcodeData + ", " + barcodeType + "\n")

    return (frame)


def main():
    # initialise class VideoCapture
    filename = datetime.datetime.now().strftime('barcodes-%Y-%m-%d-%H-%M.csv')
    csv = open(filename, "w")
    found = set()
    print("Starting video capture!")
    print("Press ESC or q to stop scanning, when Videoscreen is on top.")
    camera = cv2.VideoCapture(0)
    # activate webcam if capture was not initialised by VideoCapture
    if not camera.isOpened():
        camera.open()

    ret, frame = camera.read()
    # ret is true if frame was read correctly
    while(ret):

        # Capture frame-by-frame, ret is True if frame was read correctly
        ret, frame = camera.read()
        frame = read_barcodes(frame, csv, found)
        cv2.imshow('Barcode/QR Code reader', frame)

        # check if "ESC" or "q" was pressed
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break

    # when everything is done, release the capture
    camera.release()
    print("Cleaning up, finished scanning.")
    csv.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
