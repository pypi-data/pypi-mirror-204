from .vbo import VBO
from .shader_program import ShaderProgram

class Vao:
    def __init__(self, progs, vbo, ctx):
        self.ctx = ctx
        self.vbo = vbo
        self.vaos = [[self.get_vao(program=progs['default'], vbo=v, v=vbo), self.get_vao(program=progs['shadow_map'], vbo=v, v=vbo)] for v in vbo.vbos]

    def get_vao(self, program, vbo, v):
        vao = self.ctx.vertex_array(program, [(vbo, v.format, *v.attribs)], skip_errors=True)
        return vao

    def render(self):
        [vao[0].render() for vao in self.vaos]

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}
        for name in self.vbo.vbos: self.vaos[name] = Vao(self.program.programs, self.vbo.vbos[name], ctx)
        self.vaos['cube'] = Vao(self.program.programs, self.vbo.vbos['cube'], ctx)
        self.vaos['skybox'] = self.get_vao(program=self.program.programs['skybox'], vbo=self.vbo.vbos1['skybox'])
        self.vaos['advanced_skybox'] = self.get_vao(program=self.program.programs['advanced_skybox'],vbo=self.vbo.vbos1['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
