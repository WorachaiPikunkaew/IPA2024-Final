from ncclient import manager
import xmltodict

# IP address context
def netconf_connect(ip: str):
    return manager.connect(
        host=ip,
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
def set_ip(ip):
    global m
    m = netconf_connect(ip)

# m = manager.connect(
#     host=_context["ip"],
#     port=830,
#     username="admin",
#     password="cisco",
#     hostkey_verify=False
#     )


def create():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070177</name>
                <description>NETCONF</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>172.1.77.1</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070177 is created successfully"
    except:
        print("Cannot create the interface loopback 66070177 using Netconf")
        return "Cannot create: Interface loopback 66070177"


def delete():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback66070177</name>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070177 is deleted successfully using Netconf"
    except:
        print("Cannot delete: Interface loopback 66070177")
        return "Cannot delete: Interface loopback 66070177"


def enable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070177</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070177 is enabled successfully using Netconf"
    except:
        print("Cannot enable: Interface loopback 66070177")
        return "Cannot enable: Interface loopback 66070177"


def disable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070177</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070177 is disabled successfully using Netconf"
    except:
        print("Cannot disable: Interface loopback 66070177")
        return "Cannot disable: Interface loopback 66070177"

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)


def status():
    netconf_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070177</name>
                </interface>
            </interfaces-state>
        </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter, source="running")
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if netconf_reply_dict['rpc-reply']['data']:
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']['admin-status']
            oper_status = netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']['oper-status']
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070177 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070177 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070177 (checked by Netconf)"
    except:
       print("Cannot get status of Interface loopback 66070177")
       return "Cannot get status of Interface loopback 66070177 (checked by Netconf)"
