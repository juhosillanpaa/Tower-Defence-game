import numpy as np
import math

def calculate_angle( vec1, vec2):
    # calculate the angle between 2 vectors

    signed_angle = math.atan2(vec1[1], vec1[0]) - math.atan2(vec2[1], vec2[0])
    signed_angle = signed_angle * 180 / math.pi
    return signed_angle
