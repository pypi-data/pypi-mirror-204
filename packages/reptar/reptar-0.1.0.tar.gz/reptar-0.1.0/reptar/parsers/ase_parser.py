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

from ase.io.trajectory import Trajectory
from ..extractors import ExtractorASE
from .parser import Parser


class ParserASE(Parser):
    r"""Custom parser for ASE trajectory files."""

    # We always pass certain paths into methods here.
    # pylint: disable=unused-argument, R0801

    def __init__(self, out_path=None, geom_path=None, traj_path=None, extractors=None):
        r"""
        Parameters
        ----------
        traj_path : :obj:`str`
            Path to a trajectory file from a geometry optimization, MD
            simulation, etc.
        extractors : :obj:`list`, default: ``None``
            Additional extractors for the parser to use.
        """

        self.package = "ase"
        if extractors is None:
            extractors = []
        extractors.insert(0, ExtractorASE())
        super().__init__(traj_path, extractors)

        self.traj_path = traj_path

        self.parsed_info["runtime_info"]["prov"] = "ASE"

    def parse(self):
        r"""Parses trajectory file and extracts information."""
        self.extract_data_out()
        return self.parsed_info

    def extract_data_out(self):
        r"""Custom extractor driver for ASE trajectory since it is not a text
        file.
        """
        traj = Trajectory(self.traj_path)
        for atoms in traj:
            for extractor in self.extractors:
                for trigger in extractor.triggers:
                    if trigger[0](True):
                        getattr(extractor, trigger[1])(traj, atoms)
                        break
                else:
                    continue
                break

        self.combine_extracted()

        return self.parsed_info
