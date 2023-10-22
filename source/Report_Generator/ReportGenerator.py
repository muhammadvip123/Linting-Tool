"""
this file contains the debugger and report extractor which is coming from the engine
"""


class ReportGenerator:
    def __init__(self, Error_dictionary, File_name):
        self.Error_dic = Error_dictionary
        self.File_name = File_name
        self.Text_string = """
====================================================================
Lint Check Report
Design : """ + str(File_name) + """Sections
    Section 1 : Check Summary
    Section 2 : Check Details
====================================================================


====================================================================
Section 1 : Check Summary

------------------
| Errors (""" + str(sum(Error_dictionary["Num errors"])) + """) |
------------------
    Arithmetic over flow        :   """ + str(Error_dictionary["Num errors"][0]) + """
    Unreachable Blocks          :   """ + str(Error_dictionary["Num errors"][1]) + """
    Unreachable FSM State       :   """ + str(Error_dictionary["Num errors"][2]) + """
    Un-initialized Register     :   """ + str(Error_dictionary["Num errors"][3]) + """
    Multi-Driven Bus/Register   :   """ + str(Error_dictionary["Num errors"][4]) + """
    Non Full/Parallel Case      :   """ + str(Error_dictionary["Num errors"][5]) + """
    Infer Latch                 :   """ + str(Error_dictionary["Num errors"][6]) + """
====================================================================



====================================================================
Section 2 : Check Details
"""

    def Arange_lines(self, results):
        results_dic = {}
        # arithmetic overflow
        for i in range(len(results["Error line"][0])):
            if results["Error line"][0][i] in results_dic:
                results_dic[results["Error line"][0][i]] += "-- Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
            else:
                results_dic[results["Error line"][0][i]] = "Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
        for i in range(len(results["Error line"][1])):
            if results["Error line"][1][i] in results_dic:
                results_dic[results["Error line"][1][i]] += "-- unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
            else:
                results_dic[results["Error line"][1][i]] = "unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
        for i in range(len(results["Error line"][2])):
            if results["Error line"][2][i] in results_dic:
                results_dic[results["Error line"][2][i]] += "-- unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
            else:
                results_dic[results["Error line"][2][i]] = "unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
        for i in range(len(results["Error line"][3])):
            if results["Error line"][3][i] in results_dic:
                results_dic[results["Error line"][3][i]] += "-- uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
            else:
                results_dic[results["Error line"][3][i]] = "uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
        for i in range(len(results["variable Impacted"][4])):
            for line in results["Error line"][4][i]:
                if line in results_dic:
                    results_dic[line] += "-- multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
                else:
                    results_dic[line] = "multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
        for i in range(len(results["Error line"][5])):
            if results["Error line"][5][i] in results_dic:
                results_dic[results["Error line"][5][i]] += "-- Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
            else:
                results_dic[results["Error line"][5][i]] = "Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
        for i in range(len(results["variable Impacted"][6])):
            for line in results["Error line"][6][i]:
                if line in results_dic:
                    results_dic[line] += "-- latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][6][i])
                else:
                    results_dic[line] = "latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][6][i])
        return results_dic

    def print_lines(self):
        pass
