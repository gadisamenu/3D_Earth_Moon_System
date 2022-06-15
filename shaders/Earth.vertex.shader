#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture;

out vec2 v_texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main(){
    gl_Position = projection * model * vec4(position, 1.0);
    v_texture = texture;
}