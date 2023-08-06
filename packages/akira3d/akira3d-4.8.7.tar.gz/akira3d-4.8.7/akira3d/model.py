import numpy as np
import glm
import pygame as pg

class BaseModel1:
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, hitbox):
        self.hitbox = hitbox
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.gmm()
        self.tex_id = tex_id
        self.vao_name = vao_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def gmm(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def r(self, rot):
        self.rot = glm.vec3([glm.radians(a) for a in rot])

    def render(self):
        self.update()
        self.vao.render()


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, hitbox):
        self.hitbox = hitbox
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.gmm()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.camera = self.app.camera

    def update(self): ...

    def gmm(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def r(self, rot):
        self.rot = glm.vec3([glm.radians(a) for a in rot])

    def render(self):
        self.update()
        self.vao.render()

class ExBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, hitbox):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        [vao[0].program['camPos'].write(self.app.camera.position) for vao in self.vao.vaos]
        [vao[0].program['view'].write(glm.int8(self.app.camera.view)) for vao in self.vao.vaos]
        [vao[0].program['m_view'].write(self.app.camera.m_view) for vao in self.vao.vaos]
        [vao[0].program['m_model'].write(self.m_model) for vao in self.vao.vaos]

        [vao[1].program['m_proj'].write(self.camera.m_proj) for vao in self.vao.vaos]
        [vao[1].program['m_view_light'].write(self.app.light.m_view_light) for vao in self.vao.vaos]

        [vao[0].program['m_proj'].write(self.app.camera.m_proj) for vao in self.vao.vaos]
        #fog = max(min((glm.distance(self.app.camera.position, self.pos) - 100)/20, 1.0), 0);
        #print(fog)
        #[vao[0].program['fog'].write(glm.float64(fog)) for vao in self.vao.vaos]

    def update_shadow(self):
        [vao[1].program['m_model'].write(self.m_model) for vao in self.vao.vaos]

    def render_shadow(self):
        self.update_shadow()
        [vao[1].render() for vao in self.vao.vaos]

    def on_init(self):
        [vao[0].program['m_view_light'].write(self.app.light.m_view_light) for vao in self.vao.vaos]
        [vao[0].program['u_resolution'].write(glm.vec2(self.app.size)) for vao in self.vao.vaos]

        self.depth_texture = self.app.mesh.texture.textures['dt']
        for vao in self.vao.vaos: vao[0].program['shadowMap'] = 1
        self.depth_texture.use(location=1)

        [vao[1].program['m_proj'].write(self.camera.m_proj) for vao in self.vao.vaos]
        [vao[1].program['m_view_light'].write(self.app.light.m_view_light) for vao in self.vao.vaos]
        [vao[1].program['m_model'].write(self.m_model) for vao in self.vao.vaos]

        self.texture = self.app.mesh.texture.gt(self.tex_id)
        for vao in self.vao.vaos: vao[0].program['u_texture_0'] = 0
        self.texture.use(location=0)

        [vao[0].program['m_proj'].write(self.app.camera.m_proj) for vao in self.vao.vaos]
        [vao[0].program['m_view'].write(self.app.camera.m_view) for vao in self.vao.vaos]
        [vao[0].program['m_model'].write(self.m_model) for vao in self.vao.vaos]
        [vao[0].program['light.position'].write(self.app.light.position) for vao in self.vao.vaos]
        [vao[0].program['light.Ia'].write(self.app.light.Ia) for vao in self.vao.vaos]
        [vao[0].program['light.Id'].write(self.app.light.Id) for vao in self.vao.vaos]
        [vao[0].program['light.Is'].write(self.app.light.Is) for vao in self.vao.vaos]

    def tex(self, name=None, tex=None):
        self.tex_id = name
        self.texture = (tex if tex else self.app.mesh.texture.gt(self.tex_id))
        for vao in self.vao.vaos: vao[0].program['u_texture_0'] = 0

class Cube(ExBaseModel):
    def __init__(self, app, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), vao_name='cube', hitbox=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)

class UniverseModel(ExBaseModel):
    def __init__(self, app, vao_name, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), hitbox=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)

class MovingCube(Cube):
    def __init__(self, app, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), vao_name='cube', II=None,
                 hitbox=None):
        super().__init__(app, tex_id, pos, rot, scale, vao_name, hitbox)
        if II:
            self.ii = II(self)

    def update(self):
        self.m_model = self.gmm()
        super().update()

class MovingUniverseModel(UniverseModel):
    def __init__(self, app, vao_name, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1),II=None, hitbox=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)
        if II: self.ii = II(self)

    def update(self):
        self.m_model = self.gmm()
        super().update()

class SkyBox(BaseModel1):
    def __init__(self, app, vao_name='skybox', tex_id='1',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), hitbox=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.skyBoxes[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

class AdvancedSkyBox(BaseModel1):
    def __init__(self, app, tex_id, vao_name='advanced_skybox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), hitbox=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, hitbox)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        self.texture = self.app.mesh.texture.skyBoxes[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

    def tex(self, name):
        self.tex_id = name
        self.texture = self.app.mesh.texture.skyBoxes[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
