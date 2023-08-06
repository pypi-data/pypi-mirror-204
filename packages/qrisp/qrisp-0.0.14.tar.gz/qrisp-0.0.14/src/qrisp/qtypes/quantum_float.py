"""
/*********************************************************************
* Copyright (c) 2023 the Qrisp Authors
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
**********************************************************************/
"""


from qrisp.core import QuantumVariable
import numpy as np
import sympy as sp
from qrisp.misc import gate_wrap
from qrisp.arithmetic import polynomial_encoder, lt, gt, leq, geq, eq, neq, inpl_mult, sbp_add

def signed_int_iso(x, n):
    if int(x) < -2**n or int(x) >= 2**n:
        raise Exception("Applying signed integer isomorphism resulted in overflow")
    
    if x >= 0:
        return x%2**n
    else:
        return -abs(x)%2**(n+1)

def signed_int_iso_inv(y, n):
    y = y%2**(n+1)
    if y < 2**n:
        return y
    else:
        return -2**(n+1) + y


#Truncates a polynomial of the form p(x) = 2**k_0*x*i_0 + 2**k_1*x**i_1 ...
#where every summand where the power of the coefficients does not lie in the interval
#trunc bounds is removed
def trunc_poly(poly, trunc_bounds):
    
    #Convert to sympy polynomial
    poly = sp.poly(poly)

    #Clip upper bound
    poly = poly.trunc(2.**(trunc_bounds[1]))
    
    #Clip lower bound
    poly = poly/2.**trunc_bounds[0]
    poly = poly - sp.poly(poly).trunc(1)
    poly = poly*2.**trunc_bounds[0]
    
    return poly.expr.expand()    



