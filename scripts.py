import random
from datacenter.models import Schoolkid, Lesson, Commendation, Subject, Mark, Chastisement


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


# schoolkid = Schoolkid.objects.get(full_name="Фролов Иван")
# fix_marks(schoolkid)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


# schoolkid = Schoolkid.objects.get(full_name="Фролов Иван")
# remove_chastisements(schoolkid)

def create_commendation(student_name, chosen_subject="Математика"):
    try:
        student = Schoolkid.objects.get(full_name__icontains=student_name)
        print(f"Найден ученик: {student.full_name} {student.year_of_study}{student.group_letter}")
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем {student_name} не найден.")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {student_name}. Уточните имя.")
        return

    year_of_study = student.year_of_study
    group_letter = student.group_letter

    chosen_subjects = Subject.objects.filter(title=chosen_subject)

    if chosen_subjects.count() > 1:
        chosen_subject = chosen_subjects.filter(year_of_study=year_of_study).first()
    else:
        chosen_subject = chosen_subjects.first()

    if not chosen_subject:
        print(f"Предмет {chosen_subject} не найден для {year_of_study}{group_letter}.")
        return

    lessons = Lesson.objects.filter(
        subject=chosen_subject,
        year_of_study=year_of_study,
        group_letter=group_letter
    ).order_by('-date')

    if not lessons:
        print(f"Уроки по предмету {chosen_subject.title} для {year_of_study}{group_letter} не найдены.")
        return

    random_lesson = random.choice(lessons)

    praise_text = "Хвалю!"

    commendation = Commendation.objects.create(
        text=praise_text,
        created=random_lesson.date,
        schoolkid=student,
        subject=chosen_subject,
        teacher=random_lesson.teacher
    )
    commendation.save()
    print(f"Похвала для {student_name} по предмету {chosen_subject.title} успешно добавлена!")
