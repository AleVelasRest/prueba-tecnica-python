from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Extendido de modelo sale.order para agregar nuevos campos y métodos.

    - Restricción al numero de órden que sea 10 o mayor.
    - Campo para seleccionar la compañía externa.
    - Campo para indicar si la orden es grande cuando el total es mayor a 500.
    """

    _inherit = "sale.order"
    x_order_number = fields.Integer(
        string="Número de Orden",
        help="El número de la orden de venta debe ser mayor o igual a 10.",
    )
    x_external_company = fields.Selection(
        string="Compañía Externa",
        selection=[
            ("ecommerce", "E-commerce"),
            ("manual", "Manual"),
            ("amazon", "Amazon"),
        ],
        help="Seleccione la compañía externa para la órden.",
    )

    # Marca la órden como grande si el total es mayor a 500
    x_is_big_order = fields.Boolean(
        string="Orden Grande",
        compute="_compute_is_big_order",
        store=True,
        help="Esta órden es grande porque el total es mayor a 500.",
    )

    @api.depends("amount_total")
    def _compute_is_big_order(self):
        """
        Evalúa si el total de la órden es mayor a 500 para almacenar
        Verdadero en la base de datos.
        """
        for order in self:
            order.x_is_big_order = order.amount_total > 500

    @api.constrains("x_order_number")
    def _check_x_order_number_min(self):
        """
        Valida que el número de órden sea 10 o mayor.
        """
        for record in self:
            if record.x_order_number and record.x_order_number < 10:
                raise ValidationError("El número de orden debe ser mayor o igual a 10.")
