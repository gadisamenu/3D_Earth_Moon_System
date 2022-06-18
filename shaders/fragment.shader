#version 330 core

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main(){
    out_color = vec4(0.0, 1.0, 0.0, 1.0);
}