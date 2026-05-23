from typing import Optional


class SQLFilterBuilder:
    def __init__(
        self,
        city: Optional[str] = None,
        category: Optional[str] = None,
        payment_method: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ):
        self.city = city
        self.category = category
        self.payment_method = payment_method
        self.date_from = date_from
        self.date_until = date_until

    def build(self) -> tuple[str, tuple]:
        conditions = []
        params = []

        if self.city:
            conditions.append("ciudad = %s")
            params.append(self.city)

        if self.category:
            conditions.append("categoria = %s")
            params.append(self.category)

        if self.payment_method:
            conditions.append("metodo_pago = %s")
            params.append(self.payment_method)

        if self.date_from:
            conditions.append("fecha >= %s")
            params.append(self.date_from)

        if self.date_until:
            conditions.append("fecha <= %s")
            params.append(self.date_until)

        where_clause = (
            "WHERE " + " AND ".join(conditions)
            if conditions
            else ""
        )

        return where_clause, tuple(params)
