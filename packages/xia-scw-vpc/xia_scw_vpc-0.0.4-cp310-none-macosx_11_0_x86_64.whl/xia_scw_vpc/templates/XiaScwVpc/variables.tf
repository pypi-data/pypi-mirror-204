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

variable "ip_id" {
  type = string
  default = null  #xia#
  #xia# default = {% if ip_id is not none %}"{{ ip_id }}"{% else %}null{% endif %}

}

variable "wan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if wan_ip is not none %}"{{ wan_ip }}"{% else %}null{% endif %}

}

variable "lan_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if name is not none %}"{{ lan_name }}"{% else %}null{% endif %}

}

variable "lan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_ip is not none %}"{{ lan_ip }}"{% else %}null{% endif %}

}

variable "lan_netmask" {
  type = number
  default = null  #xia#
  #xia# default = {% if lan_netmask is not none %}{{ lan_netmask }}{% else %}null{% endif %}

}

variable "bastion_port" {
  type = number
  default = null  #xia#
  #xia# default = {% if bastion_port is not none %}{{ bastion_port }}{% else %}null{% endif %}

}
