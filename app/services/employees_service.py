import logging
from sсhemas import EmployeeDTO, EmployeeFilterDTO
from contracts import EmployeesRepositoryProtocol


class EmployeesService:
    def __init__(self, employees_repo: EmployeesRepositoryProtocol):
        self.employees_repo = employees_repo

    async def get_list(self, filter_dto: EmployeeFilterDTO) -> tuple[list[EmployeeDTO], int]: 
        employees = await self.employees_repo.get_list(filter_dto)
        count = await self.employees_repo.get_count(filter_dto)
        employees_dto = [EmployeeDTO.model_validate(emp) for emp in employees]
        return employees_dto, count

    async def get_by_id(self, employee_id: int) -> EmployeeDTO | None:
        employee = await self.employees_repo.get_by_id(employee_id)
        if not employee:
            return None
        return EmployeeDTO.model_validate(employee)

    async def create(self, dto: EmployeeDTO) -> EmployeeDTO:
        employee = await self.employees_repo.create(dto)
        await self.employees_repo.session.flush() 
        return EmployeeDTO.model_validate(employee)

    async def update(self, employee_id: int, dto: EmployeeDTO) -> EmployeeDTO | None: 
        employee = await self.employees_repo.update(employee_id, dto)
        if not employee:
            return None
        return EmployeeDTO.model_validate(employee)

    async def soft_delete(self, employee_id: int) -> EmployeeDTO | None: 
        employee = await self.employees_repo.soft_delete(employee_id)
        if not employee:
            return None
        return EmployeeDTO.model_validate(employee)