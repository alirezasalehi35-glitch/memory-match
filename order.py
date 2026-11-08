from decimal import Decimal

class Order:
    def __init__(self, order_id: int, service_category: str, 
                 starting_position: tuple, finishing_position: tuple, cost: Decimal):
        
        # اعتبارسنجی‌ها دقیقاً مطابق قرارداد پروژه
        if not isinstance(order_id, int) or isinstance(order_id, bool) or order_id <= 0:
            raise ValueError("شناسه سفارش باید یک عدد صحیح مثبت باشد.")
        if service_category not in ['BIKE', 'VAN', 'TRUCK']:
            raise ValueError("دسته وسیله نامعتبر است.")
        if not isinstance(starting_position, tuple) or len(starting_position) != 2 or not all(isinstance(c, int) and not isinstance(c, bool) for c in starting_position):
            raise TypeError("مبدأ باید یک تاپل دو عضوی از اعداد صحیح باشد.")
        if not isinstance(finishing_position, tuple) or len(finishing_position) != 2 or not all(isinstance(c, int) and not isinstance(c, bool) for c in finishing_position):
            raise TypeError("مقصد باید یک تاپل دو عضوی از اعداد صحیح باشد.")
        if not isinstance(cost, Decimal) or cost <= 0:
            raise ValueError("هزینه سفارش باید از نوع Decimal و مثبت باشد.")

        self._order_id = order_id
        self._service_category = service_category
        self._starting_position = starting_position
        self._finishing_position = finishing_position
        self._cost = cost
        self._status = 'PENDING'
        self._assigned_driver = None

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def service_category(self) -> str:
        return self._service_category

    @property
    def starting_position(self) -> tuple:
        return self._starting_position

    @property
    def finishing_position(self) -> tuple:
        return self._finishing_position

    @property
    def cost(self) -> Decimal:
        return self._cost

    @property
    def status(self) -> str:
        return self._status

    @property
    def assigned_driver(self):
        return self._assigned_driver

    def is_pending(self) -> bool:
        return self._status == 'PENDING'