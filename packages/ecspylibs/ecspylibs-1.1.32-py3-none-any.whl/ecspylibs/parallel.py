#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Apr 21 16:17:46 2023 -0400 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
blah
"""

import time
from dataclasses import dataclass

from autologging import logged, traced


@traced
@logged
@dataclass
class Parallel:
    """
    Blah
    """
    process: object
    pool_executor: object
    pool_size: object = None

    def __post_init__(self):
        """
        Blah
        """

        self.run_time = None
        self.results = None
        self.arguments = None
        self.results = None

        if self.pool_size:
            if isinstance(self.pool_size, int) or self.pool_size.isnumeric():
                self.pool_size = int(self.pool_size)
            else:
                self.pool_size = None
        else:
            self.pool_size = None

        self.__log.debug(f"Process       : {type(self.process)}")
        self.__log.debug(f"Pool Executor : {self.pool_executor}")
        self.__log.debug(f"Pool Size     : {self.pool_size}")

    def run(self, arguments: object) -> object:
        """
        Blah
        """

        self.__log.debug(f"arguments   : {arguments}")

        start_time = time.perf_counter()

        with self.pool_executor(self.pool_size) as executor:
            self.results = executor.map(self.process, arguments)

        finish_time = time.perf_counter()

        self.run_time = finish_time - start_time

        return self.results
