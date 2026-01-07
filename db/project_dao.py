import uuid

from db.dao import Dao


class ProjectDao(Dao):
    def insert_project(self, dict_project):
        project_id = str(uuid.uuid4())
        with self.db.cursor(dictionary=True) as cursor_insert_project:
            sql = "INSERT INTO bidding.project (id, customer_name, project_name, project_description, reference, tech_stack, service) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (project_id, dict_project["customer_name"], dict_project["project_name"],
                   dict_project["project_description"], dict_project["reference"], dict_project["tech_stack"],
                   dict_project["service"])
            cursor_insert_project.execute(sql, val)
            self.db.commit()
        return project_id

    def get_all_projects(self):
        with self.db.cursor(dictionary=True) as cursor_get_all_projects:
            sql = "SELECT * FROM bidding.project ORDER BY project_name"
            cursor_get_all_projects.execute(sql)
            return cursor_get_all_projects.fetchall()