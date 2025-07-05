import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

# [+ 5 7] eval plus first, then 5, then 7
# call apply on procedure + on 5 and 7. apply it on 1 and 2
# eval puts every argument in final form, after that, call scheme_apply 
# to get result of the whole expression
def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # To evaluate a call expression
        # 1) evalute the operator (which shld eval to a procedure instance)
        # 2) evalute all operands & collect results in Scheme list
        # 3) return result of scheme_apply on this Procedure & arg values
        # 
        # Recursively call scheme_eval in the first two step. map method 
        # of Pair applies one-arg function to items in new Scheme list 
        # # scheme_apply applies Scheme procedure to args represented as a 
        # Scheme list
        eval_operator = scheme_eval(first, env)
        eval_operands = rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(eval_operator, eval_operands, env)
    
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    # args is a Scheme list, Pair object or nil
    # Convert Scheme list to a Python list of args
    # args is a Pair with first and rest attributes
    # if procedure.need_ev is True, add env as last arg to Python list
    # *args notation, within the try statement.
        # return result of calling procedure.py_fun on all args
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        list = []
        while args:
            list.append(args.first)
            args = args.rest
        if procedure.need_env:
            list.append(env)

        # Built-in procedures applied by calling corresponding Python function
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            return procedure.py_func(*list)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        new_frame = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_frame)
        
        # Create new frame instance, bind formal parameters to arg values
        # by calling make_child_frame
        # within new frame, evaluate each of the expressions of the body
        # of the procedure using eval_all

        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
     
        # BEGIN PROBLEM 11
        # dynamic scoping: parent of the new call frame is environment where
        # the call expression was evaluated
        # calling procedure with same arguments from different 
        # parts of your code can crate different behavior
        mu_frame = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, mu_frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # return scheme_eval(expressions.first, env) # replace this with lines of your own code
    if expressions:
        if expressions.rest is not nil:
            scheme_eval(expressions.first, env)
            return eval_all(expressions.rest, env)
        return scheme_eval(expressions.first, env)
   
    # END PROBLEM 6


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
