import glm


class Light:
    def __init__(self, position=(50, 50, -10), color=(0.86, 0.8, 0.9)):
        self.position = glm.vec3(position)#(0.86, 0.8, 0.9)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)

        self.Ia = 0.03 * self.color
        self.Id = 0.8 * self.color
        self.Is = 7.0 * self.color

        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
