from django.core.exceptions import ValidationError
import datetime
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
import calendar

class OptionalChoiceWidget(forms.MultiWidget):
    def decompress(self,value):
        #this might need to be tweaked if the name of a choice != value of a choice
        if value: #indicates we have a updating object versus new one
            if value in [x[0] for x in self.widgets[0].choices]:
                 return [value,""] # make it set the pulldown to choice
            else:
                 return ["",value] # keep pulldown to blank, set freetext
        return ["",""] # default for new object

class OptionalChoiceField(forms.MultiValueField):
    def __init__(self, choices, max_length=80, *args, **kwargs):
        """ sets the two fields as not required but will enforce that (at least) one is set in compress """
        fields = (forms.ChoiceField(choices=choices,required=False),
                  forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(OptionalChoiceField,self).__init__(required=False,fields=fields,*args,**kwargs)
    def compress(self,data_list):
        """ return the choicefield value if selected or charfield value (if both empty, will throw exception """
        if not data_list:
            raise ValidationError('Need to select choice or enter text for this field')
        return data_list[0] or data_list[1]


def calculate():
    today = datetime.date.today()
    all_users = User.objects.filter(userprofile__joining_date__year__lte=today.year, userprofile__joining_date__month__lte=today.month).order_by('-userprofile__joining_date')
    users_count = len(all_users)
    name, to_be_paid, spent_amount, spent_per_head = [0] * users_count, [0] * users_count, [0] * users_count ,[0] * users_count

    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    range_end_day = last_day_of_month
    for main_idx, user in enumerate(all_users):

        total = 0
        if user.userprofile.joining_date > (timezone.now() - datetime.timedelta(today.day-1)):
            range_start_day = user.userprofile.joining_date.day
            user_joined_current_month = True
        else:
            range_start_day = 1
            user_joined_current_month = False

        for idx, range_user in enumerate(all_users):
            expenses = range_user.expenses_set.filter(Q(spent_date__year=today.year), Q(spent_date__month=today.month), Q(spent_date__day__gte=range_start_day) & Q(spent_date__day__lte=range_end_day))
            for expense in expenses:
                total = total + expense.spent_amount
                spent_amount[idx] += expense.spent_amount

        rent = 30000 * (((range_end_day - range_start_day+1) / last_day_of_month))
        for idx in range(main_idx, users_count):
            spent_per_head[idx] += ((total + rent)/ (users_count-main_idx))

        if user_joined_current_month:
            range_end_day = range_start_day - 1
        else:
            break


    for idx, user in enumerate(all_users):
        name[idx] = (user.first_name + " " + user.last_name)
        to_be_paid[idx] = (float("%.2f" % (spent_per_head[idx] - spent_amount[idx])))
        spent_per_head[idx] = float("%.2f" % (spent_per_head[idx]))

    return round(sum(spent_per_head),2), zip(name, spent_amount, to_be_paid,  spent_per_head)