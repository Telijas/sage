r"""
Mutable Poset

This module provides a class representing a finite partially ordered
set (poset) for the purpose of being used as a data structure. Thus
the posets introduced in this module are mutable, i.e., elements can
be added and removed from a poset at any time.

To get in touch with Sage's "usual" posets, start with the page
:mod:`Posets <sage.combinat.posets.__init__>` in the reference manual.


.. _mutable_poset_intro:

Introduction
============


.. _mutable_poset_examples:

Examples
========

First Steps
-----------

We start by creating an empty poset. This is simply done by

::

    sage: from sage.data_structures.mutable_poset import MutablePoset as MP
    sage: P = MP()
    sage: P
    poset()

A poset should contain elements, thus let us add them with

::

    sage: P.add(42)
    sage: P.add(7)
    sage: P.add(13)
    sage: P.add(3)

Let us look at the poset again::

    sage: P
    poset(3, 7, 13, 42)

We see that they elements are sorted using `\leq` which exists on the
integers `\ZZ`. Since this is even a total order, we could have used a
more efficient data structure.


A less boring Example
---------------------

Let us continue with a less boring example. We define the class

::

    sage: class T(tuple):
    ....:     def __le__(left, right):
    ....:         return all(l <= r for l, r in zip(left, right))

It is equipped with a `\leq`-operation which makes `a \leq b` if all
entries of `a` are at most `b`. For example, we have

::

    sage: a = T((1,1))
    sage: b = T((2,1))
    sage: c = T((1,2))
    sage: a <= b, a <= c, b <= c
    (True, True, False)

The last comparison gives ``False``, since the comparison of the
first component yield `2 \leq 1`.

Now, let us add such elements to a poset::

    sage: Q = MP()
    sage: Q.add(T((1, 1)))
    sage: Q.add(T((3, 3)))
    sage: Q.add(T((4, 1)))
    sage: Q.add(T((3, 2)))
    sage: Q.add(T((2, 3)))
    sage: Q.add(T((2, 2)))
    sage: Q
    poset((1, 1), (2, 2), (2, 3), (3, 2), (3, 3), (4, 1))

In the representation above, the elements are sorted topologically,
smallest first. This does not show (directly) more structural
information. We can overcome this and display a "wiring layout" by
typing::

    sage: print Q.repr_full(reverse=True)
    poset((3, 3), (2, 3), (3, 2), (2, 2), (4, 1), (1, 1))
    +-- oo
    |   +-- no successors
    |   +-- predecessors:   (3, 3), (4, 1)
    +-- (3, 3)
    |   +-- successors:   oo
    |   +-- predecessors:   (2, 3), (3, 2)
    +-- (2, 3)
    |   +-- successors:   (3, 3)
    |   +-- predecessors:   (2, 2)
    +-- (3, 2)
    |   +-- successors:   (3, 3)
    |   +-- predecessors:   (2, 2)
    +-- (2, 2)
    |   +-- successors:   (2, 3), (3, 2)
    |   +-- predecessors:   (1, 1)
    +-- (4, 1)
    |   +-- successors:   oo
    |   +-- predecessors:   (1, 1)
    +-- (1, 1)
    |   +-- successors:   (2, 2), (4, 1)
    |   +-- predecessors:   null
    +-- null
    |   +-- successors:   (1, 1)
    |   +-- no predecessors

Note that we use ``reverse=True`` to let the elements appear from
largest (on the top) to smallest (on the bottom).

If you look at the output above, you'll see two additional elements,
namely ``oo`` (`\infty`) and ``null`` (`\emptyset`). So what are these
strange animals? The answer is simple and maybe you can guess it
already. The `\infty`-element is larger than every other element,
therefore a successor of the maximal elements in the poset. Similarly,
the `\emptyset`-element is smaller than any other element, therefore a
predecessor of the poset's minimal elements. Both do not have to scare
us; they are just there and sometimes useful.


AUTHORS:

- Daniel Krenn (2015-01-21): initial version
- Daniel Krenn (2015-08-28): mapping methods, bug fixes, cleanup

ACKNOWLEDGEMENT:

- Daniel Krenn is supported by the Austrian Science Fund (FWF): P 24644-N26.

Classes and their Methods
=========================
"""
#*****************************************************************************
# Copyright (C) 2015 Daniel Krenn <dev@danielkrenn.at>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                http://www.gnu.org/licenses/
#*****************************************************************************