class QuantumFloat(QuantumVariable):
    r"""
    This subclass of :ref:`QuantumVariable` can represent floating point numbers (signed and unsigned) up to an arbitrary precision.
    
    The technical details of the employed arithmetic can be found in this `article <https://ieeexplore.ieee.org/document/9815035>`_. 
    
    To create a QuantumFloat we call the constructor:
    
    >>> from qrisp import QuantumFloat
    >>> qf_0 = QuantumFloat(3, -1, signed = False)
    
    Here, the 3 indicates the amount of mantissa qubits and the -1 indicates the exponent.
    
    For unsigned QuantumFloats, the decoder function is given by
    
    .. math::
        
        f_{k}(i) = i2^{k}
    
    Where $k$ is the exponent.
    
    We can check which values can be represented:
    
    >>> for i in range(2**qf_0.size): print(qf_0.decoder(i))
    0.0
    0.5
    1.0
    1.5
    2.0
    2.5
    3.0
    3.5
    
    We see $2^3 = 8$ values, because we have 3 mantissa qubits. The exponent is -1, implying the precision is $0.5 = 2^{-1}$.
    
    For signed QuantumFloats, the decoder function is
    
    .. math::
        
        f_{k}^{n}(i) = \begin{cases} i2^{k} & \text{if } i < 2^n \\ (i - 2^{n+1})2^k & \text{else} \end{cases}
    
    Where $k$ is again, the exponent and $n$ is the mantissa size.
    
    
    Another example:
    
    >>> qf_1 = QuantumFloat(2, -2, signed = True)
    >>> for i in range(2**qf_1.size): print(qf_1.decoder(i))
    0.0
    0.25
    0.5
    0.75
    -1.0
    -0.75
    -0.5
    -0.25
    
    Here, we have $2^2 = 4$ values and their signed equivalents. Their precision is $0.25 = 2^{-2}$.
    
    
    **Arithmetic**
    
    Many operations known from classical arithmetic work for QuantumFloats in infix notation.
    
    Addition:
    
    >>> qf_0[:] = 1.5
    >>> qf_1[:] = 0.25
    >>> qf_3 = qf_0 + qf_1
    >>> print(qf_3)
    {1.75: 1.0}
    
    Subtraction:
    
    >>> qf_4 = qf_0 - qf_3
    >>> print(qf_4)
    {-0.25: 1.0}
    
    Multiplication:
        
    >>> qf_5 = qf_4 * qf_1
    >>> print(qf_5)
    {-0.0625: 1.0}
    
    And even division:
        
    >>> qf_6 = QuantumFloat(3)
    >>> qf_7 = QuantumFloat(3)
    >>> qf_6[:] = 7
    >>> qf_7[:] = 2
    >>> qf_8 = qf_6/qf_7
    >>> print(qf_8)
    {3.5: 1.0}
    
    Floor division:
        
    >>> qf_9 = qf_6//qf_7
    >>> print(qf_9)
    {3.0: 1.0}
    
    Inversion:
    
    >>> qf_10 = QuantumFloat(3, -1)
    >>> qf_10[:] = 3.5
    >>> qf_11 = qf_10**-1
    >>> print(qf_11)
    {0.25: 1.0}
    
    Note that the latter is only an approximate result. This is because in many cases, the results of division can not be stored in a finite amount of qubits, forcing us to approximate.
    To get a better approximation we can use the :meth:`q_div <qrisp.q_div>` and :meth:`qf_inversion <qrisp.qf_inversion>` functions and specify the precision:
    
    >>> from qrisp import q_div, qf_inversion
    >>> qf_12 = QuantumFloat(3)
    >>> qf_12[:] = 1
    >>> qf_13 = QuantumFloat(3)
    >>> qf_13[:] = 7
    >>> qf_14 = q_div(qf_12, qf_13, prec = 6)
    >>> print(qf_14)
    {0.140625: 1.0}
    
    Comparing with the classical result (0.1428571428):
    
    >>> 1/7 - 0.140625
    0.002232142857142849
    
    We see that the result is inside the expected precision of $2^{-6} =  0.015625$.
    
    
    **In-place Operations**
    
    Further supported operations are inplace addition, subtraction (with both classical and quantum values):
        
    >>> qf_15 = QuantumFloat(4, signed = True)
    >>> qf_15[:] = 4
    >>> qf_16 = QuantumFloat(4)
    >>> qf_16[:] = 3
    >>> qf_15 += qf_16
    >>> print(qf_15)
    {7: 1.0}
    >>> qf_15 -= 2
    >>> print(qf_15)
    {5: 1.0}
    
    .. warning::
        Additions that would result in overflow, raise no errors. Instead the additions are performed `modular <https://en.wikipedia.org/wiki/Modular_arithmetic>`_.
        
        >>> a = QuantumFloat(3)
        >>> a += 9
        >>> print(a)
        {1: 1.0}
    
    For inplace multiplications, only classical integers are allowed:
    
    >>> qf_15 *= -3
    >>> print(qf_15)
    {-15: 1.0}
    
    .. note::
        In-place multiplications can change the mantissa size to prevent overflow errors. If you want to prevent this behavior, look into :meth:`inpl_mult <qrisp.inpl_mult>`.
        
        >>> qf.qf_15.size
        7
    
    **Bitshifts**
    
    Bitshifts can be executed for free (ie. not requiring any quantum gates). We can either use the :meth:`exp_shift <qrisp.QuantumFloat.exp_shift>` method or use the infix operators. Note that the bitshifts work in-place.
    
    
    >>> qf_15.exp_shift(3)
    >>> print(qf_15)
    {40: 1.0}
    >>> qf_15 >> 5
    >>> print(qf_15)
    {1.25: 1.0}
    
    **Comparisons**
    
    QuantumFloats can be compared to Python floats using the established operators. The return values are :ref:`QuantumBools <QuantumBool>`:
        
    >>> from qrisp import h
    >>> qf_16 = QuantumFloat(4)
    >>> h(qf_16[2])
    >>> print(qf_16)
    {0: 0.5, 4: 0.5}
    >>> comparison_qbl_0 = (qf_16 < 4 )
    >>> print(comparison_qbl_0)
    {False: 0.5, True: 0.5}

    Comparison to other QuantumFloats also works:
        
    >>> qf_17 = QuantumFloat(3)
    >>> qf_17[:] = 4
    >>> comparison_qbl_1 = (qf_17 == qf_16)
    >>> comparison_qbl_1.qs.statevector()
    sqrt(2)*(|0>*|True>*|4>*|False> + |4>*|False>*|4>*|True>)/2
    
    The first tensor factor containing a boolean value is corresponding to ``comparison_qbl_0`` and the second one is ``comparison_qbl_1``.
    
    """
    
    
    def __init__(self, msize, exponent = 0, qs = None, name = None, signed = False):
        
        #Boolean to indicate if the float is signed
        self.signed = signed
        
        #Exponent
        self.exponent = exponent
        
        #Size of the mantissa
        self.msize = msize
        
        #Array that consists of (log2(min), log2(max)) where min and max are the minimal and maximal values
        #of the absolutes that the QuantumFloat can represent
        self.mshape = np.array([exponent, exponent + msize])
        
        #Initialize QuantumVariable
        if signed:
            super().__init__(msize + 1, qs, name = name)
        else:
            super().__init__(msize, qs, name = name)
            
        
    
        
        
    #Define outcome_labels
    def decoder(self, i):
        if self.signed:
            
            res = signed_int_iso_inv(i, self.size-1)*2.**self.exponent
        else:
            res =  i*2**self.exponent
            
        if self.exponent >= 0:
            return int(res)
        else:
            return res
        
    # def encoder(self, i):
    #     if self.signed:
    #         res = int(signed_int_iso(i/2**self.exponent, self.size-1))
    #     else:
    #         res =  int(i/2**self.exponent)
            
    #     return res
        
        
    
    def sb_poly(self, m = 0):
        """
        Returns the semi-boolean polynomial of this `QuantumFloat` where `m` specifies the image extension parameter.
        
        For the technical details we refer to: https://ieeexplore.ieee.org/document/9815035
        

        Parameters
        ----------
        m : int, optional
            Image extension parameter. The default is 0.

        Returns
        -------
        Sympy expression
            The semi-boolean polynomial of this QuantumFloat.
            
        Examples
        --------
        
        >>> from qrisp import QuantumFloat
        >>> x = QuantumFloat(3, -1, signed = True, name = "x")
        >>> print(x.sb_poly(5))
        0.5*x_0 + 1.0*x_1 + 2.0*x_2 + 28.0*x_3
        
        """
        
        if m == 0:
            m = self.size
        
        symbols = [sp.symbols(self.name + "_" + str(i)) for i in range(self.size)]
        
        poly = sum([2.**(i)*symbols[i] for i in range(self.size)])
        
        
        if self.signed:
                poly += (2.**(m+1) - 2.**(self.size))*symbols[-1]
        
        return 2**self.exponent*poly
    
    
    def encode(self, encoding_number, rounding = False):
        
        
        if rounding:
            #Round value to closest fitting number    
            outcome_labels = [self.decoder(i) for i in range(2**self.size)]
            encoding_number = outcome_labels[np.argmin(np.abs(encoding_number-np.array(outcome_labels)))]
    
        super().encode(encoding_number)
        
    @gate_wrap(permeability = "args", is_qfree = True)
    def __mul__(self, other):
        
        if isinstance(other, QuantumFloat):
                return q_mult(self, other)
        elif isinstance(other, int):
            
            bit_shift = 0
            while not other%2:
                other = other>>1
                bit_shift += 1                
            
            if self.signed or other < 0:
                output_qf = QuantumFloat(self.msize + int(np.ceil(np.log2(abs(other)))),
                                         self.exponent, 
                                         signed = True)
            else:
                output_qf = QuantumFloat(self.msize + int(np.ceil(np.log2(abs(other)))), 
                                         self.exponent, 
                                         signed = False)
            
            polynomial_encoder([self], output_qf, other*sp.Symbol("x"))
            
            output_qf<<bit_shift
            
            return output_qf
        else:
            raise Exception("QuantumFloat multiplication for type " + str(type(other)) + ""
                            " not implemented (available are QuantumFloat and int)")
    
    @gate_wrap(permeability = "args", is_qfree = True)
    def __add__(self, other):
        if isinstance(other, QuantumFloat):
            return sbp_add(self, other)
        elif isinstance(other, (int, float)):
            res = self.duplicate(init = True)
            res += other
            return res            
        else:
            raise Exception("Addition with type " + str(type(other)) + " not implemented")
    
    @gate_wrap(permeability = "args", is_qfree = True)
    def __sub__(self, other):
        from qrisp.arithmetic import sbp_sub
        if isinstance(other, QuantumFloat):
            
            return sbp_sub(self, other)
        elif isinstance(other, (int, float)):
            
            res = self.duplicate(init = True)
            res -= other
            return res
        else:
            raise Exception("Subtraction with type " + str(type(other)) + " not implemented")
            
    __radd__ = __add__
    __rmul__ = __mul__
    
    @gate_wrap(permeability = "args", is_qfree = True)
    def __rsub__(self, other):
        from qrisp.arithmetic import sbp_sub
        from qrisp import x
        if isinstance(other, QuantumFloat):
            return sbp_sub(other, self)
        elif isinstance(other, (int, float)):
            
            res = self.duplicate(init = True)
            if not res.signed:
                res.add_sign()
            x(res)
            res -= other - 2**res.exponent
            return res
        else:
            raise Exception("Subtraction with type " + str(type(other)) + " not implemented")
        
    @gate_wrap(permeability = "args", is_qfree = True)
    def __truediv__(self, other):
        from qrisp.arithmetic import q_div
        
        return q_div(self, other)
    
    @gate_wrap(permeability = "args", is_qfree = True)
    def __floordiv__(self, other):
        
        if self.signed or other.signed:
            raise Exception("Floor division not implemented for signed QuantumFloats")
        
        if self.exponent < 0 or other.exponent < 0:
            raise Exception("Tried to perform floor division on non-integer QuantumFloats")
        from qrisp.arithmetic import q_div
        
        return q_div(self, other, prec = 0)
    
    @gate_wrap(permeability = "args", is_qfree = True)
    def __pow__(self, power):
        
        if power != -1:
            raise Exception("Currently the only supported power is -1")
        
        from qrisp.arithmetic import qf_inversion
        
        return qf_inversion(self)
    
    @gate_wrap(permeability = [1], is_qfree = True)
    def __iadd__(self, other):
        
        if isinstance(other, QuantumFloat):
            input_qf_list = [other]
            poly = sp.symbols("x")
            
            polynomial_encoder(input_qf_list, self, poly)
            
        
        elif isinstance(other, (int, float)):
            # self.incr(other)
            
            if not int(other/2**self.exponent) == other/2**self.exponent:
                raise Exception("Tried to perform in-place addition with invalid number. QuantumFloat precision too low.")
            
            input_qf_list = []
            poly = sp.sympify(other)
            
            polynomial_encoder(input_qf_list, self, poly)

        else:
            raise Exception("In-place addition for type " + str(type(other)) + " not implemented")
        
        return self
    
    @gate_wrap(permeability = [1], is_qfree = True)
    def __isub__(self, other):
        
        if isinstance(other, QuantumFloat):
            input_qf_list = [other]
            poly = -sp.symbols("x")
        
            polynomial_encoder(input_qf_list, self, poly)
            
        elif isinstance(other, (int, float)):
            
            if not int(other/2**self.exponent) == other/2**self.exponent:
                raise Exception("Tried to perform in-place subtraction with invalid number. QuantumFloat precision too low.")
            
            input_qf_list = []
            poly = -sp.sympify(other)
        
            polynomial_encoder(input_qf_list, self, poly)
            
        else:
            raise Exception("In-place substraction for type " + str(type(other)) + " not implemented")
        
        return self
            
    
    @gate_wrap(permeability=[], is_qfree = True)
    def __imul__(self, other):
        
        inpl_mult(self, other)
        
        return self
        
    def __rshift__(self, k):
        self.exp_shift(-k)
        return self
    
    def __lshift__(self, k):
        self.exp_shift(k)
        return self
    
    def __lt__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return lt(self, other)
        
    def __gt__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return gt(self, other)
        

    def __le__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return leq(self, other)

    def __ge__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return geq(self, other)
        
    def __eq__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return eq(self, other)

    def __ne__(self, other):
        
        if not isinstance(other, (QuantumFloat, int, float)):
            raise Exception(f"Comparison with type {type(other)} not implemented")
        
        return neq(self, other)
        
    def exp_shift(self, shift):
        
        if not isinstance(shift, int):
            raise Exception("Tried to shift QuantumFloat exponent by non-integer value")
        
        self.exponent += shift
        self.mshape = self.mshape + shift
        
    def reduce(self, qubits, verify = False):
        QuantumVariable.reduce(self, qubits, verify)
        
        
        try:
            self.mshape[1] -= len(qubits)
            self.msize -= len(qubits)
        except TypeError:
            self.mshape[1] -= 1
            self.msize -= 1
            
        
            
    def extend(self, amount, position = -1):
        QuantumVariable.extend(self, amount, position = position)
        
        self.mshape[1] += amount
        self.msize += amount
    
    def add_sign(self):
        """
        Turns an unsigned QuantumFloat into its signed version.

        Raises
        ------
        Exception
            Tried to add sign to signed QuantumFloat.

        Examples
        --------
        
        >>> from qrisp import QuantumFloat
        >>> qf = QuantumFloat(4)
        >>> qf.signed
        False
        >>> qf.add_sign()
        >>> qf.signed
        True

        """
        
        if self.signed:
            raise Exception("Tried to add sign to signed QuantumFloat")
        
        self.extend(1, self.size-1)
        self.mshape[1] -= 1
        self.msize -= 1
        self.signed = True
        
    def sign(self):
        """
        Returns the sign qubit. 
        
        This qubit is in state $\ket{1}$ if the QuantumFloat holds a negative value and in state $\ket{0}$ otherwise.
        
        For more information about the encoding of negative numbers check our `paper <https://ieeexplore.ieee.org/document/9815035>`_.
        
        .. warning::
            
            Performing an X gate on this qubit does not flip the sign! Use inplace multiplication instead
            
            >>> from qrisp import QuantumFloat
            >>> qf = QuantumFloat(3, signed = True)
            >>> qf[:] = 3
            >>> qf *= -1
            >>> print(qf)
            {-3: 1.0}

        Raises
        ------
        Exception
            Tried to retrieve sign qubit of unsigned QuantumFloat.

        Returns
        -------
        Qubit
            The qubit holding the sign.
            
        Examples
        --------
        
        We create a QuantumFloat, initiate a state that has probability 2/3 of being negative and entangle a QuantumBool with the sign qubit.
        
        >>> from qrisp import QuantumFloat, QuantumBool, cx
        >>> qf = QuantumFloat(4, signed = True)
        >>> n_amp = 1/3**0.5
        >>> qf[:] = {-1 : n_amp, -2 : n_amp, 1 : n_amp}
        >>> qbl = QuantumBool()
        >>> cx(qf.sign(), qbl)
        >>> print(qbl)
        {True: 0.6667, False: 0.3333}

        """
        if not self.signed:
            raise Exception("Tried to retrieve sign qubit of unsigned QuantumFloat")
            
        return self[-1]
    
    
    def init_from(self, other, ignore_rounding_errors = False, ignore_overflow_errors = False):
        copy_qf(self, other, ignore_rounding_errors = ignore_rounding_errors, ignore_overflow_errors= ignore_overflow_errors)
    
    def incr(self, x = None):
        from qrisp.arithmetic.incrementation import increment
        if x == None:
            x = 2**self.exponent
        increment(self, x)

    def __hash__(self):
        return id(self)
    
    def significant(self, k):
        """
        Returns the qubit with significance $k$.

        Parameters
        ----------
        k : int
            The significance.

        Raises
        ------
        Exception
            Tried to retrieve invalid significant from QuantumFloat

        Returns
        -------
        Qubit
            The Qubit with significance $k$.
            
        Examples
        --------
        
        We create a QuantumFloat and flip a qubit of specified significance.
        
        >>> from qrisp import QuantumFloat, x
        >>> qf = QuantumFloat(6, -3)
        >>> x(qf.significant(-2))
        >>> print(qf)
        {0.25: 1.0}
        
        The qubit with significance $-2$ corresponds to the value $0.25 = 2^{-2}$.
        
        >>> x(qf.significant(2))
        {4.25: 1.0}
        
        The qubit with significance $2$ corresponds to the value $4 = 2^{2}$.

        """
        
        sig_list = list(range(self.mshape[0], self.mshape[1]))
        
        if not k in sig_list:
            raise Exception(f"Tried to retrieve invalid significant {k} from QuantumFloat with mantissa shape {self.mshape}")
        
        return self[sig_list.index(k)]
        
   
    def truncate(self, x):
        """
        Receives a regular float and returns the float that is closest to the input but can still be encoded.

        Parameters
        ----------
        x : float
            A float that is supposed to be truncated.

        Returns
        -------
        float
            The truncated float.
            
        Examples
        --------
        
        We create a QuantumFloat and round a value to fit the encoder and subsequently initiate:
        
        >>> from qrisp import QuantumFloat
        >>> qf = QuantumFloat(4, -1)
        >>> value = 0.5102341
        >>> qf[:] = value
        Exception: Value 0.5102341 not supported by encoder.
        >>> rounded_value = qf.truncate(value)
        >>> rounded_value
        0.5
        >>> qf[:] = rounded_value
        >>> print(qf)
        {0.5: 1.0}

        """
        decoder_values = np.array([self.decoder(i) for i in range(2**self.size)])
        
        return decoder_values[np.argmin(np.abs(decoder_values - x))]
        


