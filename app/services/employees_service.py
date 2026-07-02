from schemas import EmployeesDTO, EmployeeFilterDTO
from contracts import EmployeesRepositoryProtocol


class EmployeesService:

    def __init__(self, employees_repo: EmployeesRepositoryProtocol):
        self.employees_repo = employees_repo


    async def get_list(self, filter: EmployeeFilterDTO) -> tuple[EmployeesDTO, int]: 
        employees = self.employees_repo.get_list(filter)
        count = self.employees_repo.get_count(filter)
        return employees, count


    async def update(self, employee_uuid: str, employee: EmployeesDTO) -> EmployeesDTO: 
        ...


    async def soft_delete(self, employee_uuid: str) -> EmployeesDTO: 
        ...
