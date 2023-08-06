# -*- coding: utf-8 -*-

"""Strain energy evaluators.

This package gathers the implementations of the strain energy
evaluators. These return the value of the strain energy density and
the outer cut-off radius. According to the elasticity theory [1]_ [2]_,
the strain energy is written:

.. math::

   dE = \\frac{1}{2} dV \\sum_{i=x,y,z} \\sum_{j=x,y,z} \\sigma_{ij}
   e_{ij}

With:

* :math:`E` strain energy (:math:`\\mathrm{J}`).

* :math:`V` volume (:math:`\\mathrm{m}^3`).

* :math:`\\sigma` stress (:math:`\\mathrm{Pa}`).

* :math:`e` strain.

The strain field induced by a single screw dislocation is written:

.. math::

   e_{xx} &= e_{yy} = e_{zz} = e_{xy} = e_{yx} = 0

   e_{xz} &= e_{zx} = - \\frac{b}{4 \\pi} \\frac{y}{x^2 + y^2}

   e_{yz} &= e_{zy} = \\frac{b}{4 \\pi} \\frac{x}{x^2 + y^2}

The stress field induced by a single screw dislocation is written:

.. math::

   \\sigma_{xx} &= \\sigma_{yy} = \\sigma_{zz} = \\sigma_{xy} =
   \\sigma_{yx} = 0

   \\sigma_{xz} &= \\sigma_{zx} = - \\frac{G b}{2 \\pi} \\frac{y}{
   x^2 + y^2}

   \\sigma_{yz} &= \\sigma_{zy} = \\frac{G b}{2 \\pi} \\frac{x}{
   x^2 + y^2}

The strain field induced by a single edge dislocation is written:

.. math::

   e_{xx} &= - \\frac{b}{4 \\pi (1 - \\nu)} \\frac{y}{x^2 + y^2} \\left(
   \\frac{x^2 - y^2}{x^2 + y^2} + 2 (1 - \\nu) \\right)

   e_{yy} &= \\frac{b}{4 \\pi (1 - \\nu)} \\frac{y}{x^2 + y^2} \\left(
   \\frac{3x^2 + y^2}{x^2 + y^2} - 2 (1 - \\nu) \\right)

   e_{zz} &= 0

   e_{xy} &= e_{yx} = \\frac{b}{4 \\pi (1 - \\nu)} \\frac{x (x^2 - y^2)
   }{(x^2 + y^2)^2}

   e_{xz} &= e_{zx} = 0

The stress field induced by a single edge dislocation is written:

.. math::

   \\sigma_{xx} &= - \\frac{G b}{2 \\pi (1 - \\nu)} \\frac{y (3x^2 +
   y^2)}{(x^2 + y^2)^2}

   \\sigma_{yy} &= \\frac{G b}{2 \\pi (1 - \\nu)} \\frac{y (x^2 - y^2)
   }{(x^2 + y^2)^2}

   \\sigma_{zz} &= \\nu(\\sigma_{xx} + \\sigma_{yy})

   \\sigma_{xy} &= \\sigma_{yx} = \\frac{G b}{2 \\pi (1 - \\nu)}
   \\frac{x (x^2 - y^2)}{(x^2 + y^2)^2}

   \\sigma_{xz} &= \\sigma_{zx} = \\sigma_{yz} = \\sigma_{zy} = 0

With:

* :math:`b` Burgers vector length (:math:`\\mathrm{m}`).

* :math:`x` dislocation x-coordinate with respect to the observation
  position (:math:`\\mathrm{m}`).

* :math:`y` dislocation y-coordinate with respect to the observation
  position (:math:`\\mathrm{m}`).

* :math:`\\nu` Poisson's number.

* :math:`G` shear modulus (:math:`\\mathrm{Pa}`).

Finally, we introduce the effective outer cut-off ratio :math:`R_e`
with the following expressions:

.. math::

   E_{\\text{screw}} &= V \\frac{G b^2}{4 \\pi} \\rho \\ln\\left(
   \\frac{R_e}{r_0} \\right)

   E_{\\text{edge}} &= V \\frac{G b^2}{4 \\pi (1 - \\nu)} \\rho
   \\ln\\left( \\frac{R_e}{r_0} \\right)


With:

* :math:`\\rho` dislocation density (:math:`\\mathrm{m}^{-2}`).

* :math:`R_e` outer cut-off radius (:math:`\\mathrm{m}`).

* :math:`r_0` dislocation core radius (:math:`\\mathrm{m}`).

.. [1] D. Hull and D. J. Bacon.
   Introduction to dislocations. Elsevier, 2011. ISBN:
   978-0-08-096672-4. DOI: 10.1016/C2009-0-64358-0.

.. [2] F. R. N. Nabarro.
   Theory of crystal dislocations. Oxford Clarendon Press, 1967.

"""
