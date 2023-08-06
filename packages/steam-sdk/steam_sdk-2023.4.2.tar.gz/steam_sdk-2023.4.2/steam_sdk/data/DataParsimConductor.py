from typing import (List, Dict, Union, Literal)
from pydantic import BaseModel

############################
# General parameters
class GeneralParameters(BaseModel):
    magnet_name: str = None
    circuit_name: str = None
    state: str = None  # measured, deduced from short-samples, deduced from design

############################
# Magnet
class Magnet(BaseModel):
    coils: List[str] = []
    measured_inductance_versus_current: List[List[float]] = []   # TODO why is this needed?

# ############################
# # Coils
# class Coil(BaseModel):
#     ID: str = None
#     cable_ID: str = None
#     coil_length: float = None
#     coil_RRR: float = None
#     T_ref_RRR_low: float = None
#     T_ref_RRR_high: float = None
#     coil_resistance_room_T: float = None
#     T_ref_coil_resistance: float = None
#     conductors: List[str] = []
#     weight_conductors: List[float] = []

############################
# Conductors
class IcMeasurement(BaseModel):
    """
        Level 1: Class for parameters of a critical current measurement to adjust Jc fit parameters
    """
    Ic: float = None
    T_ref_Ic: float = None
    B_ref_Ic: float = None
    Cu_noCu_sample: float = None


class StrandGeometry(BaseModel):
    """
        Level 2: Class for strand geometry
    """
    diameter: float = None
    bare_width: float = None
    bare_height: float = None


class ConductorSample(BaseModel):
    # ID: str = None
    # Ra: float = None
    # Rc: float = None
    index_of_conductor_in_modelData: int = None
    group_indices_in_modelData: List[int] = []  # TODO new
    number_of_strands: int = None
    width: float = None
    height: float = None
    strand_twist_pitch: float = None
    filament_twist_pitch: float = None
    # Resistance measurement attributes
    coil_resistance_room_T: float = None  # TODO new
    Cu_noCu_resistance_meas: float = None   # TODO new
    total_conductor_length: float = None  # TODO new
    # critical current measurement attributes
    Tc0: float = None
    Bc20: float = None
    f_rho_eff: float = None
    Ic_measurements: List[IcMeasurement] = []
    strand_geometry: StrandGeometry = StrandGeometry()
    # weighted entries with weight factors
    weight_factors: List[float] = []
    RRR: List[float] = []
    Cu_noCu: List[float] = []
    # names of entries that can be weighted as a read-only attribute
    _names_of_attributes_to_weight: List[str] = ['RRR', 'Cu_noCu']
    @property
    def names_of_attributes_to_weight(self) -> List[str]:
        return self._names_of_attributes_to_weight



class DataParsimConductor(BaseModel):
    '''
        **Class for the STEAM conductor**

        This class contains the data structure of a Conductor parsim  analyzed with STEAM_SDK.

        :return: DataParsimConductor object
    '''

    GeneralParameters: GeneralParameters = GeneralParameters()
    Magnet: Magnet = Magnet()
    # Coils: Dict[str, Coil] = {}
    ConductorSamples: Dict[str, ConductorSample] = {}
