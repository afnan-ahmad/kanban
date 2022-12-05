from flask_restful import Resource, reqparse
from flask_security import auth_required, current_user

from kanban.jobs.tasks import *

job_parser = reqparse.RequestParser()
job_parser.add_argument('job_name', help='Job name is required.', required=True)
job_parser.add_argument('list_id')


class JobsAPI(Resource):
    @auth_required('token')
    def get(self):
        return {
            'email': current_user.email
        }

    @auth_required('token')
    def post(self):
        args = job_parser.parse_args()
        job_name = args.get('job_name')

        if job_name == 'export_lists':
            export_lists.delay(user_id=current_user.id)
        elif job_name == 'export_cards':

            list_id = args.get('list_id')

            if not list_id:
                return False

            export_cards.delay(list_id=list_id)

        return True
