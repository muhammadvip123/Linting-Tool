from source.Parser.VerilogParser import *


################################################################################
#################################################################

class Checks:
    def __init__(self, file):  # add attribuites
        self.LHS_LIST_LINES = None
        self.LHS_LIST = None
        l = Lexer(file)
        l.doLexing()
        v = VerilogParser(file)
        self.error_panel = {
            "Type": ("Arithmetic Overflow", "Unreachable Blocks", "Unreachable FSM State", "Un-initialized Register",
                     "Multi-Driven Bus/Register", "Non Full/Parallel Case", "Infer Latch"),
            "Num errors": [0, 0, 0, 0, 0, 0, 0],
            "Error line": [[], [], [], [], [], [], []],
            "variable Impacted": [[], [], [], [], [], [], []]
        }
        self.main_node = v.Parse()

    ##################################################################
    # Arithmetic Overflow
    def check_arithmetic_overflow(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            for cont_assignment in Recursiveobject.continuous_assignment:
                if cont_assignment.left.size < cont_assignment.right.size:
                    self.error_panel["Num errors"][0] += 1
                    self.error_panel["Error line"][0].append(cont_assignment.line)
                    self.error_panel["variable Impacted"][0].append(cont_assignment.left.name)
            for always_block in Recursiveobject.procedual_assignment:
                for Assignment in always_block.Allblocks:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.left.size < Assignment.right.size:
                            self.error_panel["Num errors"][0] += 1
                            self.error_panel["Error line"][0].append(Assignment.line)
                            self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.check_arithmetic_overflow(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_arithmetic_overflow(Assignment)
        elif isinstance(Recursiveobject, IfCondition):
            for Assignment in Recursiveobject.TrueStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.left.size < Assignment.right.size:
                        self.error_panel["Num errors"][0] += 1
                        self.error_panel["Error line"][0].append(Assignment.line)
                        self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.check_arithmetic_overflow(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_arithmetic_overflow(Assignment)
            for Assignment in Recursiveobject.FalseStatements:
                if isinstance(Assignment, ContinuousAssignment):
                    if Assignment.left.size < Assignment.right.size:
                        self.error_panel["Num errors"][0] += 1
                        self.error_panel["Error line"][0].append(Assignment.line)
                        self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                elif isinstance(Assignment, IfCondition):
                    self.check_arithmetic_overflow(Assignment)
                elif isinstance(Assignment, CaseStatement):
                    self.check_arithmetic_overflow(Assignment)
        elif isinstance(Recursiveobject, CaseStatement):
            for keys in Recursiveobject.items:
                statements = Recursiveobject.items[keys]
                for Assignment in statements:
                    if isinstance(Assignment, ContinuousAssignment):
                        if Assignment.left.size < Assignment.right.size:
                            self.error_panel["Num errors"][0] += 1
                            self.error_panel["Error line"][0].append(Assignment.line)
                            self.error_panel["variable Impacted"][0].append(Assignment.left.name)
                    elif isinstance(Assignment, IfCondition):
                        self.check_arithmetic_overflow(Assignment)
                    elif isinstance(Assignment, CaseStatement):
                        self.check_arithmetic_overflow(Assignment)

    ##################################################################
    # Unreachable Blocks Func
    def check_unreachable_blocks(self, ip):
        print(f'Check Unreachable Blocks {ip}')
        return ip

    ##################################################################
    # Unreachable FSM State Func
    def check_unreachable_fSM_state(self, ip):
        print(f'Check  Unreachable FSM State {ip}')
        return ip

    ###########################################################################
    # Un-initialized Register Func
    def check_uninitialized_register(self, ip):
        print(f'Check Un-initialized Register {ip}')
        return ip

    ##################################################################
    # Multi-Driven Bus/Register
    def check_multi_Driven_bus_register(self, Recursiveobject):
        if isinstance(Recursiveobject, VerilogModule):
            self.LHS_LIST = []
            self.LHS_LIST_LINES = []
            for cont_assignment in Recursiveobject.continuous_assignment:
                if cont_assignment.left.name in self.LHS_LIST:
                    self.error_panel["Num errors"][4] += 1
                    self.error_panel["Error line"][4].append(
                        [self.LHS_LIST.index(cont_assignment.left.name), cont_assignment.line])
                    self.error_panel["variable Impacted"][4].append(cont_assignment.left.name)
                else:
                    self.LHS_LIST.append(cont_assignment.left.name)
                    self.LHS_LIST_LINES.append(cont_assignment.line)

 ##################################################################################################################################################
            list_non_overlab = set([])
            z=[]
            i = 1
            for always_block in Recursiveobject.procedual_assignment:
                j = 1
                for always_block_2 in Recursiveobject.procedual_assignment:
                    if always_block == always_block_2:
                        continue
                    else:

                        common = set(always_block.LHS).intersection(set(always_block_2.LHS))
                        print(f'common{common}')
                        print(f'non over lap{list_non_overlab}')
                        if not list_non_overlab:
                            list_non_overlab = common
                            diff = list_non_overlab
                            print("first")
                            print(f'empty{list_non_overlab}')
                        elif (common ^ list_non_overlab):
                            diff = list(common - list_non_overlab)
                            list_non_overlab=set(list(list_non_overlab)+diff)
                            print(f'difffffff{diff}')
                            print(f'yarrrrrrb{list_non_overlab}')
                            print("second")

                        else:
                            print(f'Sameeeeeee')
                            # for index in common:
                            #     x = always_block.LHS.index(index)
                            #     lines_1st_always = always_block.LHS_LINES[x]
                            #     y = always_block_2.LHS.index(index)
                            #     lines_2st_always = always_block_2.LHS_LINES[y]
                            #     mixed_list = lines_1st_always + lines_2st_always
                            #     #self.LHS_LIST.append(always_block.LHS[x])
                            #     self.LHS_LIST_LINES.append(mixed_list)
                            #     print(f'csccc{self.LHS_LIST}')
                            #     print(f'sfsf{self.LHS_LIST_LINES}')

                            j = j + 1
                            print(f"{i} ,{j}round")
                            continue
                        print(f'testtttttttttt{list_non_overlab}')
                        print(f'difffffff{diff}')
                        print(f'1r{always_block.LHS}')
                        print(f'2r{always_block.LHS_LINES}')
                        print(f'3rr{always_block_2.LHS}')
                        print(f'5rr{always_block_2.LHS_LINES}')
                        length = len(list_non_overlab)
                        z = z + [None] * (length - len(z))
                        mixed_list=[]
                        for index in common:
                            if(index in list_non_overlab ):
                                elem_ind = list(list_non_overlab).index(index)
                                x = always_block.LHS.index(index)
                                lines_1st_always = always_block.LHS_LINES[x]
                                y = always_block_2.LHS.index(index)
                                lines_2st_always = always_block_2.LHS_LINES[y]
                                mixed_list = lines_1st_always + lines_2st_always
                                #print(self.LHS_LIST_LINES)
                                print(elem_ind)
                                print(z[elem_ind])
                                if(z[elem_ind]==None):
                                    z[elem_ind] = mixed_list
                                else:
                                    z[elem_ind] = z[elem_ind] + mixed_list
                                #self.LHS_LIST_LINES[x] = (z + mixed_list)
                                #self.LHS_LIST_LINES[elem_ind] = (self.LHS_LIST_LINES[elem_ind] + mixed_list)
                            else:
                                x = always_block.LHS.index(index)
                                lines_1st_always = always_block.LHS_LINES[x]
                                y = always_block_2.LHS.index(index)
                                lines_2st_always = always_block_2.LHS_LINES[y]
                                mixed_list = lines_1st_always + lines_2st_always
                                z[elem_ind] = z[elem_ind] + mixed_list
                                #self.LHS_LIST.append(index)
                                #self.LHS_LIST_LINES.append(mixed_list)
                            print(f'list_non_overlab{list_non_overlab}')
                            print(f'zzzz{z}')
            for t in range(len (list_non_overlab)):
                z[t] = sorted(list(dict.fromkeys(z[t])))

            print(f'over lap{list_non_overlab}')
            print(f'Lines{z}')




# ################################################################################################3








    ####################################################################
    # Non full parallel Case func
    def check_non_full_parallel_case(self, ip):
        print(f'Check Non full parallel Case func {ip}')
        return ip

    ##################################################################
    # Infer Latch func
    def check_infer_latch(self, ip):
        print(f'Check Infer Latch func {ip}')
        return ip

    pass


Check = Checks("adder.v")
Check.check_arithmetic_overflow(Check.main_node)
Check.check_multi_Driven_bus_register(Check.main_node)
print(Check.error_panel)

# op = Check.check_infer_latch(ip=5)

# op1 = Check.check_non_full_parallel_case(ip=8)
#
# op2 = Check.check_uninitialized_register(ip=10)
#
# op3 = Check.check_unreachable_blocks(ip=12)

#############################################################################
# error_list = ("Arithmetic Overflow", "Unreachable Blocks", "Unreachable FSM State", "Un-initialized Register",
#               "Multi-Driven Bus/Register", "Non Full/Parallel Case", "Infer Latch")
# n_error_arithmetic_overflow = 5
# n_error_unreachable_blocks = 5
# n_error_unreachable_fSM_state = 8
# n_error_multi_Driven_bus_register = 8
# n_error_non_full_parallel_case = 10
# n_error_uninitialized_register = 10
# n_error_infer_latch = 12
#
# lines_error_arithmetic_overflow = [2, 4, 6, 8, 10]
# lines_error_unreachable_blocks = [3, 6, 9, 12, 15]
# lines_error_unreachable_fSM_state = [4, 8, 12, 16, 20]
# lines_error_multi_Driven_bus_register = [5, 10, 12, 18, 33]
# lines_error_non_full_parallel_case = [2, 4, 6, 8, 10]
# lines_error_uninitialized_register = [4, 8, 12, 16, 20]
# lines_error_infer_latch = [2, 4, 6, 8, 10]
#
# var_impacted_arithmetic_overflow = ["x", "z", "m", "t"]
# var_impacted_unreachable_blocks = ["x", "z", "m", "t"]
# var_impacted_unreachable_fSM_state = ["x", "z", "m", "t"]
# var_impacted_multi_Driven_bus_register = ["x", "z", "m", "t"]
# var_impacted_non_full_parallel_case = ["x", "z", "m", "t"]
# var_impacted_uninitialized_register = ["x", "z", "m", "t"]
# var_impacted_infer_latch = ["x", "z", "m", "t"]
#
# error_panel = {"Type": error_list,
#                "Num errors": (n_error_arithmetic_overflow, n_error_unreachable_blocks, n_error_unreachable_fSM_state,
#                               n_error_multi_Driven_bus_register, n_error_non_full_parallel_case,
#                               n_error_uninitialized_register,
#                               n_error_infer_latch),
#                "Error line": (
#                    lines_error_arithmetic_overflow, lines_error_unreachable_blocks, lines_error_unreachable_fSM_state,
#                    lines_error_multi_Driven_bus_register, lines_error_non_full_parallel_case,
#                    lines_error_uninitialized_register, lines_error_infer_latch),
#                "variable Impacted": (
#                    var_impacted_arithmetic_overflow, var_impacted_unreachable_blocks,
#                    var_impacted_unreachable_fSM_state,
#                    var_impacted_multi_Driven_bus_register, var_impacted_non_full_parallel_case,
#                    var_impacted_uninitialized_register, var_impacted_infer_latch),
#
#                }
# #
# # print(error_panel["Type"])
# # print(error_panel["Num errors"])
# # print(error_panel["Num errors"].__getitem__(3))
# # print(f'lines of errors of {error_panel["Type"].__getitem__(0)} is {error_panel["Num errors"].__getitem__(0)} &'
# #       f' place at {error_panel["Error line"].__getitem__(0)}')
