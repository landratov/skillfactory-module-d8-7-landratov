from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorityCounter
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug
        new_count = cat.todos_count
        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1

    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(post_save, sender=TodoItem)
def new_task_added(sender, instance, **kwargs):
    if instance.priority:
        counter = PriorityCounter.objects.update_or_create(priority=instance.priority)[0]
        counter.count += 1
        counter.save()


@receiver(post_delete, sender=TodoItem)
def task_deleted(sender, instance, **kwargs):
    if instance.priority:
        counter = PriorityCounter.objects.get(priority=instance.priority)
        counter.count -= 1
        counter.save()