from qrisp.misc import gate_wrap

def q_mult(factor_1, factor_2, target = None, method = "auto"):
    
    if method == "auto":
        
        if factor_1.reg == factor_2.reg:
            return q_mult(factor_1, factor_2, target, method = "sbp")
        else:
            return q_mult(factor_1, factor_2, target, method = "hybrid")

    elif method == "sbp":
        
        from qrisp import sbp_mult, merge
        if target is None:
            target = create_output_qf([factor_1, factor_2], op = "mul")
        
        merge([target, factor_1, factor_2])
        
        
        sbp_mult(factor_1, factor_2, target)
        return target
    
    elif method == "hybrid":
        from qrisp.arithmetic import hybrid_mult
        return hybrid_mult(factor_1, factor_2)

def create_output_qf(operands, op):
    
    if isinstance(op, sp.core.expr.Expr):
        from qrisp.arithmetic.poly_tools import expr_to_list
        
        expr_list = expr_to_list(op)
        
        
        for i in range(len(expr_list)):
            if not isinstance(expr_list[i][0], sp.Symbol):
                expr_list[i].pop(0)
                
        
        operands.sort(key = lambda x : x.name)
        
        
        def prod(iter):
            iter = list(iter)
            a = iter[0]
            for i in range(1, len(iter)):
                a *= iter[i]
                
            return a
        
        from sympy import Symbol, Abs, Poly
        
        poly = Poly(op)
        monom_list = [a*prod(x**k for x, k in zip(poly.gens, mon)) for a, mon in zip(poly.coeffs(), poly.monoms())]
        
        max_value_dic = {Symbol(qf.name) : 2.**qf.mshape[1] for qf in operands}
        min_value_dic = {Symbol(qf.name) : 2.**qf.mshape[0] for qf in operands}
                
        
        
        abs_poly = sum([Abs(monom) for monom in monom_list], 0)
        
        min_poly_value = min([float(Abs(monom).subs(min_value_dic)) for monom in monom_list])
        
        max_poly_value = float(abs_poly.subs(max_value_dic))
        
        
        min_sig = int(np.floor(np.log2(min_poly_value)))
        max_sig = int(np.ceil(np.log2(max_poly_value)))
        
        
        msize  = max_sig - min_sig
        exponent = min_sig
        
        
        signed = bool(sum([int(operand.signed) for operand in operands]))
        
        return QuantumFloat(msize, exponent = exponent, signed = signed)
    

    
    if op == "add":
        signed = operands[0].signed or operands[1].signed
        exponent = min(operands[0].exponent, operands[1].exponent)
        

        max_sig = int(np.ceil(np.log2(int(2**operands[0].mshape[1] + 2**operands[1].mshape[1]))))
        msize = max_sig - exponent + 1
        return QuantumFloat(msize, exponent, operands[0].qs, signed = signed, name = "add_res*")
    
    if op == "mul":
        signed = operands[0].signed or operands[1].signed
        
        if operands[0].reg == operands[1].reg and (operands[0].signed and operands[1].signed):
            signed = False
        
        return QuantumFloat(operands[0].msize + operands[1].msize + operands[0].signed*operands[1].signed, operands[0].exponent + operands[1].exponent, operands[0].qs, signed = signed, name = "mul_res*")
    
    if op == "sub":
        exponent = min(operands[0].exponent, operands[1].exponent)
        max_sig = int(np.ceil(np.log2(int(2**operands[0].mshape[1] + 2**operands[1].mshape[1]))))
        msize = max_sig - exponent + 1
        
        return QuantumFloat(msize, exponent, operands[0].qs, signed = True, name = "sub_res*")
    


