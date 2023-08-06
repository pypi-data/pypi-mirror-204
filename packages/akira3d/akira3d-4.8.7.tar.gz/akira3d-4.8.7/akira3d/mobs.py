from glm import *
import math

class Mob:
    def __init__(self):
        self.bodyParts = {}

    def sphIntersect(self, ro, rd, ra):
        b = dot(ro, rd)
        c = dot(ro, ro) - ra * ra
        h = b * b - c
        if h < 0.0:
            return vec2(-1.0, -1.0)
        else:
            h = math.sqrt(h)
            return vec2(-b - h, -b + h)

    def boxIntersection(self, ro, rd, pos1, pos2):
        pass

    def lineHit(self, vPosLine, vDirectionLine):
        for _ in self.bodyParts:
            hit = _.hitbox
            if hit['type'] == 'sphere':
                it = self.sphIntersect(vPosLine-_['pos'], vDirectionLine, _['rad'])
                it = it[0] if it[0] > 0.0 else it[1]
                if it < 0.0:
                    return False
                else:
                    itPos = vPosLine + vDirectionLine * it
                    s = distance(vPosLine, itPos)
                    return s
            elif hit['type'] == 'cube':
                return False



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

