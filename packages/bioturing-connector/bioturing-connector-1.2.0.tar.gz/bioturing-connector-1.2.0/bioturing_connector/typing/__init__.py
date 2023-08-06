"""Custom typing"""

from enum import Enum


class StudyType(Enum):
	BBROWSER = 0
	H5_10X=1
	H5AD=2
	MTX_10X=3
	BCS=4
	RDS=5
	TSV=6
	DSP=7
	VISIUM=8


class Species(Enum):
  HUMAN='human'
  MOUSE='mouse'
  NON_HUMAN_PRIMATE='primate'


class InputMatrixType(Enum):
  RAW='raw'
  NORMALIZED='normalized'


UNIT_RAW = 'raw'
UNIT_LOGNORM = 'lognorm'
