bee
===

### bhyve configuration tool

bee allows you to create, modify and control [bhyve](http://www.bhyve.org)
virtual machines.  It's meant to be an easy to use but powerful tool.

### Current usage
`
usage: bee [-h] [-d] {create,start,stop,destroy,modify,list} ...

bhyve configuration tool

positional arguments:
  {create,start,stop,destroy,modify,list}
    create              Create a new bhyve VM
    start               Start a bhyve VM
    stop                Stopa bhyve VM
    destroy             Destroy a bhyve VM
    modify              Modify a bhyve VM
    list                List available VMs

optional arguments:
  -h, --help            show this help message and exit
  -d                    Enable debugging
`

It's under development, so it might not be very useful for now.
