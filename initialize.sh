#!/usr/bin/env bash
printf "\n+ Przygotowuje wstepne rekordy dla bazy...\n"
printf "\nMigruje...\n"
python manage.py migrate \
&& printf "+ Przygotowuje superusera\n" \
&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'contact@mign.pl', 'asdasd123')" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('marek', 'marek@gobit.com.pl', 'asdasd123')" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('bartek', 'bartosz.suchecki@gobit.com.pl', 'asdasd123')" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('darek', 'dariusz.czaplicki@gobit.com.pl', 'asdasd123')" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('damian', 'damian.kruk@gobit.com.pl', 'asdasd123')" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; u=User.objects.get(email='contact@mign.pl'); u.first_name='Mateusz'; u.last_name='Ignatowicz'; u.save()" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; u=User.objects.get(email='marek@gobit.com.pl'); u.first_name='Marek'; u.last_name='Walczyński'; u.save()" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; u=User.objects.get(email='bartosz.suchecki@gobit.com.pl'); u.first_name='Bartosz'; u.last_name='Suchecki'; u.save()" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; u=User.objects.get(email='dariusz.czaplicki@gobit.com.pl'); u.first_name='Darek'; u.last_name='Czaplicki'; u.save()" | python manage.py shell \
&& echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; u=User.objects.get(email='damian.kruk@gobit.com.pl'); u.first_name='Damian'; u.last_name='Kruk'; u.save()" | python manage.py shell \
&& echo "+ Tworze rekordy modelow aplikacji models.json..." \
&& python manage.py loaddata export/models.json \
&& echo "+ Tworze typy zleceń modelu OrderType..." \
&& python manage.py loaddata export/model_ordertype.json \
&& echo "+ Tworze rekordy modelu ImplemetationType..." \
&& python manage.py loaddata export/model_implementationtype.json \
&& echo "+ Tworze rekordy modelu AgreementStatus..." \
&& python manage.py loaddata export/model_agreementstatus.json \
&& echo "+ Tworze rekordy modelu OrderStatus..." \
&& python manage.py loaddata export/model_orderstatus.json \
&& echo "+ Tworze rekordy modelu OrderCategory..." \
&& python manage.py loaddata export/model_ordercategory.json \
&& echo "+ Tworze rekordy modelu Rate..." \
&& python manage.py loaddata export/rate.json \
&& echo "+ Tworze rekordy modelu RateStack..." \
&& python manage.py loaddata export/ratestack.json \
&& echo "+ Tworze rekordy modelu Pakiet..." \
&& python manage.py loaddata export/pakiet.json \
&& echo "+ Tworze rekordy modelu DistanceCalcProfile..." \
&& python manage.py loaddata export/distancecalcprofile.json \
&& echo "+ Tworze rekordy modelu OrderTempalte..." \
&& python manage.py loaddata export/ordertemplate.json \
&& echo "+ Tworze rekordy modelu AgreementType..." \
&& python manage.py loaddata export/agreementtype.json \
&& echo "+ Tworze token dla admina" \ 
python manage.py shell < export/make_token.py

