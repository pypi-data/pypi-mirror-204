import logging
import os


def validate_sigma_model_data(model_data, constants):
    """
    Method checks the SIGMA options in the model_data to be valid to parse into SIGMA.
    :return:
    """
    logging.getLogger().setLevel(logging.INFO)

    # logging.warning('And this, too')
    options_sigma = model_data.Options_SIGMA

    # Check key time_vector_solution.time_step
    time_step = options_sigma.time_vector_solution.time_step
    # Check type list[list] with three values
    if type(time_step) == list:
        if any(isinstance(el, list) for el in time_step):
            # Check data in vector is valid;
            for i in range(len(time_step)):
                if len(time_step[i]) == 3:
                    if time_step[i][0] > time_step[i][2]:
                        raise ValueError(
                            "Options_SIGMA.time_vector_solution.time_step has invalid data. Start value can not be larger than end value.")
                    else:
                        logging.info('time_vector_solution valid')
                    if i <= len(time_step) - 2:
                        if time_step[i][2] > time_step[i + 1][0]:
                            raise ValueError(
                                "Options_SIGMA.time_vector_solution.time_step has overlapping time step intervals")
                else:
                    raise ValueError(
                        "Options_SIGMA.time_vector_solution.time_step has invalid data. Three element per sublist needed")

    # Check Options_SIGMA.simulation
    study_type = options_sigma.simulation.study_type
    print(constants.LABEL_TRANSIENT)
    if study_type == constants.LABEL_TRANSIENT or study_type == constants.LABEL_STATIONARY:
        pass
    else:
        raise ValueError(f"String is not Transient or Stationary.")

    # Check Options_SIGMA.physics
    for key, value in options_sigma.physics:
        print(key, value)
        if value is None:
            logging.warning(f'{key} is set to null. To make sigma run this will be set to 0 as default.')
        if key == "tauCC_PE":
            logging.warning(f'{key} SPECIAL CASE!')
    # Check Options_SIGMA.quench_initialization
    for key, value in options_sigma.quench_initialization:
        if "FLAG" in key:
            if value is None:
                logging.warning(f'{key} is set to null. To make sigma run this will be set to 0 as default.')
        if key == "num_qh_div":
            if len(value) != model_data.Quench_Protection.Quench_Heaters.N_strips:
                raise ValueError(
                    f"The number of quench heater divisions must be {model_data.Quench_Protection.Quench_Heaters.N_strips}")
        if key == "quench_init_heat":
            if value is None:
                raise ValueError(f"{key} can't be none")
            else:
                if value < 0:
                    raise ValueError("Power for initialize quench can't be negative")
        if key == "quench_stop_temp":
            if value is None:
                raise ValueError(f"{key} can't be none")
            if value < 0:
                raise ValueError("Tempereatur for initialize quench can't be negative")

    # Check Options_SIGMA.postprocessing.out_2D_at_points
    for key, value in options_sigma.postprocessing.out_2D_at_points:
        if key == "coordinate_source":
            # Check if source exists
            if value is not None:
                if not os.path.exists(value):
                    raise ValueError("Given coordinate file path does not exist")

                else:
                    logging.info("Using coordinate file to evaluate 2D plots")

        if key == "time":
            # Check number of values
            if len(value) != len(options_sigma.postprocessing.out_2D_at_points.variables):
                raise ValueError("Number of time vectors must be the same as number of variables.")
            else:
                for i in range(len(value)):
                    if len(value[i]) == 3:
                        if value[0] > value[2]:
                            raise ValueError(
                                "Options_SIGMA.postprocessing.out_2D_at_points.time has invalid data. Start value can not be larger than end value.")
                        else:
                            logging.info('time_vector_solution valid')
                    else:
                        raise ValueError(
                            "Options_SIGMA.postprocessing.out_2D_at_points.time has invalid data. Three elements needed.")

    for key, value in options_sigma.postprocessing.out_1D_vs_times:
        if key == "time":
            # Check number of values
            if len(value) != len(options_sigma.postprocessing.out_1D_vs_times.variables):
                raise ValueError("Number of time vectors must be the same as number of variables.")
            else:
                for i in range(len(value)):
                    if len(value[i]) == 3:
                        if value[0] > value[2]:
                            raise ValueError(
                                f"Options_SIGMA.postprocessing.out_1D_vs_times.time has invalid data for value {value}. Start value can not be larger than end value.")
                    else:
                        raise ValueError(
                            "Options_SIGMA.postprocessing.out_1D_vs_times.time has invalid data. Three elements needed.")

    # Options_SIGMA.quench_heaters
    # th_coils = options_sigma.quench_heaters.th_coils
    # if 0 in th_coils:
    #     raise ValueError("List contains zero values")


