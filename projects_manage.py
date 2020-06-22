from db_core import *

try:
    UnitOfWork.new_current()
    new_employee_1 = Employee(None, 'Petr', 'Petrov')
    new_employee_1.mark_new()

    new_employee_2 = Employee(None, 'Igor', 'Igorev')
    new_employee_2.mark_new()

    employee_mapper_2 = EmployeeMapper(connection, Employee)
    exists_employee_1 = employee_mapper_2.find_by_id(2)
    exists_employee_1.mark_dirty()
    print(exists_employee_1.name)
    exists_employee_1.name += ' Senior'
    print(exists_employee_1.name)

    exists_employee_2 = employee_mapper_2.find_by_id(2)
    exists_employee_2.mark_removed()

    print(UnitOfWork.get_current().__dict__)

    UnitOfWork.get_current().commit()

except Exception as e:
    print(e.args)
finally:
    UnitOfWork.set_current(None)

print(UnitOfWork.get_current())
