from source.Parser.CoreFunctions import *
import threading

"""
this file contains the base class for all the required nodes by the
parser
"""


class ContinuousAssignment:
    def __init__(self, left, right, lineNum):
        self.left = left
        self.right = right
        self.line = lineNum
        self.contributors = []
        self.operations = []
        self.left_nBits = (1 << self.left.size) - 1
        self.get_contributors(self.right)
        self.operations.reverse()

    def get_contributors(self, objsearch):
        if isinstance(objsearch, UnaryOperations):
            self.operations.append("Reduction " + objsearch.type)
            self.get_contributors(objsearch.operand)
        elif isinstance(objsearch, BaseOperations):
            self.operations.append(objsearch.type)
            self.get_contributors(objsearch.right)
            self.get_contributors(objsearch.left)
        else:
            self.contributors.append(objsearch)

    def run_assignment(self):
        if self.right.value != "x":
            self.left.value = self.right.value & self.left_nBits
        else:
            self.left.value = "x"


class ProcedualAssignment:
    def __init__(self, sensitivity_list, blocks, Start_end_list):
        self.sensitivity_list = sensitivity_list
        self.Allblocks = blocks
        self.start_line = Start_end_list[0]
        self.end_line = Start_end_list[1]
        self.LHS = []
        self.LHS_LINES = []
        self.get_all_LHS(self)

    def get_all_LHS(self, ObjectRecursive):
        if isinstance(ObjectRecursive, ProcedualAssignment):
            for statement in ObjectRecursive.Allblocks:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)
                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
        elif isinstance(ObjectRecursive, IfCondition):
            for statement in ObjectRecursive.TrueStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)
                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
            for statement in ObjectRecursive.FalseStatements:
                if isinstance(statement, ContinuousAssignment):
                    if statement.left.name in self.LHS:
                        index = self.LHS.index(statement.left.name)
                        self.LHS_LINES[index].append(statement.line)
                    else:
                        self.LHS.append(statement.left.name)
                        self.LHS_LINES.append([statement.line])
                elif isinstance(statement, IfCondition):
                    self.get_all_LHS(statement)
                elif isinstance(statement, CaseStatement):
                    self.get_all_LHS(statement)
        elif isinstance(ObjectRecursive, CaseStatement):
            for key in ObjectRecursive.items:
                statements = ObjectRecursive.items[key]
                for statement in statements:
                    if isinstance(statement, ContinuousAssignment):
                        if statement.left.name in self.LHS:
                            index = self.LHS.index(statement.left.name)
                            self.LHS_LINES[index].append(statement.line)
                        else:
                            self.LHS.append(statement.left.name)
                            self.LHS_LINES.append([statement.line])
                    elif isinstance(statement, IfCondition):
                        self.get_all_LHS(statement)
                    elif isinstance(statement, CaseStatement):
                        self.get_all_LHS(statement)



class IfCondition:
    def __init__(self, cond, TrueStatements, FalseStatements, lines):
        self.condition = cond
        self.TrueStatements = TrueStatements
        self.FalseStatements = FalseStatements
        self.start_line = lines[0]
        self.stop_line = lines[1]
        self.current_statements = []


class CaseStatement:
    def __init__(self, Statement, Items):
        self.statement = Statement
        self.items = Items
        self.current_item = []


class ContinuousObserver:
    def __init__(self):
        self.subscribers = set()

    def Register(self, block):
        self.subscribers.add(block)

    def update(self):
        for subscriber in self.subscribers:
            subscriber.run_assignment()


class Constant:
    def __init__(self, value, size):
        self.value = value
        self.size = size


class SignalNode:
    def __init__(self, name, type, size, observer):
        self._value = "x"
        self.size = size
        self.name = name
        self.type = type
        self.observer = observer

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, valuechng):
        if valuechng != self._value:
            self._value = valuechng
            self.observer.update()


class VerilogModule:
    def __init__(self, name):
        self.module_name = name
        self.inputs = {}
        self.outputs = {}
        self.internal = {}
        self.continuous_assignment = []
        self.procedual_assignment = []

    def add_input(self, inputAdd: SignalNode):
        self.inputs[inputAdd.name] = inputAdd

    def add_output(self, outputAdd: SignalNode):
        self.outputs[outputAdd.name] = outputAdd

    def add_internal(self, internalAdd: SignalNode):
        self.internal[internalAdd.name] = internalAdd

    def add_always(self, alwaysAdd):
        self.procedual_assignment.append(alwaysAdd)

    def add_assign(self, assignAdd: ContinuousAssignment):
        self.continuous_assignment.append(assignAdd)


class BaseOperations:
    def __init__(self, type: str, left, right, size):
        self.type = type
        self.left = left
        self.right = right
        self.size = size

    @property
    def value(self):
        # print("type is " + self.type + " and left value is " + str(self.left.value) + " and right is "+str(self.right.value))
        if not (self.left.value == "x" or self.right.value == "x"):
            if self.type == "&":
                return self.left.value & self.right.value
            elif self.type == "|":
                return self.left.value | self.right.value
            elif self.type == "^":
                return self.left.value ^ self.right.value
            elif self.type == "+":
                return self.left.value + self.right.value
            elif self.type == "*":
                return self.left.value * self.right.value
            elif self.type == "/":
                return self.left.value / self.right.value
            elif self.type == "~^" or self.type == "^~":
                return xnor(self.left.value, self.right.value)
            elif self.type == "<<":
                return self.left.value << self.right.value
            elif self.type == ">>":
                return self.left.value >> self.right.value
            elif self.type == "<":
                return int(self.left.value < self.right.value)
            elif self.type == "<=":
                return int(self.left.value <= self.right.value)
            elif self.type == ">":
                return int(self.left.value > self.right.value)
            elif self.type == ">=":
                return int(self.left.value >= self.right.value)
            elif self.type == "==":
                return int(self.left.value == self.right.value)
            elif self.type == "!=":
                return int(self.left.value != self.right.value)
            else:
                return "x"
        else:
            return "x"


class UnaryOperations:
    def __init__(self, operand, type: str, size):
        self.operand = operand
        self.type = type
        if self.type == "~":
            self.size = size
        else:
            self.size = 1

    @property
    def value(self):
        # print("type is "+ str(self.type)+ " and operand is "+str(self.operand.value))
        if not self.operand.value == "x":
            if self.type == "~":
                return not_gate(self.operand.value, self.size)
            elif self.type == "&":
                return ReductionAnd(self.operand.value)
            elif self.type == "|":
                return ReductionOr(self.operand.value)
            elif self.type == "~&":
                return not_gate(ReductionAnd(self.operand.value), self.size)
            elif self.type == "~|":
                return not_gate(ReductionOr(self.operand.value), self.size)
            elif self.type == "^":
                return ReductionXor(self.operand.value)
            elif self.type == "~^" or self.type == "^~":
                return not_gate(ReductionXor(self.operand.value), self.size)
            else:
                return "x"
        else:
            return "x"
