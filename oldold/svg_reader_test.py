from xml.dom import minidom
def read_file(filename):

    mydoc = minidom.parse(filename)
    features = []
    feature = mydoc.getElementsByTagName('polygon')
    for i in range(len(feature)):
        x = []
        y = []
        points = feature[i].attributes['points'].value
        points = points.split()
        for i in range(len(points)):
            if (i % 2) == 0:
                x.append(points[i])
            else:
                y.append(points[i])
        features.append((x, y))
    return features
    #print(features[2][0][1])

