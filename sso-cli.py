https://kb.vmware.com/s/article/55934

vi /opt/vmware/share/htdocs/vami/backend/sso-cli.py

-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------

#!/opt/vmware/bin/python
# Copyright 2015 (C) VMware, Inc.  All rights reserved.

import sys
import vami
import os
import ssl
import six

sys.path.append("/opt/vmware/lib64")
sys.path.append("/usr/lib/vmware/site-packages/deploy")
from deploy_common import Message
from OpenSSL import crypto

try:
   import libvmidentityclientpython as libssopy
except:
   #so we can log errors when requests come
   pass

def ldapUserStrConvert(ssoDomainUser):
    ''' @param ssoDomainUser
        @type string sso user name in 'Administrator@vsphere.local' form.
        @return LDAP object to bind
        @string object as 'cn=Administrator,cn=Users,dc=vsphere,dc=local'
    '''
    sepUserStr = ssoDomainUser.split('@')
    if len(sepUserStr) > 1:
        #there is domain after '@'
        domainList = sepUserStr[1].split('.')
        dcListStr = ""
        for dc in domainList:
            dcStr = "dc=%s" % dc
            if dcListStr != "":
               dcListStr = "%s,%s" % (dcListStr, dcStr)
            else:
                dcListStr = dcStr
    else:
        #there is no domain, user default
        dcListStr='dc=vsphere,dc=local'
    return "cn=%s,cn=Users,%s" %(sepUserStr[0], dcListStr)

def processException(response, errMsg, args):
    errMsg.args = args
    vami.log_error(errMsg)
    response.setStatus(False, errMsg)

def validate_cert_hostname(host, port='443'):
    """
    validate if the SAN in certificate has the hostname
    """
    cert = None
    vami.log_info("Fetch SSL Certificate for %s:%s" % (host, port))
    try:
        cert = ssl.get_server_certificate((host, port))
    except Exception as e:
        vami.log_error("Exception white fetching SSL Certificate: %s" % e)

    if not cert:
        raise Exception("Unable to fetch SSL certificate for %s:%s" %(host, port))

    EXT_IP_SUFFIX = "IP Address:"
    EXT_DNS_SUFFIX = "DNS:"

    cert_ips = set([])
    cert_fqdns = set([])
    root_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    for ind in range(root_cert.get_extension_count()):
        ext = root_cert.get_extension(ind)
        ext_type = ext.get_short_name()
        # The entry we are interested in
        sub_an = 'subjectAltName'
        if six.PY3 and isinstance(ext_type, bytes):  # python3 on windows
            sub_an = b'subjectAltName'
        if ext_type == sub_an:
            for ext_str in str(ext).split(", "):
                if ext_str.startswith(EXT_IP_SUFFIX):
                    cert_ips.add(ext_str[len(EXT_IP_SUFFIX):].lower())
                elif ext_str.startswith(EXT_DNS_SUFFIX):
                    cert_fqdns.add(ext_str[len(EXT_DNS_SUFFIX):].lower())
                else:
                    vami.log_info("Ignoring non-IP/DNS subjectAltName extension: '%s'" % ext_str)
    if cert_fqdns and host in cert_fqdns:
        return True
    if cert_ips and host in cert_ips:
        return True
    raise Exception("'%s' doesn't match with hostname in Platform Services "
                    "Controller certificate" % host)

class Controller:

    def getSSOVersion(self, response, locale, action, input):
        '''@response output field 'version' is the string value of target SSO
        '''
        try:
            server = input.getWidgetValue('server')
            port = input.getWidgetValue('port')
            if port == "":
                portnum = 7444
            else:
               portnum = int(port)
            vami.log_info("query SSO version: %s:%s" % (server, str(portnum)))
            version = libssopy.VmDeployGetSSOVersion(server, portnum)
            response.addKeyValue("version", version)
            response.setStatus(True, Message.success)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.sso_version_report_err, args)

    def validateSSO(self, response, locale, action, input):
        '''@response output field 'status' is the result of credential verification
           This API is not working with 5.5
        '''
        try:
            server = input.getWidgetValue('server')
            user = input.getWidgetValue('user')
            password = input.getWidgetValue('password')
            port = input.getWidgetValue('port')
            if not port:
                port='443'
            ldapUserStr = ldapUserStrConvert(user)
            validated = False
            validated = libssopy.VmDeployValidateVMDirCredentials_Secure(
                server, ldapUserStr, password)
            validated = validated and validate_cert_hostname(server, port)
            if validated:
                response.setStatus(True, Message.success)
            else:
                response.setStatus(False, Message.failure)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.sso_validation_err, args)

    def validateSSO55(self, response, locale, action, input):
        '''@response output field 'status' is the result of credential verification
           This API is for SSO 5.5
        '''
        try:
            server = input.getWidgetValue('server')
            user = input.getWidgetValue('user')
            password = input.getWidgetValue('password')
            if not port:
                port='443'
            ldapUserStr = ldapUserStrConvert(user)
            validated = False
            validated = libssopy.VmDeployValidateVMDirCredentials_Secure_5_5(
                    server, ldapUserStr, password)
            validated = validated and validate_cert_hostname(server, port)
            if validated:
                response.setStatus(True, Message.success)
            else:
                response.setStatus(False, Message.failure)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.sso_validation_err, args)

    def getSSODomain(self, response, locale, action, input):
        '''@response output field 'domain' is the string value of SSO domain, e.g. vsphere.local
        '''
        try:
            server = input.getWidgetValue('server')
            domain = libssopy.VmDeployGetSSODomainName(server)
            response.addKeyValue("domain", domain)
            response.setStatus(True, Message.success)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.sso_domain_err, args)

    def getSSOSiteNames(self, response, locale, action, input):
        try:
            server = input.getWidgetValue('server')
            user = input.getWidgetValue('user')
            password = input.getWidgetValue('password')
            ldapUserStr = ldapUserStrConvert(user)
            sites = libssopy.VmDeployGetVMDirSiteNames(server, ldapUserStr, password)
            response.addObject("sites", sites)
            response.setStatus(True, Message.success)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.sso_site_names_err, args)

    def getNodeType(self, response, locale, action, input):
        try:
            deployTypes = { libssopy.node_type.unknown: "unknown",
                            libssopy.node_type.embedded: "embedded",
                            libssopy.node_type.infrastructure: "infrastructure"}
            server = input.getWidgetValue('server')
            user = input.getWidgetValue('user')
            password = input.getWidgetValue('password')
            ldapUserStr = ldapUserStrConvert(user)
            nodeType = libssopy.VmDeployGetNodeType(server, ldapUserStr, password)
            if nodeType in deployTypes:
                response.addKeyValue("nodeType", deployTypes[nodeType])
                response.setStatus(True, Message.success)
            else:
                errMsg = Message.node_type_invalid
                errMsg.args = [str(nodeType)]
                response.setStatus(False, errMsg)
        except libssopy.vmdeploy_exception as ssoex:
            args = [str(ssoex)]
            processException(response, Message.sso_validation_err, args)
        except Exception as e:
            args = [str(e)]
            processException(response, Message.node_type_report_err, args)


vami.execute(Controller())
