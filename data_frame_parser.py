class DataFrameParser:
    """
    Class that parses sensor data frame lines.
    """
    def __init__(self):
        self.__single_event_error_count = 0
        self.__total_error_count = 0
        self.__frames_analyzed = 0
        self.__dtcs_encountered = set()
    
    def parse_frame(self, s_sensor: str, s_data_a: str, s_data_b: str, s_data_c: str, s_error: str) -> str:
        """
        Parses one line of sensor data frame

        :param s_sensor: Hexadecimal byte corresponding to type of sensor data
        :param s_data_a: Hexadecimal byte corresponding to first data byte
        :param s_data_b: Hexadecimal byte corresponding to second data byte
        :param s_data_c: Hexadecimal byte corresponding to third data byte
        :param s_error: Hexadecimal byte corresponding to error byte
        """

        sensor_dict = {
            "0a": ("fuel pressure",              lambda a, b, c: 3 * a              , "kPa"  , (0, 765)       , ("P009B", "P0092")),
            "0c": ("engine speed",               lambda a, b, c: (256 * a + b) / 4  , "rpm"  , (0, 16383.75)  , ("P0725", "P0321")),
            "0d": ("vehicle speed",              lambda a, b, c: c                  , "km/h" , (0, 255)       , ("P0500", "P0503")),
            "11": ("throttle position",          lambda a, b, c: (100/255) * a      , "%"    , (0, 100)       , ("P0223", "P0227")),   
            "2f": ("fuel tank level",            lambda a, b, c: (100/255) * a      , "%"    , (0, 100)       , ("P0451", "P0450")),   
            "5c": ("oil temperature",            lambda a, b, c: (a - 40)           , "C"    , (-40, 215)     , ("P0195", "P0196")),
            "67": ("engine coolant temperature", lambda a, b, c: (b - 40)           , "C"    , (-40, 215)     , ("P00B7", "P0117")), 
            "68": ("air intake temperature",     lambda a, b, c: (c - 40)           , "C"    , (-40, 215)     , ("P0100", "P0113"))
        }

        sd_row = sensor_dict[s_sensor]
        sensor_name = sd_row[0]
        dtc_major, dtc_minor = sd_row[4]

        self.__frames_analyzed += 1

        if s_error == "ff":
            self.__single_event_error_count = 0
            self.__total_error_count += 1
            self.__dtcs_encountered.add(dtc_major)

            return f"{sensor_name} - DTC[MAJOR] - {dtc_major}"
        else:
            data_a, data_b, data_c = int(s_data_a, 16), int(s_data_b, 16), int(s_data_c, 16)
            measurement = round(sd_row[1](data_a, data_b, data_c), 2)
            min_val, max_val = sd_row[3]
            unit = sd_row[2]
            measurement_string = f"{measurement}{unit}" if unit == "%" else f"{measurement} {unit}"

            if s_error == "00":
                self.__single_event_error_count = 0
                return f"{sensor_name} - {measurement_string}"
            elif s_error == "0f":
                self.__total_error_count += 1
                self.__single_event_error_count += 1

                if self.__single_event_error_count >= 3:
                    self.__dtcs_encountered.add(dtc_minor)
                    return f"{sensor_name} - DTC[MINOR] - {dtc_minor}"
                
                return sensor_name if measurement < min_val or max_val < measurement else f"{sensor_name} - {measurement_string}"
            else:
                raise ValueError("Invalid error code")
            

        return ""
    
    def summary(self) -> str:
        dtc_table = {
           "P009B": "Fuel Pressure Relief Control Circuit/Open",
           "P0092": "Fuel Pressure Regulator 1 Control Circuit High",
           "P0725": "Engine Speed Input Circuit Malfunction",
           "P0321": "Ignition/Distributor Engine Speed Input Circuit Range/Performance",
           "P0500": "Vehicle Speed Sensor (VSS) Malfunction",
           "P0503": "Vehicle Speed Sensor A Intermittent",
           "P0223": "Throttle Position Sensor/Switch B Circuit High Input",
           "P0227": "Throttle Position Sensor Circuit Input Low",
           "P0451": "Evap Emission System Pressure Sensor Performance",
           "P0450": "Evap Emission System Pressure Sensor Malfunction",
           "P0195": "Engine Oil Temperature Sensor Malfunction",
           "P0196": "Engine Oil Temperature Sensor Range Performance",
           "P00B7": "Engine Coolant Flow Low/Performance",
           "P0117": "ECT Sensor Circuit Low Input",
           "P0100": "Air Intake Temperature Circuit Malfunction",
           "P0113": "Air Intake Temperature Circuit High Input"
        }

        return (f"Number of frames analyzed: {self.__frames_analyzed}\n"
        f"Total number of errors: {self.__total_error_count}\n"
        "DTCs encountered:\n"
        "| DTC Code |                            Description                            |\n"
        "|----------|-------------------------------------------------------------------|\n") + \
        '\n'.join(f"| {dtc_code:^8} | {dtc_table[dtc_code]:^65} |" for dtc_code in self.__dtcs_encountered)

