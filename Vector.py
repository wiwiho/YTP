import math

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def vectorLength2(a):
    return a[0] * a[0] + a[1] * a[1]

def vectorLength(a):
    return math.sqrt(vectorLength2(a))

def calcAngle(p, p1, p2):
    cosv = dot(p1 - p, p2 - p) / vectorLength(p1 - p) / vectorLength(p2 - p)
    cosv = max(-1.0, cosv)
    cosv = min(1.0, cosv)
    # print('calcAngle', p1, p, p2, dot(p1 - p, p2 - p), cross(p - p1, p2 - p1), cosv, math.acos(cosv))
    ans = math.acos(cosv)
    if cross(p - p1, p2 - p1) < 0.0:
        ans += 2 * math.pi
        # print('add', ans)
    return ans

def interpolate(p1, p2, len):
    v = p2 - p1
    v = v / vectorLength(v) * len
    # print('interpolate', p1, p2, len, p1 + v)
    return p1 + v

def cartesianToPolar(p):
    x = p[0]
    y = p[1]
    r = math.sqrt(x * x + y * y)
    return (r, math.atan2(y, x))

def polarToCartesian(p):
    r = p[0]
    t = p[1]
    return (r * math.cos(t), r * math.sin(t))

def polyArea(ps):
    lst = ps[-1]
    ans = 0.0
    for i in ps:
        ans += cross(lst, i)
        lst = i
    ans /= 2
    return ans
    