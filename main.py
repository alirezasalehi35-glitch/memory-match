from delivery_system import DeliverySystem

def main():
    system = DeliverySystem()
    
    while True:
        try:
            line = input()
            if not line:
                continue
            parts = line.strip().split()
            command = parts[0]
            
            if command == 'END':
                break
                
            elif command == 'ADD-DRIVER':
                # ADD-DRIVER username x y category
                username = parts[1]
                x = int(parts[2])
                y = int(parts[3])
                category = parts[4]
                result = system.add_driver(username, (x, y), category)
                print("True" if result else "False")
                
            elif command == 'CREATE-ORDER':
                # CREATE-ORDER category start_x start_y finish_x finish_y
                category = parts[1]
                start_x, start_y = int(parts[2]), int(parts[3])
                finish_x, finish_y = int(parts[4]), int(parts[5])
                order_id = system.create_order(category, (start_x, start_y), (finish_x, finish_y))
                print(order_id if order_id is not None else "None")
                
            elif command == 'ASSIGN-NEXT-ORDER':
                # ASSIGN-NEXT-ORDER username
                username = parts[1]
                order_id = system.assign_next_order(username)
                print(order_id if order_id is not None else "None")
                
            elif command == 'ORDER-UPDATE':
                # ORDER-UPDATE username order_id status
                username = parts[1]
                order_id = int(parts[2])
                status = parts[3]
                result = system.update_order_status(username, order_id, status)
                print("True" if result else "False")
                
            elif command == 'GET-DRIVER':
                # GET-DRIVER username
                username = parts[1]
                res = system.get_driver(username)
                if res is None:
                    print("None")
                else:
                    status, pos, credit = res
                    print(f"{status} {pos[0]} {pos[1]} {credit}")
                    
            elif command == 'GET-ORDER':
                # GET-ORDER order_id
                order_id = int(parts[1])
                res = system.get_order(order_id)
                if res is None:
                    print("None")
                else:
                    status, driver_name, cost = res
                    print(f"{status} {driver_name} {cost}")
                    
            elif command == 'GET-ORDER-LIST':
                # GET-ORDER-LIST status
                status = parts[1]
                orders = system.get_order_list(status)
                print(" ".join(map(str, orders)))
                
            elif command == 'GET-DRIVER-LIST':
                # GET-DRIVER-LIST status
                status = parts[1]
                drivers = system.get_driver_list(status)
                print(" ".join(drivers))
                
            elif command == 'GET-NEAR-DRIVER':
                # GET-NEAR-DRIVER x y count
                x, y = int(parts[1]), int(parts[2])
                count = int(parts[3])
                drivers = system.get_near_drivers((x, y), count)
                print(" ".join(drivers))
                
            elif command == 'GET-CNT-ORDER':
                # GET-CNT-ORDER x y distance endpoint
                x, y = int(parts[1]), int(parts[2])
                distance = int(parts[3])
                endpoint = parts[4]
                cnt = system.count_orders((x, y), distance, endpoint)
                print(cnt)
                
            elif command == 'GET-NEAREST-PENDING-ORDER':
                # GET-NEAREST-PENDING-ORDER x y
                x, y = int(parts[1]), int(parts[2])
                order_id = system.get_nearest_pending_order((x, y))
                print(order_id if order_id is not None else "None")
                
            elif command == 'GET-COMPANY':
                # GET-COMPANY
                print(system.get_company_credit())
                
        except Exception as e:
            # مدیریت خطاهای اجرایی در رابط متنی
            print(f"Error: {e}")

if __name__ == '__main__':
    main()