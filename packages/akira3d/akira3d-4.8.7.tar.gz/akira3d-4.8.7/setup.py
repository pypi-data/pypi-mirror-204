from setuptools import setup

setup(name='akira3d',
      version='4.8.7',
      description='Modern 3D Graphics Engine by alexCoder23',
      packages=['akira3d'],
      author_email='alekseybeldem@gmail.com',
      zip_safe=False,
      install_requires=[
        'pygame',
        'moderngl',
        'numpy',
        'pywavefront',
        'pyGLM',
        'moviepy',
        'pyautogui',
        'sounddevice',
        'opencv-python'
])