#Initiates the value of qf2 into qf1 where qf1 has to hold the value 0
def copy_qf(qf1, qf2, ignore_overflow_errors = False, ignore_rounding_errors = False):
    
    #Lists that translate Qubit index => Significance
    qf1_sign_list = [qf1.exponent + i for i in range(qf1.size)]
    qf2_sign_list = [qf2.exponent + i for i in range(qf2.size)]
    
    
    #Check overflow/underflow
    if max(qf1_sign_list) < max(qf2_sign_list) and not ignore_overflow_errors:
        raise Exception("Copy operation would result in overflow (use ignore_overflow_errors = True)")
        
    if min(qf1_sign_list) > min(qf2_sign_list) and not ignore_rounding_errors:
        raise Exception("Copy operation would result in rounding (use ignore_rounding_errors = True)")
    
    qs = qf1.qs
    
    if qf2.signed:
        if not qf1.signed:
            raise Exception("Tried to copy signed into unsigend float")
        
        #Remove last entry from significance list (last qubit is the sign qubit)
        qf2_sign_list.pop(-1)
        qf1_sign_list.pop(-1)
        
        
    
    for i in range(len(qf1_sign_list)):
        
        #If we are in a realm where both floats have overlapping significance => CNOT into each other
        if qf1_sign_list[i] in qf2_sign_list:
            qf2_index = qf2_sign_list.index(qf1_sign_list[i])
            qs.cx(qf2[qf2_index], qf1[i])
            continue
        
        #Otherwise copy the sign bit into the bits of higher significance than qf2
        if qf1_sign_list[i] > max(qf2_sign_list) and qf2.signed:
            qs.cx(qf2[-1], qf1[i])
    
    #Copy the sign bit
    if qf2.signed:
        qs.cx(qf2[-1], qf1[-1])




