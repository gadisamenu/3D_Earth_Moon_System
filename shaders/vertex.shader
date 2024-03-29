#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture;
// layout(location = 2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 v_texture;

void main(){
     gl_Position = projection * view *  model * vec4(position, 1.0);
     v_texture = vec2(texture.x, 1-texture.y);
}