FROM python:3.7.5-slim
RUN python -m pip install \
        parse \
        realpython-reader \
        face_recognition
FROM python:3.7.5-slim
RUN python -m pip install --upgrade pip wheel setuptools
FROM python:3.7.5-slim
RUN python -m pip install \ 
        docutils \ 
        pygments \ 
        pypiwin32 \ 
        kivy.deps.sdl2 \ 
        kivy.deps.glew \ 
        kivy.deps.gstreamer \ 
        kivy.deps.angle \ 
        pygame \ 
        kivy