# @adaptive_condition
# def less_than(qf_0, qf_1):
#     lt_qbl = QuantumBool()
#     if qf_0.signed:
#         qf_0 -= qf_1
#         cx(qf_1[-1], lt_qbl)
#         # The last qubit holds the sign of the QuantumFloat
#         qf_0 += qf_1
#         return lt_qbl
#     else:
#         temp_qf = qf_0 - qf_1
#         cx(temp_qf[-1], lt_qbl)
#         return lt_qbl

# @adaptive_condition
# def greater_than(qf_0, qf_1):
#     gt_qbl = QuantumBool()
#     if qf_0.signed:
#         qf_1 -= qf_0
#         # The last qubit holds the sign of the QuantumFloat
#         cx(qf_1[-1], gt_qbl)
#         qf_1 += qf_0
#         return gt_qbl
#     else:
#         temp_qf = qf_1 - qf_0
#         cx(temp_qf[-1], gt_qbl)
#         return gt_qbl

# @adaptive_condition
# def less_than_or_equal(qf_0, qf_1):
#     leq_qbl = QuantumBool()
#     if qf_0.signed:
#         qf_1 -= qf_0
#         # The last qubit holds the sign of the QuantumFloat
#         cx(qf_0[-1], leq_qbl)
#         qf_1 += qf_0
#         leq_qbl.flip()
#         return leq_qbl
#     else:
#         temp_qf = qf_1 - qf_0
        
