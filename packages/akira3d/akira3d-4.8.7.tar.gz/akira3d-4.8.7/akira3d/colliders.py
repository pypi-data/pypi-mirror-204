import math
import glm


def sphInter(p1, p2, rd, ra):
    ro = p1-p2
    b = glm.dot(ro, rd)
    c = glm.dot(ro, ro) - ra * ra
    h = b * b - c
    it = None
    if h < 0.0: it = glm.vec2(-1.0, -1.0)
    else: h = math.sqrt(h); it = glm.vec2(-b - h, -b + h);
    it = it[0] if it[0] > 0.0 else it[1]
    if it < 0.0: return False
    else: itPos = p1 + rd * it; return glm.distance(p1, itPos)

def sumM(lists):
    list1 = [0 for i in range(len(lists[0]))]
    for _ in lists:
        for i in range(len(_)):
            list1[i] += _[i]
    return list1

def revList(list):
    return [-i for i in list]

def rotPoint(p, p1, alpha, version='2d'):
    if version == '2d':
        X = p1.x + ((p.x-p1.x)*math.cos(math.radians(alpha)) - (p.y-p1.y)*math.sin(math.radians(alpha)))
        Y = p1.y + ((p.x-p1.x)*math.sin(math.radians(alpha)) + (p.y-p1.y)*math.cos(math.radians(alpha)))
        return glm.vec2(X, Y)
    elif version == '3d':
        X = p.x
        Z = p1.z + ((p.z - p1.z) * math.cos(math.radians(alpha[0])) - (p.y - p1.y) * math.sin(math.radians(alpha[0])))
        Y = p1.y + ((p.z - p1.z) * math.sin(math.radians(alpha[0])) + (p.y - p1.y) * math.cos(math.radians(alpha[0])))

        X = p1.x + ((Z - p1.z) * math.sin(math.radians(alpha[1])) + (X - p1.x) * math.cos(math.radians(alpha[1])))
        Z = p1.z + ((Z - p1.z) * math.cos(math.radians(alpha[1])) - (X - p1.x) * math.sin(math.radians(alpha[1])))
        Y = Y

        X = p1.x + ((Y - p1.y) * math.sin(math.radians(alpha[2])) + (X - p1.x) * math.cos(math.radians(alpha[2])))
        Y = p1.y + ((Y - p1.y) * math.cos(math.radians(alpha[2])) - (X - p1.x) * math.sin(math.radians(alpha[2])))
        Z = Z
        return glm.vec3(X, Y, Z)

def rotFigure(poss, pos, alpha, version='2d'):
    poss1 = []
    for p in poss:
        poss1.append(rotPoint(p, pos, alpha, version))
    return poss1

def isIn(a, b, c, version='1d'):
    if version == '1d':
        return (a >= b and a <= c)
    elif version == '2d':
        return (a.x >= min(b.x, c.x) and a.x <= max(b.x, c.x) and a.y >= min(b.y, c.y) and a.y <= max(b.y, c.y))
    elif version == '3d':
        return (a.x >= min(b.x, c.x) and a.x <= max(b.x, c.x) and a.y >= min(b.y, c.y) and a.y <= max(b.y, c.y) and a.z >= min(b.z, c.z) and a.z <= max(b.z, c.z))

def checkCollizion(rect, rect1, version='2d'):
    col = False
    for p in rect1.gposs:
        rp = rotPoint(rotPoint(p, rect1.pos, rect1.angle, version), rect.pos, (-rect.angle if version == '2d' else revList(rect.angle)), version)
        if isIn(rp, rect.grect[0], rect.grect[1], version): col = True
    for p in rect.gposs:
        rp = rotPoint(rotPoint(p, rect.pos, rect.angle, version), rect1.pos, (-rect1.angle if version == '2d' else revList(rect1.angle)), version)
        if isIn(rp, rect1.grect[0], rect1.grect[1], version): col = True
    return col

class HitBox:
    def __init__(self, type, v, pos, mode, *args, **kwargs):
        self.type = type
        self.version = v
        self.pos = pos
        self.mode = mode
        if type == 'box':
            self.rect = kwargs['rect']
            self.angle = kwargs['angle'] if mode == 'rotable' else [0, 0, 0]
            self.lposs = self.CLPL(self.rect)
            self.grect = list(map(lambda x: x + self.pos, self.rect))
            self.gposs = list(map(lambda x: x + self.pos, self.lposs))

    def update(self, pos=None):
        self.pos = pos if pos else self.pos
        if self.type == 'box':
            self.grect = list(map(lambda x: x + self.pos, self.rect))
            self.gposs = list(map(lambda x: x + self.pos, self.lposs))

    def CLPL(self, rect):
        lposs = None
        if self.version == '3d':
            lposs = [rect[0],
                    glm.vec3(rect[0][0], rect[0][1], rect[1][2]),
                    glm.vec3(rect[0][0], rect[0][2], rect[1][0]),
                    glm.vec3(rect[0][0], rect[0][2], rect[1][1]),
                    glm.vec3(rect[1][0], rect[1][1], rect[0][2]),
                    glm.vec3(rect[1][0], rect[1][2], rect[0][0]),
                    glm.vec3(rect[1][0], rect[1][2], rect[0][1]),
                    rect[1]]
        else:
            lposs = [self.lrect[0],
                    glm.vec2(rect[0][0], rect[1][1]),
                    self.lrect[1],
                    glm.vec2(rect[1][0], rect[0][1])]
        return lposs

# boxN;
# vec3
# boxPos = vec3(3.0, 1.0, -0.001);
# it = boxIntersection(ro - boxPos, rd, vec3(1.0), boxN);
# if (it.x > 0 & & it.x < it.y) {it.x = it.x;} else {it.x = it.y;};
# if (it.x > 0.0 & & it.x < minIt.x) {
# minIt = it;
# n = boxN;
# col = vec4(0.9, 0.2, 0.2, -0.5);
# }
