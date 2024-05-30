import pandas as pd
import plotly.graph_objects as go
import trc.evaluation.functional_test_cases.constants as fc
import trc.evaluation.functional_test_cases.ft_helper as fh
import trc.evaluation.functional_test_cases.PLP.MF.ft_helper as fhp
from trc.evaluation.functional_test_cases.PLP.MF.constants import ConstantsLSCA, PlotlyTemplate, GeneralConstants


class FtLSCA:
    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def name():
        """Name"""
        return "MF LSCA"

    @staticmethod
    def test_cluster_name():
        """
         entries can be one of following: "Functional Test", "Safety Test", "Other"
        """
        return fc.FUNCTIONAL_TEST

    @staticmethod
    def test_case_id():
        """Case Id"""
        return ["1", "2", "3"]

    @staticmethod
    def req_id():
        """Id"""
        return ["1", "2", "3"]

    @staticmethod
    def test_case_txt():
        """Case Message"""
        return [
            "Check the following conditions: \
                ('AP.lscaDisabled_nu' == 1 \
                AND 'Sensor.Collision.Vhcl.Fr1.Count' == 1 once \
                AND 'LSCA.statusPort.brakingModuleState_nu' == 0 \
                AND 'LSCA.brakePort.requestMode' == 0) \
                OR TestCase 2 OR TestCase 3",
            "Check the following conditions: \
                ('AP.evaluationPort.useCase_nu' == 0 \
                AND 'Sensor.Collision.Vhcl.Fr1.Count' == 1 once \
                AND 'LSCA.brakePort.requestMode' == 0) \
                OR TestCase 1 OR TestCase 3.",
            "Check the following conditions: \
                ('AP.lscaDisabled_nu has' == 0 \
                AND 'Sensor.Collision.Vhcl.Fr1.Count' == 0 \
                AND 'LSCA.brakePort.requestMode' == 2 once \
                AND 'LSCA.statusPort.brakingModuleState_nu' == 2) \
                OR TestCase 1 OR TestCase 2.",
        ]

    @staticmethod
    def projects():
        """
         possible entries "Honda GEN", "Knorr", "ARS540BW11"
        """
        return ["PARKING"]

    @staticmethod
    def planned_for():
        """Returns a string that contains the planned release for which the test is relevant"""
        return fc.NOT_AVAILABLE

    @staticmethod
    def safety_relevant():
        """
         possible entries SAFETY_RELEVANT_{QM}/{ASIL_A}/{ASIL_B}/{ASIL_C}/{ASIL_D}
        """
        return fc.NOT_AVAILABLE

    def calc(self, reader, ego_params, fun_platform, ignore_samples):
        test_case_name = self.name()
        test_cluster_name = self.test_cluster_name()
        test_result = fc.INPUT_MISSING  # Result

        # plots and remarks need to have the same length
        plot_titles, plots, remarks = fh.rep([], 3)

        '''signal handling'''
        try:
            basestring = fhp.Parking.get_base_string(reader, fun_platform)
            read_data = {}
            signal_name = {}
            for signal, signal_info in fhp.Parking.data_mapping(basestring).items():
                for name in signal_info['string']:
                    try:
                        read_data[signal] = reader[basestring + name]
                        signal_name[signal] = str([basestring + name]).replace("['", "").replace("']", "")
                        if read_data[signal] is not None:
                            break
                    except BaseException:
                        pass
            for signal, signal_info in fhp.Parking.data_mapping_EgoVehicle(basestring).items():
                try:
                    read_data[signal] = reader[signal_info['string']]
                    signal_name[signal] = str([signal_info['string']]).replace("['", "").replace("']", "")
                except (Exception,):
                    pass
        except BaseException:
            test_result = fc.INPUT_MISSING

        ap_usecase = read_data['ApUsecase']
        ap_lsca_disabled = read_data['lscaDisabled']
        lsca_request_mode = read_data['lscaRequestMode']
        lsca_braking_module_state = read_data['brakeModeState']
        ap_time = read_data['time']
        car_v = read_data['Car_v']
        sensor_collision_count = read_data['CollisionCount']

        class LscaFirstCheck:
            def __init__(self) -> None:
                self.test_result: str = fc.INPUT_MISSING
                self.sig_sum = None
                self.fig = None

            def run(self):
                t2 = 0
                signal_summary = {}
                evaluation_lsca_disabled_1 = ' '.join(f"The condition is PASSED, the value of \
                                                {signal_name['lscaDisabled']} is 1 all the time.".split())
                evaluation_collision_count = ' '.join(f"The condition is PASSED,the signal \
                                                {signal_name['CollisionCount']} has the value 1 minimum once.".split())
                evaluation_brake_mode_state = ' '.join(f"The condition is PASSED, the value of \
                                                {signal_name['brakeModeState']} is 0.".split())
                evaluation_lsca_request_mode = ' '.join(f"The condition is PASSED, the value of \
                                                {signal_name['lscaRequestMode']} is 0.".split())

                """ignore the first samples, because they might not be relevant"""
                for idx, val in enumerate(ap_time):
                    if val > 0:
                        t2 = idx
                        break

                if t2 is not None:
                    eval_cond = [True] * 4
                    for idx in range(t2, len(ap_time)):

                        if ap_lsca_disabled[idx] != 1 and eval_cond[0]:
                            evaluation_lsca_disabled_1 = ' '.join(f"The condition is FAILED, the value of \
                                                                    {signal_name['lscaDisabled']} is != 1 at \
                                                                    timestamp {round(ap_time[idx],3)} s.".split())
                            eval_cond[0] = False

                        if not (1 in sensor_collision_count) and eval_cond[1]:
                            evaluation_collision_count = ' '.join(f"The condition is FAILED, the value of \
                                                                    {signal_name['CollisionCount']} is !=1, first \
                                                                    point at {round(ap_time[idx], 3)} s.".split())
                            eval_cond[1] = False

                        if lsca_braking_module_state[idx] != 0 and eval_cond[2]:
                            evaluation_brake_mode_state = ' '.join(f"The condition is FAILED, the value of \
                                                                {signal_name['brakeModeState']} is  != 0 at \
                                                                timestamp {round(ap_time[idx], 3)} s.".split())
                            eval_cond[2] = False

                        if lsca_request_mode[idx] != 0 and eval_cond[3]:
                            evaluation_lsca_request_mode = ' '.join(f"The condition is FAILED, the value of \
                                                                    {signal_name['lscaRequestMode']} is  != 0 at \
                                                                    timestamp {round(ap_time[idx], 3)} s.".split())
                            eval_cond[3] = False

                if all(eval_cond):
                    self.test_result = fc.PASS
                else:
                    self.test_result = fc.FAIL

                signal_summary[signal_name['lscaDisabled']] = evaluation_lsca_disabled_1
                signal_summary[signal_name['CollisionCount']] = evaluation_collision_count
                signal_summary[signal_name['brakeModeState']] = evaluation_brake_mode_state
                signal_summary[signal_name['lscaRequestMode']] = evaluation_lsca_request_mode

                self.sig_sum = go.Figure(data=[go.Table(columnwidth=[3, 5],
                                                        header=dict(values=['Signal Evaluation', 'Summary'],
                                                                    align='center'),
                                                        cells=dict(values=[list(signal_summary.keys()),
                                                                           list(signal_summary.values())],
                                                                   height=42, align='center', font=dict(size=12)))])

                self.sig_sum.update_layout(height=fhp.Parking.calc_table_height(signal_summary))
                self.sig_sum.update_layout(PlotlyTemplate.drk_tmplt)

                if self.test_result == fc.FAIL or bool(GeneralConstants.ACTIVATE_PLOTS):
                    self.fig = go.Figure()
                    self.fig.add_trace(go.Scatter(x=ap_time, y=sensor_collision_count,
                                                  mode='lines', name=signal_name['CollisionCount']))
                    self.fig.add_trace(
                        go.Scatter(x=ap_time, y=ap_lsca_disabled, mode='lines', name=signal_name['lscaDisabled']))
                    self.fig.add_trace(
                        go.Scatter(x=ap_time, y=lsca_request_mode, mode='lines', name=signal_name['lscaRequestMode']))
                    self.fig.add_trace(
                        go.Scatter(x=ap_time, y=lsca_braking_module_state, mode='lines',
                                   name=signal_name['brakeModeState']))

                    self.fig.layout = go.Layout(autosize=True, yaxis=dict(tickformat="5"), xaxis=dict(tickformat="5"),
                                                xaxis_title="Time[s]")
                    self.fig.update_layout(PlotlyTemplate.drk_tmplt)

        class LscaSecondCheck:
            def __init__(self) -> None:
                self.test_result: str = fc.INPUT_MISSING
                self.sig_sum = None
                self.fig = None

            def run(self):
                t2 = 0
                signal_summary = {}

                evaluation_ap_usecase = ' '.join(f"The condition is PASSED, all values for signal \
                                                {signal_name['ApUsecase']} are == 0.".split())
                evaluation_collision_count = ' '.join(f"The condition is PASSED,the value of \
                                                {signal_name['CollisionCount']} is 1 minimum once.".split())
                evaluation_lsca_request_mode = ' '.join(f"The condition is PASSED, all values for signal \
                                                {signal_name['lscaRequestMode']} are 0.".split())

                for idx, val in enumerate(ap_time):
                    if val > 0:
                        t2 = idx
                        break

                if t2 is not None:
                    eval_cond = [True] * 3
                    for idx in range(t2, len(ap_time)):
                        if not (ap_usecase[idx] == 0) and eval_cond[0]:
                            evaluation_ap_usecase = ' '.join(f"The condition is FAILED, the value of \
                                                        {signal_name['ApUsecase']} is != 0 at timestamp \
                                                        {round(ap_time[idx], 3)} s.".split())
                            eval_cond[0] = False
                        if not (1 in sensor_collision_count) and eval_cond[1]:
                            evaluation_collision_count = ' '.join(f"The condition is FAILED, the value of \
                                                            {signal_name['CollisionCount']} is never 1.".split())
                            eval_cond[1] = False
                        if not (lsca_request_mode[idx] == 0) and eval_cond[2]:
                            evaluation_lsca_request_mode = ' '.join(f"The condition is FAILED, the value of \
                                                            {signal_name['lscaRequestMode']} is != 0 at \
                                                            timestamp {round(ap_time[idx], 3)} s.".split())
                            eval_cond[2] = False
                if all(eval_cond):
                    self.test_result = fc.PASS
                else:
                    self.test_result = fc.FAIL

                signal_summary[signal_name['ApUsecase']] = evaluation_ap_usecase
                signal_summary[signal_name['CollisionCount']] = evaluation_collision_count
                signal_summary[signal_name['lscaRequestMode']] = evaluation_lsca_request_mode

                self.sig_sum = go.Figure(data=[go.Table(columnwidth=[3, 5],
                                                        header=dict(values=['Signal Evaluation', 'Summary'],
                                                                    align='center'),
                                                        cells=dict(values=[list(signal_summary.keys()),
                                                                           list(signal_summary.values())],
                                                                   height=42, align='center', font=dict(size=12)))])
                self.sig_sum.update_layout(height=fhp.Parking.calc_table_height(signal_summary))
                self.sig_sum.update_layout(PlotlyTemplate.drk_tmplt)

                if self.test_result == fc.FAIL or bool(GeneralConstants.ACTIVATE_PLOTS):
                    self.fig = go.Figure()
                    self.fig.add_trace(
                        go.Scatter(x=ap_time, y=car_v, mode='lines', name=signal_name['Car_v']))
                    self.fig.add_trace(
                        go.Scatter(x=ap_time, y=sensor_collision_count, mode='lines',
                                   name=signal_name['CollisionCount']))

                    self.fig.layout = go.Layout(yaxis=dict(tickformat="20"), xaxis=dict(tickformat="20"),
                                                xaxis_title="Time[s]")
                    self.fig.update_layout(PlotlyTemplate.drk_tmplt)

        class LscaThirdCheck:
            def __init__(self) -> None:
                self.test_result: str = fc.INPUT_MISSING
                self.sig_sum = None
                self.fig = None

            def run(self):
                t2 = 0
                signal_summary = {}

                evaluation_lsca_disabled_0 = ' '.join(f"The condition is PASSED, the value of \
                                                {signal_name['lscaDisabled']} is = 0.".split())
                evaluation_collision_count_1 = ' '.join(f"The condition is PASSED,all the value of \
                                                    {signal_name['CollisionCount']} is = 0.".split())
                evaluation_brake_mode_state_2 = ' '.join(f"The condition is PASSED, the value of \
                                                    {signal_name['brakeModeState']} is equale with 2 \
                                                    minimum once.".split())
                evaluation_lsca_request_mode_2 = ' '.join(f"The condition is PASSED, the value of \
                                                    {signal_name['lscaRequestMode']}is equale with 2 \
                                                    minimum once.".split())

                for idx, val in enumerate(ap_time):
                    if val > 0:
                        t2 = idx
                        break

                if t2 is not None:
                    eval_cond = [True] * 4
                    for idx in range(t2, len(ap_time)):

                        if ap_lsca_disabled[idx] != 0 and eval_cond[0]:
                            evaluation_lsca_disabled_0 = ' '.join(f"The condition is FAILED, the value of \
                                                            {signal_name['lscaDisabled']} is != 0 at \
                                                            timestamp {round(ap_time[idx], 3)} s.".split())
                            eval_cond[0] = False
                        if sensor_collision_count[idx] != 0 and eval_cond[1]:
                            evaluation_collision_count_1 = ' '.join(f"The condition is FAILED, the value of \
                                                                {signal_name['CollisionCount']} is != 0 at\
                                                                timestamp {round(ap_time[idx], 3)} s.".split())
                            eval_cond[1] = False
                        if not (ConstantsLSCA.VAL_LSCA in lsca_braking_module_state[t2:]) and eval_cond[2]:
                            evaluation_brake_mode_state_2 = ' '.join(f"The condition is FAILED, the value of \
                                                                {signal_name['brakeModeState']} = \
                                                                {ConstantsLSCA.VAL_LSCA} was never found.".split())
                            eval_cond[2] = False
                        if not (ConstantsLSCA.VAL_LSCA in lsca_braking_module_state[t2:]) and eval_cond[3]:
                            evaluation_lsca_request_mode_2 = ' '.join(f"The condition is FAILED, the value of \
                                                                    {signal_name['lscaRequestMode']} = \
                                                                    {ConstantsLSCA.VAL_LSCA} was never found.".split())
                            eval_cond[3] = False

                if all(eval_cond):
                    self.test_result = fc.PASS
                else:
                    self.test_result = fc.FAIL

                signal_summary[f" {signal_name['lscaDisabled']}"] = evaluation_lsca_disabled_0
                signal_summary[f" {signal_name['CollisionCount']}"] = evaluation_collision_count_1
                signal_summary[f" {signal_name['brakeModeState']}"] = evaluation_brake_mode_state_2
                signal_summary[f" {signal_name['lscaRequestMode']}"] = evaluation_lsca_request_mode_2

                self.sig_sum = go.Figure(data=[go.Table(columnwidth=[3, 5],
                                                        header=dict(values=['Signal Evaluation', 'Summary'],
                                                                    align='center'),
                                                        cells=dict(values=[list(signal_summary.keys()),
                                                                           list(signal_summary.values())],
                                                                   height=42, align='center', font=dict(size=12)))])
                self.sig_sum.update_layout(height=fhp.Parking.calc_table_height(signal_summary))
                self.sig_sum.update_layout(PlotlyTemplate.drk_tmplt)

        lsca_1 = LscaFirstCheck()
        lsca_1.run()

        lsca_2 = LscaSecondCheck()
        lsca_2.run()

        lsca_3 = LscaThirdCheck()
        lsca_3.run()

        if lsca_1.test_result is fc.PASS or lsca_2.test_result is fc.PASS or lsca_3.test_result is fc.PASS:
            test_result = fc.PASS
        else:
            test_result = fc.FAIL

        plot_titles.append("Signal Evaluation")
        plots.append(lsca_1.sig_sum)
        remarks.append(
            "TestCase 1"
        )

        plot_titles.append("")
        plots.append(lsca_2.sig_sum)
        remarks.append(
            "TestCase 2"
        )

        plot_titles.append("")
        plots.append(lsca_3.sig_sum)
        remarks.append(
            "TestCase 3"
        )

        if lsca_1.fig:
            plot_titles.append("Graphical Overview")
            plots.append(lsca_1.fig)
            remarks.append("Test Graphics LSCA")
        if lsca_2.fig:
            plot_titles.append(" ")
            plots.append(lsca_2.fig)
            remarks.append("Test Graphics evaluation CarMaker")

        result_df = pd.DataFrame(
            {fc.REQ_ID: [self.req_id()[i] for i in range(0, 3)],
             fc.TESTCASE_ID: [self.test_case_id()[i] for i in range(0, 3)],
             fc.TEST_SAFETY_RELEVANT: [self.safety_relevant() for _ in range(0, 3)],
             fc.TEST_DESCRIPTION: [self.test_case_txt()[i] for i in range(0, 3)],
             fc.TEST_RESULT: [lsca_1.test_result, lsca_2.test_result, lsca_3.test_result]})

        max_collision = max(sensor_collision_count)
        additional_results_dict = {
            "max Collisions": {"value": max_collision,
                               "color": 'rgb(33,39,43)'}}
        return test_case_name, test_cluster_name, plot_titles, plots, remarks, result_df, test_result, \
            additional_results_dict