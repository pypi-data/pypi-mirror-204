variable "project_id" {
  type = string
  default = null  #xia#
  #xia# default = {% if project_id is defined and project_id is not none %}"{{ project_id }}"{% else %}null{% endif %}

}

variable "vpc_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if vpc_name is defined and vpc_name is not none %}"{{ vpc_name }}"{% else %}null{% endif %}

}

variable "instance_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if instance_name is defined and instance_name is not none %}"{{ instance_name }}"{% else %}null{% endif %}

}

variable "service_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if service_name is defined and service_name is not none %}"{{ service_name }}"{% else %}null{% endif %}

}

variable "lan_name" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_name is defined and lan_name is not none %}"{{ lan_name }}"{% else %}null{% endif %}

}

variable "lan_ip" {
  type = string
  default = null  #xia#
  #xia# default = {% if lan_ip is defined and lan_ip is not none %}"{{ lan_ip }}"{% else %}null{% endif %}

}

variable "wan_port" {
  type = number
  default = null  #xia#
  #xia# default = {% if wan_port is defined and wan_port is not none %}{{ wan_port }}{% else %}null{% endif %}

}

variable "lan_port" {
  type = number
  default = null  #xia#
  #xia# default = {% if lan_port is defined and lan_port is not none %}{{ lan_port }}{% else %}null{% endif %}

}

variable "protocol" {
  type = string
  default = null  #xia#
  #xia# default = {% if protocol is defined and protocol is not none %}"{{ protocol }}"{% else %}null{% endif %}

}

variable "allowed_ips" {
    type = list(string)
    default = null  #xia#
    #xia# default = [{% for v in allowed_ips %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}"{{ v }}"{% else %}null{% endif %}{% endfor %}]

  validation {
    condition = (
      alltrue([
        for ip in var.allowed_ips: (
          can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)) ||
          can(regex("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|[12]?[0-9])$", ip))
        )
      ])
    )
    error_message = "Each element of the allowed_ip variable must be a valid IPv4 address or an IPv4 address with a subnet mask."
  }
}

variable "ssh_private_key" {
  type = string
  default = null
}
