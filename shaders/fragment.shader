#version 330 core

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D earthTex;
uniform sampler2D cloudTex;

void main(){
    out_color = mix(texture(earthTex, v_texture), texture(cloudTex, v_texture), 0.5);
}