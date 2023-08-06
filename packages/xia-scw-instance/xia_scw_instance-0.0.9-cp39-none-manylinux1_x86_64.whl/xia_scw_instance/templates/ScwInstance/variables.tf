variable "state" {
  type = string
  default = null  #xia#
  #xia# default = {% if state is defined and state is not none %}"{{ state }}"{% else %}null{% endif %}

}

variable "project_id" {
  type = string
  default = null  #xia#
  #xia# default = {% if project_id is defined and project_id is not none %}"{{ project_id }}"{% else %}null{% endif %}

}

variable "name" {
  type = string
  default = null  #xia#
  #xia# default = {% if name is defined and name is not none %}"{{ name }}"{% else %}null{% endif %}

}

variable "type" {
  type = string
  default = null  #xia#
  #xia# default = {% if type is defined and type is not none %}"{{ type }}"{% else %}null{% endif %}

}

variable "image" {
  type = string
  default = null  #xia#
  #xia# default = {% if image is defined and image is not none %}"{{ image }}"{% else %}null{% endif %}

}

variable "tags" {
    type = list(string)
    default = null  #xia#
    #xia# default = [{% for v in tags %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}"{{ v }}"{% else %}null{% endif %}{% endfor %}]
}

variable "vpc_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if vpc_name is defined and vpc_name is not none %}"{{ vpc_name }}"{% else %}null{% endif %}

}

variable "wan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if wan_ip is defined and wan_ip is not none %}"{{ wan_ip }}"{% else %}null{% endif %}

}

variable "lan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_ip is defined and lan_ip is not none %}"{{ lan_ip }}"{% else %}null{% endif %}

}

variable "lan_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_name is defined and lan_name is not none %}"{{ lan_name }}"{% else %}null{% endif %}

}

variable "ssh_hosts" {
    type = list(string)
    default = null  #xia#
    #xia# default = [{% for v in ssh_hosts %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}"{{ v }}"{% else %}null{% endif %}{% endfor %}]

    validation {
    condition = (
      alltrue([
        for ip in var.ssh_hosts: (
          can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)) ||
          can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|[12]?[0-9])$", ip))
        )
      ])
    )
    error_message = "Each element of the allowed_ip variable must be a valid IPv4 address or an IPv4 address with a subnet mask."
  }
}

variable "forwards" {
    type = list(object({
      protocol = string
      wan_port = number
      lan_port = number
      allowed_ips = list(string)
    }))
    default = null  #xia#
#xia#     default = [{% for v in forwards %}
#xia#             {% if loop.index > 1 %},{% endif %}{
#xia#             {% for w, x in v.items() %}
#xia#                 {% if x is boolean %}
#xia#         {{ w }} = {% if x is none %}null{% elif x %}true{% else %}false{% endif %}

#xia#                 {% elif x is string %}
#xia#         {{ w }} = {% if x is not none %}"{{ x }}"{% else %}null{% endif %}

#xia#                 {% elif x is number %}
#xia#         {{ w }} = {% if x is not none %}{{ x }}{% else %}null{% endif %}

#xia#                 {% elif x is sequence and x is not string %}
#xia#         {{ w }} = [{% for y in x %}{% if loop.index > 1 %}, {% endif %}{% if y is not none %}"{{ y }}"{% else %}null{% endif %}{% endfor %}]

#xia#                 {% endif %}
#xia#             {% endfor %}
#xia#     }{% endfor %}]
    validation {
      condition = alltrue([
         for rule in var.forwards : alltrue([
           for ip in rule.allowed_ips: (
             can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)) ||
             can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|[12]?[0-9])$", ip))
           )
         ])
      ])

      error_message = "Each element of the allowed_ips variable must be a valid IPv4 address or an IPv4 address with a subnet mask."
    }
}

variable "ssh_private_key" {
  type = string
  default = null
}
