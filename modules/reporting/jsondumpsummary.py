# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import copy
import os
import json
import codecs

from lib.cuckoo.common.abstracts import Report
from lib.cuckoo.common.exceptions import CuckooReportError

class JsonDumpSummary(Report):
    """Saves analysis results in JSON format."""

    def run(self, results):
        """Writes report.
        @param results: Cuckoo results dict.
        @raise CuckooReportError: if fails to write report.
        """
        indent = self.options.get("indent", 4)
        encoding = self.options.get("encoding", "utf-8")
        ram_boost = self.options.get("ram_boost", True)
	remove = self.options.get("remove", "")
	
	to_remove = remove.split(',')
	simple = results.copy()
	for tr in to_remove:
		del simple[tr]

        try:
            path = os.path.join(self.reports_path, "summary-report.json")
            with codecs.open(path, "w", "utf-8") as report:
                if ram_boost:
                    buf = json.dumps(simple, sort_keys=False,
                              indent=int(indent), encoding=encoding)
                    report.write(buf)
                else:
                    json.dump(simple, report, sort_keys=False,
                              indent=int(indent), encoding=encoding)
        except (UnicodeError, TypeError, IOError) as e:
            raise CuckooReportError("Failed to generate JSON report: %s" % e)