class MutablePosetShell(object):
    r"""
    A shell for an element of a :class:`mutable poset <MutablePoset>`.

    INPUT:

    - ``poset`` -- the poset to which this shell belongs.

    - ``element`` -- the element which should be
      contained/encapsulated in this shell.

    OUTPUT:

    A shell for the given element.

    EXAMPLES::

        sage: from sage.data_structures.mutable_poset import MutablePoset as MP
        sage: P = MP()
        sage: P.add(66)
        sage: P
        poset(66)
        sage: s = P.shell(66)
        sage: type(s)
        <class 'sage.data_structures.mutable_poset.MutablePosetShell'>
    """
    def __init__(self, poset, element):
        r"""
        See :class:`MutablePosetShell` for details.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: MutablePosetShell(P, (1, 2))
            (1, 2)
        """
        self._poset_ = poset
        self._element_ = element
        self._predecessors_ = set()
        self._successors_ = set()


    @property
    def poset(self):
        r"""
        The poset to which this shell belongs.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: e.poset is P
            True
        """
        return self._poset_


    @property
    def element(self):
        r"""
        The element contained in this shell.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: e.element
            (1, 2)
        """
        return self._element_


    @property
    def key(self):
        r"""
        The key of the element contained in this shell.

        The element is converted by the poset to the key.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: P = MP()
            sage: e = MutablePosetShell(P, (1, 2))
            sage: e.key
            (1, 2)
            sage: Q = MP(key=lambda k: k[0])
            sage: f = MutablePosetShell(Q, (1, 2))
            sage: f.key
            1
        """
        return self.poset.get_key(self._element_)


    def predecessors(self, reverse=False):
        r"""
        Return the predecessors of this shell.

        INPUT:

        - ``reverse`` -- (default: ``False``) if set, then returns
          successors instead.

        OUTPUT:

        A set.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: e.predecessors()
            set()
        """
        if reverse:
            return self._successors_
        return self._predecessors_


    def successors(self, reverse=False):
        r"""
        Return the successors of this shell.

        INPUT:

        - ``reverse`` -- (default: ``False``) if set, then returns
          predecessors instead.

        OUTPUT:

        A set.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: e.successors()
            set()
        """
        if reverse:
            return self._predecessors_
        return self._successors_


    def is_special(self):
        r"""
        Return if this shell contains either the null-element, i.e., the
        element smaller than any possible other element or the
        infinity-element, i.e., the element larger than any possible
        other element.

        INPUT:

        Nothing.

        OUTPUT:

        ``True`` or ``False``.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.null.is_special()
            True
            sage: P.oo.is_special()
            True
        """
        return self.element is None


    def is_null(self):
        r"""
        Return if this shell contains the null-element, i.e., the element
        smaller than any possible other element.

        OUTPUT:

        ``True`` or ``False``.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.null.is_null()
            True
            sage: P.oo.is_null()
            False
        """
        return self.element is None and not self.predecessors()


    def is_oo(self):
        r"""
        Return if this shell contains the infinity-element, i.e., the element
        larger than any possible other element.

        OUTPUT:

        ``True`` or ``False``.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.null.is_oo()
            False
            sage: P.oo.is_oo()
            True
        """
        return self.element is None and not self.successors()


    def __repr__(self):
        r"""
        Return the representation of this shell.

        INPUT:

        Nothing.

        OUTPUT:

        A string.

        .. NOTE::

            If the :meth:`element` of this shell is not ``None``,
            this method returns the respective representation string.
            Otherwise, ``'null'`` or ``'oo'`` are returned,
            depending on the non-existence of predecessors or
            successors, respectively.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: repr(MutablePosetShell(P, (1, 2)))  # indirect doctest
            '(1, 2)'
            sage: repr(P.null)  # indirect doctest
            'null'
            sage: repr(P.oo)  # indirect doctest
            'oo'
        """
        if self.element is None:
            if not self.predecessors():
                return 'null'
            if not self.successors():
                return 'oo'
        return repr(self.element)


    def __hash__(self):
        r"""
        Return the hash of this shell.

        INPUT:

        Nothing.

        OUTPUT:

        A hash value.

        This returns the hash value of the key of the element
        contained in this shell.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: hash(MutablePosetShell(P, (1, 2))) == hash((1, 2))
            True
        """
        return hash(self.key)


    def le(self, other, reverse=False):
        r"""
        Return whether this shell is less than or equal to ``other``.

        INPUT:

        - ``other`` -- a shell.

        - ``reverse`` -- (default: ``False``) if set, then return
          ``right <= left`` instead.

        OUTPUT:

        ``True`` or ``False``.

        .. NOTE::

            The comparison of the shells is based on the comparison
            of the keys of the elements contained in the shells,
            except for the shells containing ``None``. These special
            shells are interpreted as smaller or larger than all
            other elements, depending on whether they have no
            predecessors or no successors, respectively.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: z = P.null
            sage: oo = P.oo
            sage: z <= e  # indirect doctest
            True
            sage: e <= oo  # indirect doctest
            True
            sage: z <= oo  # indirect doctest
            True
            sage: oo <= z  # indirect doctest
            False
            sage: oo <= e  # indirect doctest
            False
            sage: e <= z  # indirect doctest
            False
            sage: z <= z  # indirect doctest
            True
            sage: oo <= oo  # indirect doctest
            True
            sage: e <= e  # indirect doctest
            True

        ::

            sage: z.le(e, reverse=True)
            False
            sage: e.le(oo, reverse=True)
            False
            sage: z.le(oo, reverse=True)
            False
            sage: oo.le(z, reverse=True)
            True
            sage: oo.le(e, reverse=True)
            True
            sage: e.le(z, reverse=True)
            True
            sage: z.le(z, reverse=True)
            True
            sage: oo.le(oo, reverse=True)
            True
            sage: e.le(e, reverse=True)
            True
        """
        if reverse:
            return other.le(self, reverse=False)

        if self.element is None:
            if not self.predecessors():
                # null on the left
                return True
            else:
                # oo on the left
                if other.element is None:
                    # null or oo on the right
                    return not other.successors()
                else:
                    # not null, not oo on the right
                    return False
        if other.element is None:
            if not other.successors():
                # oo on the right
                return True
            else:
                # null on the right
                if self.element is None:
                    # null or oo on the left
                    return not self.predecessors()
                else:
                    # not null, not oo on the right
                    return False
        return self.key <= other.key


    __le__ = le


    def eq(self, other):
        r"""
        Return whether this shell is equal to ``other``.

        INPUT:

        - ``right`` -- a shell.

        OUTPUT:

        ``True`` or ``False``.

        .. NOTE::

            This method compares the keys of the elements contained
            in the shells, if the elements are not both ``None``.
            Otherwise, this method checks if both shells describe the
            same special element.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: e = MutablePosetShell(P, (1, 2))
            sage: z = P.null
            sage: oo = P.oo
            sage: z == z
            True
            sage: oo == oo
            True
            sage: e == e
            True
            sage: z == e
            False
            sage: e == oo
            False
            sage: oo == z
            False
        """
        if self.element is None and other.element is None:
            return self.is_null() == other.is_null()
        return self.key == other.key


    __eq__ = eq


    def _copy_all_linked_(self, memo, poset, mapping):
        r"""
        Return a copy of all shells linked to this shell
        (including a copy of this shell).

        This is a helper function for :meth:`MutablePoset.copy`.

        INPUT:

        - ``memo`` -- a dictionary which assigns to the id of the
          calling shell to a copy of it.

        - ``poset`` -- the poset to which the newly created shells belongs.

        - ``mapping`` -- a function which is applied on each of the elements.

        OUTPUT:

        A new shell.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: Q = MP()
            sage: memo = {}
            sage: z = P.null._copy_all_linked_(memo, Q, lambda e: e)
            sage: z.poset is Q
            True
            sage: oo = z.successors().pop()
            sage: oo == P.oo
            True
        """
        try:
            return memo[id(self)]
        except KeyError:
            pass

        new = self.__class__(poset, mapping(self.element)
                             if self.element is not None else None)
        memo[id(self)] = new

        for reverse in (False, True):
            for e in self.successors(reverse):
                new.successors(reverse).add(e._copy_all_linked_(memo, poset, mapping))

        return new


    def _search_covers_(self, covers, shell, reverse=False):
        r"""
        Search for cover shells of this shell.

        This is a helper function for :meth:`covers`.

        INPUT:

        - ``covers`` -- a set which finally contains all covers.

        - ``shell`` -- the shell for which to find the covering shells.

        - ``reverse`` -- (default: ``False``) if not set, then find
          the lower covers, otherwise find the upper covers.

        OUTPUT:

        ``True`` or ``False``.

        Note that ``False`` is returned if we do not have
        ``self <= shell``.

       TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1, 1)))
            sage: P.add(T((1, 3, 1)))
            sage: P.add(T((2, 1, 2)))
            sage: P.add(T((4, 4, 2)))
            sage: P.add(T((1, 2, 2)))
            sage: P.add(T((2, 2, 2)))
            sage: e = P.shell(T((2, 2, 2))); e
            (2, 2, 2)
            sage: covers = set()
            sage: P.null._search_covers_(covers, e)
            True
            sage: sorted(covers, key=lambda c: repr(c.element))
            [(1, 2, 2), (2, 1, 2)]
        """
        if not self.le(shell, reverse) or self == shell:
            return False
        if not any([e._search_covers_(covers, shell, reverse)
                    for e in self.successors(reverse)]):
            covers.add(self)
        return True


    def covers(self, shell, reverse=False):
        r"""
        Return the covers of the given shell (considering only
        shells which originate from this shell).

        INPUT:

        - ``shell`` -- the shell for which to find the covering shells.

        - ``reverse`` -- (default: ``False``) if not set, then find
          the lower covers, otherwise find the upper covers.

        OUTPUT:

        A set of the covers.

        Suppose ``reverse`` is ``False``. This method returns all the
        lower covers of the given ``shell``, i.e., shells in the
        poset, which are at most the given shell and maximal with
        this property. Only shells which are (not necessarily
        direct) successors of the calling shell are considered.

        If ``reverse`` is ``True``, then the reverse direction is
        taken, i.e., in the text above replace lower covers by upper
        covers, maximal by minimal, and successors by predecessors.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: e = P.shell(T((2, 2))); e
            (2, 2)
            sage: sorted(P.null.covers(e),
            ....:        key=lambda c: repr(c.element))
            [(1, 2), (2, 1)]
            sage: sorted(P.oo.covers(e, reverse=True),
            ....:        key=lambda c: repr(c.element))
            [(4, 4)]
        """
        covers = set()
        self._search_covers_(covers, shell, reverse)
        return covers


    def _iter_depth_first_visit_(self, marked,
                                 reverse=False, key=None,
                                 condition=None):
        r"""
        Return an iterator over all shells in depth first order.

        This is a helper function for :meth:`iter_depth_first`.

        INPUT:

        - ``marked`` -- a set in which marked shells are stored.

        - ``reverse`` -- (default: ``False``) if set, reverses the
          order, i.e., ``False`` searches towards ``'oo'`` and
          ``True`` searches towards ``'null'``.

        - ``key`` -- (default: ``None``) a function used for sorting
          the direct successors of a shell (used in case of a
          tie). If this is ``None``, no sorting occurs.

        - ``condition`` -- (default: ``None``) a function mapping a
          shell to ``True`` (include in iteration) or ``False`` (do
          not include). ``None`` is equivalent to a function returning
          always ``True``. Note that the iteration does not go beyond a
          not shell included shell.

        OUTPUT:

        An iterator.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(42)
            sage: P.add(5)
            sage: marked = set()
            sage: list(P.oo._iter_depth_first_visit_(marked, True))
            [oo, 42, 5, null]
        """
        if (condition is not None and
                not self.is_special() and not condition(self)):
            return
        if self in marked:
            return
        marked.add(self)
        yield self
        S = self.successors(reverse)
        if key is not None:
            S = sorted(S, key=key)
        for shell in S:
            for e in shell._iter_depth_first_visit_(marked, reverse,
                                                    key, condition):
                yield e


    def iter_depth_first(self, reverse=False, key=None, condition=None):
        r"""
        Iterates over all shells in depth first order.

        INPUT:

        - ``reverse`` -- (default: ``False``) if set, reverses the
          order, i.e., ``False`` searches towards ``'oo'`` and
          ``True`` searches towards ``'null'``.

        - ``key`` -- (default: ``None``) a function used for sorting
          the direct successors of a shell (used in case of a
          tie). If this is ``None``, no sorting occurs.

        - ``condition`` -- (default: ``None``) a function mapping a
          shell to ``True`` (include in iteration) or ``False`` (do
          not include). ``None`` is equivalent to a function returning
          always ``True``. Note that the iteration does not go beyond a
          not shell included shell.

        OUTPUT:

        An iterator.

        ALGORITHM:

        See :wikipedia:`Depth-first_search`.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: list(P.null.iter_depth_first(reverse=False, key=repr))
            [null, (1, 1), (1, 2), (1, 3), (4, 4), oo, (2, 2), (2, 1)]
            sage: list(P.oo.iter_depth_first(reverse=True, key=repr))
            [oo, (4, 4), (1, 3), (1, 2), (1, 1), null, (2, 2), (2, 1)]
            sage: list(P.null.iter_depth_first(
            ....:     condition=lambda s: s.element[0] == 1))
            [null, (1, 1), (1, 2), (1, 3)]
        """
        marked = set()
        return self._iter_depth_first_visit_(marked, reverse, key, condition)


    def _iter_topological_visit_(self, marked,
                                 reverse=False, key=None,
                                 condition=None):
        r"""
        Return an iterator over all shells in topological order.

        This is a helper function for :meth:`iter_topological`.

        INPUT:

        - ``marked`` -- a set in which marked shells are stored.

        - ``reverse`` -- (default: ``False``) if set, reverses the
          order, i.e., ``False`` searches towards ``'oo'`` and
          ``True`` searches towards ``'null'``.

        - ``key`` -- (default: ``None``) a function used for sorting
          the direct successors of a shell (used in case of a
          tie). If this is ``None``, no sorting occurs.

        - ``condition`` -- (default: ``None``) a function mapping a
          shell to ``True`` (include in iteration) or ``False`` (do
          not include). ``None`` is equivalent to a function returning
          always ``True``. Note that the iteration does not go beyond a
          not shell included shell.

        OUTPUT:

        An iterator.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(42)
            sage: P.add(5)
            sage: marked = set()
            sage: list(P.null._iter_topological_visit_(marked, True))
            [oo, 42, 5, null]
        """
        if (condition is not None and
                not self.is_special() and not condition(self)):
            return
        if self in marked:
            return
        marked.add(self)
        S = self.predecessors(reverse)
        if key is not None:
            S = sorted(S, key=key)
        for shell in S:
            for e in shell._iter_topological_visit_(marked, reverse,
                                                    key, condition):
                yield e
        yield self


    def iter_topological(self, reverse=False, key=None, condition=None):
        r"""
        Iterates over all shells in topological order.

        INPUT:

        - ``reverse`` -- (default: ``False``) if set, reverses the
          order, i.e., ``False`` searches towards ``'oo'`` and
          ``True`` searches towards ``'null'``.

        - ``key`` -- (default: ``None``) a function used for sorting
          the direct successors of a shell (used in case of a
          tie). If this is ``None``, no sorting occurs.

        - ``condition`` -- (default: ``None``) a function mapping a
          shell to ``True`` (include in iteration) or ``False`` (do
          not include). ``None`` is equivalent to a function returning
          always ``True``. Note that the iteration does not go beyond a
          not shell included shell.

        OUTPUT:

        An iterator.

        ALGORITHM:

        Here a simplified version of the algorithm found in [T1976]_
        and [CLRS2001]_ is used. See also
        :wikipedia:`Topological_sorting`.

        .. [T1976] Robert E. Tarjan, *Edge-disjoint spanning trees and
           depth-first search*, Acta Informatica 6 (2), 1976, 171-185,
           :doi:`10.1007/BF00268499`.

        .. [CLRS2001] Thomas H. Cormen, Charles E. Leiserson, Ronald
           L. Rivest and Clifford Stein, *Section 22.4: Topological
           sort*, Introduction to Algorithms (2nd ed.), MIT Press and
           McGraw-Hill, 2001, 549-552, ISBN 0-262-03293-7.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))

        ::

            sage: for e in P.shells_topological(include_special=True,
            ....:                                 reverse=True):
            ....:     print e
            ....:     print list(e.iter_topological(reverse=True, key=repr))
            oo
            [oo]
            (4, 4)
            [oo, (4, 4)]
            (1, 3)
            [oo, (4, 4), (1, 3)]
            (2, 2)
            [oo, (4, 4), (2, 2)]
            (1, 2)
            [oo, (4, 4), (1, 3), (2, 2), (1, 2)]
            (2, 1)
            [oo, (4, 4), (2, 2), (2, 1)]
            (1, 1)
            [oo, (4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1)]
            null
            [oo, (4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1), null]

        ::

            sage: for e in P.shells_topological(include_special=True,
            ....:                                 reverse=True):
            ....:     print e
            ....:     print list(e.iter_topological(reverse=False, key=repr))
            oo
            [null, (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (4, 4), oo]
            (4, 4)
            [null, (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (4, 4)]
            (1, 3)
            [null, (1, 1), (1, 2), (1, 3)]
            (2, 2)
            [null, (1, 1), (1, 2), (2, 1), (2, 2)]
            (1, 2)
            [null, (1, 1), (1, 2)]
            (2, 1)
            [null, (1, 1), (2, 1)]
            (1, 1)
            [null, (1, 1)]
            null
            [null]

        ::

            sage: def C(shell):
            ....:     return shell.element[0] == 1
            sage: list(P.null.iter_topological(
            ....:     reverse=True, condition=lambda s: s.element[0] == 1))
            [(1, 3), (1, 2), (1, 1), null]
        """
        marked = set()
        return self._iter_topological_visit_(marked, reverse, key, condition)


    def merge(self, element, check=True, delete=True):
        r"""
        Merge the given element with the element contained in this
        shell.

        INPUT:

        - ``element`` -- an element (of the poset).

        - ``check`` -- (default: ``True``) if set, then the
          ``can_merge``-function of :class:`MutablePoset` determines
          if the merge is possible.

        - ``delete`` -- (default: ``True``) if set, then the passed
          element is removed from the poset after the merge.

        OUTPUT:

        Nothing.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: def add(left, right):
            ....:     return (left[0], ''.join(sorted(left[1] + right[1])))
            sage: def can_add(left, right):
            ....:     return left[0] <= right[0]
            sage: P = MP(key=lambda c: c[0], merge=add, can_merge=can_add)
            sage: P.add((1, 'a'))
            sage: P.add((3, 'b'))
            sage: P.add((2, 'c'))
            sage: P.add((4, 'd'))
            sage: P
            poset((1, 'a'), (2, 'c'), (3, 'b'), (4, 'd'))
            sage: P.shell(2).merge((3, 'b'))
            sage: P
            poset((1, 'a'), (2, 'bc'), (4, 'd'))
        """
        poset = self.poset
        if poset._merge_ is None:
            return
        self_element = self.element
        if check and poset._can_merge_ is not None and \
                not poset._can_merge_(self_element, element):
            return
        new = poset._merge_(self_element, element)
        if new is None:
            poset.discard(poset.get_key(self.element))
        else:
            self._element_ = new
        if delete:
            poset.remove(poset.get_key(element))


