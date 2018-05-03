# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.syscohada_2018.tests.test_syscohada_2018 import create_chart
except ImportError:
    from .test_syscohada_2018 import create_chart

__all__ = ['create_chart']