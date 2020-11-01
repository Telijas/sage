r"""
Spinor genus computations.

This file contains some groups used for the computation of spinor genera. It is meant for internal use only.

EXAMPLES::

<Lots and lots of examples>

AUTHORS:

- Simon Brandhorst (2020-11-1): initial version
"""

# ****************************************************************************
#       Copyright (C) 2020 Simon Brandhorst <sbrandhorst@web.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.groups.abelian_gps.abelian_group_gap import AbelianGroupGap, AbelianGroupElement_gap
from sage.quadratic_forms.genera.normal_form import _min_nonsquare
from sage.rings.all import ZZ,QQ

class AdelicSquareClass(AbelianGroupElement_gap):

    def _repr_(self):
        r"""
        Return the print representation.

        EXAMPLES::
        """
        e = self.exponents()
        p = self.parent()._primes
        s = "[2:"
        if e[0]==0 and e[1]==0:
            s += "1"
        elif e[0]==1 and e[1]==0:
            s += "3"
        elif e[0]==0 and e[1]==1:
            s += "5"
        elif e[0]==1 and e[1]==1:
            s += "7"
        for k in range(1,len(p)):
            s += ", %s:%s"%(p[k], (-1)**e[k+1])
        s += "]"
        return s


class AdelicSquareClasses(AbelianGroupGap):
    r"""
    A group of square classes used for spinor norm computations.

    INPUT:

    - a tuple of primes `(p_1=2,\dots, p_n`)

    OUTPUT

    MATH::

      \QQ_{p_1^*/(\QQ_{p_1}^*)^2 \times \dots \ times \QQ_{p_n^*/(\QQ_{p_n}^*)^2

    EXAMPLES::


    """
    def __init__(self, primes):
        r"""
        """
        if primes[0] != 2:
            raise ValueError("first prime must be 2")
        self._primes = tuple(ZZ(p) for p in primes)
        orders = len(self._primes)*[2] + [2]
        # 3, 5, unit_p1, unit_p2,...
        order = tuple(orders)
        AbelianGroupGap.__init__(self, orders)

    Element = AdelicSquareClass

    def to_square_class(self, x, p):
        r"""
        Return `(1, ..., 1, x, 1, ..., 1)` with the square class of `x` at position `p`.

        INPUT:

        - ``p`` -- a prime

        - ``x```-- a non zero rational number

        EXAMPLES::

            sage: from sage.quadratic_forms.genera.spinor_genus import AdelicSquareClasses
            sage: AS = AdelicSquareClasses((2, 3, 7))
            sage: AS.to_square_class(5, 7)
            [2:1, 3:1, 7:-1]
            sage: AS.to_square_class(5, 2)
            [2:5, 3:1, 7:1]
            sage: AS.to_square_class(-5, 2)
            [2:3, 3:1, 7:1]
            sage: AS.to_square_class(7, 2)
            [2:7, 3:1, 7:1]
        """
        x = QQ(x)
        if x == 0:
            raise ValueError("x must be non zero")
        if not p in self._primes:
            raise ValueError("not a coordinate prime")
        v, u = x.val_unit(p)
        v = v % 2
        if v != 0:
            raise ValueError("x(=%s) must be a p-adic unit" %x)
        y = self.one()
        if p == 2:
            u = u % 8
            if u == 3:
                y *= self.gens()[0]
            if u == 5:
                y *= self.gens()[1]
            if u == 7:
                y *= self.gens()[0] * self.gens()[1]
            return y
        i = 1 + self._primes.index(p)
        if not u.is_padic_square(p):
            y *= self.gens()[i]
        return y

    def delta(self, r, prime=None):
        r"""
        Diagonal embedding of rational square classes.

        INPUT:

        - ``r`` -- a non zero rational number

        - ``prime`` --(default:``None``) a prime or `-1`

        OUTPUT:

        If a prime `p` is given the method returns
        `\Delta_p(r)`
        otherwise returns `\Delta(r)`
        where both are as defined by Conway-Sloane.

        EXAMPLES::

            sage: from sage.quadratic_forms.genera.spinor_genus import AdelicSquareClasses
            sage: AS = AdelicSquareClasses((2, 3, 7))
            sage: AS.delta(2, prime=3)
            [2:1, 3:-1, 7:1]
            sage: AS.delta(11)
            [2:3, 3:-1, 7:1]
            sage: AS.delta(3, prime=7)
            [2:1, 3:1, 7:-1]
        """
        r = QQ(r)
        if prime is None:
            return self.prod([self.to_square_class(r, p) for p in self._primes])
        prime = ZZ(prime)
        if prime == -1:
            r = r.sign()
            return self.prod([self.to_square_class(r, p) for p in self._primes])
        if prime not in self._primes:
            raise ValueError("prime must be among %s"%self._primes)
        v, u = r.val_unit(prime)
        pv = prime**v
        y = self.prod([self.to_square_class(pv,q) for q in self._primes if q!=prime])
        if prime in self._primes:
            y *= self.to_square_class(u, p=prime)
        return y