def helper_check_time_step_valid(time_step):
    if type(time_step) == list:
        if any(isinstance(el, list) for el in time_step):
            # Check data in vector is valid;
            for i in range(len(time_step)):
                if len(time_step[i]) == 3:
                    if time_step[i][0] > time_step[i][2]:
                        raise ValueError(
                            "#Options_SIGMA.time_vector_solution.time_step has invalid data. Start value can not be larger than end value.")
                    else:
                        logging.info('time_vector_solution valid')
                    if i <= len(time_step) - 2:
                        if time_step[i][2] > time_step[i + 1][0]:
                            raise ValueError(
                                "Options_SIGMA.time_vector_solution.time_step has overlapping time step intervals")
                else:
                    raise ValueError(
                        "Options_SIGMA.time_vector_solution.time_step has invalid data. Three element per sublist needed")


def build_global_variables(g, model_data):
    """
    Function builds all global variables nessesary for QH simulations.
    :return: map with global variables
    """
    map = g.gateway.jvm.java.util.HashMap()
    constants = g.MPHC
    FLAG_M_pers = model_data.Options_SIGMA.physics.FLAG_M_pers
    FLAG_M_pers = "0" if FLAG_M_pers is None else FLAG_M_pers

    FLAG_ifcc = model_data.Options_SIGMA.physics.FLAG_ifcc
    FLAG_ifcc = "0" if FLAG_ifcc is None else FLAG_ifcc

    FLAG_iscc_crossover = model_data.Options_SIGMA.physics.FLAG_iscc_crossover
    FLAG_iscc_crossover = "0" if FLAG_iscc_crossover is None else FLAG_iscc_crossover

    FLAG_iscc_adjw = model_data.Options_SIGMA.physics.FLAG_iscc_adjw
    FLAG_iscc_adjw = "0" if FLAG_iscc_adjw is None else FLAG_iscc_adjw

    FLAG_iscc_adjn =  model_data.Options_SIGMA.physics.FLAG_iscc_adjn
    FLAG_iscc_adjn = "0" if FLAG_iscc_adjn is None else FLAG_iscc_adjn

    FLAG_quench_all =  model_data.Options_SIGMA.quench_initialization.FLAG_quench_all
    FLAG_quench_all = "0" if FLAG_quench_all is None else FLAG_quench_all

    FLAG_quench_off = model_data.Options_SIGMA.quench_initialization.FLAG_quench_off
    FLAG_quench_off = "0" if FLAG_quench_off is None else FLAG_quench_off


    PARAM_time_quench = model_data.Options_SIGMA.quench_initialization.PARAM_time_quench
    PARAM_time_quench = "0" if PARAM_time_quench is None else PARAM_time_quench

    magnetic_length = model_data.GeneralParameters.magnetic_length
    T_initial = model_data.GeneralParameters.T_initial

    quench_heat = model_data.Options_SIGMA.quench_initialization.quench_init_heat
    quench_temp = model_data.Options_SIGMA.quench_initialization.quench_stop_temp

    map.put(constants.LABEL_FLAG_IFCC, FLAG_ifcc)
    map.put(constants.LABEL_FLAG_ISCC_CROSSOVER, FLAG_iscc_crossover)
    map.put(constants.LABEL_FLAG_ISCC_ADJW, FLAG_iscc_adjw)
    map.put(constants.LABEL_FLAG_ISCC_ADJN, FLAG_iscc_adjn)
    map.put(constants.LABEL_FLAG_MPERS, FLAG_M_pers)
    map.put(constants.LABEL_FLAG_QUENCH_ALL, FLAG_quench_all)
    map.put(constants.LABEL_FLAG_QUENCH_OFF, FLAG_quench_off)
    map.put(constants.LABEL_PARAM_QUENCH_TIME, PARAM_time_quench)
    map.put(constants.LABEL_MAGNETIC_LENGTH, magnetic_length)
    map.put(constants.LABEL_OPERATIONAL_TEMPERATUR, str(T_initial))
    map.put(constants.LABEL_INIT_QUENCH_HEAT, str(quench_heat))
    map.put(constants.LABEL_QUENCH_TEMP, str(quench_temp))

    ins_list = model_data.Quench_Protection.Quench_Heaters.s_ins
    w_list = model_data.Quench_Protection.Quench_Heaters.w
    qh_to_bath_list = model_data.Quench_Protection.Quench_Heaters.s_ins_He
    qh_steel_strip = model_data.Quench_Protection.Quench_Heaters.h
    tau = [round(a*b, 4) for a,b in zip(model_data.Quench_Protection.Quench_Heaters.R_warm,model_data.Quench_Protection.Quench_Heaters.C)]
    num_qh_div = model_data.Options_SIGMA.quench_initialization.num_qh_div
    u_init = model_data.Quench_Protection.Quench_Heaters.U0
    i_init = [round(a/b, 3) for a,b in zip(model_data.Quench_Protection.Quench_Heaters.U0,model_data.Quench_Protection.Quench_Heaters.R_warm)]
    frac_heater = model_data.Quench_Protection.Quench_Heaters.f_cover
    trigger_time = model_data.Quench_Protection.Quench_Heaters.t_trigger
    ins_thick_to_coil = model_data.Options_SIGMA.quench_heaters.th_coils
    lengths_qh = model_data.Quench_Protection.Quench_Heaters.l

    for i in range(model_data.Quench_Protection.Quench_Heaters.N_strips):
        if model_data.Options_SIGMA.time_vector_solution.time_step[-1][-1] < trigger_time[i]:
            trigger_time[i] = model_data.Options_SIGMA.time_vector_solution.time_step[-1][-1]
        map.put(constants.LABEL_INSULATION_THICKNESS_QH_TO_COIL+str(i+1), str(ins_list[i]))
        map.put(constants.LABEL_WIDTH_QH+str(i+1), str(w_list[i]))
        map.put(constants.LABEL_INSULATION_THICKNESS_QH_TO_BATH+str(i+1), str(qh_to_bath_list[i]))
        map.put(constants.LABEL_INSULATION_THICKNESS_QH_STRIP + str(i + 1), str(qh_steel_strip[i]))
        map.put(constants.LABEL_EXPONENTIAL_TIME_CONSTANT_DECAY + str(i + 1), str(tau[i]))
        map.put(constants.LABEL_QH + constants.LABEL_L + str(i + 1), str(lengths_qh[i]))
        map.put(constants.LABEL_NUMBER_OF_QH_SUBDIVISIONS + str(i + 1), str(num_qh_div[i]))
        map.put(constants.LABEL_INITIAL_QH_CURRENT + str(i + 1), str(i_init[i]))
        map.put(constants.LABEL_INITIAL_QH_VOLTAGE + str(i + 1), str(u_init[i]))
        map.put(constants.LABEL_QH  + str(i + 1) + constants.LABEL_FRACTION_OF_QH_STATION, str(frac_heater[i]))
        map.put(constants.LABEL_TRIGGER_TIME_QH + str(i + 1), str(trigger_time[i]))
        map.put(constants.LABEL_INSULATION_THICKNESS_TO_COIL + str(i + 1), str(ins_thick_to_coil[i]))

    return map
