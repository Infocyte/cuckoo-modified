# Copyright (C) 2016 jstauffer
# This file is part of Infocyte's Implementation of the Cuckoo Sandbox - http://www.cuckoosandbox.org

import logging
import os
import uuid

from lib.api.utils import Utils
from lib.common.abstracts import Auxiliary

log = logging.getLogger(__name__)
util = Utils()

class S1Survey(Auxiliary):
    """Runs Infocyte's S1 survey from the windows/analyzer/bin directory and
    sends the information back to the Pulse server for analysis. Your welcome
    Russ!"""

    def __init__(self, options, config):
        Auxiliary.__init__(self, options, config)
        self.enabled = True

    def start(self):
        if not self.enabled:
            return True

        try:
            # Get IP address from configuration file
            ip_address = self.options.get("pulseserverip")
            if not ip_address:
                log.warning("No IP address for the Pulse Server is configured")
                return True

            port = self.options.get("pulseserverport")
            if not port:
                port = "80"
            
            # Check if S1 exists
            s1_path = os.path.join(os.getcwd(), "bin", "S1.exe")
            if not os.path.exists(sign_path):
                log.info("Skipping S1 execution not found in bin/")
                return True

            # Run S1
            guid = uuid.uuid1()
            log.debug("Running S1.exe...")
            cmd = '{0} --postback {1} --sessionid {2}'.format(s1_path, ip_address + ":" + port, guid)
            ret, out, err = util.cmd_wrapper(cmd)
            
            # Return was 0, authenticode certificate validated successfully
            if not ret:
                log.debug("S1 executed successfully")

            # Non-zero return, it didn't validate or exist
            else:
                log.error("S1 did not execute: {0}",err);

        except Exception:
            import traceback
            log.exception(traceback.format_exc())

        return True
