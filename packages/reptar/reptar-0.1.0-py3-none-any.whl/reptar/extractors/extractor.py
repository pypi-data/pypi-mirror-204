# MIT License
#
# Copyright (c) 2022-2023, Alex M. Maldonado
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABC, abstractmethod


class Extractor(ABC):
    r"""Base class for extracting information from files."""

    def __init__(self):
        self.parsed_info = {"system_info": {}, "runtime_info": {}, "outputs": {}}

    @property
    @abstractmethod
    def triggers(self):
        r"""A collection of triggers that activate the corresponding extractor.

        The trigger is a lambda function that returns True or False depending
        on the criteria and the name of the extractor method.

        :type: :obj:`tuple`
        """

    @property
    def parsed_info(self):
        r"""Information parsed from files. Contains the following keys.

        ``system_info``
            Information specifying the system prior to any computation. Such
            as the initial cartesian coordinates, total system charge and
            multiplicity, etc.

        ``runtime_info``
            Contains information about setting up the job/calculation or running
            the job. Defining convergence criteria, parameters, etc.

        ``outputs``
            Results, requested or not, of the job. For example, SCF
            cycle values, optimized coordinates, trajectory, number of
            electrons, generated structures, etc.

        :type: :obj:`dict`
        """
        return self._parsed_info

    @parsed_info.setter
    def parsed_info(self, value):
        self._parsed_info = value

    @parsed_info.deleter
    def parsed_info(self):
        del self._parsed_info

    def skip_lines(self, f, n):
        r"""Skip a number of lines.

        Parameters
        ----------
        f : :obj:`io.TextIOWrapper`
            Buffered text stream of the file.
        n : :obj:`int`
            Number of lines to skip

        Returns
        -------
        :obj:`str`
            Line of file.
        """
        for _ in range(n):
            line = next(f)
        return line
