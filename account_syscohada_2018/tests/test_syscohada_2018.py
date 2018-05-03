# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from trytond.pool import Pool
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import doctest_teardown
from trytond.tests.test_tryton import doctest_checker
from trytond.transaction import Transaction
from trytond.exceptions import UserError

from trytond.modules.company.tests import create_company, set_company
from trytond.modules.currency.tests import create_currency


def create_chart(company, tax=False):
    pool = Pool()
    AccountTemplate = pool.get('account.account.template')
    TaxTemplate = pool.get('account.tax.template')
    TaxCodeTemplate = pool.get('account.tax.code.template')
    ModelData = pool.get('ir.model.data')
    CreateChart = pool.get('account.create_chart', type='wizard')
    Account = pool.get('account.account')

    template = AccountTemplate(ModelData.get_id(
            'account', 'account_syscohada_2018_1'))

    session_id, _, _ = CreateChart.create()
    create_chart = CreateChart(session_id)
    create_chart.account.account_template = template
    create_chart.account.company = company
    create_chart.transition_create_account()
    receivable, = Account.search([
            ('kind', '=', 'receivable'),
            ('company', '=', company.id),
            ])
    payable, = Account.search([
            ('kind', '=', 'payable'),
            ('company', '=', company.id),
            ])
    create_chart.properties.company = company
    create_chart.properties.account_receivable = receivable
    create_chart.properties.account_payable = payable
    create_chart.transition_create_properties()