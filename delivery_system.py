from decimal import Decimal
from driver import Driver
from order import Order

class DeliverySystem:
    def __init__(self):
        self._drivers = {}  # دیکشنری برای نگهداری راننده‌ها بر اساس نام کاربری
        self._orders = {}   # دیکشنری برای نگهداری سفارش‌ها بر اساس شناسه
        self._company_credit = Decimal('0')

    @property
    def company_credit(self) -> Decimal:
        return self._company_credit

    @property
    def total_drivers(self) -> int:
        return len(self._drivers)

    def add_driver(self, username: str, position: tuple, service_category: str) -> bool:
        # اعتبارسنجی‌ها دقیقاً مطابق قرارداد
        if not isinstance(username, str) or not username.strip():
            raise ValueError("نام کاربری نامعتبر است.")
        if username in self._drivers:
            return False  # نام تکراری، بدون تغییر وضعیت سامانه
        
        # ساخت راننده (اعتبارسنجی‌های داخلی Driver اجرا می‌شوند)
        new_driver = Driver(username, position, service_category)
        self._drivers[username] = new_driver
        return True

    def create_order(self, service_category: str, starting_position: tuple, finishing_position: tuple) -> int | None:
        if starting_position == finishing_position:
            return None  # مبدأ و مقصد برابر، بدون مصرف شناسه
        
        order_id = len(self._orders) + 1  # شناسه‌ها از ۱ و پیوسته
        
        # محاسبه هزینه: Decimal(100) * Decimal(k + d)
        # k: شمار سفارش‌های PENDING همان دسته با احتساب سفارش تازه
        k = sum(1 for o in self._orders.values() if o.service_category == service_category and o.is_pending()) + 1
        
        # فاصله Manhattan: abs(x1-x2) + abs(y1-y2)
        d = abs(starting_position[0] - finishing_position[0]) + abs(starting_position[1] - finishing_position[1])
        
        cost = Decimal(100) * Decimal(k + d)
        
        new_order = Order(order_id, service_category, starting_position, finishing_position, cost)
        self._orders[order_id] = new_order
        return order_id

    def assign_next_order(self, username: str) -> int | None:
        if username not in self._drivers:
            raise KeyError("راننده یافت نشد.")
        
        driver = self._drivers[username]
        if not driver.is_available():
            raise RuntimeError("راننده مشغول است.")
        
        # یافتن سفارش‌های PENDING با همان نوع وسیله
        compatible_pending_orders = [
            o for o in self._orders.values()
            if o.service_category == driver.service_category and o.is_pending()
        ]
        
        if not compatible_pending_orders:
            return None

        # نزدیک‌ترین سفارش بر اساس فاصله Manhattan مبدأ سفارش تا موقعیت راننده
        # در تساوی فاصله، قدیمی‌تر (شناسه کمتر) اولویت دارد
        def order_sort_key(order):
            dist = abs(order.starting_position[0] - driver.position[0]) + abs(order.starting_position[1] - driver.position[1])
            return (dist, order.order_id)

        target_order = min(compatible_pending_orders, key=order_sort_key)

        # تغییر وضعیت‌ها و برقراری ارتباط دوطرفه
        target_order._status = 'ARRIVED'
        target_order._assigned_driver = driver
        driver._status = 'BUSY'
        driver._current_order = target_order

        return target_order.order_id

    def update_order_status(self, username: str, order_id: int, new_status: str) -> bool:
        if username not in self._drivers:
            raise KeyError("راننده یافت نشد.")
        if order_id not in self._orders:
            return False

        driver = self._drivers[username]
        order = self._orders[order_id]

        # بررسی تعلق سفارش به راننده
        if order.assigned_driver != driver:
            return False

        if new_status == 'PICKUP':
            if order.status != 'ARRIVED':
                return False
            order._status = 'PICKUP'
            driver._position = order.starting_position
            return True

        elif new_status == 'DELIVERED':
            if order.status != 'PICKUP':
                return False
            order._status = 'DELIVERED'
            driver._position = order.finishing_position
            
            # محاسبه درآمد: ۸۰٪ راننده، ۲۰٪ شرکت
            driver_share = order.cost * Decimal('0.8')
            company_share = order.cost * Decimal('0.2')
            
            driver._credit += driver_share
            self._company_credit += company_share
            
            driver._status = 'FREE'
            driver._current_order = None
            return True

        return False

    def get_driver(self, username: str) -> tuple | None:
        if username not in self._drivers:
            return None
        d = self._drivers[username]
        return (d.status, d.position, d.credit)

    def get_order(self, order_id: int) -> tuple | None:
        if order_id not in self._orders:
            return None
        o = self._orders[order_id]
        assigned_name = o.assigned_driver.username if o.assigned_driver else None
        return (o.status, assigned_name, o.cost)

    def get_order_list(self, status: str) -> list[int]:
        return [o.order_id for o in self._orders.values() if o.status == status]

    def get_driver_list(self, status: str) -> list[str]:
        return [d.username for d in self._drivers.values() if d.status == status]

    def get_near_drivers(self, position: tuple, count: int) -> list[str]:
        free_drivers = [d for d in self._drivers.values() if d.is_available()]
        
        def driver_sort_key(d):
            dist = abs(d.position[0] - position[0]) + abs(d.position[1] - position[1])
            # در تساوی فاصله، ثبت قدیمی‌تر (ترتیب ورود به دیکشنری حفظ شده)
            return dist

        sorted_drivers = sorted(free_drivers, key=driver_sort_key)
        return [d.username for d in sorted_drivers[:count]]

    def count_orders(self, position: tuple, distance: int, endpoint: str) -> int:
        count = 0
        for o in self._orders.values():
            target_pos = o.starting_position if endpoint == 'START' else o.finishing_position
            dist = abs(target_pos[0] - position[0]) + abs(target_pos[1] - position[1])
            if dist <= distance:
                count += 1
        return count

    def get_nearest_pending_order(self, position: tuple) -> int | None:
        pending_orders = [o for o in self._orders.values() if o.is_pending()]
        if not pending_orders:
            return None

        def order_sort_key(o):
            dist = abs(o.starting_position[0] - position[0]) + abs(o.starting_position[1] - position[1])
            return (dist, o.order_id)

        nearest = min(pending_orders, key=order_sort_key)
        return nearest.order_id

    def get_company_credit(self) -> Decimal:
        return self._company_credit
    def rate_driver(self, username: str, rating: int) -> bool:
        if username not in self._drivers:
            return False
        if not (1 <= rating <= 5) or isinstance(rating, bool):
            raise ValueError("امتیاز باید عددی بین ۱ تا ۵ باشد.")
        
        # ذخیره یا میانگین‌گیری امتیازات راننده (می‌تونیم یه ویژگی به Driver اضافه کنیم)
        driver = self._drivers[username]
        if not hasattr(driver, '_ratings'):
            driver._ratings = []
        driver._ratings.append(rating)
        return True