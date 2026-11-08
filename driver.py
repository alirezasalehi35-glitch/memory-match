from decimal import Decimal

class Driver:
    def __init__(self, username: str, position: tuple, service_category: str):
        # اعتبارسنجی‌ها و مقداردهی اولیه
        if not isinstance(username, str) or not username.strip():
            raise ValueError("نام کاربری نامعتبر است.")
        if not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(coord, int) and not isinstance(coord, bool) for coord in position):
            raise TypeError("موقعیت باید یک تاپل دو عضوی از اعداد صحیح باشد.")
        if service_category not in ['BIKE', 'VAN', 'TRUCK']:
            raise ValueError("دسته وسیله نامعتبر است.")

        self._username = username
        self._position = position
        self._service_category = service_category
        self._credit = Decimal('0')
        self._status = 'FREE'
        self._current_order = None

    @property
    def username(self) -> str:
        return self._username

    @property
    def position(self) -> tuple:
        return self._position

    @property
    def service_category(self) -> str:
        return self._service_category

    @property
    def credit(self) -> Decimal:
        return self._credit

    @property
    def status(self) -> str:
        return self._status

    @property
    def current_order(self):
        return self._current_order

    def is_available(self) -> bool:
        return self._status == 'FREE'