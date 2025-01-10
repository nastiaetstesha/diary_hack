from datacenter.models import Schoolkid, Lesson, Commendation, Subject, Mark, Chastisement
from django.core.exceptions import ValidationError

praise_text = "Хвалю!"


def get_student_by_name(student_name):
    try:
        student = Schoolkid.objects.get(full_name__icontains=student_name)
        return student
    except Schoolkid.DoesNotExist:
        raise ValidationError(f"Ученик с именем {student_name} не найден.")
    except Schoolkid.MultipleObjectsReturned:
        raise ValidationError(f"Найдено несколько учеников с именем {student_name}. Уточните имя.")


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_marks.update(points=5)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(student_name, chosen_subject="Математика"):
    student = get_student_by_name(student_name)

    year_of_study = student.year_of_study
    group_letter = student.group_letter

    chosen_subjects = Subject.objects.filter(title=chosen_subject)

    if chosen_subjects.count() > 1:
        chosen_subject = chosen_subjects.filter(year_of_study=year_of_study).first()
    else:
        chosen_subject = chosen_subjects.first()

    if not chosen_subject:
        raise ValueError(f"Предмет {chosen_subject} не найден для {year_of_study}{group_letter}.")

    lessons = Lesson.objects.filter(
        subject=chosen_subject,
        year_of_study=year_of_study,
        group_letter=group_letter
    ).order_by('?')

    random_lesson = lessons.first()

    if random_lesson is None:
        raise ValueError(f"Уроки по предмету {chosen_subject.title} для {year_of_study}{group_letter} не найдены.")

    Commendation.objects.create(
        text=praise_text,
        created=random_lesson.date,
        schoolkid=student,
        subject=chosen_subject,
        teacher=random_lesson.teacher
    )
