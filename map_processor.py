import cv2

# top left - 40.78757643381836, -96.60957915160421
# bottom right - 40.78420606216668, -96.605521169836

def get_image_size(image_path):
    image = cv2.imread(image_path)

    return image.shape

def get_coord_pixel_location(lat, lon):
    image_size = get_image_size("somerset.png")

    top_lat = 40.787576
    top_lon = -96.609579

    bottom_lat = 40.784206
    bottom_lon = -96.605521

    X = (lon - top_lon) / (bottom_lon - top_lon) * image_size[1]
    Y = (top_lat - lat) / (top_lat - bottom_lat) * image_size[0]

    return (int(X), int(Y))

def update_image(coords):
    map = cv2.imread("somerset.png")
    print("Coords: ", coords)
    #40.78647490131012, -96.60745776292396
    pic_location = get_coord_pixel_location(coords[0], coords[1])
    print("Pic locations: ", pic_location)
    cv2.imwrite("static/map_copy.png", map)

    map_copy = cv2.imread("static/map_copy.png")
    cv2.circle(map_copy, pic_location, 5, (0, 255, 0), 2)
    cv2.imwrite("static/map_copy.png", map_copy)