#         cx(temp_qf[-1], leq_qbl)
#         leq_qbl.flip()
#         return leq_qbl

# @adaptive_condition
# def greater_than_or_equal(qf_0, qf_1):
#     geq_qbl = QuantumBool()
#     if hasattr(qf_0, 'signed') and qf_0.signed:
#         qf_0 -= qf_1
#         # The last qubit holds the sign of the QuantumFloat
#         cx(qf_0[-1], geq_qbl)
#         qf_0 += qf_1
#         geq_qbl.flip()
#         return geq_qbl
#     else:
#         temp_qf = qf_0 - qf_1
#         cx(temp_qf[-1], geq_qbl)
#         geq_qbl.flip()
#         return geq_qbl


# #TO-DO implement without arithmetic?
# @adaptive_condition
# def equal(qf_0, qf_1):
    
#     eq_qbl = QuantumBool()
    
#     if isinstance(qf_1, QuantumFloat):
#         if not qf_0.signed and not qf_1.signed:
#             if qf_0.exponent > qf_1.exponent:
#                 qf_0, qf_1 = qf_1, qf_0
                
#             min_sig = qf_0.mshape[0]
#             max_sig = max(qf_0.mshape[1], qf_1.mshape[1])
            
#             temp_qf = QuantumFloat(max_sig - min_sig)
            
#             cx(qf_0, temp_qf[:qf_0.size])
#             cx(qf_1, temp_qf[-qf_1.size:])
            
#             mcx(temp_qf, eq_qbl, ctrl_state = 0)
            
#             return eq_qbl
        
#     temp_qf = qf_0 - qf_1
        
#     mcx(temp_qf, eq_qbl, ctrl_state = 0)
    
#     return eq_qbl

# @adaptive_condition
# def always_true():
#     qbl = QuantumBool()
#     qbl.flip()
#     return qbl

# @adaptive_condition
# def always_false():
#     from qrisp import QuantumBool
#     qbl = QuantumBool()
#     return qbl



