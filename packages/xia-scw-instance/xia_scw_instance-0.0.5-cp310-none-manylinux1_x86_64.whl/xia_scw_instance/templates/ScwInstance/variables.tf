variable "project_id" {
  type = string
  default = null  #xia#
  #xia# default = {% if project_id is not none %}"{{ project_id }}"{% else %}null{% endif %}

}

variable "name" {
  type = string
  default = null  #xia#
  #xia# default = {% if name is not none %}"{{ name }}"{% else %}null{% endif %}

}

variable "type" {
  type = string
  default = null  #xia#
  #xia# default = {% if type is not none %}"{{ type }}"{% else %}null{% endif %}

}

variable "image" {
  type = string
  default = null  #xia#
  #xia# default = {% if image is not none %}"{{ image }}"{% else %}null{% endif %}

}

variable "state" {
  type = string
  default = null  #xia#
  #xia# default = {% if state is not none %}"{{ state }}"{% else %}null{% endif %}

}

variable "tags" {
    type = list(string)
    default = null  #xia#
    #xia# default = [{% for v in tags %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}"{{ v }}"{% else %}null{% endif %}{% endfor %}]
}