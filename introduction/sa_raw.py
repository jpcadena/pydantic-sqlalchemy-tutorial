"""
This module demonstrates the use of SQLAlchemy for executing raw SQL queries
 directly. The example provided queries an enterprise database for information
  about employees and their departments, specifically focusing on those within
   the Engineering department.
"""

import csv
from typing import Any

# import pandas as pd
from sqlalchemy import CursorResult, Engine, TextClause, create_engine, text

engine: Engine = create_engine(
    "postgresql://user:Password123@0.0.0.0:5432/data_science_prd",
)
text_clause: TextClause = text(
    """
SELECT
    employees.name,
    departments.name AS department,
    COUNT(projects.id) AS project_count,
    AVG(salaries.amount) AS average_salary
FROM
    employees
JOIN
    departments ON employees.department_id = departments.id
LEFT JOIN
    projects ON projects.employee_id = employees.id
JOIN
    salaries ON employees.id = salaries.employee_id
WHERE
    departments.name = 'Engineering'
GROUP BY
    employees.name, departments.name
HAVING
    COUNT(projects.id) > 5
ORDER BY
    average_salary DESC;
"""
)

with engine.connect() as connection:
    cursor_result: CursorResult[Any] = connection.execute(
        text_clause,
    )
    data: list[tuple[Any, ...]] = [tuple(row) for row in cursor_result]
    # [(1, "A", 54.4,), (2, "ASDA", 0.42, ), (...), (), (), (), (), (), ... ]
    for record in data:
        print(record)

file_header: list[str] = [
    "EMPLOYEE_NAME",
    "DEPARTMENT",
    "PROJECT_COUNT",
    "AVERAGE_SALARY",
]
filename: str = "data.csv"
with open(filename, "w") as text_io_wrapper:
    writer = csv.writer(
        text_io_wrapper,
    )
    writer.writerow(file_header)
    for record in data:
        writer.writerow(record)

# Another option with Pandas
# dataframe: pd.DataFrame = pd.DataFrame(data, columns=file_header,)
