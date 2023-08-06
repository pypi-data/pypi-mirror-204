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

variable "ip_id" {
  type = string
  default = null  #xia#
  #xia# default = {% if ip_id is defined and ip_id is not none %}"{{ ip_id }}"{% else %}null{% endif %}

}

variable "wan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if wan_ip is defined and wan_ip is not none %}"{{ wan_ip }}"{% else %}null{% endif %}

}

variable "bastion_port" {
  type = number
  default = null  #xia#
  #xia# default = {% if bastion_port is defined and bastion_port is not none %}{{ bastion_port }}{% else %}null{% endif %}

}

variable "lan_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_name is defined and lan_name is not none %}"{{ lan_name }}"{% else %}null{% endif %}

}

variable "lan_subnet" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_subnet is defined and lan_subnet is not none %}"{{ lan_subnet }}"{% else %}null{% endif %}

}

variable "lan_address" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_address is defined and lan_address is not none %}"{{ lan_address }}"{% else %}null{% endif %}

}

variable "lan_low" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_low is defined and lan_low is not none %}"{{ lan_low }}"{% else %}null{% endif %}

}

variable "lan_high" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_high is defined and lan_high is not none %}"{{ lan_high }}"{% else %}null{% endif %}

}