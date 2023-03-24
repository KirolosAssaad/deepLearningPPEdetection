import bs4 as bs
import glob

labelsDict = {
    'helmet': 0,
    'head': 1,
    'person': 2
}


def yolofy(xml):
    soup = bs.BeautifulSoup(xml, 'xml')
    objects = []
    fileName = soup.find('filename').text

    # replace the extension if jpg or jpeg or png
    fileName = fileName.replace('.jpg', '.txt')
    fileName = fileName.replace('.jpeg', '.txt')
    fileName = fileName.replace('.png', '.txt')

    # Get the image size
    width = int(soup.find('width').text)
    height = int(soup.find('height').text)
    for tag in soup.find_all('object'):
        name = labelsDict[tag.find('name').text]
        # Get the bounding box
        bndbox = tag.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # Get the center point
        x = (xmin + xmax) / 2
        y = (ymin + ymax) / 2

        # Get the width and height
        w = xmax - xmin
        h = ymax - ymin

        # Normalize the values
        x /= width
        w /= width
        y /= height
        h /= height

        # Add the object to the list
        objects.append((name, x, y, w, h))

    # return all the objects to a string
    string = ''

    if (len(objects) == 0):
        return
    for obj in objects:
        string += ' '.join([str(a) for a in obj])
        if obj != objects[-1]:
            string += '\n'

    return fileName, string


def main():
    # loop over the annotations folder
    for xml in glob.glob('./annotations/*.xml'):
        # Read the xml file
        with open(xml, 'r') as f:
            xml = f.read()

            # Get the objects
            fileName, string = yolofy(xml)

            # If there are no objects, continue
            if (string == None):
                continue

            # Write the objects to a file
            with open('./labels/' + fileName, 'w') as f:
                f.write(string)


if __name__ == '__main__':
    main()
