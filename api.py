# This file is part of the carrier_send_shipments_mrw module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Equal
import logging

try:
    from mrw.picking import API
except ImportError:
    logger = logging.getLogger(__name__)
    message = 'Install MRW: pip install mrw'
    logger.error(message)
    raise Exception(message)

__all__ = ['CarrierApi']
__metaclass__ = PoolMeta


class CarrierApi:
    __name__ = 'carrier.api'
    mrw_franchise = fields.Char('Franchise', states={
            'required': Eval('method') == 'mrw',
        }, help='MRW franchise')
    mrw_subscriber = fields.Char('Subscriber', states={
            'required': Eval('method') == 'mrw',
        }, help='MRW subscriber')
    mrw_department = fields.Char('Department', states={
            'required': Eval('method') == 'mrw',
        }, help='MRW department')

    @classmethod
    def get_carrier_app(cls):
        'Add Carrier MRW APP'
        res = super(CarrierApi, cls).get_carrier_app()
        res.append(('mrw', 'MRW'))
        return res

    @classmethod
    def view_attributes(cls):
        return super(CarrierApi, cls).view_attributes() + [
            ('//page[@id="mrw"]', 'states', {
                    'invisible': Not(Equal(Eval('method'), 'mrw')),
                    })]

    @classmethod
    def test_mrw(cls, api):
        'Test MRW connection'
        message = 'Connection unknown result'

        with API(api.username, api.password, api.mrw_franchise, api.mrw_subscriber, api.mrw_department, api.debug) \
                as mrw_api:
            message = mrw_api.test_connection()
        cls.raise_user_error(message)