# *****************************************************************************


def is_MutablePoset(P):
    r"""
    Tests if ``P`` inherits from :class:`MutablePoset`.

    TESTS::

        sage: from sage.data_structures.mutable_poset import MutablePoset as MP
        sage: from sage.data_structures.mutable_poset import is_MutablePoset
        sage: P = MP()
        sage: is_MutablePoset(P)
        True
    """
    return isinstance(P, MutablePoset)


class MutablePoset(object):
    r"""
    A data structure that models a mutable poset (partially ordered
    set).

    INPUT:

    - ``data`` -- data from which to construct the poset. It can be
      any of the following:

      #. ``None`` (default), in which case an empty poset is created,

      #. a :class:`MutablePoset`, which will be copied during creation,

      #. an iterable, whose elements will be in the poset.

    - ``key`` -- a function which maps elements to keys. If ``None``
      (default), this is the identity, i.e., keys are equal to their
      elements.

    - ``merge`` -- a function which merges its second argument (an
      element) to its first (again an element) and returns the result
      (as an element). If the return value is ``None``, the element is
      removed out of the poset.

      This hook is called by :meth:`merge`. Moreover it is used during
      :meth:`add` when an element (more precisely its key) is already
      in this poset.

      ``merge`` is ``None`` (default) is equivalent to ``merge``
      returns its first argument. Note that it is not allowed that the
      key of the returning element differs from the key of the first
      input parameter.

    - ``can_merge`` -- a function which checks if its second argument
      can be merged to its first.

      This hook is called by :meth:`merge`. Moreover it is used during
      :meth:`add` when an element (more precisely its key) is already
      in this poset.

      ``can_merge`` is ``None`` (default) is equivalent to ``can_merge``
      returns ``True`` in all cases.

    OUTPUT:

    A mutable poset.

    You can find a short introduction and examples
    :mod:`here <sage.data_structures.mutable_poset>`.

    EXAMPLES::

        sage: from sage.data_structures.mutable_poset import MutablePoset as MP

    We illustrate the different input formats

    #. No input::

        sage: A = MP(); A
        poset()

    #. A :class:`MutablePoset`::

        sage: B = MP(A); B
        poset()
        sage: B.add(42)
        sage: C = MP(B); C
        poset(42)

    #. An iterable::

        sage: C = MP([5, 3, 11]); C
        poset(3, 5, 11)
    """
    def __init__(self, data=None, key=None, merge=None, can_merge=None):
        r"""
        See :class:`MutablePoset` for details.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: MP()
            poset()

        ::

            sage: P = MP()
            sage: P.add(42)
            sage: MP(P)
            poset(42)

        ::

            sage: MP([3, 5, 7])
            poset(3, 5, 7)

        ::

            sage: MP(33)
            Traceback (most recent call last):
            ...
            TypeError: 33 is not iterable; do not know what to do with it.
        """
        if is_MutablePoset(data):
            if key is not None:
                raise TypeError('Cannot use key when data is a poset.')
            self._copy_shells_(data, lambda e: e)

        else:
            self.clear()

            if key is None:
                self._key_ = lambda k: k
            else:
                self._key_ = key

            self._merge_ = merge
            self._can_merge_ = can_merge

            if data is not None:
                try:
                    it = iter(data)
                except TypeError:
                    raise TypeError('%s is not iterable; do not know what to '
                                    'do with it.' % (data,))
                self.union_update(it)


    def clear(self):
        r"""
        Remove all elements from this poset.

        INPUT:

        Nothing.

        OUTPUT:

        Nothing.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(42); P
            poset(42)
            sage: P.clear()
            sage: print P.repr_full()
            poset()
            +-- null
            |   +-- no predecessors
            |   +-- successors:   oo
            +-- oo
            |   +-- predecessors:   null
            |   +-- no successors
        """
        self._null_ = MutablePosetShell(self, None)
        self._oo_ = MutablePosetShell(self, None)
        self._null_.successors().add(self._oo_)
        self._oo_.predecessors().add(self._null_)
        self._shells_ = {}


    def __len__(self):
        r"""
        Return the number of elements contained in this poset.

        INPUT:

        Nothing.

        OUTPUT:

        An integer.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: len(P)  # indirect doctest
            0
            sage: bool(P)
            False
            sage: P.add(42)
            sage: len(P)
            1
            sage: bool(P)
            True
        """
        return len(self._shells_)


    @property
    def null(self):
        r"""
        The shell `\emptyset` whose element is smaller than any
        other element.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: z = P.null; z
            null
            sage: z.is_null()
            True
        """
        return self._null_


    @property
    def oo(self):
        r"""
        The shell `\infty` whose element is larger than any other
        element.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: oo = P.oo; oo
            oo
            sage: oo.is_oo()
            True
        """
        return self._oo_


    def shell(self, key):
        r"""
        Return the shell of the element corresponding to ``key``.

        INPUT:

        ``key`` -- the key of an object.

        OUTPUT:

        An instance of :class:`MutablePosetShell`.

        .. NOTE::

            Each element is contained/encapsulated in a shell inside
            the poset.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(42)
            sage: e = P.shell(42); e
            42
            sage: type(e)
            <class 'sage.data_structures.mutable_poset.MutablePosetShell'>
        """
        return self._shells_[key]


    def element(self, key):
        r"""
        Return the element corresponding to ``key``.

        INPUT:

        ``key`` -- the key of an object.

        OUTPUT:

        An object.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(42)
            sage: e = P.element(42); e
            42
            sage: type(e)
            <type 'sage.rings.integer.Integer'>
        """
        return self.shell(key).element


    def get_key(self, element):
        r"""
        Return the key corresponding to the given element.

        INPUT:

        - ``element`` -- an object.

        OUTPUT:

        An object (the key of ``element``).

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: from sage.data_structures.mutable_poset import MutablePosetShell
            sage: P = MP()
            sage: P.get_key(None) is None
            True
            sage: P.get_key((1, 2))
            (1, 2)
            sage: Q = MP(key=lambda k: k[0])
            sage: Q.get_key((1, 2))
            1
        """
        if element is None:
            return None
        return self._key_(element)


    def _copy_shells_(self, other, mapping):
        r"""
        Copy shells from another poset.

        INPUT:

        - ``other`` -- the mutable poset from which the shells
          should be copied to this poset.

        - ``mapping`` -- a function that is applied to each element.

        OUTPUT:

        Nothing.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: Q = MP()
            sage: Q._copy_shells_(P, lambda e: e)
            sage: P.repr_full() == Q.repr_full()
            True
        """
        from copy import copy
        self._key_ = copy(other._key_)
        self._merge_ = copy(other._merge_)
        self._can_merge_ = copy(other._can_merge_)
        memo = {}
        self._null_ = other._null_._copy_all_linked_(memo, self, mapping)
        self._oo_ = memo[id(other._oo_)]
        self._shells_ = dict((f.key, f) for f in
                             iter(memo[id(e)] for e in
                                  other._shells_.itervalues()))


    def copy(self, mapping=None):
        r"""
        Creates a shallow copy.

        INPUT:

        - ``mapping`` -- a function which is applied on each of the elements.

        OUTPUT:

        A poset with the same content as ``self``.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: Q = copy(P)  # indirect doctest
            sage: P.repr_full() == Q.repr_full()
            True
        """
        if mapping is None:
            mapping = lambda element: element
        new = self.__class__()
        new._copy_shells_(self, mapping)
        return new


    __copy__ = copy


    def shells(self, include_special=False):
        r"""
        Return an iterator over all shells.

        INPUT:

        - ``include_special`` -- (default: ``False``) if set, then
          including shells containing a smallest element (`\emptyset`)
          and a largest element (`\infty`).

        OUTPUT:

        An iterator.

        .. NOTE::

            Each element is contained/encapsulated in a shell inside
            the poset.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: tuple(P.shells())
            ()
            sage: tuple(P.shells(include_special=True))
            (null, oo)
        """
        if include_special:
            yield self.null
        for e in self._shells_.itervalues():
            yield e
        if include_special:
            yield self.oo


    def shells_topological(self, include_special=False,
                           reverse=False, key=None):
        r"""
        Return an iterator over all shells in topological order.

        INPUT:

        - ``include_special`` -- (default: ``False``) if set, then
          including shells containing a smallest element (`\emptyset`)
          and a largest element (`\infty`).
 
        - ``reverse`` -- (default: ``False``) -- if set, reverses the
          order, i.e., ``False`` gives smallest elements first,
          ``True`` gives largest first.

        - ``key`` -- (default: ``None``) a function used for sorting
          the direct successors of a shell (used in case of a
          tie). If this is ``None``, no sorting according to the
          representation string occurs.

        OUTPUT:

        An iterator.

        .. NOTE::

            Each element is contained/encapsulated in a shell inside
            the poset.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: list(P.shells_topological())
            [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (4, 4)]
            sage: list(P.shells_topological(reverse=True))
            [(4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1)]
            sage: list(P.shells_topological(include_special=True))
            [null, (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (4, 4), oo]
            sage: list(P.shells_topological(
            ....:     include_special=True, reverse=True))
            [oo, (4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1), null]
        """
        if key is None:
            key = repr
        shell = self.oo if not reverse else self.null
        return iter(e for e in shell.iter_topological(reverse, key)
                    if include_special or not e.is_special())


    def elements(self, **kwargs):
        r"""
        Return an iterator over all elements.

        INPUT:

        - ``kwargs`` -- arguments are passed to :meth:`shells`.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3)
            sage: P.add(42)
            sage: P.add(7)
            sage: [(v, type(v)) for v in sorted(P.elements())]
            [(3, <type 'sage.rings.integer.Integer'>),
             (7, <type 'sage.rings.integer.Integer'>),
             (42, <type 'sage.rings.integer.Integer'>)]

        Note that

        ::

            sage: it = iter(P)
            sage: sorted(it)
            [3, 7, 42]

        returns all elements as well.
        """
        for shell in self.shells(**kwargs):
            yield shell.element


    __iter__ = elements


    def elements_topological(self, **kwargs):
        r"""
        Return an iterator over all elements in topological order.

        INPUT:

        - ``kwargs`` -- arguments are passed to :meth:`shells_topological`.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: [(v, type(v)) for v in P.elements_topological()]
            [((1, 1), <class '__main__.T'>),
             ((1, 2), <class '__main__.T'>),
             ((1, 3), <class '__main__.T'>),
             ((2, 1), <class '__main__.T'>),
             ((2, 2), <class '__main__.T'>),
             ((4, 4), <class '__main__.T'>)]
        """
        for shell in self.shells_topological(**kwargs):
            yield shell.element


    def keys(self, **kwargs):
        r"""
        Return an iterator over all keys of the elements.

        INPUT:

        - ``kwargs`` -- arguments are passed to :meth:`shells`.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP(key=lambda c: -c)
            sage: P.add(3)
            sage: P.add(42)
            sage: P.add(7)
            sage: [(v, type(v)) for v in sorted(P.keys())]
            [(-42, <type 'sage.rings.integer.Integer'>),
             (-7, <type 'sage.rings.integer.Integer'>),
             (-3, <type 'sage.rings.integer.Integer'>)]

            sage: [(v, type(v)) for v in sorted(P.elements())]
            [(3, <type 'sage.rings.integer.Integer'>),
             (7, <type 'sage.rings.integer.Integer'>),
             (42, <type 'sage.rings.integer.Integer'>)]

            sage: [(v, type(v)) for v in sorted(P.shells(),
            ....:                               key=lambda c: c.element)]
            [(3, <class 'sage.data_structures.mutable_poset.MutablePosetShell'>),
             (7, <class 'sage.data_structures.mutable_poset.MutablePosetShell'>),
             (42, <class 'sage.data_structures.mutable_poset.MutablePosetShell'>)]
        """
        for shell in self.shells(**kwargs):
            yield shell.key


    def keys_topological(self, **kwargs):
        r"""
        Return an iterator over all keys of the elements in
        topological order.

        INPUT:

        - ``kwargs`` -- arguments are passed to :meth:`shells_topological`.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP(key=lambda c: c[0])
            sage: P.add((1, 1))
            sage: P.add((1, 3))
            sage: P.add((2, 1))
            sage: P.add((4, 4))
            sage: P.add((1, 2))
            sage: P.add((2, 2))
            sage: [(v, type(v)) for v in P.keys_topological()]
            [(1, <type 'sage.rings.integer.Integer'>),
             (2, <type 'sage.rings.integer.Integer'>),
             (4, <type 'sage.rings.integer.Integer'>)]
            sage: [(v, type(v)) for v in P.elements_topological()]
            [((1, 1), <type 'tuple'>),
             ((2, 1), <type 'tuple'>),
             ((4, 4), <type 'tuple'>)]
            sage: [(v, type(v)) for v in P.shells_topological()]
            [((1, 1), <class 'sage.data_structures.mutable_poset.MutablePosetShell'>),
             ((2, 1), <class 'sage.data_structures.mutable_poset.MutablePosetShell'>),
             ((4, 4), <class 'sage.data_structures.mutable_poset.MutablePosetShell'>)]
        """
        for shell in self.shells_topological(**kwargs):
            yield shell.key


    def repr(self, include_special=False, reverse=False):
        r"""
        Return a representation of the poset.

        INPUT:

        Nothing.

        OUTPUT:

        A string.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: print MP().repr()
            poset()
        """
        s = 'poset('
        s += ', '.join(repr(shell) for shell in
                       self.shells_topological(include_special, reverse))
        s += ')'
        return s


    def repr_full(self, reverse=False):
        r"""
        Return a representation with ordering details of the poset.

        INPUT:

        Nothing.

        OUTPUT:

        A string.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: print MP().repr_full(reverse=True)
            poset()
            +-- oo
            |   +-- no successors
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   oo
            |   +-- no predecessors
        """
        sortedshells = tuple(
            self.shells_topological(include_special=True, reverse=reverse))
        strings = [self.repr(include_special=False, reverse=reverse)]
        for shell in sortedshells:
            strings.append('+-- ' + repr(shell))
            for rev in (not reverse, reverse):
                what = 'successors' if not rev else 'predecessors'
                if shell.successors(rev):
                    s = '|   +-- ' + what + ':   '
                    s += ', '.join(repr(e) for e in
                                   sortedshells if e in shell.successors(rev))
                else:
                    s = '|   +-- no ' + what
                strings.append(s)
        return '\n'.join(strings)


    __repr__ = repr


    def contains(self, key):
        r"""
        Tests if ``key`` is encapsulated by one of the poset's elements.

        INPUT:

        - ``key`` -- an object.

        OUTPUT:

        ``True`` or ``False``.

        TESTS::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: T((1, 1)) in P  # indirect doctest
            True
            sage: T((1, 2)) in P  # indirect doctest
            False
        """
        return key in self._shells_


    __contains__ = contains


    def add(self, element):
        r"""
        Add the given object as element to the poset.

        INPUT:

        - ``element`` -- an object (hashable and supporting comparison
          with the operator ``<=``.

        OUTPUT:

        Nothing.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: print P.repr_full(reverse=True)
            poset((4, 4), (1, 3), (1, 2), (2, 1), (1, 1))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4)
            +-- (4, 4)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3), (2, 1)
            +-- (1, 3)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 2)
            +-- (1, 2)
            |   +-- successors:   (1, 3)
            |   +-- predecessors: (1, 1)
            +-- (2, 1)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 1)
            +-- (1, 1)
            |   +-- successors:   (1, 2), (2, 1)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 1)
            |   +-- no predecessors
            sage: P.add(T((2, 2)))
            sage: reprP = P.repr_full(reverse=True); print reprP
            poset((4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4)
            +-- (4, 4)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3), (2, 2)
            +-- (1, 3)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 2)
            +-- (2, 2)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 2), (2, 1)
            +-- (1, 2)
            |   +-- successors:   (1, 3), (2, 2)
            |   +-- predecessors: (1, 1)
            +-- (2, 1)
            |   +-- successors:   (2, 2)
            |   +-- predecessors: (1, 1)
            +-- (1, 1)
            |   +-- successors:   (1, 2), (2, 1)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 1)
            |   +-- no predecessors

        When adding an element which is already in the poset, nothing happens::

            sage: e = T((2, 2))
            sage: P.add(e)
            sage: P.repr_full(reverse=True) == reprP
            True

        We can influence the behavior when an element with existing key
        is to be inserted in the poset. For example, we can perform an
        addition on some argument of the elements::

            sage: def add(left, right):
            ....:     return (left[0], ''.join(sorted(left[1] + right[1])))
            sage: A = MP(key=lambda k: k[0], merge=add)
            sage: A.add((3, 'a'))
            sage: A
            poset((3, 'a'))
            sage: A.add((3, 'b'))
            sage: A
            poset((3, 'ab'))

        We can also deal with cancellations. If the return value of
        our hook-function is ``None``, then the element is removed out of
        the poset::

            sage: def add_None(left, right):
            ....:     s = left[1] + right[1]
            ....:     if s == 0:
            ....:         return None
            ....:     return (left[0], s)
            sage: B = MP(key=lambda k: k[0],
            ....:        merge=add_None)
            sage: B.add((7, 42))
            sage: B.add((7, -42))
            sage: B
            poset()

        TESTS::

            sage: R = MP(key=lambda k: T(k[2:3]))
            sage: R.add((1, 1, 42))
            sage: R.add((1, 3, 42))
            sage: R.add((2, 1, 7))
            sage: R.add((4, 4, 42))
            sage: R.add((1, 2, 7))
            sage: R.add((2, 2, 7))
            sage: print R.repr_full(reverse=True)
            poset((1, 1, 42), (2, 1, 7))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (1, 1, 42)
            +-- (1, 1, 42)
            |   +-- successors:   oo
            |   +-- predecessors: (2, 1, 7)
            +-- (2, 1, 7)
            |   +-- successors:   (1, 1, 42)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (2, 1, 7)
            |   +-- no predecessors

        ::

            sage: P = MP()
            sage: P.add(None)
            Traceback (most recent call last):
            ...
            ValueError: None is not an allowed element.
        """
        if element is None:
            raise ValueError('None is not an allowed element.')
        key = self.get_key(element)

        if key in self._shells_:
            if self._merge_ is not None:
                self.shell(key).merge(element, delete=False)
            return

        new = MutablePosetShell(self, element)
        smaller = self.null.covers(new, reverse=False)
        larger = self.oo.covers(new, reverse=True)

        # In the following we first search towards oo (reverse=False) and
        # then towards null (reverse=True; everything is "inverted").
        for reverse in (False, True):
            sm = smaller if not reverse else larger
            la = larger if not reverse else smaller
            for shell in sm:
                for e in shell.successors(reverse).intersection(la):
                    e.predecessors(reverse).remove(shell)
                    shell.successors(reverse).remove(e)
                new.predecessors(reverse).add(shell)
                shell.successors(reverse).add(new)

        self._shells_[key] = new


    def remove(self, key, raise_key_error=True):
        r"""
        Remove the given object from the poset.

        INPUT:

        - ``key`` -- the key of an object.

        - ``raise_key_error`` -- (default: ``True``) switch raising
          ``KeyError`` on and off.

        OUTPUT:

        Nothing.

        If the element is not a member and ``raise_key_error`` is set
        (default), raise a ``KeyError``.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: print P.repr_full(reverse=True)
            poset((4, 4), (1, 3), (2, 2), (1, 2), (2, 1), (1, 1))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4)
            +-- (4, 4)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3), (2, 2)
            +-- (1, 3)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 2)
            +-- (2, 2)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 2), (2, 1)
            +-- (1, 2)
            |   +-- successors:   (1, 3), (2, 2)
            |   +-- predecessors: (1, 1)
            +-- (2, 1)
            |   +-- successors:   (2, 2)
            |   +-- predecessors: (1, 1)
            +-- (1, 1)
            |   +-- successors:   (1, 2), (2, 1)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 1)
            |   +-- no predecessors
            sage: P.remove(T((1, 2)))
            sage: print P.repr_full(reverse=True)
            poset((4, 4), (1, 3), (2, 2), (2, 1), (1, 1))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4)
            +-- (4, 4)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3), (2, 2)
            +-- (1, 3)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (1, 1)
            +-- (2, 2)
            |   +-- successors:   (4, 4)
            |   +-- predecessors: (2, 1)
            +-- (2, 1)
            |   +-- successors:   (2, 2)
            |   +-- predecessors: (1, 1)
            +-- (1, 1)
            |   +-- successors:   (1, 3), (2, 1)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 1)
            |   +-- no predecessors

        TESTS::

            sage: Q = MP(key=lambda k: T(k[0:2]))
            sage: Q.add((1, 1, 42))
            sage: Q.add((1, 3, 42))
            sage: Q.add((2, 1, 7))
            sage: Q.add((4, 4, 42))
            sage: Q.add((1, 2, 7))
            sage: Q.add((2, 2, 7))
            sage: print Q.repr_full(reverse=True)
            poset((4, 4, 42), (1, 3, 42), (2, 2, 7),
                  (1, 2, 7), (2, 1, 7), (1, 1, 42))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4, 42)
            +-- (4, 4, 42)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3, 42), (2, 2, 7)
            +-- (1, 3, 42)
            |   +-- successors:   (4, 4, 42)
            |   +-- predecessors: (1, 2, 7)
            +-- (2, 2, 7)
            |   +-- successors:   (4, 4, 42)
            |   +-- predecessors: (1, 2, 7), (2, 1, 7)
            +-- (1, 2, 7)
            |   +-- successors:   (1, 3, 42), (2, 2, 7)
            |   +-- predecessors: (1, 1, 42)
            +-- (2, 1, 7)
            |   +-- successors:   (2, 2, 7)
            |   +-- predecessors: (1, 1, 42)
            +-- (1, 1, 42)
            |   +-- successors:   (1, 2, 7), (2, 1, 7)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 1, 42)
            |   +-- no predecessors
            sage: Q.remove((1,1))
            sage: print Q.repr_full(reverse=True)
            poset((4, 4, 42), (1, 3, 42), (2, 2, 7), (1, 2, 7), (2, 1, 7))
            +-- oo
            |   +-- no successors
            |   +-- predecessors: (4, 4, 42)
            +-- (4, 4, 42)
            |   +-- successors:   oo
            |   +-- predecessors: (1, 3, 42), (2, 2, 7)
            +-- (1, 3, 42)
            |   +-- successors:   (4, 4, 42)
            |   +-- predecessors: (1, 2, 7)
            +-- (2, 2, 7)
            |   +-- successors:   (4, 4, 42)
            |   +-- predecessors: (1, 2, 7), (2, 1, 7)
            +-- (1, 2, 7)
            |   +-- successors:   (1, 3, 42), (2, 2, 7)
            |   +-- predecessors: null
            +-- (2, 1, 7)
            |   +-- successors:   (2, 2, 7)
            |   +-- predecessors: null
            +-- null
            |   +-- successors:   (1, 2, 7), (2, 1, 7)
            |   +-- no predecessors

        ::

            sage: P = MP()
            sage: P.remove(None)
            Traceback (most recent call last):
            ...
            ValueError: None is not an allowed key.
        """
        if key is None:
            raise ValueError('None is not an allowed key.')

        try:
            shell = self._shells_[key]
        except KeyError:
            if not raise_key_error:
                return
            raise KeyError('Key %s is not contained in this poset.' % (key,))

        for reverse in (False, True):
            for p in shell.predecessors(reverse):
                S = p.successors(reverse)
                S.remove(shell)
                D = set(s for s in p.iter_depth_first(reverse)
                        if s in shell.successors(reverse))
                S.update(shell.successors(reverse))
                S.difference_update(D)
        del self._shells_[key]


    def discard(self, key, raise_key_error=False):
        r"""
        Remove the given object from the poset.

        INPUT:

        - ``key`` -- the key of an object.

        - ``raise_key_error`` -- (default: ``False``) switch raising
          ``KeyError`` on and off.

        OUTPUT:

        Nothing.

        If the element is not a member and ``raise_key_error`` is set
        (not default), raise a ``KeyError``.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: P.discard(T((1, 2)))
            sage: P.remove(T((1, 2)))
            Traceback (most recent call last):
            ...
            KeyError: 'Key (1, 2) is not contained in this poset.'
            sage: P.discard(T((1, 2)))
        """
        return self.remove(key, raise_key_error)


    def pop(self, **kwargs):
        r"""
        Remove and return an arbitrary poset element.

        INPUT:

        - ``kwargs`` -- arguments are passed to :meth:`shells_topological`.

        OUTPUT:

        An object.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP(key=lambda c: -c)
            sage: P.add(3)
            sage: P
            poset(3)
            sage: P.pop()
            3
            sage: P
            poset()
            sage: P.pop()
            Traceback (most recent call last):
            ...
            KeyError: 'pop from an empty poset'
        """
        try:
            del kwargs['include_special']
        except KeyError:
            pass
        kwargs['include_special'] = False

        try:
            shell = next(self.shells_topological(**kwargs))
        except StopIteration:
            raise KeyError('pop from an empty poset')
        self.remove(shell.key)
        return shell.element


    def union(self, *other):
        r"""
        Return the union of the given posets as a new poset

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        A poset.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.union(Q)
            poset(3, 4, 7, 8, 42)

        TESTS::

            sage: P.union(P, Q, Q, P)
            poset(3, 4, 7, 8, 42)
       """
        new = self.copy()
        for o in other:
            new.update(o)
        return new


    def union_update(self, other):
        r"""
        Update this poset with the union of itself and another poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        .. TODO::

            Use the already existing information in the other poset to speed
            up this function. (At the moment each element of the other poset
            is inserted one by one and without using this information.)

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.union_update(Q)
            sage: P
            poset(3, 4, 7, 8, 42)

        TESTS::

            sage: Q.update(P)
            sage: Q
            poset(3, 4, 7, 8, 42)
        """
        try:
            it = other.elements()
        except AttributeError:
            it = iter(other)
        for element in it:
            self.add(element)


    update = union_update  # as in a Python set
    r"""
    Alias of :meth:`union_update`.
    """


    def difference(self, *other):
        r"""
        Return a new poset where all elements of this poset, which are
        contained in one of the other given posets, are removed.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        A poset.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.difference(Q)
            poset(3, 7)

        TESTS::

            sage: P.difference(Q, Q)
            poset(3, 7)
            sage: P.difference(P)
            poset()
            sage: P.difference(Q, P)
            poset()
        """
        new = self.copy()
        for o in other:
            new.difference_update(o)
        return new


    def difference_update(self, other):
        r"""
        Remove all elements of another poset from this poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.difference_update(Q)
            sage: P
            poset(3, 7)
        """
        try:
            it = other.keys()
        except AttributeError:
            it = iter(other)
        for key in it:
            self.discard(key)


    def intersection(self, *other):
        r"""
        Return the intersection of the given posets as a new poset

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        A poset.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.intersection(Q)
            poset(42)

        TESTS::

            sage: P.intersection(P, Q, Q, P)
            poset(42)
        """
        new = self.copy()
        for o in other:
            new.intersection_update(o)
        return new


    def intersection_update(self, other):
        r"""
        Update this poset with the intersection of itself and another poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.intersection_update(Q)
            sage: P
            poset(42)
        """
        try:
            keys = tuple(self.keys())
        except AttributeError:
            keys = tuple(iter(self))
        for key in keys:
            if key not in other:
                self.discard(key)


    def symmetric_difference(self, other):
        r"""
        Return the symmetric difference of two posets as a new poset.

        INPUT:

        - ``other`` -- a poset.

        OUTPUT:

        A poset.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.symmetric_difference(Q)
            poset(3, 4, 7, 8)
        """
        new = self.copy()
        new.symmetric_difference_update(other)
        return new


    def symmetric_difference_update(self, other):
        r"""
        Update this poset with the symmetric difference of itself and
        another poset.

        INPUT:

        - ``other`` -- a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.symmetric_difference_update(Q)
            sage: P
            poset(3, 4, 7, 8)
        """
        T = other.difference(self)
        self.difference_update(other)
        self.union_update(T)


    def is_disjoint(self, other):
        r"""
        Return if another poset is disjoint to this poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.is_disjoint(Q)
            False
            sage: P.is_disjoint(Q.difference(P))
            True
        """
        return all(key not in other for key in self.keys())


    isdisjoint = is_disjoint  # as in a Python set
    r"""
    Alias of :meth:`is_disjoint`.
    """


    def is_subset(self, other):
        r"""
        Return if another poset contains this poset, i.e., if this poset
        is a subset of the other poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.is_subset(Q)
            False
            sage: Q.is_subset(P)
            False
            sage: P.is_subset(P)
            True
            sage: P.is_subset(P.union(Q))
            True
        """
        return all(key in other for key in self.keys())


    issubset = is_subset  # as in a Python set
    r"""
    Alias of :meth:`is_subset`.
    """


    def is_superset(self, other):
        r"""
        Return if this poset contains another poset, i.e., if this poset
        is a superset of the other poset.

        INPUT:

        - ``other`` -- a poset or an iterable. In the latter case the
          iterated objects are seen as elements of a poset.

        OUTPUT:

        Nothing.

        .. NOTE::

            If this poset uses a ``key``-function, then all
            comparisons are performed on the keys of the elements (and
            not on the elements themselves).

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: P = MP()
            sage: P.add(3); P.add(42); P.add(7); P
            poset(3, 7, 42)
            sage: Q = MP()
            sage: Q.add(4); Q.add(8); Q.add(42); Q
            poset(4, 8, 42)
            sage: P.is_superset(Q)
            False
            sage: Q.is_superset(P)
            False
            sage: P.is_superset(P)
            True
            sage: P.union(Q).is_superset(P)
            True
        """
        try:
            it = other.keys()
        except AttributeError:
            it = iter(other)
        return all(key in self for key in it)


    issuperset = is_superset  # as in a Python set
    r"""
    Alias of :meth:`is_superset`.
    """


    def merge(self, key=None, reverse=False):
        r"""
        Merge the given element with its successors/predecessors.

        INPUT:

        - ``key`` -- the key specifying an element or ``None``
          (default), in which case this method is called on each
          element in this poset.

        - ``reverse`` -- (default: ``False``) specifies which
          direction to go first. When ``key=None``, then this also
          specifies which elements are merged first.

        OUTPUT:

        Nothing.

        This method tests all (not necessarily direct) successors and
        predecessors of the given element if they can be merged with
        the element itself. This is done by the ``can_merge``-function
        of :class:`MutablePoset`. If this merge is possible, then it
        is performed by calling :class:`MutablePoset`'s
        ``merge``-function and the corresponding successor/predecessor
        is removed from the poset.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: key = lambda t: T(t[0:2])
            sage: def add(left, right):
            ....:     return (left[0], left[1],
            ....:             ''.join(sorted(left[2] + right[2])))
            sage: def can_add(left, right):
            ....:     return key(left) >= key(right)
            sage: P = MP(key=key, merge=add, can_merge=can_add)
            sage: P.add((1, 1, 'a'))
            sage: P.add((1, 3, 'b'))
            sage: P.add((2, 1, 'c'))
            sage: P.add((4, 4, 'd'))
            sage: P.add((1, 2, 'e'))
            sage: P.add((2, 2, 'f'))
            sage: Q = copy(P)
            sage: Q.merge(T((1, 3)))
            sage: print Q.repr_full(reverse=True)
            poset((4, 4, 'd'), (1, 3, 'abe'), (2, 2, 'f'), (2, 1, 'c'))
            +-- oo
            |   +-- no successors
            |   +-- predecessors:   (4, 4, 'd')
            +-- (4, 4, 'd')
            |   +-- successors:   oo
            |   +-- predecessors:   (1, 3, 'abe'), (2, 2, 'f')
            +-- (1, 3, 'abe')
            |   +-- successors:   (4, 4, 'd')
            |   +-- predecessors:   null
            +-- (2, 2, 'f')
            |   +-- successors:   (4, 4, 'd')
            |   +-- predecessors:   (2, 1, 'c')
            +-- (2, 1, 'c')
            |   +-- successors:   (2, 2, 'f')
            |   +-- predecessors:   null
            +-- null
            |   +-- successors:   (1, 3, 'abe'), (2, 1, 'c')
            |   +-- no predecessors
            sage: for k in P.keys():
            ....:     Q = copy(P)
            ....:     Q.merge(k)
            ....:     print 'merging %s: %s' % (k, Q)
            merging (1, 2): poset((1, 2, 'ae'), (1, 3, 'b'),
                                  (2, 1, 'c'), (2, 2, 'f'), (4, 4, 'd'))
            merging (1, 3): poset((1, 3, 'abe'), (2, 1, 'c'),
                                  (2, 2, 'f'), (4, 4, 'd'))
            merging (4, 4): poset((4, 4, 'abcdef'))
            merging (2, 1): poset((1, 2, 'e'), (1, 3, 'b'),
                                  (2, 1, 'ac'), (2, 2, 'f'), (4, 4, 'd'))
            merging (2, 2): poset((1, 3, 'b'), (2, 2, 'acef'), (4, 4, 'd'))
            merging (1, 1): poset((1, 1, 'a'), (1, 2, 'e'), (1, 3, 'b'),
                                  (2, 1, 'c'), (2, 2, 'f'), (4, 4, 'd'))
            sage: Q = copy(P)
            sage: Q.merge(); Q
            poset((4, 4, 'abcdef'))

        TESTS::

            sage: copy(P).merge(reverse=False) == copy(P).merge(reverse=True)
            True

        ::

            sage: P = MP(srange(4),
            ....:        merge=lambda l, r: l, can_merge=lambda l, r: l >= r); P
            poset(0, 1, 2, 3)
            sage: Q = P.copy()
            sage: Q.merge(reverse=True); Q
            poset(3)
            sage: R = P.mapped(lambda x: x+1)
            sage: R.merge(reverse=True); R
            poset(4)
        """
        if key is None:
            for shell in tuple(self.shells_topological(reverse=reverse)):
                if shell.key in self._shells_:
                    self.merge(key=shell.key)
            return

        shell = self.shell(key)
        def can_merge(other):
            return self._can_merge_(shell.element, other.element)
        for rev in (reverse, not reverse):
            to_merge = shell.iter_depth_first(
                reverse=rev, condition=can_merge)
            try:
                next(to_merge)
            except StopIteration:
                raise RuntimeError('Stopping merge before started; the '
                                   'can_merge-function is not reflexive.')
            for m in tuple(to_merge):
                if m.is_special():
                    continue
                shell.merge(m.element, delete=True)


    def maximal_elements(self):
        r"""
        Return an iterator over the maximal elements of this poset.

        INPUT:

        Nothing.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 1)))
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: list(P.maximal_elements())
            [(1, 3), (2, 2)]
        """
        return iter(shell.element
                    for shell in self.oo.predecessors()
                    if not shell.is_special())


    def minimal_elements(self):
        r"""
        Return an iterator over the minimal elements of this poset.

        INPUT:

        Nothing.

        OUTPUT:

        An iterator.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: list(P.minimal_elements())
            [(1, 2), (2, 1)]
        """
        return iter(shell.element
                    for shell in self.null.successors()
                    if not shell.is_special())


    def map(self, function, topological=False, reverse=False):
        r"""
        Apply the given ``function`` to each element of this poset.

        INPUT:

        - ``function`` -- a function mapping an existing element to
          a new element.

        - ``topological`` -- (default: ``False``) if set, then the
          mapping is done in topological order, otherwise unordered.

        - ``reverse`` -- is passed on to topological ordering.

        OUTPUT:

        Nothing.

        .. NOTE::

            Since this method works inplace, it is not allowed that
            ``function`` alters the key of an element.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: P.map(lambda e: str(e))
            sage: P
            poset('(1, 2)', '(1, 3)', '(2, 1)', '(2, 2)', '(4, 4)')
        """
        shells = self.shells_topological(reverse=reverse) \
            if topological else self.shells()
        for shell in shells:
            shell._element_ = function(shell._element_)


    def mapped(self, function):
        r"""
        Return a poset where on each element the given ``function``
        was applied.

        INPUT:

        - ``function`` -- a function mapping an existing element to
          a new element.

        - ``topological`` -- (default: ``False``) if set, then the
          mapping is done in topological order, otherwise unordered.

        - ``reverse`` -- is passed on to topological ordering.

        OUTPUT:

        A :class:`MutablePoset`.

        EXAMPLES::

            sage: from sage.data_structures.mutable_poset import MutablePoset as MP
            sage: class T(tuple):
            ....:     def __le__(left, right):
            ....:         return all(l <= r for l, r in zip(left, right))
            sage: P = MP()
            sage: P.add(T((1, 3)))
            sage: P.add(T((2, 1)))
            sage: P.add(T((4, 4)))
            sage: P.add(T((1, 2)))
            sage: P.add(T((2, 2)))
            sage: P.mapped(lambda e: str(e))
            poset('(1, 2)', '(1, 3)', '(2, 1)', '(2, 2)', '(4, 4)')
        """
        return self.copy(mapping=function)


# *****************************************************************************
