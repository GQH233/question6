POLYGON_FILE_NAME = 'input_question_6_polygon.py'
POINTS_FILE_NAME = 'input_question_6_points.py'
OUT_FILE_NAME = 'output_question_6.py'


def read_file(file_name):
    """
    Read points from the file.
    :param file_name: str the name of the file
    :return: a 2D-list of coordinates of points
    """
    point_list = []
    file = open(file_name)
    for line in file.readlines():
        line = line.strip('\n')
        data = line.split(' ')  # split the string according to the space
        if len(data) == 2:
            data = [float(x) for x in data]  # convert the string to number
            point_list.append(data)
    return point_list


def is_on_line(point_x, point_y, endpoint1_x, endpoint1_y,
               endpoint2_x, endpoint2_y):
    """
    Return whether the point is on the line or not.
    :param point_x: x coordinate of the point
    :param point_y: y coordinate of the point
    :param endpoint1_x: x coordinate of one endpoint of the line
    :param endpoint1_y: y coordinate of one endpoint of the line
    :param endpoint2_x: x coordinate of another endpoint of the line
    :param endpoint2_y: x coordinate of another endpoint of the line
    :return: True if the point is on the line, return False otherwise
    """
    # return True if the slopes of vector point->endpoint1
    # and vector point->endpoint2 are equal
    value = (endpoint2_y - point_y) * (endpoint1_x - point_x) \
            - (endpoint1_y - point_y) * (endpoint2_x - point_x)
    return abs(value) < 1e-6


def is_intersected(px1, py1, px2, py2, px3, py3, px4, py4):
    """
    Return whether two lines are intersect
    :param px1: x coordinate of one endpoint of the first line
    :param py1: y coordinate of one endpoint of the first line
    :param px2: x coordinate of another endpoint of the first line
    :param py2: y coordinate of another endpoint of the first line
    :param px3: x coordinate of one endpoint of the second line
    :param py3: y coordinate of one endpoint of the second line
    :param px4: x coordinate of another endpoint of the second line
    :param py4: y coordinate of another endpoint of the second line
    :return: True if the lines are intersected, False otherwise
    """
    value = (px2 - px1) * (py4 - py3) - (py2 - py1) * (px4 - px3)
    if value != 0:
        k1 = ((py1 - py3) * (px4 - px3) - (px1 - px3) * (py4 - py3)) / value
        k2 = ((py1 - py3) * (px2 - px1) - (px1 - px3) * (py2 - py1)) / value
        if 0 <= k1 <= 1 and 0 <= k2 <= 1:
            return True
    return False


def is_inside(polygon, point):
    """
    Return whether the point is inside the polygon
    :param polygon: a 2D-list of points of polygon
    :param point: a 1D-list of a point
    :return: True if the point is inside the polygon, False otherwise
    """
    # count the number of intersection point of
    # the vertical line passing through the point and the polygon
    count = 0
    # find the minimum x coordinate among the points of polygon
    min_x = polygon[0][0]
    for p in polygon:
        if min_x > p[0]:
            min_x = p[0]
    # traverse all the edges of the polygon
    for i in range(len(polygon)):  # point 1
        for j in range(i + 1, len(polygon)):  # point 2
            j = j % len(polygon)
            # return True if the point is on the line
            if is_on_line(point[0], point[1], polygon[i][0],
                          polygon[i][1], polygon[j][0], polygon[j][1]):
                return True
            # if the line is not vertical
            # continue to count the intersection point
            if abs(polygon[j][1] - polygon[i][1]) >= 1e-6:
                if is_on_line(polygon[i][0], polygon[i][1],
                              point[0], point[1], min_x - 10, point[1]):
                    if polygon[j][1] > polygon[i][1]:
                        count += 1
                elif is_on_line(polygon[j][0], polygon[j][1],
                                point[0], point[1], min_x - 10, point[1]):
                    count += 1
                elif is_intersected(point[0], point[1], min_x - 10,
                                    point[1], polygon[i][0],
                                    polygon[i][1], polygon[j][0],
                                    polygon[j][1]):
                    count += 1
    # if the number of intersection point is odd, return True
    # return False otherwise
    return count % 2 == 1


if __name__ == "__main__":
    points = read_file(POINTS_FILE_NAME)  # read points from file
    polygon = read_file(POLYGON_FILE_NAME)  # read polygon from file
    file = open(OUT_FILE_NAME, 'w')
    for i in range(len(points)):
        # write the result to the file
        if is_inside(polygon, points[i]):
            file.write('{:g}'.format(points[i][0]) + ' '
                       + '{:g}'.format(points[i][1]) + ' inside\n')
        else:
            file.write('{:g}'.format(points[i][0]) + ' '
                       + '{:g}'.format(points[i][1]) + ' outside\n')
    file.close()
