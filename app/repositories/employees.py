import logging
from sqlalchemy import select, func, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.employee import Employee
from sсhemas import EmployeeFilterDTO, EmployeeDTO

logger = logging.getLogger("employee_board")

class EmployeesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _build_filter_query(self, filter_dto: EmployeeFilterDTO):
        query = select(Employee).where(Employee.is_deleted == False)

        if filter_dto.search:
            search_term = f"%{filter_dto.search}%"
            query = query.where(
                or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.patronymic.ilike(search_term),
                    Employee.phone.ilike(search_term),
                )
            )

        if filter_dto.gender:
            query = query.where(Employee.gender == filter_dto.gender)

        if filter_dto.age_from is not None:
            age_expr = func.extract('year', func.age(Employee.birth_date))
            query = query.where(age_expr >= filter_dto.age_from)

        if filter_dto.age_to is not None:
            age_expr = func.extract('year', func.age(Employee.birth_date))
            query = query.where(age_expr <= filter_dto.age_to)

        return query

    async def get_list(self, filter_dto: EmployeeFilterDTO) -> list[Employee]:
        query = self._build_filter_query(filter_dto)
        query = query.order_by(Employee.id.desc()) 
        offset = (filter_dto.page - 1) * filter_dto.per_page
        query = query.offset(offset).limit(filter_dto.per_page)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_count(self, filter_dto: EmployeeFilterDTO) -> int:
        base_query = self._build_filter_query(filter_dto)
        count_query = select(func.count()).select_from(base_query.subquery())
        result = await self.session.execute(count_query)
        return result.scalar_one_or_none() or 0

    async def get_by_id(self, employee_id: int) -> EmployeeDTO | None:
        query = select(Employee).where(Employee.id == employee_id, Employee.is_deleted == False)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, dto: EmployeeDTO) -> EmployeeDTO:
        employee = Employee(**dto.model_dump())
        self.session.add(employee)
        return employee

    async def update(self, employee_id: int, dto: EmployeeDTO) -> EmployeeDTO | None:
        update_data = {**dto.model_dump(), "id":employee_id}
        logger.critical(update_data)
        if not update_data:
            return await self.get_by_id(employee_id)
        
        stmt = (
            update(Employee)
            .where(Employee.id == employee_id)
            .values(**update_data)
            .returning(Employee)  
        )
        
        result = await self.session.execute(stmt)
        updated_employee = result.scalar_one_or_none()
        
        return EmployeeDTO.model_validate(updated_employee)

    async def soft_delete(self, employee_id: int) -> EmployeeDTO | None:
        employee = await self.get_by_id(employee_id)
        if employee:
            employee.is_deleted = True
        return employee