

# a robot is DEFINED by
# - a name
# - an IP for the raspberry
# - the DOFs with all the corresponding configurations. It's a DOFNAME-string dictionary:
#    --- for each DOF, it also has the SERIAL PORT of the CORRESPONDING ARDUINO that is associated to that DOF.
#    --- the DOFNAME is the DOF, while the STRING is the SERIAL PORT for that DOF.

class Robot:
    def __init__(self, name, ip, dofs,dof_serial_mapping=None):
        self.robot_name = name
        self.ip = ip
        if name=="room":
            self.dof_name_esp_udp_dict = dofs
            self.serial_mapping_dict = dof_serial_mapping
            self.dof_name_to_serial_port_dict = dofs

        else:
            self.dof_name_to_serial_port_dict = dofs

    def has_dof(self, dof_key):
        # returns TRUE if there is a DOF with the corresponding input DOF_KEY
        for dof_enum in self.dof_name_to_serial_port_dict.keys():
            if dof_enum.value.key == dof_key:
                return True
        return False

    def is_serial_port_correct(self, dof_name, serial_port):
        # returns TRUE if the input 'dof' is controlled by the arduino on the input 'serial_port', for this robot
        return self.dof_name_to_serial_port_dict[dof_name] == serial_port
