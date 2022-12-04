from flask_restful import Resource, marshal_with, fields
from flask_security import auth_required, current_user

from datetime import date, timedelta
from matplotlib import pyplot as plt

from io import BytesIO
from base64 import b64encode

from kanban.util import date_text

plt.rcParams['font.size'] = 24

from kanban.models import Card

output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'total': fields.Integer,
    'completed': fields.Integer,
    'overdue': fields.Integer,
    'completed_percent': fields.Integer,
    'overdue_percent': fields.Integer,
    'fig_data': fields.String
}


class SummaryAPI(Resource):
    @auth_required('token')
    @marshal_with(output_fields)
    def get(self):
        data = []

        for lst in current_user.lists:
            total_count = len(lst.cards)

            completed_count = Card.query.with_parent(lst).filter_by(completed=True).count()
            overdue_count = Card.query.with_parent(lst).filter_by(completed=False).filter(
                Card.deadline < date.today()).count()

            previous_week = date.today() - timedelta(days=7)

            x, y = [], []
            for d in range(8):
                next_day = previous_week + timedelta(days=d)
                x.append(date_text(next_day))

                count = Card.query.with_parent(lst).filter_by(completed_on=next_day).count()
                y.append(count)

            fig, ax = plt.subplots(figsize=(8, 8))

            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            ax.bar(x, y, color='#23BE75')

            ax.set_axisbelow(True)
            ax.grid(axis='y')

            ax.yaxis.set_ticks(range(total_count + 1))

            plt.xticks(rotation=45)
            plt.tight_layout()

            fig_file = BytesIO()
            plt.savefig(fig_file, format='png')

            fig_data = str(b64encode(fig_file.getvalue()), 'utf-8')

            data.append({
                'id': lst.id,
                'name': lst.name,
                'total': total_count,
                'completed': completed_count,
                'overdue': overdue_count,
                'completed_percent': (completed_count / max(total_count, 1)) * 100,
                'overdue_percent': (overdue_count / max(total_count, 1)) * 100,
                'fig_data': fig_data
            })

        return data
